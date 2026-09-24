---
name: b4-measurement-model
description: >-
  Block 4 of the Four Building Block Design workflow (Wilson's BEAR Assessment System): choose,
  at design time, how scored responses will be put on one interval scale and read back against
  the construct map — Rasch, Partial Credit, multidimensional (MRCM), explanatory IRT, Saltus or
  testlet models — plan the Wright-map check of the hypothesised waypoint order, and list open
  validity risks. Use via the `design` orchestrator, or directly when the user asks which
  measurement model fits their instrument or how to read a Wright map against a construct map.
---

# B4 — Measurement model

Needs an outcome space in `fbb-state.json` (`stages.b3.status == "approved"`). Set
`stages.b4.status` to `in_progress`. You don't have to fit the model yet; this block writes the plan.

Decision tree and named models → `references/measurement-model-selection.md`.

## 1. Choose the model

| Structure | Model |
|---|---|
| One construct, dichotomous items | Rasch |
| One construct, ordered polytomous scores (rubric 0–3) | Partial Credit Model |
| Several strands measured together | Multidimensional (MRCM) |
| Person or item predictors matter (DIF, growth, groups) | Explanatory IRT (GLMM framing) |
| Stage-like, discontinuous development | Saltus / mixture |
| Items share a stimulus or passage | Testlet / item bundle |

If more than one fits, it's a **decision point**. Dispatch
`four-building-block-design:measurement-reviewer` on the choice. Record `model`, `rationale`
and suggested `software` in `measurement_model`.

## 2. Plan the Wright-map check

Write in `wright_map_check` the order the construct map predicts: which item thresholds should
sit near which waypoint, from low to high. When real data comes in, thresholds out of that order
are a **loop-back to B1**. That is how the method is meant to work, not a failure.

## 3. Open validity risks

List in `measurement_model.risks`: construct underrepresentation, construct-irrelevant variance,
rater reliability, DIF groups named by the equity reviewer, and any waypoint confusion still
unresolved from the B1 blind sort.

## 4. Gate and hand-off

Set `awaiting_gate`, summarise, and ask the block gate. On approval, return to the `design`
orchestrator to assemble the final design document. Fitting the model needs real data. If a
`rasch-analysis` skill is installed, point the user to it for that step.
