---
name: b3-outcome-space
description: >-
  Block 3 of the Four Building Block Design workflow (Wilson's BEAR Assessment System): turn raw
  responses into ordered, scoreable categories — a scoring guide or rubric per item or item
  family, each category mapped to a construct-map waypoint, with exemplars and rater-training
  notes, checked for being well-defined, research-based, exhaustive, finite and ordered. Use via
  the `design` orchestrator, or directly when the user asks to write a scoring guide, rubric or
  outcome space for items already written against a construct map.
---

# B3 — Outcome space

Needs an item bank in `fbb-state.json` (`stages.b2.status == "approved"`). Set
`stages.b3.status` to `in_progress`.

Guidance and quality checklist →
`${CLAUDE_PLUGIN_ROOT}/skills/b2-items/references/items-and-outcome-space.md` (Block 3 section).

## 1. Scoring guide per item or item family

Write ordered categories into `outcome_space`, each with `score`, the `waypoint` it maps to,
and a `description` another rater could apply. Scores must rise with waypoint order.

## 2. Quality check

- **Well-defined**: someone else could score consistently from the guide alone.
- **Research-based**: grounded in real responses. If there are no pilot responses yet, this is a
  **data stop**: offer to mark the guide *pending real responses* and continue.
- **Exhaustive** (every plausible response has a home, including off-task / blank) and **finite**.
- **Ordered**: categories line up with the waypoint order.

Dispatch `four-building-block-design:measurement-reviewer` with the outcome space and the
waypoint table.

## 3. Exemplars and raters

Attach 2–3 exemplar responses per category. Label any you wrote yourself as **synthetic** and
say they must be replaced with real responses. If humans will score, add a short rater-training note.

## 4. Gate

Set `awaiting_gate`, summarise (categories per item, which guides still need real responses),
and ask the block gate. If a category can't be mapped to any waypoint, or real responses show
a level the map lacks, recommend a **loop-back to B1**.
