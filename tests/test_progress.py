import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location("progress", Path(__file__).resolve().parents[1] / "progress.py")
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)

METHODS = """### Method coverage
| Interface | Methods | On `main` | In open PRs | Open |
|---|---:|---:|---:|---:|
| `ID3D12Device11` | 8 | 3 | 2 | 3 |
| `ID3D12Fence1` | 3 | 1 | 0 | 2 |

### Up for grabs
| ID | What | Needs |
|---|---|---|
| D3D-99 | A synthetic task | CPU |

### Who builds what
| ID | Item | Owner | PR | Status |
|---|---|---|---|---|
| D3D-1 | Example | @example | #5 | PR open |
| D3D-2 | Example | @example | #6 | waits for #5 |
"""
TASKS = r"""### Up for grabs
| ID | What | Needs |
|---|---|---|
| ⭐ TEST-1 | A test with `a|b` and x\|y | CPU |
| NEW-9 | A newly introduced workstream | CPU |

### Open work
| ID | Item | Owner | PR | Status |
|---|---|---|---|---|
| TEST-2 | Example | @example | #7 | PR open |
| TEST-3 | Example | @example | #8 merged, #9 | older work merged; PR open |
| TEST-4 | Example | — | — | uncertain |
| D3D-99 | Example | @example | #10 | claimed |

**Blocked, not up for grabs yet:** RT-5 Boot (waits for executable); FUZZ-10 Case (waits for SHADER-90).
"""


def issue(number, body):
    return {"number": number, "body": body, "html_url": f"https://github.com/example/project/issues/{number}",
            "updated_at": "2026-01-01T00:00:00Z", "state": "open"}


class FakeAPI:
    def __init__(self, coordination=TASKS, methods=METHODS):
        self.coordination = issue(700, coordination)
        self.methods = issue(313, methods)
        self.calls = []

    def get(self, endpoint):
        self.calls.append(endpoint)
        if endpoint.startswith("search/issues?"):
            return {"items": [{"number": 700, "title": "Coordinating who works on what (4)"}],
                    "incomplete_results": False}
        return self.methods if endpoint.endswith("/313") else self.coordination


CONFIG = {"upstream": "example/project", "method_issue": 313,
          "coordination_title": "Coordinating who works on what", "repository": "example/tracker"}


