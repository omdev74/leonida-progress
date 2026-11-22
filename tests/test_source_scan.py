import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('source_scan', Path(__file__).resolve().parents[1] / 'source_scan.py')
s = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s)

HEADER = '''MIDL_INTERFACE("00000000-0000-0000-0000-000000000001")
ID3D12Object : public IUnknown {
public:
 virtual HRESULT STDMETHODCALLTYPE GetPrivateData() = 0;
 virtual HRESULT STDMETHODCALLTYPE SetName() = 0;
};
MIDL_INTERFACE("00000000-0000-0000-0000-000000000002")
ID3D12Sample : public ID3D12Object {
public:
 virtual HRESULT STDMETHODCALLTYPE Run() = 0;
 virtual HRESULT STDMETHODCALLTYPE Partial() = 0;
 virtual HRESULT STDMETHODCALLTYPE Missing() = 0;
 virtual HRESULT STDMETHODCALLTYPE Noop() = 0;
 virtual HRESULT STDMETHODCALLTYPE Deferred() = 0;
 virtual HRESULT STDMETHODCALLTYPE Explicit() = 0;
 virtual HRESULT STDMETHODCALLTYPE Outside() = 0;
};
'''
SHARED = '''template<class Derived, class Stubs, class... Interfaces>
class Object : public Stubs {
public:
 HRESULT STDMETHODCALLTYPE GetPrivateData() override { return value_; }
 HRESULT STDMETHODCALLTYPE SetName() override { return S_OK; }
 ULONG STDMETHODCALLTYPE AddRef() override { return ++refs_; }
};
'''
SOURCE = r'''class Sample final : public Object<Sample, ID3D12SampleStubs, ID3D12Object, ID3D12Sample> {
public:
 HRESULT STDMETHODCALLTYPE Run() override {
    // E_NOTIMPL and stub() in a comment are not code.
    const char* normal = "E_NOTIMPL and stub()";
    const char* raw = R"x({ stub("no"); })x";
    return work();
 }
 HRESULT STDMETHODCALLTYPE Partial() override { if (ready()) return work(); return E_NOTIMPL; }
 HRESULT STDMETHODCALLTYPE Noop() override {}
 HRESULT STDMETHODCALLTYPE Deferred() override { return helper(); }
 HRESULT STDMETHODCALLTYPE Explicit() override { stub("unsupported"); return E_NOTIMPL; }
 HRESULT STDMETHODCALLTYPE Outside() override;
private:
 HRESULT helper() { stub("helper"); return E_NOTIMPL; }
};
HRESULT STDMETHODCALLTYPE Sample::Outside() { return value_; }
'''
CMAKE = '''COMMAND Python3::Interpreter -I ${ROOT}/tools/gen_d3d12_stubs.py --out ${OUT}
 ID3D12Sample
 DEPENDS ${ROOT}/tools/gen_d3d12_stubs.py'''
FILES = {'runtime/CMakeLists.txt': CMAKE, 'runtime/shims/shared.h': SHARED, 'runtime/shims/sample.cpp': SOURCE}
REFERENCE = {'sha256': 'b' * 64, 'url': 'https://example.org/sdk'}


def scan(files=None, header=HEADER):
    return s.scan(FILES if files is None else files, header, 'a' * 40, 'example/repo', REFERENCE)


