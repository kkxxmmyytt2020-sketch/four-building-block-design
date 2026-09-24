---
type: llm
focus: files
weight: 3
---

Judge the files the run wrote (fbb-state.json, the stress_test folder, the dashboard and design document). A successful run satisfies ALL of these:

1. B1: an ordered mobility construct map (e.g. from bed-bound to independent walking/stairs)
   stress-tested by a blind sort whose sorter never saw the answer key.
2. B2: observation or performance items tagged to waypoints, with both extremes covered, and at
   least one construct-irrelevant-variance risk named (e.g. pain medication timing, drains,
   equipment access, ward layout).
3. B3: ordered scoring categories mapped to waypoints; exemplars written by the model are labelled
   synthetic, and rater training / inter-rater agreement is flagged as needing real data.
4. B4: a model chosen with a reason (e.g. Partial Credit for ordered ratings; rater effects or
   repeated days considered), and a Wright-map check that would send the work back to B1 if the
   order fails.
5. Every decision is `proposed` and no block is `approved` in the state file.
6. No fabricated psychometric results (no invented reliabilities, fit statistics or cut-offs
   presented as findings).

Score 1.0 if all six hold, deduct proportionally for each miss, 0 if the workflow was not used.
