---
name: b1-construct-map
description: >-
  Block 1 of the Four Building Block Design workflow (Wilson's BEAR Assessment System): draft a
  construct map — an ordered low-to-high continuum with 3–6 waypoints — and stress-test it before
  any items exist, with a multi-phrasing jingle-jangle literature check, independent reviewer
  agents (content, measurement, equity) and a truly blind sort of shuffled vignettes by the
  blind-sorter agent. Use via the `design` orchestrator, or directly when the user asks to draft,
  critique or stress-test a construct map, learning progression or set of levels, or to check
  whether their construct already exists under another name.
---

# B1 — Construct map, stress-tested as you build it

Read and update `fbb-state.json` (schema: `${CLAUDE_PLUGIN_ROOT}/skills/design/references/state-schema.md`).
Set `stages.b1.status` to `in_progress` when you start.

## 1. Jingle-jangle literature check

Search **several phrasings, each as its own query**: the exact construct name, 2–3 close
synonyms, and broader/narrower field terms. One phrasing routinely misses the literature this
check exists to find.

- **Jingle**: a *different* construct already uses *our name* → sharpen the definition or rename.
- **Jangle**: an *established* construct under *another name* is the same thing → consider
  adopting its name, definition, and (if accessible) its map or items. This is a **decision
  point**: ask the user whether to adopt or build.

Record every keyword and finding in `literature` (paraphrase, never quote definitions verbatim).
Render the dashboard (Panel 1).
Method → `references/construct-map-guide.md` (Jingle-jangle section).

## 2. Draft the map

1. **Extremes first**: the lowest and highest levels in concrete, observable terms.
2. **3–6 intermediate waypoints**, each with a short label and a 1–2 sentence definition.
3. **Map type**: respondent side (developmental theory), item-response side, or full.
4. If it isn't one continuum (strands, ordered partitions, latent classes), say so now →
   `references/construct-map-guide.md` (non-simple structures).

Write `construct_map.waypoints` **low → high**.

## 3. Expert panel (independent agents, in parallel)

Dispatch in one message, each given the construct definition, the context (respondents, setting,
decision) and the waypoint table, and nothing of your own reasoning:
- `four-building-block-design:content-expert`
- `four-building-block-design:measurement-reviewer`
- `four-building-block-design:equity-reviewer`

Revise the map on their feedback. Record each review and whether you applied it in
`construct_map.expert_review`. If a reviewer found nothing, record that; don't add filler.

## 4. Blind sort

This checks that the waypoints are **operationally** distinct. It needs no items.

1. Write **2–4 vignettes per waypoint**: concrete, narrative descriptions of a respondent (or a
   response) at that level. Don't restate the definition in other words, and don't echo the label.
   Save as `stress_test/round<N>/vignettes.json`:
   `{"waypoints": [...from state...], "vignettes": [{"waypoint": "W1", "text": "..."}]}`.
2. Shuffle and split:
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/shuffle_vignettes.py stress_test/round<N>/vignettes.json --out-dir stress_test/round<N>`
3. Dispatch `four-building-block-design:blind-sorter` with the **contents of `sort_packet.json`
   only**. Never include `answer_key.json`, `vignettes.json`, or any hint of which waypoint a
   vignette was written for. This separation is the reason the plugin exists: the sorter doesn't
   share your context, so the sort is actually blind.
4. Save its CSV to `stress_test/round<N>/sort.csv` and score:
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/blind_sort_score.py stress_test/round<N>/answer_key.json stress_test/round<N>/sort.csv --round <N> --state fbb-state.json`
5. Interpret the verdict:
   - **clean** → proceed.
   - **adjacent confusion** → sharpen the named pair with a distinguishing feature, or merge them.
   - **non-adjacent confusion** → the continuum may not be single; revisit structure (step 2.4).
   - **unplaced only** → rewrite those vignettes; don't blame the waypoint.
6. If there was real confusion, revise, write a `stress_test.resolution` note per affected
   waypoint, and run **one** more round with fresh vignettes. Two rounds is normally enough.
7. If you reword any definition after the last sort, even as a precaution, either run another
   round or state in the summary that the sort tested the earlier wording.
8. A perfect sort is weaker evidence than it looks: you wrote the vignettes knowing the
   definitions, so they tend to be clear-cut. Include some borderline vignettes near each boundary,
   and report the sorter's runner-up and low-confidence calls, not only the accuracy.

Render the dashboard: Panel 2 now shows each waypoint's definition with its ✓/⚠ badge.
Method in depth → `references/waypoint-stress-test.md`.

## 5. Sanity check and gate

- Each waypoint gets its meaning from the ones above and below it.
- The order is falsifiable: B4's Wright map could contradict it.

Set `stages.b1.status` to `awaiting_gate`, give the ≤ 8-line summary (waypoints, what the panel
changed, blind-sort accuracy and verdict, open risks), `open fbb-dashboard.html`, and ask the
**block gate** question. Say plainly that the panel and sort are design-time checks: they test
the idea of the map, not real items or people.

## References

- `references/construct-map-guide.md` — drafting tactics, variables clarification, jingle-jangle
  search, the ten worked examples, non-simple structures.
- `references/waypoint-stress-test.md` — expert review and blind-sort method, and its limits.
- `references/literature-dashboard.md` — what each dashboard panel contains.
