# The literature dashboard: spec and build method

Built across three moments — Panel 1 right after Step 1's jingle-jangle search, Panel 2 right
after Step 1's blind-sort stress-test, Panel 3 after Step 2's existing-item search — so the user
has one place to see everything the literature turned up, plus an interactive, evidence-backed
view of the construct map itself, before the instrument gets built. It exists to make prior-art
search and the construct map **visible and reusable**, not just a paragraph of prose that gets
read once and forgotten.

## Why a dashboard instead of prose

Search findings are naturally tabular (many rows, few repeated columns), get referred back to
more than once (when revising waypoints, when deciding item reuse, when writing the final design
document's provenance section), and benefit from being scannable at a glance rather than read
linearly. A dashboard the user can keep open while working beats re-reading a paragraph every
time they want to check "wait, did we already find something like this?" or "what did we say
waypoint 3 means again?"

## Content: Panel 1 — Existing constructs (from Step 1)

One row per relevant finding from the jingle-jangle search:

| Column | Content |
|---|---|
| Keyword searched | which of the exact-name/synonym/adjacent-term queries surfaced this |
| Construct/instrument name found | as named in the source |
| Source | citation or link |
| Definition (short) | 1–2 sentence paraphrase, never a verbatim quote of copyrighted text |
| Relationship | Jingle risk / Jangle risk / Related-but-distinct / No conflict |
| Recommended action | rename ours / sharpen distinction / adopt this one instead / adapt / proceed as-is |

Include a short header summary above the table: which keywords were searched in total, and a
one-line verdict (e.g., "no jangle risk found; one jingle risk found and resolved by renaming").

### Panel 1's Venn diagram

Directly under the verdict, add a **schematic overlap diagram** — one circle per construct (yours
plus each relevant finding) — so the pattern of findings reads at a glance instead of row by row.
This is a qualitative diagram, not a mathematically proportional Venn diagram; overlap size is a
judgment call, not a computed statistic, and the dashboard should say so in a small caption.

Overlap-to-relationship mapping:
- **No conflict** — circles apart, no overlap.
- **Related-but-distinct** — circles overlap roughly 20–40%.
- **Jangle risk** (probably the same construct under a different name) — circles overlap heavily,
  roughly 70–90%, since the whole point of flagging jangle is "these are nearly the same thing."
- **Jingle risk** (same name, but a *different* construct) — circles should have little or no
  overlap, since the meanings genuinely differ. Flag these instead with a **dashed outline** in
  the jingle color, so the diagram doesn't visually claim overlap that isn't there while still
  marking "watch out, name collision."

Skip the diagram entirely if Panel 1 has no rows (nothing found either way) — an empty diagram
adds noise, not signal. Cap it at roughly 5–6 circles for legibility; if more than that are found,
show the most relevant ones and note the rest in the table only.

## Content: Panel 2 — Construct map, click-to-expand (from Step 1, completed in Step 2)

One collapsible entry per waypoint, ordered top-to-bottom or bottom-to-top (say which in the
panel's header note). Clicking a waypoint reveals three fields:

| Field | Content |
|---|---|
| Definition | the 1–2 sentence waypoint description from the Step 1 construct map |
| Stress-test result | the outcome of Step 1's blind-sort test for this waypoint — see below |
| Example item(s) targeting this waypoint | pulled from the Step 2 item bank once it exists, tagged new/adapted/reused |

### Stress-test result field (from the Step 1 blind-sort)

This is what turns the stress-test log from a raw table into something an assessment developer
can actually act on: instead of scanning a flat list of vignette-by-vignette results, they open
the one waypoint they're worried about and see its verdict directly.

For each waypoint, show one of two states:
- **Clean** — a green "✓ No confusion" badge, plus "sorted correctly in N/N vignettes, R round(s)."
- **Confused** — an amber "⚠ Confused with [other waypoint]" badge, plus how many of that
  waypoint's vignettes were mis-sorted into the other waypoint, what fixed it (sharper wording,
  a merge, etc.) if it was resolved by a later round, or a note that it's still an open risk if it
  wasn't.

Keep the raw vignette-by-vignette table (vignette → true waypoint → sorter's waypoint → match)
too, but make it a secondary, optional detail — e.g., a small "see raw sort log" note or a
collapsed sub-table — rather than the primary way the developer reads stress-test results. The
badge-plus-note format is what most people will actually use; the raw table is there for anyone
who wants to double-check a specific call.

Build this panel in two passes, same as the rest of the dashboard:
- **Right after Step 1's blind-sort stress-test finishes** (sub-step 6): create one entry per
  waypoint with its definition and stress-test result together — by this point both exist, so
  there's no reason to split them across two passes. Leave the example-item field as "Not yet
  available — completes in Step 2."
- **After Step 2**: fill in each waypoint's example-item field from the tagged item bank. A
  waypoint with no item yet (a coverage gap flagged in Step 2) should say so plainly rather than
  being left blank.

This panel is the one place a reader can see the whole construct map and a concrete example of
what each level looks like in practice, without flipping between the construct-map table and the
item bank.

## Content: Panel 3 — Existing items/instruments (added in Step 2)

One row per usable item/instrument found:

| Column | Content |
|---|---|
| Source instrument | name of the published scale/item bank it came from |
| Item/task description | short paraphrase, not verbatim if copyrighted |
| Target waypoint(s) | which waypoint(s) from the Step 1 construct map it corresponds to |
| Format | multiple-choice, rating scale, performance task, etc. |
| License/copyright status | open / owned by user / unclear / restricted |
| Reuse decision | reuse / adapt / inspired-by-rewrite / not used |

Same header pattern: keywords searched, one-line verdict (e.g., "3 reusable items found for the
middle waypoints; top and bottom waypoints have no existing coverage — will need new items").

## How to build it

**Preferred: an interactive HTML page.** If the current session can create and show HTML content
(a file-creation tool, an artifact/canvas feature, or similar), build the dashboard as a single
self-contained HTML file:
- Three clearly labeled sections — Existing Constructs (with its Venn diagram), Construct Map
  (click-to-expand), Existing Items.
- A short summary strip at the top (counts, verdicts) so the user gets the headline without
  reading every row.
- The click-to-expand waypoint panel needs no JavaScript — native `<details>`/`<summary>` elements
  give click-to-reveal behavior for free and stay accessible; don't reach for custom JS toggles.
- The Venn diagram is inline SVG with manually placed circles (see Panel 1's spec above) — no
  charting library needed for 2–6 circles.
- Simple, readable styling — this is a working document, not a polished deliverable; don't spend
  effort on visual design beyond making the tables and diagram easy to scan.
- In this plugin, don't hand-edit HTML: record findings in `fbb-state.json` and run
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render_dashboard.py fbb-state.json`, which builds all three
  panels (and the overlap diagram) using the styling in `assets/literature-dashboard-template.html`.
- **Update in place** across both passes — same file/artifact, not a new one, so the user has a
  single link to return to.

**Fallback: Markdown.** If the session has no way to render or show an HTML page, produce the same
three panels in the working conversation or the design document: Panels 1 and 3 as Markdown
tables; Panel 2 as a simple list of "**[Waypoint]**: definition — stress-test verdict (clean, or
confused with [X], N/N) — example item," since a plain Markdown file can't do click-to-expand.
Skip the Venn diagram in this fallback, or describe the overlap pattern in one sentence per
relationship type instead. The content is identical — only the interactivity is lost.

## What NOT to put on the dashboard

- No verbatim reproduction of copyrighted definitions or item text — paraphrase, per the copyright
  notes in `construct-map-guide.md` (jingle-jangle section) and `items-and-outcome-space.md`
  (existing-item search section).
- No speculative entries — only include a row/circle/waypoint entry when there's real content
  behind it; an empty panel with a clear "searched X keywords, nothing relevant found" note is a
  valid and useful result, not a gap to fill with guesses.
- No precise-looking overlap percentages on the Venn diagram — it's a schematic judgment call, not
  a computed statistic; don't dress it up with numbers that imply more rigor than it has.
- Don't let the dashboard replace the narrative reasoning in Step 1/Step 2 — it's a reference
  companion to the workflow, not a substitute for actually resolving jingle/jangle risks or making
  reuse decisions in the design document itself.

**See also:** `construct-map-guide.md` (jingle-jangle search this dashboard's Panel 1 records, and
the waypoints Panel 2 displays); `items-and-outcome-space.md` (existing-item search this
dashboard's Panel 3 records); `assets/literature-dashboard-template.html` (starter markup).
