---
name: b2-items
description: >-
  Block 2 of the Four Building Block Design workflow (Wilson's BEAR Assessment System): design
  items or tasks that act as a transducer for an approved construct map — search for existing
  items and instruments first (with licensing), choose formats, separate construct-relevant from
  incidental features, flag construct-irrelevant variance and underrepresentation, and make sure
  every waypoint is covered. Use via the `design` orchestrator, or directly when the user asks to
  write or find items for a construct map, check item coverage, or decide whether an existing
  instrument's items can be reused.
---

# B2 — Items design

Needs an approved construct map in `fbb-state.json` (`stages.b1.status == "approved"`). If not,
say which B1 decisions are missing and route back. Set `stages.b2.status` to `in_progress`.

## 1. Search existing items first

Search several phrasings (exact construct name, synonyms, and the related/jangle constructs in
`literature.constructs`), plus any item bank the user has. For each usable find, record in
`items.existing`: the waypoint(s) it targets, format, and **licence status**.

- Reuse or adapt only where the licence clearly allows it.
- Unclear or restricted → use it as a model of "a good item at this waypoint" and write an
  original item inspired by it. Never reproduce restricted item text.
- Licence status the plugin cannot verify is a **data stop**: ask the user.

Render the dashboard: Panel 3 fills in, and Panel 2 gains example items.
Detail → `references/items-and-outcome-space.md` (Block 2).

## 2. Formats

Pick formats that fit the construct and setting: multiple choice, open response, performance
task, rating scale, observation checklist, log/behavioural trace, interview protocol. Ask the
user if the choice changes cost or administration (a **decision point**).

## 3. Write the item bank

For each item record `id`, `text`, target `waypoints`, `format`, `origin`
(new / adapted / reused) and `source`. For each item, separate:
- **construct-relevant** features (what should move someone along the map), from
- **incidental** features (surface details that shouldn't matter). Note any that risk
  **construct-irrelevant variance** in `irrelevant_features`, e.g. reading load in a maths item.

## 4. Coverage check

- Every waypoint, **including both extremes**, has several items. The dashboard marks gaps as
  "No item yet — coverage gap".
- No part of the construct is missing (**underrepresentation**).
- If items can't be written to reach a waypoint, that is a **loop-back to B1**: the waypoint may
  be unobservable or mis-specified.

## 5. Optional review

Dispatch `four-building-block-design:equity-reviewer` (and `content-expert` for high-stakes
uses) on the item bank. Apply or record their points.

## 6. Gate

Set `awaiting_gate`, summarise (items per waypoint, reused vs new, licence issues, gaps), and ask
the block gate. Recommend cognitive interviews with real respondents before B3 scoring is
finalised; that is real data the plugin cannot produce.
