# Step 1 in depth: stress-testing the construct map with role-played agents

This happens **while drafting the construct map**, before any items exist. It's a cheap way to
check that the waypoints are real, distinct, ordered categories — not just plausible-sounding
labels — before investing in item writing against them.

## What this can and can't tell you

**Can catch, cheaply, before writing a single item:**
- Waypoints that sound different on paper but describe the same underlying behavior.
- Waypoints that aren't actually orderable (a sign the construct may need an ordered-partition or
  latent-class structure instead — see `construct-map-guide.md` §6).
- Vague waypoint wording that even a careful reader can't apply consistently.
- Obvious content gaps or fairness concerns a domain/equity reviewer would catch immediately.

**Cannot tell you (real item writing and real piloting are still required for these):**
- Whether real items written against these waypoints will actually discriminate between them.
- Real respondents' item difficulty, response variability, or fit statistics — those need real
  data and a fitted measurement model (Block 4 / the `rasch-analysis` skill).
- Rater reliability, real-world sampling, or administration effects.

Say this plainly to the user: this stress-test validates the *idea* of the construct map, not the
eventual instrument.

## Part A — Content-expert review

Adopt 2–3 reviewer personas suited to the construct. Typical panel:

1. **Domain/content expert** — is this construct defined the way practitioners in the field would
   recognize it? Any obvious content gaps in the waypoints?
2. **Measurement-minded reviewer** — are the waypoints genuinely ordered and distinct? Is there a
   clear rationale for why waypoint N comes before N+1? Any waypoint that's really two ideas
   glued together?
3. **Equity/bias reviewer** — could any waypoint description disadvantage respondents for reasons
   unrelated to the construct (language, culture, background)?

Produce a short structured review per persona:

```
### Reviewer: [persona name/role]
- Issues found (by waypoint):
- Top 2–3 recommended revisions:
```

Revise the waypoint table on this feedback before moving to Part B. If a persona finds nothing
wrong, say so — don't invent filler critique.

## Part B — Synthetic respondent blind-sort

This is the core check that the waypoints are **operationally** distinct, not just theoretically
tidy.

### Building the test set

1. For each waypoint, write **2–4 short vignettes** — a concrete, narrative description of a
   respondent or item response at that level. Make them realistic and specific (not just a
   restatement of the waypoint description in different words).
2. Keep a hidden answer key: vignette → true waypoint. Never let this leak into the vignette text
   itself, and don't number vignettes in waypoint order.
3. Shuffle all vignettes from all waypoints together into one list.

### Running the sort

Adopt a **blind-sorter** persona whose only information is the waypoint **definitions** (not the
hidden answer key). Go through the shuffled vignette list and assign each one to the waypoint it
best fits, noting any vignette that feels genuinely ambiguous between two waypoints.

### Scoring and revising

1. Compare the sorter's assignments to the hidden answer key.
2. Build a quick confusion check:

   | Vignette | True waypoint | Sorter's waypoint | Match? |
   |---|---|---|---|

3. Interpret the pattern:
   - **High accuracy, few ambiguous cases** → waypoints are well operationalized; proceed to Step 2.
   - **Confusion concentrated between two adjacent waypoints** → sharpen their wording with a
     distinguishing feature, or consider merging them into one waypoint.
   - **Confusion scattered across the map** → the underlying continuum may not be as clean as
     hoped; revisit whether this is really a single-construct map (see `construct-map-guide.md`
     §6 on latent classes / ordered partitions / multiple strands).
   - **A vignette can't be placed at all** → likely a poorly written vignette rather than a
     waypoint problem; rewrite it and re-test rather than concluding the waypoint is broken.
4. Revise the waypoint table and repeat once if the first round surfaced real confusion. One or
   two rounds is normally enough — don't over-iterate a design-time heuristic.

### Reporting

Note the stress-test outcome directly on the construct-map deliverable (as in
`assets/design-worksheet-template.md` §1): rounds run, what was confused, what was revised, and
the final result. Also feed it into **Panel 2 of the literature dashboard**
(`references/literature-dashboard.md`) as each waypoint's clean/confused badge, so a reader can see
the verdict for a single waypoint without reading the whole raw vignette-by-vignette log. Carry any
unresolved concerns into the design document's open-risks section for attention once real piloting
is possible.

**See also:** `construct-map-guide.md` (drafting tactics and non-simple structures this stress-test
might reveal); `literature-dashboard.md` (how per-waypoint results get surfaced on the dashboard);
`items-and-outcome-space.md` (item design now proceeds against a validated map);
`measurement-model-selection.md` (the real empirical check this heuristic is a cheap proxy for).
