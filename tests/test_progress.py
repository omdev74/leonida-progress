import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location('progress', Path(__file__).resolve().parents[1] / 'progress.py')
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)

TASKS = r'''### Up for grabs
| ID | What | Needs |
|---|---|---|
| TEST-1 | Test `a|b` and x\|y | CPU |
| NEW-9 | A new workstream | CPU |

### Open work
| ID | Item | Owner | PR | Status |
|---|---|---|---|---|
| TEST-2 | Example | @example | #7 | PR open |
| TEST-3 | Example | @example | #8 merged, #9 | older work merged; PR open |
| TEST-4 | Example | — | — | uncertain |
| D3D-99 | Example | @example | #10 | claimed |
| D3D-2 | Example | @example | #11 | waits for #5 |

**Blocked, not up for grabs yet:** RT-5 Boot (waits for executable); FUZZ-10 Case (waits for SHADER-90).
'''


class FakeAPI:
    def __init__(self):
        self.calls = []

    def get(self, endpoint):
        self.calls.append(endpoint)
        if endpoint.startswith('search/issues?'):
            return {'items': [{'number': 700, 'title': 'Coordinating who works on what (4)'}]}
        n = 313 if endpoint.endswith('/313') else 700
        return {'number': n, 'body': TASKS, 'html_url': f'https://github.com/example/project/issues/{n}',
                'updated_at': '2026-01-01T00:00:00Z', 'state': 'open'}


CONFIG = {'upstream': 'example/project', 'method_issue': 313,
          'coordination_title': 'Coordinating who works on what', 'repository': 'example/tracker'}
SOURCE = {'revision': 'a' * 40, 'rules_id': 'rule-a', 'files_scanned': 3,
          'reference': {'url': 'https://example.org/sdk', 'sha256': 'b' * 64},
          'groups': [{'name': 'ID3D12Sample', 'total': 11,
                      'counts': {'body': 4, 'partial': 2, 'noop': 1, 'stub': 4}}], 'symbols': []}


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeAPI()
        self.data = p.collect(CONFIG, self.api, '2026-01-01 00:00 UTC', copy.deepcopy(SOURCE))
        self.history = p.report_assets.update_history(None, SOURCE, '2026-01-01')

    def test_task_dedup_pipes_states_and_dependencies(self):
        states = {t['id']: t['state'] for t in self.data['tasks']}
        self.assertEqual(len(states), len(self.data['tasks']))
        self.assertEqual(states['TEST-1'], 'available')
        self.assertEqual(states['TEST-3'], 'active')
        self.assertEqual(states['TEST-4'], 'unknown')
        self.assertEqual(states['D3D-2'], 'blocked')
        self.assertEqual(states['RT-5'], 'blocked')
        self.assertNotIn('SHADER-90', states)
        self.assertIn('NEW', {g['name'] for g in self.data['panels'][1]['groups']})

    def test_coordination_rollover_discovered(self):
        self.assertEqual(self.data['sources'][1]['number'], 700)
        self.assertTrue(any(call.endswith('/700') for call in self.api.calls))

    def test_coordination_failure_does_not_block_source_scan(self):
        class Unavailable:
            def get(self, endpoint):
                raise p.SourceError('Unavailable')
        data = p.collect(CONFIG, Unavailable(), 'now', SOURCE)
        self.assertEqual(data['source'], SOURCE)
        self.assertEqual(len(data['panels']), 1)
        self.assertTrue(data['warnings'])
        self.assertIn('queue unavailable', p.render_svg(data))

    def test_ambiguous_coordination_search_not_guessed(self):
        class Ambiguous(FakeAPI):
            def get(self, endpoint):
                return {'items': [{'number': n, 'title': 'Coordinating who works on what'} for n in (1, 2)]}
        data = p.collect(CONFIG, Ambiguous(), 'now', SOURCE)
        self.assertFalse(data['tasks'])
        self.assertTrue(data['warnings'])

    def test_malformed_task_rows_rejected(self):
        issue = FakeAPI().get('repos/example/project/issues/700')
        issue['body'] = TASKS.replace('| NEW-9 |', '| no-id |')
        with self.assertRaises(p.SourceError):
            p.task_inventory([issue])

    def test_one_square_per_item_and_correct_colors(self):
        svg = ET.fromstring(p.render_svg(self.data))
        cells = [r for r in svg.iter() if r.get('class') == 'cell']
        self.assertEqual(len(cells), sum(g['total'] for panel in self.data['panels'] for g in panel['groups']))
        self.assertEqual(sum(r.get('data-state') == 'body' for r in cells), 4)
        self.assertTrue(all(r.get('fill') == p.COLORS[r.get('data-state')] for r in cells))
        self.assertFalse(any(r.tag.endswith('script') for r in svg.iter()))

    def test_xml_escaping_and_method_links(self):
        self.data['panels'][1]['groups'][0]['name'] = '<script>alert("x")</script> & category'
        self.data['source']['symbols'] = [{'interface': 'ID3D12Sample', 'method': 'Read', 'state': 'body',
                                          'reason': 'Present', 'url': 'https://example.org/source#L4'}]
        svg = p.render_svg(self.data)
        ET.fromstring(svg)
        self.assertNotIn('<script>', svg)
        self.assertIn('href="https://example.org/source#L4"', svg)
        self.assertIn('ID3D12Sample::Read', svg)

    def test_expansion_does_not_clip_cells(self):
        self.data['panels'][0]['groups'] = [
            {'name': f'ID3D12Object{i}', 'total': i + 1, 'counts': {'body': i, 'partial': 1, 'noop': 0, 'stub': 0}}
            for i in range(35)]
        svg = ET.fromstring(p.render_svg(self.data))
        ns = {'s': 'http://www.w3.org/2000/svg'}
        for group in svg.findall('s:g', ns):
            bounds = group.find('s:rect', ns)
            x, y, w, h = (float(bounds.get(k)) for k in ('x', 'y', 'width', 'height'))
            for cell in group.findall('.//s:rect[@class="cell"]', ns):
                cx, cy, cw, ch = (float(cell.get(k)) for k in ('x', 'y', 'width', 'height'))
                self.assertGreaterEqual(cx, x)
                self.assertGreaterEqual(cy, y)
                self.assertLessEqual(cx + cw, x + w + 0.2)
                self.assertLessEqual(cy + ch, y + h + 0.2)
        self.assertGreater(float(svg.get('height')), 1500)

    def test_failed_render_preserves_all_previous_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            p.publish(self.data, output, self.history)
            before = {f.name: f.read_bytes() for f in output.iterdir()}
            broken = copy.deepcopy(self.data)
            broken['panels'][0]['groups'][0]['total'] = 10 ** 12
            with self.assertRaises(p.SourceError):
                p.publish(broken, output, self.history)
            self.assertEqual(before, {f.name: f.read_bytes() for f in output.iterdir()})

    def test_all_artifacts_published_with_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            p.publish(self.data, output, self.history)
            report = (output / 'report.md').read_text(encoding='utf-8')
            self.assertIn('Named method evidence', report)
            self.assertIn('Code measurements do not depend', report)
            self.assertEqual(json.loads((output / 'progress.json').read_text()), self.data)
            for filename in ['history.svg', 'badge-methods.svg', 'badge-updated.svg']:
                ET.parse(output / filename)


if __name__ == '__main__':
    unittest.main()