class SourceTests(unittest.TestCase):
    def test_named_methods_inheritance_and_classifications(self):
        result = scan()
        states = {m['method']: m['state'] for m in result['symbols']}
        self.assertEqual(states, {'GetPrivateData': 'body', 'SetName': 'noop', 'Run': 'body', 'Partial': 'partial',
                                  'Missing': 'stub', 'Noop': 'noop', 'Deferred': 'partial', 'Explicit': 'stub', 'Outside': 'body'})
        self.assertEqual(result['groups'][0]['total'], 9)
        self.assertNotIn('AddRef', states)
        self.assertTrue(all('/' + 'a' * 40 + '/' in m['url'] for m in result['symbols']))

    def test_literals_and_comments_do_not_create_unsupported_paths(self):
        self.assertEqual(next(m for m in scan()['symbols'] if m['method'] == 'Run')['state'], 'body')

    def test_unsigned_cast_grammar_workaround_preserves_offsets(self):
        source = SOURCE.replace('return work();', 'if (unsigned(mode) > unsigned(limit)) return E_INVALIDARG; return work();')
        result = scan({**FILES, 'runtime/shims/sample.cpp': source})
        method = next(m for m in result['symbols'] if m['method'] == 'Run')
        self.assertEqual(method['state'], 'body')
        self.assertEqual(method['line'], 3)

    def test_stub_to_body_and_regression_visible(self):
        files = dict(FILES)
        files['runtime/shims/sample.cpp'] = SOURCE.replace('stub("unsupported"); return E_NOTIMPL;', 'return work();')
        self.assertEqual(next(m for m in scan(files)['symbols'] if m['method'] == 'Explicit')['state'], 'body')
        files['runtime/shims/sample.cpp'] = files['runtime/shims/sample.cpp'].replace('return work();', 'return E_NOTIMPL;')
        self.assertEqual(next(m for m in scan(files)['symbols'] if m['method'] == 'Explicit')['state'], 'stub')

    def test_new_interface_expands_denominator(self):
        files = {**FILES, 'runtime/CMakeLists.txt': CMAKE.replace('ID3D12Sample\n', 'ID3D12Sample ID3D12New\n')}
        header = HEADER + '''MIDL_INTERFACE("00000000-0000-0000-0000-000000000003")
ID3D12New : public ID3D12Object {
public:
 virtual HRESULT STDMETHODCALLTYPE NewMethod() = 0;
};
'''
        result = scan(files, header)
        self.assertEqual(len(result['groups']), 2)
        self.assertEqual(sum(g['total'] for g in result['groups']), 12)

    def test_test_fixtures_and_unrelated_classes_do_not_count(self):
        files = {**FILES, 'runtime/shims/tests/fake.cpp': SOURCE,
                 'runtime/src/other.cpp': 'class Unrelated { int Missing() { return work(); } };'}
        self.assertEqual(scan(files)['groups'], scan()['groups'])

    def test_unrecognized_source_patterns_fail_closed(self):
        for body in [SOURCE.replace('Object<', 'UnrecognizedWrapper<'),
                     SOURCE.replace('return work();', 'return @;'),
                     SOURCE.replace('HRESULT STDMETHODCALLTYPE Noop() override {}', '#if 0\nHRESULT STDMETHODCALLTYPE Noop() override {}\n#endif'),
                     SOURCE.replace('Noop()', 'NotInSDK()')]:
            with self.subTest(body=body), self.assertRaises(s.ScanError):
                scan({**FILES, 'runtime/shims/sample.cpp': body})

    def test_unknown_generator_or_sdk_interface_fails_closed(self):
        for files, header in [({**FILES, 'runtime/CMakeLists.txt': 'changed generator'}, HEADER),
                              (FILES, HEADER.replace('ID3D12Sample :', 'ID3D12Other :'))]:
            with self.assertRaises(s.ScanError):
                scan(files, header)

    def test_sdk_alternative_declarations_deduplicated(self):
        repeated = HEADER.replace('virtual HRESULT STDMETHODCALLTYPE Run() = 0;',
                                  'virtual HRESULT STDMETHODCALLTYPE Run() = 0;\n virtual HRESULT STDMETHODCALLTYPE Run() = 0;')
        self.assertEqual(scan(header=repeated)['groups'][0]['total'], 9)

    def test_sdk_inheritance_cycle_rejected(self):
        with self.assertRaises(s.ScanError):
            s.interface_methods({'A': ('B', {'x'}), 'B': ('A', {'y'})}, 'A')


class GitSourceTests(unittest.TestCase):
    def test_pinned_tree_read_and_test_exclusion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def git(*args):
                return subprocess.run(['git', '-C', temp, *args], check=True, capture_output=True).stdout.decode().strip()
            git('init', '-b', 'main')
            path = root / 'runtime/shims/sample.cpp'
            path.parent.mkdir(parents=True)
            path.write_text('first', encoding='utf-8')
            tests = root / 'runtime/shims/tests/fake.cpp'
            tests.parent.mkdir()
            tests.write_text('not counted')
            git('add', '.')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-m', 'first')
            revision = git('rev-parse', 'HEAD')
            path.write_text('second')
            repository = s.SourceRepository('example/repo', root / 'cache')
            repository.gitdir = root / '.git'
            files = repository.files(revision)
            self.assertEqual(files['runtime/shims/sample.cpp'], 'first')
            self.assertNotIn('runtime/shims/tests/fake.cpp', files)


if __name__ == '__main__':
    unittest.main()
