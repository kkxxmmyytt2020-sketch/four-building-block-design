"""Render the three-panel literature dashboard from the project state file.

    python3 render_dashboard.py fbb-state.json [-o fbb-dashboard.html]

Panel 1  existing constructs (jingle-jangle check) + schematic overlap diagram
Panel 2  construct map, click-to-expand: definition, blind-sort verdict, example items
Panel 3  existing items / instruments

Styling comes from assets/literature-dashboard-template.html so the two never drift.
Re-run after every state change; the output file is overwritten in place.
"""
import argparse
import datetime as dt
import html
import json
import math
import re
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "literature-dashboard-template.html"

REL = {  # relationship -> (tag class, label, venn colour, circle radius, distance from ours, dashed)
    "jangle": ("tag-jangle", "Jangle risk", "#c99a1f", 62, 38, False),
    "related": ("tag-clear", "Related but distinct", "#4a9d6f", 46, 100, False),
    "jingle": ("tag-jingle", "Jingle risk", "#b13a3a", 40, 150, True),
    "none": ("tag-clear", "No conflict", "#8c959f", 36, 150, False),
}
OUR_R = 72
CX, CY, VW, VH = 230, 170, 460, 340


def e(x):
    return html.escape(str(x if x is not None else ""))


def style_block():
    m = re.search(r"<style>.*?</style>", TEMPLATE.read_text(), re.S)
    return m.group(0) if m else "<style></style>"


def venn(construct_name, rows):
    rows = [r for r in rows if r.get("relationship") in REL][:6]
    if not rows:
        return ""
    parts = [
        f'<circle cx="{CX}" cy="{CY}" r="{OUR_R}" fill="#3a5a8c" fill-opacity="0.35" '
        f'stroke="#3a5a8c" stroke-width="2"/>',
        f'<text x="{CX}" y="{CY + 4}" font-size="13" text-anchor="middle" font-weight="600" '
        f'fill="#1a1a1a">{e(construct_name)}</text>',
    ]
    for i, r in enumerate(rows):
        _, _, colour, rad, dist, dashed = REL[r["relationship"]]
        ang = -math.pi / 2 + i * 2 * math.pi / len(rows)
        x = CX + dist * math.cos(ang) * 1.25
        y = CY + dist * math.sin(ang) * 0.75
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        opacity = "0.12" if dashed else "0.30"
        parts.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="{colour}" fill-opacity="{opacity}" '
            f'stroke="{colour}" stroke-width="2"{dash}/>'
        )
        ty = y - rad - 6 if y < CY else y + rad + 14
        ty = min(max(ty, 14), VH - 4)
        parts.append(
            f'<text x="{x:.0f}" y="{ty:.0f}" font-size="12" text-anchor="middle" font-weight="600" '
            f'fill="#1a1a1a">{e(r.get("name", ""))}</text>'
        )
    legend = "".join(
        f'<div class="legend-row"><span class="swatch" style="background:{c};"></span> {e(lbl)}</div>'
        for key, (_, lbl, c, *_rest) in REL.items()
        if any(r["relationship"] == key for r in rows)
    )
    return (
        '<div class="venn-wrap">'
        f'<svg viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" role="img" '
        f'aria-label="Schematic overlap between our construct and constructs found">{"".join(parts)}</svg>'
        '<div class="venn-legend"><div class="legend-row"><span class="swatch" style="background:#3a5a8c;">'
        f'</span> Our construct</div>{legend}'
        '<p class="venn-note">Overlap is a qualitative judgment made during the search, not a '
        "statistic. Dashed outline = same name, different meaning.</p></div></div>"
    )


