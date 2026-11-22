"""Badges and a dated history for comparable source measurements."""
from collections import Counter
from copy import deepcopy
import json
from xml.sax.saxutils import escape

BG, TEXT, MUTED = "#0d1117", "#e6edf3", "#8b949e"


def totals(snapshot):
    counts = Counter()
    for group in snapshot["groups"]:
        counts.update(group["counts"])
    return {**dict(counts), "total": sum(group["total"] for group in snapshot["groups"])}


def history_point(snapshot, day, origin):
    return {"date": day, "revision": snapshot["revision"], "origin": origin, **totals(snapshot)}


def update_history(previous, snapshot, day, backfill=(), skipped=()):
    history = deepcopy(previous) if previous else {"schema_version": 1, "series": []}
    series = next((s for s in history["series"] if s["rules_id"] == snapshot["rules_id"]), None)
    if series is None:
        series = {"rules_id": snapshot["rules_id"], "reference": snapshot["reference"], "points": []}
        history["series"].append(series)
    points = {point["date"]: point for point in series["points"]}
    for point in backfill:
        points.setdefault(point["date"], point)
    points[day] = history_point(snapshot, day, "observed")
    series["points"] = [points[d] for d in sorted(points)]
    history["current_rules_id"] = snapshot["rules_id"]
    if skipped:
        series["unmeasured_history"] = list(skipped)
    return history


def current_series(history):
    return next(s for s in history["series"] if s["rules_id"] == history["current_rules_id"])


def text(x, y, value, size=13, fill=TEXT):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}">{escape(value)}</text>'


def render_history(history, repo):
    series = current_series(history)
    points = series["points"]
    width, height = 1200, 390
    left, top, chart_width, chart_height = 66, 92, 1090, 218
    maximum = max(p["total"] for p in points)
    maximum = max(10, ((maximum + 49) // 50) * 50)
    dates = [p["date"] for p in points]
    from datetime import date
    first = date.fromisoformat(dates[0])
    days = max(1, (date.fromisoformat(dates[-1]) - first).days)
    def x(point):
        if len(points) == 1:
            return left + chart_width / 2
        return left + (date.fromisoformat(point["date"]) - first).days / days * chart_width
    def y(value):
        return top + chart_height * (1 - value / maximum)
    parts = [f'<rect width="{width}" height="{height}" rx="8" fill="{BG}"/>',
             text(28, 34, "D3D12 source history", 22),
             text(28, 58, "Daily snapshots · same scanner rules and SDK reference · counts, not game completion", 13, MUTED)]
    for i in range(6):
        value = maximum * i / 5
        py = y(value)
        parts.append(f'<path d="M {left} {py:.1f} H {left + chart_width}" stroke="#21262d"/>')
        parts.append(text(18, py + 4, str(round(value)), 12, MUTED))
    for field, color, dash, label in (("total", "#8b949e", ' stroke-dasharray="6 5"', "Reference methods"),
                                    ("body", "#2ea043", "", "Nontrivial bodies")):
        coords = " ".join(f"{x(p):.1f},{y(p[field]):.1f}" for p in points)
        parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="3"{dash}/>')
        for p in points:
            title = f"{p['date']}: {p[field]} {label.lower()} · {p['revision'][:8]} · {p['origin']}"
            parts.append(f'<a href="https://github.com/{repo}/commit/{p["revision"]}">'
                         f'<circle cx="{x(p):.1f}" cy="{y(p[field]):.1f}" r="4" fill="{color}">'
                         f'<title>{escape(title)}</title></circle></a>')
    stride = max(1, (len(points) + 7) // 8)
    for i, point in enumerate(points):
        if i % stride == 0 or i == len(points) - 1:
            px = min(max(x(point) - 34, 20), width - 95)
            parts.append(text(px, top + chart_height + 22, point["date"], 12, MUTED))
    parts += [text(28, 357, "Green: nontrivial body without a recognized unsupported marker. Dashed: SDK method total.", 12, MUTED),
              text(28, 377, f"Rules {series['rules_id']} · historical trees rescanned; earlier table-based counts are excluded.", 11, MUTED)]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" font-family="Segoe UI,Arial,sans-serif">'
            '<title id="title">Leonida D3D12 source measurement history</title>'
            '<desc id="desc">Nontrivial method bodies and the known method total over time. '
            'See history.md for dates, counts and commit links. Source presence is not verified correctness.</desc>'
            + "".join(parts) + "</svg>\n")


def history_report(history, repo):
    series = current_series(history)
    lines = ["# Source history", "", "Same scanner rules and pinned SDK reference for every point in this series.",
             "Historical points use the last first-parent main commit in each available UTC day, rescanned with today's rules.",
             "Live points use the latest main revision observed that UTC day. Missing days are not interpolated measurements.",
             "Previous coordinator-table totals are not included. Body counts do not prove correctness or compatibility.", "",
             f"Rules: `{series['rules_id']}`. [Pinned reference]({series['reference']['url']}).", "",
             "| UTC day | Bodies | Partial | No-op | Stubs | Total | Source | Measurement |",
             "|---|---:|---:|---:|---:|---:|---|---|"]
    for p in series["points"]:
        lines.append(f"| {p['date']} | {p['body']} | {p['partial']} | {p['noop']} | {p['stub']} | {p['total']} | "
                     f"[{p['revision'][:8]}](https://github.com/{repo}/commit/{p['revision']}) | {p['origin']} |")
    if series.get("unmeasured_history"):
        lines += ["", "## Unmeasured historical trees", "",
                  "These commits could not be measured with the current adapter. They are not treated as zero.", ""]
        for point in series["unmeasured_history"]:
            lines.append(f"- {point['date']} ({point['revision'][:8]}): {point['reason']}")
    if len(history["series"]) > 1:
        lines += ["", "Older rule versions are retained as separate series in history.json and are not joined to this chart."]
    return "\n".join(lines) + "\n"


def badge(label, value, color):
    left, right = max(50, 13 + len(label) * 7), max(35, 14 + len(value) * 7)
    width = left + right
    title = escape(f"{label}: {value}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="22" role="img" aria-label="{title}">'
            f'<title>{title}</title><rect width="{width}" height="22" rx="4" fill="#30363d"/>'
            f'<path d="M{left} 0h{right}v22H{left}z" fill="{color}"/>'
            '<g fill="#fff" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="11">'
            f'<text x="{left / 2}" y="15">{escape(label)}</text>'
            f'<text x="{left + right / 2}" y="15">{escape(value)}</text></g></svg>\n')


def assets(data, history):
    snapshot = data["source"]
    count = totals(snapshot)
    return {"history.json": json.dumps(history, indent=2) + "\n",
            "history.svg": render_history(history, data["upstream"]),
            "history.md": history_report(history, data["upstream"]),
            "badge-methods.svg": badge("method bodies", f"{count['body']}/{count['total']}", "#238636"),
            "badge-partial.svg": badge("partial", str(count["partial"]), "#9e6a03"),
            "badge-stubs.svg": badge("stubs", str(count["stub"]), "#484f58"),
            "badge-source.svg": badge("source", snapshot["revision"][:8], "#1f6feb"),
            "badge-updated.svg": badge("checked", data["observed_at"], "#30363d")}
