"""Build an evidence-linked README SVG from Leonida's public coordination tables.

Python 3.12+, standard library only. Reads metadata, never runs upstream code.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
METHOD_STATES = ("main", "pr", "open")
TASK_STATES = ("active", "available", "blocked", "unknown")
COLORS = {"main": "#2ea043", "pr": "#d29922", "open": "#484f58",
          "active": "#d29922", "available": "#484f58", "blocked": "#f47067", "unknown": "#79c0ff"}
LABELS = {"main": "On main", "pr": "In open PRs", "open": "Unimplemented",
          "active": "Active / claimed", "available": "Available", "blocked": "Blocked", "unknown": "Unclear"}
WORKSTREAMS = {"D3D": "D3D12 / Vulkan", "SHADER": "Shader translator", "ASSET": "Assets / formats",
               "BUILD": "Build / tools", "TEST": "Tests / CI", "RT": "Runtime", "FUZZ": "Fuzzing",
               "PROC": "Contributor process"}
ID = re.compile(r"(?<![A-Z0-9])([A-Z][A-Z0-9]*-\d+)\b")
BG, PANEL, TEXT, MUTED, BORDER = "#0d1117", "#161b22", "#e6edf3", "#8b949e", "#30363d"


class SourceError(ValueError):
    """A source no longer has the structure or invariants we can measure."""


def clean(value: str) -> str:
    return re.sub(r"[*`_]", "", value).strip().lower()


def markdown_tables(body: str):
    """Yield (section, headers, rows); escaped pipes and pipes in code stay in a cell."""
    def cells(line):
        result, current, in_code, escaped = [], [], False, False
        for char in line.strip().strip("|"):
            if escaped:
                current.append(char)
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "`":
                in_code = not in_code
                current.append(char)
            elif char == "|" and not in_code:
                result.append("".join(current).strip())
                current = []
            else:
                current.append(char)
        result.append("".join(current).strip())
        return result

    section, header, rows = "", None, []
    for line in [*body.splitlines(), ""]:
        if not line.strip().startswith("|"):
            if header is not None:
                yield section, header, rows
                header, rows = None, []
            if re.match(r"^#{1,6}\s", line):
                section = re.sub(r"^#+\s*", "", line).strip()
            continue
        row = cells(line)
        if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in row):
            continue
        if header is None:
            header = row
        else:
            rows.append(row)


def method_groups(body: str):
    groups = []
    for _, headers, rows in markdown_tables(body):
        if [clean(h) for h in headers] != ["interface", "methods", "on main", "in open prs", "open"]:
            continue
        for row in rows:
            if len(row) != 5:
                raise SourceError("Method table column count changed")
            name = row[0].strip().strip("`")
            if not re.fullmatch(r"I[A-Z][A-Za-z0-9_]+", name):
                raise SourceError(f"Unexpected interface name: {name!r}")
            try:
                total, main, pr, opened = [int(clean(c).replace(",", "")) for c in row[1:]]
            except ValueError as error:
                raise SourceError(f"Non-numeric method counts for {name}") from error
            if min(total, main, pr, opened) < 0 or total == 0 or main + pr + opened != total:
                raise SourceError(f"Method counts do not sum to total for {name}")
            groups.append({"name": name, "total": total, "counts": {"main": main, "pr": pr, "open": opened}})
    if not groups or len({g["name"] for g in groups}) != len(groups):
        raise SourceError("Method coverage table missing, empty or duplicated; keeping last good output")
    return sorted(groups, key=lambda g: (-g["total"], g["name"]))


def task_inventory(issues):
    tasks = {}
    precedence = {"unknown": 0, "available": 1, "active": 2, "blocked": 3}

    def add(task_id, state, issue):
        previous = tasks.get(task_id)
        if previous is None or precedence[state] > precedence[previous["state"]]:
            tasks[task_id] = {"id": task_id, "state": state, "source": issue["html_url"]}

    for issue in issues:
        found = 0
        for section, headers, rows in markdown_tables(issue["body"]):
            names = [clean(h) for h in headers]
            if not names or names[0] != "id":
                continue
            found += 1
            for row in rows:
                if len(row) != len(headers):
                    raise SourceError(f"Task table column count changed in #{issue['number']}")
                matches = ID.findall(row[0])
                if len(matches) != 1:
                    raise SourceError(f"Task row without one task ID in #{issue['number']}")
                state = "unknown"
                status = row[names.index("status")] if "status" in names else ""
                if re.search(r"\b(blocked|waits? for|waiting|depends on|held by)\b", status, re.I):
                    state = "blocked"
                elif clean(section) == "up for grabs":
                    state = "available"
                elif "owner" in names and row[names.index("owner")].strip() not in ("", "—", "-"):
                    # An open-work row stays active even if it mentions an older merged PR.
                    state = "active"
                add(matches[0], state, issue)
        if not found:
            raise SourceError(f"No task tables found in #{issue['number']}")
        for line in issue["body"].splitlines():
            if line.startswith("**Blocked, not up for grabs"):
                _, _, tail = line.partition(":**")
                for part in tail.split(";"):
                    match = re.match(r"\s*([A-Z][A-Z0-9]*-\d+)\b", part)
                    if match:
                        add(match[1], "blocked", issue)
    if not tasks:
        raise SourceError("Task inventory is empty")
    return sorted(tasks.values(), key=lambda t: (t["id"].split("-")[0], int(t["id"].split("-")[1])))


def task_groups(tasks):
    counts = defaultdict(Counter)
    for task in tasks:
        counts[task["id"].split("-")[0]][task["state"]] += 1
    return sorted([{"name": WORKSTREAMS.get(prefix, prefix), "prefix": prefix,
                    "total": sum(states.values()), "counts": {s: states[s] for s in TASK_STATES}}
                   for prefix, states in counts.items()], key=lambda g: (-g["total"], g["prefix"]))


class GitHub:
    def __init__(self, use_cli=False):
        self.use_cli = use_cli

    def get(self, endpoint):
        # Endpoints are constructed here, never from an upstream document.
        for attempt in range(3):
            try:
                if self.use_cli:
                    run = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True,
                                         encoding="utf-8", check=True, timeout=60)
                    return json.loads(run.stdout)
                headers = {"Accept": "application/vnd.github+json", "User-Agent": "leonida-progress/1.0",
                           "X-GitHub-Api-Version": "2022-11-28"}
                token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
                if token:
                    headers["Authorization"] = "Bearer " + token
                with urlopen(Request("https://api.github.com/" + endpoint, headers=headers), timeout=45) as response:
                    return json.load(response)
            except HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise SourceError(f"GitHub API HTTP {error.code}; keeping last good output") from error
            except (URLError, TimeoutError, subprocess.SubprocessError, json.JSONDecodeError) as error:
                if attempt == 2:
                    raise SourceError("GitHub request failed; keeping last good output") from error
            time.sleep(2 ** attempt)


def collect(config, api, observed_at):
    repo = config["upstream"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise SourceError("Invalid upstream repository")
    query = f'repo:{repo} is:issue is:open in:title "{config["coordination_title"]}"'
    search = api.get("search/issues?" + urlencode({"q": query, "per_page": 100}))
    if search.get("incomplete_results"):
        raise SourceError("Incomplete coordination issue search")
    candidates = [i for i in search.get("items", [])
                  if i["title"].startswith(config["coordination_title"]) and not i.get("pull_request")]
    if len(candidates) != 1:
        raise SourceError("Expected one open coordination issue; keeping last good output")
    coordination = api.get(f"repos/{repo}/issues/{candidates[0]['number']}")
    methods = api.get(f"repos/{repo}/issues/{int(config['method_issue'])}")
    for issue in (methods, coordination):
        if not issue.get("body") or issue.get("state") != "open":
            raise SourceError(f"Source issue #{issue.get('number')} is closed or empty")
    tasks = task_inventory([methods, coordination])
    sources = [{"number": i["number"], "url": i["html_url"], "updated_at": i["updated_at"]}
               for i in (methods, coordination)]
    panels = [
        {"id": "methods", "title": "D3D12 method implementation", "unit": "methods",
         "note": "Coordinator-reported implementation status. Green does not mean GPU-tested.",
         "states": list(METHOD_STATES), "groups": method_groups(methods["body"])},
        {"id": "tasks", "title": "Open contribution tasks", "unit": "tasks",
         "note": "Current coordination tables only. Tasks leaving these tables are not assumed complete.",
         "states": list(TASK_STATES), "groups": task_groups(tasks)},
    ]
    if sum(g["total"] for p in panels for g in p["groups"]) > 50000:
        raise SourceError("Inventory exceeds 50,000 cells; review the source before rendering")
    return {"schema_version": 1, "upstream": repo, "repository": config["repository"], "observed_at": observed_at,
            "sources": sources, "panels": panels, "tasks": tasks,
            "verification": "No game, runtime or GPU tests run by this tracker. Not a game-completion estimate."}


def treemap(items, x, y, width, height):
    """Pack descending category areas into rows with near-square rectangles."""
    remaining = [(name, size * width * height / sum(v for _, v in items)) for name, size in items]
    output = {}

    def aspect(row, side):
        total = sum(v for _, v in row)
        return max(max(side * side * v / total ** 2, total ** 2 / (side * side * v)) for _, v in row)

    while remaining:
        side, count = min(width, height), 1
        while count < len(remaining) and aspect(remaining[:count + 1], side) <= aspect(remaining[:count], side):
            count += 1
        row, remaining = remaining[:count], remaining[count:]
        area = sum(v for _, v in row)
        if width >= height:
            strip, offset = area / height, y
            for name, value in row:
                output[name] = (x, offset, strip, value / strip)
                offset += value / strip
            x, width = x + strip, width - strip
        else:
            strip, offset = area / width, x
            for name, value in row:
                output[name] = (offset, y, value / strip, strip)
                offset += value / strip
            y, height = y + strip, height - strip
    return output


def fit_cells(total, width, height):
    for size in range(min(36, int(width), int(height)), 1, -1):
        columns = int((width + 2) // (size + 2))
        if columns and math.ceil(total / columns) * (size + 2) - 2 <= height:
            return size, columns
    raise SourceError("Category too small to draw every square; increase the panel size")


def svg_text(x, y, value, size=14, fill=TEXT, bold=False):
    weight = ' font-weight="600"' if bold else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"{weight}>{escape(value)}</text>'


def render_svg(data):
    width, y = 1200, 144
    parts = [svg_text(28, 40, "Leonida progress tracker", 25, bold=True),
             svg_text(28, 66, "Implementation and contribution inventory · not a measure of game completion.", 14, MUTED),
             svg_text(28, 90, f"Checked {data['observed_at']} · hourly refresh · sources: "
                      + ", ".join(f"#{s['number']}" for s in data["sources"]), 13, MUTED),
             svg_text(28, 114, "Reported by Leonida's coordinator; this tracker does not run GPU or game tests.", 13, MUTED)]
    for panel in data["panels"]:
        groups, states = panel["groups"], panel["states"]
        total = sum(g["total"] for g in groups)
        chart_height = max(330, math.ceil(total / 500) * 330, math.ceil(len(groups) / 9) * 330)
        boxes = treemap([(g["name"], g["total"]) for g in groups], 40, y + 108, width - 80, chart_height)
        contents, unlabelled = [], []
        for group in groups:
            gx, gy, gw, gh = boxes[group["name"]]
            short = group["name"].removeprefix("ID3D12")
            summary = " / ".join(str(group["counts"][s]) for s in states)
            labelled = max(len(short) * 7.2, len(summary) * 6.5) <= gw - 14 and gh > 88
            inset = 52 if labelled else 6
            size, cols = fit_cells(group["total"], gw - 12, gh - inset - 6)
            details = ", ".join(f"{group['counts'][s]} {LABELS[s]}" for s in states)
            contents.append(f'<g><title>{escape(group["name"] + ": " + details)}</title>'
                            f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}" '
                            f'fill="{PANEL}" stroke="{BG}" stroke-width="3"/>')
            if labelled:
                contents += [svg_text(gx + 7, gy + 20, short, 14, bold=True),
                             svg_text(gx + 7, gy + 39, summary, 12, MUTED)]
            else:
                unlabelled.append(f"{short}: {summary}")
            index = 0
            for state in states:
                for _ in range(group["counts"][state]):
                    cx, cy = gx + 6 + index % cols * (size + 2), gy + inset + index // cols * (size + 2)
                    contents.append(f'<rect class="cell" data-state="{state}" x="{cx:.1f}" y="{cy:.1f}" '
                                    f'width="{size}" height="{size}" fill="{COLORS[state]}"/>')
                    index += 1
            contents.append("</g>")
        notes = []
        # Small categories keep their full counts outside the treemap, as in the reference graphic.
        line = ""
        for label in unlabelled:
            if len(line + label) > 140:
                notes.append(line)
                line = ""
            line += (" · " if line else "") + label
        if line:
            notes.append(line)
        panel_height = 126 + chart_height + 19 * len(notes)
        parts.append(f'<rect x="24" y="{y}" width="{width - 48}" height="{panel_height}" rx="8" '
                     f'fill="{PANEL}" stroke="{BORDER}"/>')
        counts = Counter()
        for group in groups:
            counts.update(group["counts"])
        heading = f"{panel['title']}: {total} {panel['unit']}"
        if panel["id"] == "methods":
            heading += f" · {counts['main']} on main · {counts['pr']} in PRs · {counts['open']} open"
        parts += [svg_text(40, y + 27, heading, 18, bold=True),
                  svg_text(40, y + 51, panel["note"], 13, MUTED)]
        lx = 40
        for state in states:
            label = f"{LABELS[state]} ({counts[state]})"
            parts.append(f'<rect x="{lx}" y="{y + 72}" width="11" height="11" fill="{COLORS[state]}"/>')
            parts.append(svg_text(lx + 18, y + 82, label, 12))
            lx += 34 + len(label) * 7
        parts.append(svg_text(40, y + 101, "Group counts follow the legend order. One square = one "
                              + ("method." if panel["id"] == "methods" else "listed task."), 11, MUTED))
        parts.extend(contents)
        for i, note in enumerate(notes):
            parts.append(svg_text(40, y + 108 + chart_height + 17 + 19 * i, note, 11, MUTED))
        y += panel_height + 18
    parts.append(svg_text(28, y + 12, f"Sources and definitions: github.com/{data['repository']} · open the README for evidence links.", 12, MUTED))
    height = y + 36
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" '
            'font-family="Segoe UI,Helvetica,Arial,sans-serif">'
            '<title id="title">Leonida implementation and contribution tracker</title>'
            '<desc id="desc">One square per reported method or listed task. '
            'Implementation is not test verification or game completion. See data/report.md for a text table.</desc>'
            f'<rect width="{width}" height="{height}" fill="{BG}"/>' + "".join(parts) + "</svg>\n")


def render_report(data):
    lines = ["# Leonida tracker evidence", "", f"Checked: {data['observed_at']}", "", data["verification"], "",
             "## Sources", ""]
    for source in data["sources"]:
        lines.append(f"- [Issue #{source['number']}]({source['url']}); source updated {source['updated_at']}.")
    lines += ["", "The source update time includes comments; it does not prove when the tables were last reconciled.",
              "Counts are coordinator-reported, not independently scanned from C++ or verified by this tracker.", ""]
    for panel in data["panels"]:
        lines += ["## " + panel["title"], "", panel["note"], "",
                  "| Group | Total | " + " | ".join(LABELS[s] for s in panel["states"]) + " |",
                  "|---|---:|" + "---:|" * len(panel["states"])]
        for group in panel["groups"]:
            lines.append(f"| {group['name']} | {group['total']} | "
                         + " | ".join(str(group["counts"][s]) for s in panel["states"]) + " |")
        lines.append("")
    lines += ["## Listed task IDs", "", "This is an inventory of the current tables, not a lifetime completion ledger.",
              "Active includes claimed work and PRs; blocked is recognized only from explicit status text.",
              "New task prefixes are discovered automatically. Repeated task IDs count once.", "",
              "| Task | State | Evidence |", "|---|---|---|"]
    lines += [f"| {task['id']} | {LABELS[task['state']]} | [Coordination table]({task['source']}) |"
              for task in data["tasks"]]
    return "\n".join(lines) + "\n"


def publish(data, output):
    """Validate and render everything before replacing any last-known-good file."""
    payloads = {"progress.json": json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                "dashboard.svg": render_svg(data), "report.md": render_report(data)}
    output.mkdir(parents=True, exist_ok=True)
    # Workflow commits only after the process succeeds; a failed run never publishes partial outputs.
    for name, content in payloads.items():
        fd, temporary = tempfile.mkstemp(dir=output, prefix=".pending-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
            os.replace(temporary, output / name)
        finally:
            Path(temporary).unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "tracker.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data")
    parser.add_argument("--gh-cli", action="store_true", help="use your authenticated gh CLI for local requests")
    args = parser.parse_args(argv)
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        data = collect(config, GitHub(args.gh_cli), now)
        publish(data, args.output)
    except (SourceError, OSError, KeyError, json.JSONDecodeError) as error:
        print(f"Tracker refresh failed: {error}", file=sys.stderr)
        return 1
    print(f"Updated {args.output}: {sum(g['total'] for g in data['panels'][0]['groups'])} methods, "
          f"{len(data['tasks'])} listed tasks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