def panel1(state):
    lit = state.get("literature", {})
    rows = lit.get("constructs", [])
    kws = lit.get("keywords", [])
    body = "".join(
        "<tr>"
        f"<td>{e(r.get('keyword'))}</td><td>{e(r.get('name'))}</td><td>{e(r.get('source'))}</td>"
        f"<td>{e(r.get('definition'))}</td>"
        f"<td><span class=\"tag {REL.get(r.get('relationship'), REL['none'])[0]}\">"
        f"{e(REL.get(r.get('relationship'), REL['none'])[1])}</span></td>"
        f"<td>{e(r.get('action'))}</td></tr>"
        for r in rows
    )
    if not rows:
        msg = f"Searched {', '.join(kws)}; nothing relevant found." if kws else "Not yet run."
        body = f'<tr><td colspan="6" class="empty-note">{e(msg)}</td></tr>'
    name = state.get("project", {}).get("construct", "Our construct")
    return (
        '<section id="constructs"><h2>Panel 1 — Existing constructs (jingle-jangle check)</h2>'
        f'<p class="verdict">{e(lit.get("verdict", ""))}'
        + (f"<br>Keywords searched: {e('; '.join(kws))}" if kws else "")
        + "</p>"
        + venn(name, rows)
        + "<table><thead><tr><th>Keyword searched</th><th>Construct/instrument found</th><th>Source</th>"
        "<th>Definition (short)</th><th>Relationship</th><th>Recommended action</th></tr></thead>"
        f"<tbody>{body}</tbody></table></section>"
    )


def stress_field(wid, stress):
    rounds = stress.get("rounds", [])
    if not rounds:
        return '<div class="stress-detail">Not yet run.</div>'
    history = []
    for r in rounds:
        for pw in r.get("per_waypoint", []):
            if pw["waypoint"] == wid:
                history.append((r["round"], pw))
    if not history:
        return '<div class="stress-detail">No vignettes for this waypoint.</div>'
    last_round, last = history[-1]
    note = stress.get("resolution", {}).get(wid, "")
    earlier = [
        f"round {rn}: confused with {', '.join(c['waypoint'] for c in pw['confused_with'])}"
        for rn, pw in history[:-1]
        if pw["status"] == "confused"
    ]
    if last["status"] == "clean":
        badge = '<span class="stress-badge stress-clean">✓ No confusion</span>'
        detail = f"Sorted correctly in {last['correct']}/{last['n']} vignettes, round {last_round}."
    elif last["status"] == "confused":
        others = ", ".join(c["waypoint"] for c in last["confused_with"])
        badge = f'<span class="stress-badge stress-confused">⚠ Confused with {e(others)}</span>'
        wrong = last["n"] - last["correct"]
        detail = f"{wrong} of {last['n']} vignettes sorted elsewhere in round {last_round}."
        if not note:
            note = "Not yet resolved — open risk in the design document."
    else:
        return '<div class="stress-detail">No vignettes for this waypoint.</div>'
    if earlier:
        detail += " Earlier: " + "; ".join(earlier) + "."
    if note:
        detail += " " + note
    return f'{badge}<div class="stress-detail">{e(detail)}</div>'


