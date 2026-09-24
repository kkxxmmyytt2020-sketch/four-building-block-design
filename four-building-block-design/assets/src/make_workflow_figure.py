"""Render the Four Building Block Design workflow figure (assets/workflow.png).

Each column is one BEAR Assessment System building block. Every step carries
the source or agent/script behind it.

    python3 make_workflow_figure.py   # writes ../workflow.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "workflow.png"

INK = "#1f2328"
MUTED = "#57606a"
RULE = "#d0d7de"
PAPER = "#ffffff"

STAGES = [
    {
        "key": "B1",
        "name": "Construct map",
        "question": "What is the continuum, low to high?",
        "hue": "#2f6f9f",
        "tint": "#e8f1f8",
        "steps": [
            ("Scope: one construct, who, what decision", "Step 0 · variables clarification"),
            ("Jingle-jangle literature check", "several phrasings → dashboard Panel 1"),
            ("Extremes first, then 3–6 waypoints", "Wilson, Constructing Measures"),
            ("Expert panel reviews the map", "agents: content · measurement · equity"),
            ("Blind sort of shuffled vignettes", "agent: blind-sorter · shuffle / score scripts"),
        ],
        "output": "Waypoint table, stress-tested\n+ dashboard Panels 1–2",
        "sources": "Wilson 2005/2023 · jingle-jangle lit.",
        "ai": "Literature search, reviewer\nagents, blind sort, scoring",
        "human": "Approve the construct;\nreal expert review",
    },
    {
        "key": "B2",
        "name": "Items design",
        "question": "How do we elicit it?",
        "hue": "#8a5a00",
        "tint": "#fbf1e0",
        "steps": [
            ("Search existing items + licensing", "dashboard Panel 3"),
            ("Pick item format(s)", "MC · open · task · rating · log"),
            ("Construct-relevant vs incidental features", "transducer: provoke the construct"),
            ("Flag CIV and underrepresentation", "Messick; AERA/APA/NCME 2014"),
            ("Span every waypoint, several items each", "item bank tagged by waypoint"),
        ],
        "output": "Item bank, each item tagged\nwaypoint · new / adapted / reused",
        "sources": "Wilson · AERA/APA/NCME Standards",
        "ai": "Find prior items, draft gap\nitems, coverage check",
        "human": "Check licences; cognitive\ninterviews with respondents",
    },
    {
        "key": "B3",
        "name": "Outcome space",
        "question": "How do we score it?",
        "hue": "#1a7f5a",
        "tint": "#e6f4ee",
        "steps": [
            ("Ordered categories per item", "each mapped to a waypoint"),
            ("Well-defined, research-based", "someone else could apply it"),
            ("Exhaustive, finite, ordered", "every response has a home"),
            ("2–3 exemplars per category", "rater-training note"),
        ],
        "output": "Scoring guide / rubric\nper item or item family",
        "sources": "Wilson · phenomenography",
        "ai": "Draft rubric, exemplars,\nordering check",
        "human": "Pilot responses; rater\ntraining and agreement",
    },
    {
        "key": "B4",
        "name": "Measurement model",
        "question": "How do we scale it?",
        "hue": "#6e40aa",
        "tint": "#f1ebf8",
        "steps": [
            ("Dichotomous → Rasch; ordered → PCM", "single construct"),
            ("Several strands → MRCM", "multidimensional"),
            ("Predictors / DIF / growth → explanatory IRT", "De Boeck & Wilson 2004"),
            ("Stages → Saltus; shared stimulus → testlet", "mixture · bundle models"),
            ("Read the Wright map against the map", "order wrong → revise B1"),
        ],
        "output": "Measurement-model plan\n+ open validity risks",
        "sources": "Wilson · De Boeck & Wilson 2004",
        "ai": "Pick model, write analysis\nplan, risk list",
        "human": "Collect real data; fit\nthe model; Wright map",
    },
]

LOOPS = [  # (from stage index, to stage index, label)
    (1, 0, "items can't span a waypoint"),
    (3, 0, "Wright map order contradicts the construct map"),
]

W, H = 20.0, 11.9
COL_W, GAP, LEFT = 4.45, 0.55, 0.35

HEAD_TOP, HEAD_H = 10.55, 1.05
STEP_TOP, STEP_H = 9.35, 3.95
OUT_TOP, OUT_H = 5.25, 0.95
SRC_TOP, SRC_H = 4.15, 0.45
ROLE_TOP, ROLE_H = 3.55, 1.2


def box(ax, x, y_top, w, h, face, edge=None, lw=1.0, r=0.12, hatch=None):
    ax.add_patch(FancyBboxPatch(
        (x, y_top - h), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=face, edgecolor=edge or face, linewidth=lw, hatch=hatch,
    ))


def main():
    plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
    fig = plt.figure(figsize=(W, H - 0.8), dpi=160)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0.8, H)
    ax.axis("off")
    fig.patch.set_facecolor(PAPER)

    ax.text(LEFT, 11.4, "Four Building Block Design: from a fuzzy trait to a scaled measure",
            fontsize=20, weight="bold", color=INK, va="center")
    ax.text(LEFT, 10.98,
            "One column per BEAR Assessment System block (Wilson, Constructing Measures). Each step shows its source, agent or script; "
            "the bottom rows show what AI does and what needs real people.",
            fontsize=11.5, color=MUTED, va="center")

    xs = [LEFT + i * (COL_W + GAP) for i in range(len(STAGES))]

    for i, (s, x) in enumerate(zip(STAGES, xs)):
        # header
        box(ax, x, HEAD_TOP, COL_W, HEAD_H, s["hue"])
        ax.text(x + 0.2, HEAD_TOP - 0.36, f'{s["key"]}  {s["name"]}',
                fontsize=15, weight="bold", color="white", va="center")
        ax.text(x + 0.2, HEAD_TOP - 0.78, s["question"],
                fontsize=10.5, color="white", va="center", style="italic")

        # steps
        box(ax, x, STEP_TOP, COL_W, STEP_H, s["tint"])
        n = len(s["steps"])
        pitch = (STEP_H - 0.25) / n
        for j, (step, cite) in enumerate(s["steps"]):
            y = STEP_TOP - 0.22 - j * pitch
            ax.add_patch(plt.Circle((x + 0.3, y - 0.17), 0.13, color=s["hue"]))
            ax.text(x + 0.3, y - 0.17, str(j + 1), fontsize=8.5, color="white",
                    ha="center", va="center", weight="bold")
            ax.text(x + 0.55, y - 0.1, step, fontsize=10.2, color=INK, va="center")
            ax.text(x + 0.55, y - 0.4, cite, fontsize=8.6, color=MUTED, va="center")

        # output
        box(ax, x, OUT_TOP, COL_W, OUT_H, PAPER, edge=s["hue"], lw=1.8)
        ax.text(x + 0.2, OUT_TOP - 0.2, "DECISION OUTPUT", fontsize=7.8,
                color=s["hue"], weight="bold", va="center")
        ax.text(x + 0.2, OUT_TOP - 0.6, s["output"], fontsize=10.2, color=INK,
                va="center", weight="bold", linespacing=1.25)

        # sources
        ax.text(x + 0.2, SRC_TOP - SRC_H / 2, "Sources:  " + s["sources"],
                fontsize=9.2, color=MUTED, va="center")

        # AI vs human
        half = (COL_W - 0.12) / 2
        box(ax, x, ROLE_TOP, half, ROLE_H, "#f6f8fa", edge=RULE)
        box(ax, x + half + 0.12, ROLE_TOP, half, ROLE_H, PAPER, edge=RULE, hatch="////")
        ax.text(x + 0.15, ROLE_TOP - 0.22, "AI ASSISTS", fontsize=7.8, color=INK,
                weight="bold", va="center")
        ax.text(x + 0.15, ROLE_TOP - 0.68, s["ai"], fontsize=8.8, color=INK,
                va="center", linespacing=1.3)
        hx = x + half + 0.12
        ax.text(hx + 0.15, ROLE_TOP - 0.22, "NEEDS REAL PEOPLE / DATA",
                fontsize=7.8, color=INK, weight="bold", va="center",
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.2))
        ax.text(hx + 0.15, ROLE_TOP - 0.68, s["human"], fontsize=8.8, color=INK,
                va="center", linespacing=1.3,
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5))

        # forward arrow to next stage
        if i < len(STAGES) - 1:
            ax.add_patch(FancyArrowPatch(
                (x + COL_W + 0.04, HEAD_TOP - HEAD_H / 2),
                (x + COL_W + GAP - 0.04, HEAD_TOP - HEAD_H / 2),
                arrowstyle="-|>", mutation_scale=18, color=INK, lw=1.6))

    # loop-backs, drawn under the columns
    base = ROLE_TOP - ROLE_H - 0.15
    for k, (a, b, label) in enumerate(LOOPS):
        xa = xs[a] + COL_W * 0.3
        xb = xs[b] + COL_W * 0.7
        ax.add_patch(FancyArrowPatch(
            (xa, base), (xb, base),
            connectionstyle=f"arc3,rad={-0.3 / abs(a - b)}", arrowstyle="-|>",
            mutation_scale=15, color=MUTED, lw=1.3, linestyle=(0, (4, 3))))
        ax.text((xa + xb) / 2, base - 0.12 - 0.5 / abs(a - b) ** 0.5 - 0.1 * (abs(a - b) > 1), label, fontsize=9.2, color=MUTED,
                ha="center", va="center", style="italic",
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5))
    ax.text(LEFT, 1.2, "↺  Dashed arrows: loop-backs. A later block can reopen the construct map; "
            "every loop-back is logged in the state file.",
            fontsize=9.5, color=MUTED, va="center")
    ax.text(W - LEFT, 1.2,
            "Reviewer agents and the blind sort are design-time checks, never a substitute for piloting.",
            fontsize=9.5, color=INK, va="center", ha="right", weight="bold")

    fig.savefig(OUT, dpi=160, facecolor=PAPER)
    print(OUT)


if __name__ == "__main__":
    main()
