"""Read Leonida's C++ implementation surface without building or importing upstream code.

The C++ AST identifies classes, inheritance and definitions. This is a static
inventory, not a compiler, control-flow proof, or test of API behavior.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import subprocess
from urllib.request import urlopen

from tree_sitter import Language, Parser
import tree_sitter_cpp

STATES = ("body", "partial", "noop", "stub")
EXCLUDED = {"test", "tests", "generated", "third_party"}


class ScanError(ValueError):
    pass


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


def cpp_input(data):
    # Calling convention annotations are macros, not return types. Keep offsets.
    data = re.sub(rb"\b(?:STDMETHODCALLTYPE|WINAPI|APIENTRY|__stdcall)\b",
                  lambda m: b" " * len(m[0]), data)
    # tree-sitter-cpp 0.23.4 misparses unsigned(expr) in comparisons. A same-length
    # placeholder type preserves the AST's function/call structure and source offsets.
    return re.sub(rb"\bunsigned(?=\s*\()", b"uint32_t", data)


def declarator_name(node):
    if node is None:
        return ""
    if node.type in ("identifier", "field_identifier", "type_identifier", "destructor_name"):
        return node.text.decode()
    if node.type == "qualified_identifier":
        return node.text.decode()
    return declarator_name(node.child_by_field_name("declarator") or node.child_by_field_name("name"))


def parse_reference(header):
    # Public SDK interface declarations use MIDL_INTERFACE and an IUnknown chain.
    # Alternative platform ABI declarations are deduplicated by method name.
    text = re.sub(r"/\*.*?\*/|//[^\n]*", " ", header, flags=re.S)
    interfaces = {}
    pattern = re.compile(r'MIDL_INTERFACE\("[a-fA-F0-9-]+"\)\s*(\w+)\s*:\s*public\s+(\w+)\s*\{(.*?)\n\s*\};', re.S)
    for match in pattern.finditer(text):
        name, base, body = match.groups()
        methods = set(re.findall(r"\bSTDMETHODCALLTYPE\s+(\w+)\s*\(", body))
        if not methods and re.search(r"\bvirtual\b", body):
            raise ScanError(f"Unrecognized SDK declarations in {name}")
        interfaces[name] = (base, methods)
    if not interfaces:
        raise ScanError("No SDK interfaces parsed")
    return interfaces


def interface_methods(interfaces, leaf):
    result, seen = set(), set()
    while leaf != "IUnknown":
        if leaf in seen or leaf not in interfaces:
            raise ScanError(f"Unknown or cyclic SDK interface: {leaf}")
        seen.add(leaf)
        leaf, methods = interfaces[leaf]
        result.update(methods)
    return result


def parse_sources(files):
    parser = Parser(Language(tree_sitter_cpp.language()))
    classes, functions = {}, []
    for path, original in sorted(files.items()):
        if not path.endswith((".cpp", ".h", ".hpp")) or EXCLUDED.intersection(Path(path).parts):
            continue
        data = cpp_input(original.encode("utf-8"))
        root = parser.parse(data).root_node
        if root.has_error and re.search(rb"\bI[A-Z]\w*Stubs\b", data):
            raise ScanError(f"C++ parse error in generated-stub implementation file {path}")
        for node in walk(root):
            if node.type in ("class_specifier", "struct_specifier"):
                name_node = node.child_by_field_name("name")
                body = node.child_by_field_name("body")
                bases = next((c for c in node.named_children if c.type == "base_class_clause"), None)
                if name_node is None or body is None or bases is None:
                    continue
                name, base_text = name_node.text.decode(), bases.text.decode()
                # Only the generated-stub objects and their two shared template bases
                # define the measured surface. Other runtime classes are not API units.
                leaves = re.findall(r"\b(I[A-Z]\w*)Stubs\b", base_text)
                if not leaves and name not in ("Object", "Child"):
                    continue
                if name in classes:
                    raise ScanError(f"Ambiguous measured class name: {name}")
                if node.has_error:
                    errors = [str(n.start_point.row + 1) for n in walk(node) if n.type == "ERROR" or n.is_missing]
                    raise ScanError(f"C++ parse error in {path}, {name}, lines {', '.join(errors)}")
                conditions = [n for n in walk(node) if n.type.startswith(("preproc_if", "preproc_elif"))]
                ancestor = node.parent
                while ancestor is not None:
                    if ancestor.type.startswith(("preproc_if", "preproc_elif")):
                        conditions.append(ancestor)
                    ancestor = ancestor.parent
                if conditions:
                    raise ScanError(f"Conditional compilation in measured class {name}; compiler configuration needs an adapter")
                if len(set(leaves)) > 1:
                    raise ScanError(f"Multiple generated-stub bases in {name}")
                helper = re.search(r"\b(?:Child|Object)\s*<", base_text)
                if leaves and not helper and not re.fullmatch(r":\s*(?:public\s+)?I[A-Z]\w*Stubs\s*", base_text):
                    raise ScanError(f"Unrecognized generated-stub inheritance wrapper in {name}")
                parent = helper[0].split("<")[0].strip() if helper else ""
                if name == "Child":
                    parent = "Object"
                elif name == "Object":
                    parent = ""
                classes[name] = {"leaf": leaves[0] if leaves else None, "parent": parent,
                                 "path": path, "line": node.start_point.row + 1, "methods": {}, "node": node}
            elif node.type == "function_definition":
                name = declarator_name(node.child_by_field_name("declarator"))
                body = node.child_by_field_name("body")
                if not name or body is None:
                    continue
                ancestor, owner = node.parent, ""
                while ancestor is not None:
                    if ancestor.type in ("class_specifier", "struct_specifier"):
                        n = ancestor.child_by_field_name("name")
                        owner = n.text.decode() if n else ""
                        break
                    ancestor = ancestor.parent
                if "::" in name:
                    owner, name = name.rsplit("::", 1)
                    owner = owner.split("::")[-1]
                functions.append({"name": name, "owner": owner, "path": path,
                                  "line": node.start_point.row + 1, "node": node, "body": body,
                                  "parse_error": node.has_error})
    for function in functions:
        owner, name = function["owner"], function["name"]
        if owner in classes:
            if name in classes[owner]["methods"]:
                # Overloaded helpers are resolved conservatively below; COM overrides
                # cannot be ambiguous in our method-name inventory.
                classes[owner]["methods"][name].append(function)
            else:
                classes[owner]["methods"][name] = [function]
    return classes, functions


def details(function):
    body = function["body"]
    identifiers, calls = set(), set()
    for node in walk(body):
        if node.type == "identifier":
            identifiers.add(node.text.decode())
        if node.type == "call_expression":
            callee = node.child_by_field_name("function")
            if callee is None:
                continue
            if callee.type in ("identifier", "qualified_identifier", "template_function"):
                calls.add(callee.text.decode().split("::")[-1].split("<")[0])
            elif callee.type == "field_expression":
                receiver = callee.child_by_field_name("argument")
                field = callee.child_by_field_name("field")
                if receiver is not None and receiver.type == "this" and field is not None:
                    calls.add(field.text.decode())
    statements = [n for n in body.named_children if n.type != "comment"]
    trivial = not statements
    if len(statements) == 1 and statements[0].type == "return_statement":
        value = re.sub(r"\s+", "", statements[0].text.decode())[6:].rstrip(";")
        trivial = bool(re.fullmatch(r"(?:S_OK|S_FALSE|E_NOTIMPL|true|false|nullptr|NULL|\d+[uUlL]*|\{\})?", value))
    direct = bool(calls & {"stub", "note_once", "not_implemented", "unimplemented"} or "E_NOTIMPL" in identifiers)
    pure_stub = direct and (trivial or all(
        n.type in ("return_statement", "expression_statement") and
        (b"E_NOTIMPL" in n.text or re.search(rb"\b(?:stub|note_once|not_implemented|unimplemented)\s*\(", n.text))
        for n in statements))
    return {"calls": calls, "unsupported": direct, "trivial": trivial, "pure_stub": pure_stub}


def scan(files, header, revision, repo, reference):
    interfaces = parse_reference(header)
    cmake = files.get("runtime/CMakeLists.txt", "")
    commands = re.findall(r"COMMAND\s+Python3::Interpreter\s+-I\s+\S*gen_d3d12_stubs\.py(.*?)\bDEPENDS", cmake, re.S)
    requested = set(re.findall(r"\bID3D12\w+\b", " ".join(commands)))
    if not requested:
        raise ScanError("Generated D3D12 interface list not found in runtime/CMakeLists.txt")
    classes, functions = parse_sources(files)
    concrete = {name: c for name, c in classes.items() if c["leaf"]}
    if not concrete:
        raise ScanError("No concrete generated-stub classes found")
    owners = defaultdict(list)
    for name, c in concrete.items():
        owners[c["leaf"]].append(name)
        if c["leaf"] not in requested:
            raise ScanError(f"{c['leaf']} found in source but not the recognized CMake generator command")
    info = {id(f): details(f) for f in functions}
    by_owner = defaultdict(lambda: defaultdict(list))
    by_file = defaultdict(lambda: defaultdict(list))
    for f in functions:
        if f["owner"]:
            by_owner[f["owner"]][f["name"]].append(f)
        else:
            by_file[f["path"]][f["name"]].append(f)
    # Propagate unsupported markers through recognized local helpers (including
    # overloads). This is conservative: any matching overload marks the caller.
    changed = True
    while changed:
        changed = False
        for f in functions:
            d = info[id(f)]
            if d["unsupported"]:
                continue
            candidates = []
            for call in d["calls"]:
                candidates.extend(by_owner[f["owner"]].get(call, []))
                candidates.extend(by_file[f["path"]].get(call, []))
            if any(info[id(candidate)]["unsupported"] for candidate in candidates):
                d["unsupported"], changed = True, True
    symbols, groups = [], []
    for leaf in sorted(requested):
        names = interface_methods(interfaces, leaf)
        if not names:
            raise ScanError(f"Empty SDK method set for {leaf}")
        if len(owners[leaf]) > 1:
            raise ScanError(f"Multiple implementations of {leaf}; an adapter must disambiguate them")
        owner = owners[leaf][0] if owners[leaf] else None
        inherited, seen = {}, set()
        current = owner
        while current:
            if current in seen or current not in classes:
                raise ScanError(f"Unrecognized template-base chain for {leaf}: {current}")
            seen.add(current)
            for name, definitions in classes[current]["methods"].items():
                inherited.setdefault(name, definitions)
            current = classes[current]["parent"]
        counts = Counter()
        for method in sorted(names):
            definitions = inherited.get(method, [])
            state, reason, path, line = "stub", "Inherited generated fallback", "runtime/CMakeLists.txt", 1
            if definitions:
                if len(definitions) != 1 or definitions[0]["parse_error"]:
                    raise ScanError(f"Ambiguous or unparsed definition for {leaf}::{method}")
                f = definitions[0]
                d = info[id(f)]
                path, line = f["path"], f["line"]
                if d["pure_stub"]:
                    state, reason = "stub", "Explicit unsupported/logging-only body"
                elif d["unsupported"]:
                    state, reason = "partial", "Unsupported marker in body or a recognized local helper"
                elif d["trivial"]:
                    state, reason = "noop", "Empty or constant-return body (may be intentional)"
                else:
                    state, reason = "body", "Nontrivial definition; no recognized unsupported marker"
            elif owner:
                path, line = concrete[owner]["path"], concrete[owner]["line"]
            counts[state] += 1
            symbols.append({"interface": leaf, "method": method, "state": state, "reason": reason,
                            "path": path, "line": line,
                            "url": f"https://github.com/{repo}/blob/{revision}/{path}#L{line}"})
        # An override outside the reference means the pinned SDK is incomplete or
        # source patterns changed. Do not silently leave the new method out.
        if owner:
            overrides = set()
            for fns in concrete[owner]["methods"].values():
                for f in fns:
                    declarator = f["node"].child_by_field_name("declarator")
                    if declarator is not None and re.search(rb"\boverride\b", declarator.text):
                        overrides.add(f["name"])
            unknown = overrides - names - {"QueryInterface", "AddRef", "Release", "~" + owner}
            if unknown:
                raise ScanError(f"Overrides missing from reference for {leaf}: {sorted(unknown)}")
        groups.append({"name": leaf, "total": len(names), "counts": {s: counts[s] for s in STATES}})
    scanner = Path(__file__).read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    parsers = f"{version('tree-sitter')}:{version('tree-sitter-cpp')}".encode()
    rules = hashlib.sha256(scanner + reference["sha256"].encode() + parsers).hexdigest()[:16]
    return {"revision": revision, "reference": reference, "rules_id": rules,
            "files_scanned": len([p for p in files if p.endswith((".cpp", ".h", ".hpp"))]),
            "groups": sorted(groups, key=lambda g: (-g["total"], g["name"])), "symbols": symbols}


class SourceRepository:
    def __init__(self, repo, cache):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ScanError("Invalid source repository")
        self.repo, self.cache = repo, Path(cache)
        self.gitdir = self.cache / "upstream.git"

    def git(self, *args, input=None):
        result = subprocess.run(["git", "--git-dir", str(self.gitdir), *args], input=input,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        if result.returncode:
            raise ScanError(f"Git source operation failed: {result.stderr.decode(errors='replace')[:400]}")
        return result.stdout

    def refresh(self):
        self.cache.mkdir(parents=True, exist_ok=True)
        url = f"https://github.com/{self.repo}.git"
        if not self.gitdir.exists():
            result = subprocess.run(["git", "clone", "--bare", url, str(self.gitdir)], capture_output=True, timeout=180)
            if result.returncode:
                raise ScanError("Unable to cache public upstream source")
        if self.git("remote", "get-url", "origin").decode().strip() != url:
            raise ScanError("Cached source origin differs from configured repository")
        self.git("fetch", "--quiet", "origin", "+refs/heads/main:refs/heads/main")
        return self.git("rev-parse", "refs/heads/main").decode().strip()

    def files(self, revision):
        entries = self.git("ls-tree", "-rz", revision, "runtime/shims", "runtime/src", "runtime/CMakeLists.txt")
        selected = []
        for record in entries.split(b"\0"):
            if not record:
                continue
            meta, raw_path = record.split(b"\t", 1)
            mode, kind, oid = meta.split()
            path = raw_path.decode()
            if kind != b"blob" or mode not in (b"100644", b"100755"):
                continue
            if EXCLUDED.intersection(Path(path).parts):
                continue
            if path.endswith((".cpp", ".h", ".hpp")) or path == "runtime/CMakeLists.txt":
                selected.append((path, oid))
        blobs = self.git("cat-file", "--batch", input=b"".join(oid + b"\n" for _, oid in selected))
        output, cursor = {}, 0
        for path, _ in selected:
            end = blobs.index(b"\n", cursor)
            _, kind, size = blobs[cursor:end].split()
            if kind != b"blob":
                raise ScanError("Unexpected source Git object")
            cursor = end + 1
            output[path] = blobs[cursor:cursor + int(size)].decode("utf-8")
            cursor += int(size) + 1
        return output

    def history_revisions(self, days=14):
        log = self.git("log", "--first-parent", "--format=%H %cI", "refs/heads/main").decode().splitlines()
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
        daily = {}
        for line in log:
            revision, timestamp = line.split(" ", 1)
            day = datetime.fromisoformat(timestamp).astimezone(timezone.utc).date().isoformat()
            if day >= cutoff:
                daily.setdefault(day, (revision, timestamp))
        return [(day, *daily[day]) for day in sorted(daily)]


def load_reference(config, cache):
    revision, expected = config["revision"], config["sha256"]
    if not re.fullmatch(r"[a-f0-9]{40}", revision) or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise ScanError("Invalid pinned SDK reference")
    url = f"https://raw.githubusercontent.com/microsoft/DirectX-Headers/{revision}/include/directx/d3d12.h"
    path = Path(cache) / f"d3d12-{revision}.h"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        data = path.read_bytes()
    else:
        with urlopen(url, timeout=45) as response:
            data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ScanError("Pinned SDK header hash mismatch")
    if not path.exists():
        path.write_bytes(data)
    return data.decode("utf-8"), {"url": url, "revision": revision, "sha256": expected,
                                 "denominator": "SDK inheritance chains excluding IUnknown"}