def panel2(state):
    cm = state.get("construct_map", {})
    wps = cm.get("waypoints", [])
    stress = cm.get("stress_test", {})
    bank = state.get("items", {}).get("bank", [])
    items_started = bool(bank) or state.get("stages", {}).get("b2", {}).get("status") not in (None, "not_started")
    entries = []
    for w in reversed(wps):  # show the top of the map first
        mine = [it for it in bank if w["id"] in it.get("waypoints", [])]
        if mine:
            ex = "<br>".join(f"{e(it.get('text'))} <em>({e(it.get('origin', 'new'))})</em>" for it in mine[:3])
        elif items_started:
            ex = "<em>No item yet — coverage gap.</em>"
        else:
            ex = "Not yet available — completes in Block 2."
        entries.append(
            '<details class="waypoint">'
            f"<summary>{e(w['id'])} {e(w.get('label', ''))}"
            + (f" — {e(w['cue'])}" if w.get("cue") else "")
            + "</summary><div class=\"wp-body\">"
            f'<div class="field"><span class="field-label">Definition</span>{e(w.get("definition"))}</div>'
            f'<div class="field"><span class="field-label">Stress-test result</span>{stress_field(w["id"], stress)}</div>'
            f'<div class="field"><span class="field-label">Example item(s) targeting this waypoint</span>{ex}</div>'
            "</div></details>"
        )
    if not entries:
        entries = ['<p class="empty-note">Construct map not drafted yet.</p>']
    last = stress.get("rounds", [])[-1:] or [{}]
    verdict = (
        f"{len(wps)} waypoints, {e(cm.get('map_type', 'map type not set'))} map, shown top (high) to bottom (low). "
        + (f"Blind sort: {e(last[0].get('verdict'))}." if last[0] else "Blind sort not yet run.")
    )
    return (
        '<section id="waypoints"><h2>Panel 2 — Construct map (click a waypoint)</h2>'
        f'<p class="verdict">{verdict}</p><div class="waypoint-list">{"".join(entries)}</div></section>'
    )


def panel3(state):
    it = state.get("items", {})
    rows = it.get("existing", [])
    body = "".join(
        "<tr>"
        f"<td>{e(r.get('source'))}</td><td>{e(r.get('description'))}</td>"
        f"<td>{e(', '.join(r.get('waypoints', [])))}</td><td>{e(r.get('format'))}</td>"
        f"<td>{e(r.get('license'))}</td><td>{e(r.get('decision'))}</td></tr>"
        for r in rows
    )
    if not rows:
        kws = it.get("keywords", [])
        msg = f"Searched {', '.join(kws)}; nothing reusable found." if kws else "Not yet run — completes in Block 2."
        body = f'<tr><td colspan="6" class="empty-note">{e(msg)}</td></tr>'
    return (
        '<section id="items"><h2>Panel 3 — Existing items/instruments</h2>'
        f'<p class="verdict">{e(it.get("verdict", ""))}</p>'
        "<table><thead><tr><th>Source instrument</th><th>Item/task description</th><th>Target waypoint(s)</th>"
        "<th>Format</th><th>License status</th><th>Reuse decision</th></tr></thead>"
        f"<tbody>{body}</tbody></table></section>"
    )


def render(state):
    name = state.get("project", {}).get("construct", "[Construct]")
    lit = state.get("literature", {})
    rounds = state.get("construct_map", {}).get("stress_test", {}).get("rounds", [])
    acc = rounds[-1].get("accuracy") if rounds else None
    updated = state.get("project", {}).get("updated") or dt.date.today().isoformat()
    strip = (
        f"<div><strong>{len(lit.get('keywords', []))}</strong>keywords searched</div>"
        f"<div><strong>{len(lit.get('constructs', []))}</strong>existing constructs found</div>"
        f"<div><strong>{'—' if acc is None else f'{acc:.0%}'}</strong>blind-sort accuracy (latest round)</div>"
        f"<div><strong>{len(state.get('items', {}).get('existing', []))}</strong>existing items found</div>"
        f"<div><strong>{e(updated)}</strong>last updated</div>"
    )
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>Literature Dashboard — {e(name)}</title>{style_block()}</head><body>"
        f"<h1>Literature Dashboard</h1><div class=\"subtitle\">{e(name)} — prior-art search and "
        "construct map, built in Block 1 and completed in Block 2</div>"
        f'<div class="summary-strip">{strip}</div>'
        + panel1(state) + panel2(state) + panel3(state)
        + "</body></html>\n"
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("state")
    ap.add_argument("-o", "--out", default=None)
    args = ap.parse_args(argv)
    state_path = Path(args.state)
    out = Path(args.out) if args.out else state_path.with_name("fbb-dashboard.html")
    out.write_text(render(json.loads(state_path.read_text())))
    print(out)


if __name__ == "__main__":
    main()