class ParserTests(unittest.TestCase):
    def test_method_counts(self):
        groups = p.method_groups(METHODS)
        self.assertEqual(groups[0]["counts"], {"main": 3, "pr": 2, "open": 3})
        self.assertEqual(sum(g["total"] for g in groups), 11)

    def test_new_interfaces_are_discovered(self):
        body = METHODS.replace("| `ID3D12Fence1`", "| `ID3D12BrandNewObject` | 1 | 0 | 1 | 0 |\n| `ID3D12Fence1`")
        self.assertEqual(len(p.method_groups(body)), 3)

    def test_rejects_bad_denominators_and_missing_tables(self):
        for bad in [METHODS.replace("| 8 | 3 | 2 | 3 |", "| 8 | 8 | 2 | 3 |"),
                    METHODS.replace("| 8 | 3 | 2 | 3 |", "| 8 | -1 | 2 | 7 |"),
                    METHODS.replace("| 8 | 3 | 2 | 3 |", "| 8 | yes | 2 | 3 |"),
                    METHODS.replace("In open PRs", "Changed schema"), "no table"]:
            with self.subTest(bad=bad), self.assertRaises(p.SourceError):
                p.method_groups(bad)

    def test_duplicate_interfaces_rejected(self):
        with self.assertRaises(p.SourceError):
            p.method_groups(METHODS + METHODS)

    def test_escaped_and_code_pipes(self):
        tasks = p.task_inventory([issue(1, TASKS)])
        self.assertIn("TEST-1", {t["id"] for t in tasks})

    def test_dedup_and_blocked_dependencies_not_counted(self):
        tasks = p.task_inventory([issue(1, METHODS), issue(2, TASKS)])
        states = {t["id"]: t["state"] for t in tasks}
        self.assertEqual(states["D3D-99"], "active")
        self.assertEqual(states["D3D-2"], "blocked")
        self.assertEqual(states["RT-5"], "blocked")
        self.assertNotIn("SHADER-90", states)
        self.assertEqual(states["TEST-4"], "unknown")
        self.assertEqual(states["TEST-3"], "active")
        self.assertEqual(len(states), len(tasks))

    def test_new_workstream(self):
        groups = p.task_groups(p.task_inventory([issue(1, TASKS)]))
        self.assertIn("NEW", {g["name"] for g in groups})

    def test_malformed_task_row_fails_closed(self):
        with self.assertRaises(p.SourceError):
            p.task_inventory([issue(1, TASKS.replace("| NEW-9 |", "| not-an-id |"))])

    def test_missing_task_tables_fail_closed(self):
        with self.assertRaises(p.SourceError):
            p.task_inventory([issue(1, "Only prose")])

    def test_coordinator_rollover_is_discovered(self):
        api = FakeAPI()
        data = p.collect(CONFIG, api, "2026-01-01 00:00 UTC")
        self.assertEqual(data["sources"][1]["number"], 700)
        self.assertTrue(any(call.endswith("/700") for call in api.calls))

    def test_ambiguous_search_does_not_guess(self):
        class Ambiguous(FakeAPI):
            def get(self, endpoint):
                if endpoint.startswith("search/"):
                    return {"items": [{"number": n, "title": "Coordinating who works on what"} for n in (1, 2)]}
                return super().get(endpoint)
        with self.assertRaises(p.SourceError):
            p.collect(CONFIG, Ambiguous(), "now")

    def test_closed_source_fails(self):
        api = FakeAPI()
        api.methods["state"] = "closed"
        with self.assertRaises(p.SourceError):
            p.collect(CONFIG, api, "now")


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.data = p.collect(CONFIG, FakeAPI(), "2026-01-01 00:00 UTC")

    def test_one_square_per_item_and_correct_colors(self):
        svg = ET.fromstring(p.render_svg(self.data))
        cells = [r for r in svg.iter() if r.get("class") == "cell"]
        expected = sum(g["total"] for panel in self.data["panels"] for g in panel["groups"])
        self.assertEqual(len(cells), expected)
        self.assertEqual(sum(r.get("data-state") == "main" for r in cells), 4)
        self.assertTrue(all(r.get("fill") == p.COLORS[r.get("data-state")] for r in cells))
        self.assertFalse(any(r.tag.endswith("script") for r in svg.iter()))

    def test_xml_escapes_untrusted_names(self):
        self.data["panels"][1]["groups"][0]["name"] = '<script>alert("x")</script> & category'
        svg = p.render_svg(self.data)
        ET.fromstring(svg)
        self.assertNotIn("<script>", svg)

    def test_auto_expansion_and_no_cells_outside_groups(self):
        self.data["panels"][0]["groups"] = [
            {"name": f"ID3D12Object{i}", "total": i + 1, "counts": {"main": i, "pr": 1, "open": 0}}
            for i in range(35)]
        svg = ET.fromstring(p.render_svg(self.data))
        ns = {"s": "http://www.w3.org/2000/svg"}
        for group in svg.findall("s:g", ns):
            bounds = group.find("s:rect", ns)
            x, y, w, h = (float(bounds.get(k)) for k in ("x", "y", "width", "height"))
            for cell in group.findall("s:rect[@class='cell']", ns):
                cx, cy, cw, ch = (float(cell.get(k)) for k in ("x", "y", "width", "height"))
                self.assertGreaterEqual(cx, x)
                self.assertGreaterEqual(cy, y)
                self.assertLessEqual(cx + cw, x + w + 0.2)
                self.assertLessEqual(cy + ch, y + h + 0.2)
        self.assertGreater(float(svg.get("height")), 1500)

    def test_failed_render_preserves_previous_files(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            p.publish(self.data, output)
            before = {f.name: f.read_bytes() for f in output.iterdir()}
            broken = copy.deepcopy(self.data)
            broken["panels"][0]["groups"][0]["total"] = 10 ** 12
            with self.assertRaises(p.SourceError):
                p.publish(broken, output)
            self.assertEqual(before, {f.name: f.read_bytes() for f in output.iterdir()})

    def test_report_and_json_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            p.publish(self.data, Path(temp))
            report = (Path(temp) / "report.md").read_text(encoding="utf-8")
            self.assertIn("https://github.com/example/project/issues/313", report)
            self.assertIn("not independently", report)
            self.assertEqual(json.loads((Path(temp) / "progress.json").read_text()), self.data)


if __name__ == "__main__":
    unittest.main()
