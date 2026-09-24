# Block 1 in depth: the construct map

Source: *Constructing Measures* (Wilson, 2005; 2nd ed. 2023), Ch. 2.

## Drafting tactics

1. **Extremes first.** Name the lowest and highest levels concretely (e.g., "novice" ↔ "expert";
   "loathes" ↔ "loves"; "no evidence of X" ↔ "consistently demonstrates X unprompted").
2. **Make the extremes concrete** with a short behavioral or attitudinal description — something
   an observer could recognize, not just a label.
3. **Fill in intermediate waypoints** between the extremes. For each, draft the *typical response*
   a respondent at that level would give to a first-draft item. Usually 3–6 waypoints is enough;
   more than ~7 tends to blur into noise.
4. Decide the **map type**:
   - **Respondent map** (order respondents low→high) — use when there's a developmental theory of
     how people progress on this construct.
   - **Item-response map** (order responses low→high) — use when the construct is mainly defined
     by a set of items and how people answer them.
   - **Full map** (both sides aligned) — the ideal; build it once you have enough of both to align
     them.

## Variables clarification

Before finalizing the construct, check it isn't secretly 2–3 constructs bundled together:
- List 2–3 neighboring constructs that could be confused with this one.
- Ask: could a respondent plausibly be **high on one and low on another**? If such people exist and
  are meaningfully different, the constructs are genuinely distinct — measure them **one at a
  time** (run this whole four-block workflow per construct, or design a multidimensional
  instrument — see "Multiple strands" below).
- Correlated ≠ identical. Two constructs can move together in your population and still be
  conceptually and measurably separate.

## Jingle-jangle fallacy: search before you finalize the definition

Named by Kelley (1927) and Thorndike; a longstanding trap in construct definition, distinct from
(but related to) variables clarification above:

- **Jingle fallacy** — assuming two things are the same because they're called by the **same
  name**. The literature may already use your construct's exact label for something meaningfully
  different (a different field, a different operationalization, a narrower or broader scope).
  Building your map without checking this risks silently importing the wrong assumptions, or
  confusing readers/collaborators who know the term's other meaning.
- **Jangle fallacy** — assuming two things are **different because they have different names**.
  An established construct — possibly with a published construct map, validated items, and norms
  already — may be functionally the same as what you're about to build from scratch under a new
  label. This is the more expensive mistake: duplicated effort, and an instrument that can't be
  compared to existing literature.

### How to search

Don't run one query and stop — the whole point of this check is that a single phrasing won't
surface a differently-labeled twin (jangle) or reveal a same-labeled stranger (jingle). Search
**separately** with:
1. The exact construct name/label you're planning to use.
2. 2–3 close synonyms or near-equivalent phrasings.
3. Broader and narrower terms from the relevant field (e.g., for "customer trust in a brand":
   also try "brand trust," "consumer confidence," "perceived brand integrity," "relationship
   trust").

For each search, skim results for: (a) other definitions of your exact term — jingle check; (b)
instruments/scales under a different name whose description sounds like your construct — jangle
check.

### Resolving what you find

- **Jingle found** (same name, different construct elsewhere): either rename yours to avoid the
  collision, or keep the name but state the distinction explicitly and early in your construct
  definition (Step 0), so nobody downstream conflates the two.
- **Jangle found** (different name, same/near-same construct elsewhere): don't default to
  rebuilding from zero. Options, roughly in order of preference: adopt the established name and
  definition outright if it fits your population and use case; adapt the existing construct map
  and items to your setting (checking licensing — see `items-and-outcome-space.md`); or, if your
  construct is genuinely a meaningful variant, keep your own map but explicitly note the
  relationship to the established construct in the design document so users can compare results
  across instruments.
- **Nothing relevant found either way**: proceed with the current definition, but note in the
  design document that the jingle-jangle check was run and came up clear — useful provenance if
  someone questions the construct's originality later.

## Quality checks for a finished construct map

- Waypoints are **qualitatively distinct** from each other (not just "more of the same" restated).
- Waypoints are **theoretically motivated** — you can say *why* this level comes before that one.
- Each waypoint description **derives meaning from its neighbors** (what makes level 3 level 3 is
  partly that it's more than level 2 and less than level 4).
- The map is **falsifiable**: once real data comes in (Block 4), the empirical order of item
  thresholds should be checkable against this hypothesized order. If they clash, revise the map —
  don't force the data to fit.
- Avoid the "messy middle" trap: if an intermediate waypoint won't pin down to a clear description
  or location, it's fine to leave it loosely specified and let data help place it later, but say so
  explicitly rather than pretending it's crisp.

## The ten worked examples (for inspiration / precedent)

| Domain | Construct | Notable feature |
|---|---|---|
| Math/stats education | Models of Variability (MoV) | clean respondent map; two waypoints can co-locate empirically |
| Social-emotional learning | Researcher Identity Scale | table-format map; four strands (Agency, Community, Fit, Self) |
| Environmental attitude | General Ecological Behavior | built *a posteriori* from item calibration, not theory-first |
| 21st-century skills | Argumentation learning progression | built on Toulmin's claim/evidence/warrant/backing |
| Math/stats education | Data Modeling (6 constructs) | multiple strands, multidimensional |
| Process/collaboration | Collaborative Problem Solving | 5-strand process × proficiency rows; log-file scoring |
| Health outcomes | Physical Functioning (SF-36 style) | item ordering by ease of physical task |
| Science education | Evolution understanding | learning progression from interview data; two converging strands |
| Early childhood | Developmental Profile | observation-based, embedded in a teacher rating form |
| Middle-school science | Issues, Evidence and You | original BAS testbed; multiple constructs incl. "Using Evidence" |

Use these as reference points for how varied "a construct map" can look in practice — tables,
strands, interview-derived, item-calibration-derived, observation-based — the underlying logic
(ordered, waypoint-marked continuum) is the same.

## When it's *not* a simple single-continuum construct

- **Latent classes** — the categories are discrete and *unordered* (e.g., different problem-solving
  strategies with no "better/worse"). A construct map doesn't apply; use latent class analysis
  instead, and don't force an order onto categories that don't have one.
- **Ordered partitions** — a *partial* order, e.g., "doesn't understand" < {strategy A, strategy B}
  < "solves it," where A and B are equally advanced but different. Can be folded into a construct
  map with some information loss (the ordered partition model handles this properly later).
- **Multiple strands (multidimensional)** — the construct is really several related constructs
  that need to be reported together (e.g., a 5-strand process skill). Build a construct map **per
  strand**, then use a multidimensional measurement model in Block 4.
- **Multiple strands + a composite** — you want both strand-level and overall scores. This needs a
  multilevel measurement model; flag it early since it changes the Block 4 plan substantially.

**See also:** `items-and-outcome-space.md` (how the construct map drives item and scoring-guide
design, and how the jingle-jangle search connects to searching for existing items);
`measurement-model-selection.md` (how the map gets empirically tested as a Wright map).
