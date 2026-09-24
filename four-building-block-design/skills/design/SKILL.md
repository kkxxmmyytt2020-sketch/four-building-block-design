---
name: design
description: >-
  Start, resume, or check status of a measurement-instrument design (test, survey, rubric, rating
  scale, assessment, questionnaire) using Mark Wilson's BEAR Assessment System four building
  blocks: construct map → items design → outcome space (scoring guide) → measurement model. Use
  whenever the user wants to build, draft, or design an assessment, survey, questionnaire,
  rubric, rating scale, or measure from scratch — even if they don't name Wilson or "four
  building blocks". Triggers: "design an assessment/survey/rubric for X", "build a measure of Y",
  "create a construct map", "build an outcome space/scoring guide", "stress-test my construct",
  "check for existing items/measures", or turning a fuzzy trait into something scoreable. This is
  the entry point; it routes to the b1–b4 block skills. For theory alone, with no deliverable,
  prefer `mark-wilson-measurement` if installed.
---

# Four Building Block Design — orchestrator

This skill runs the whole workflow. It owns the **state file**, the **gates** (where the
workflow stops and asks the user), **Step 0 scoping**, and the **final design document**. The
block work lives in four skills:

```
B1 construct map  →  B2 items design  →  B3 outcome space  →  B4 measurement model
(four-building-block-design:b1-construct-map) (…:b2-items) (…:b3-outcome-space) (…:b4-measurement-model)
        ▲── items can't span a waypoint ──┘                                     │
        └──────────── Wright map order contradicts the construct map ───────────┘
```

Draft each block, move on, and come back when a later block shows a problem. Don't perfect B1
before touching B2. The loop-backs are the point of the method, not a failure.

## 1. Open every run with the workflow figure

Read `${CLAUDE_PLUGIN_ROOT}/assets/workflow.png` so it renders, and give a two-sentence
orientation. If a state file exists, say which block the project is at.
Regenerate only if block content changes: `python3 ${CLAUDE_PLUGIN_ROOT}/assets/src/make_workflow_figure.py`.

## 2. State file

Each project lives in the user's working folder as `fbb-state.json` (create it at Step 0; never
inside the plugin). Schema → `references/state-schema.md`; a filled example →
`references/example-state.json`.

- Read it at the start of every turn that touches the project; write it after every decision.
- Every decision records **who decided** (`user` or `proposed`) and what it rests on:
  `literature`, `synthetic` (agents, vignettes, blind sort) or `real_data` (pilot responses,
  fitted model).
- After any change to literature, construct map, stress test or items, re-render the dashboard:
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render_dashboard.py fbb-state.json` → `fbb-dashboard.html`
  (same file, overwritten). Tell the user the path; `open` it at gates.

## 3. Gates

The workflow never runs end-to-end on its own. Use `AskUserQuestion` (1–4 questions, recommended
option first and labelled "(Recommended)", each description saying the consequence):

| Pause | When |
|---|---|
| **Scope** | Step 0, if construct, respondents, setting or decision is unclear |
| **Decision point** | Inside a block, when there is a real choice (adopt an existing construct vs build; map type; reuse vs rewrite an item; which model) |
| **Data stop** | A step needs something only the user has (pilot responses, rater data, an item bank, licences) — offer: provide it now · mark *pending real data* and continue · pause |
| **Block gate** | End of every block: Approve & continue · Revise this block · Loop back to an earlier block · Pause here |

Rules:
- No block starts until the previous gate is `approved` in the state file. If the user jumps
  ahead, record the skipped decisions as `proposed` and confirm them at the next gate.
- Before a gate question, give a summary of at most 8 lines: what the block decided and what is
  still open. The dashboard and design document hold the detail.
- Agents in `agents/` cannot ask the user anything. Dispatch them, collect their output, then pause.
- **Unattended draft** — only when the user explicitly asks ("draft the whole thing without
  asking") or `AskUserQuestion` is unavailable: run all four blocks, record every decision as
  `proposed`, leave every block at `awaiting_gate`, and end with a numbered list of every gate
  and decision question still open, each with the recommended option.

## 4. Step 0 — scope the construct

Ask, or infer from context:
1. **What** is the construct, in one sentence?
2. **Who** responds, and in what **setting**?
3. **What decision** will scores support? This sets how much validity and reliability rigour is needed.
4. **One construct or several?** Name 2–3 neighbouring constructs and ask whether someone could
   be high on one and low on another. If yes, they're separate: run the workflow per construct,
   or plan a multidimensional design (`${CLAUDE_PLUGIN_ROOT}/skills/b1-construct-map/references/construct-map-guide.md`).

One or two exchanges is enough. Write `project` in the state file, then invoke
`four-building-block-design:b1-construct-map`.

## 5. Routing

| Block | Skill | Starts when |
|---|---|---|
| B1 | `four-building-block-design:b1-construct-map` | Step 0 done |
| B2 | `four-building-block-design:b2-items` | B1 gate approved |
| B3 | `four-building-block-design:b3-outcome-space` | B2 gate approved |
| B4 | `four-building-block-design:b4-measurement-model` | B3 gate approved |

A loop-back sets the target block to `in_progress`, logs `{from, to, reason, date}` in
`loopbacks`, and re-opens that block's skill at the relevant step.

## 6. Final design document

When all four blocks have a draft, fill `${CLAUDE_PLUGIN_ROOT}/assets/design-worksheet-template.md`
from the state file: scope → waypoint table with expert review and blind-sort outcome → tagged
item bank → scoring guides → measurement-model plan → open validity risks (construct
underrepresentation, construct-irrelevant variance, rater reliability, unresolved waypoint
confusions). Link `fbb-dashboard.html`.

Save it as HTML (`<construct>-design.html`) unless the user asks for Word, PDF or a spreadsheet;
then use that format's skill. Before writing it, propose a title and ask the user to confirm.

## 7. Guardrail: design-time checks are not evidence

Reviewer agents, vignettes and the blind sort test whether the **idea** of the construct map
holds together. They do not show how real items or real people behave. Say this plainly
whenever you report their results, and never label synthetic output as pilot data.
