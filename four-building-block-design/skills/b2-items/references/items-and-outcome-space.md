# Blocks 2 and 3 in depth: items design and outcome space

## Block 2 — Items design

The job of an item is to act as a **transducer**: a task or prompt that provokes a response
revealing where the respondent sits on the construct map.

### Search for existing items before writing new ones

Writing every item from scratch is usually the expensive, last-resort option. Before drafting:

1. **Search using multiple keyword phrasings** — the exact construct name, the synonyms/adjacent
   terms surfaced during Step 1's jingle-jangle check, and field-typical terms for the item format
   you expect (e.g., "rubric," "scale," "item bank," "questionnaire"). One query rarely surfaces
   everything; search each phrasing separately.
2. **Look in likely places**: published validated scales and their appendices, academic item banks
   and repositories for the field, institutional or organizational item banks the user has access
   to, and the user's own prior instruments if they mention having built something similar before.
3. **For each usable item found, record**: which waypoint(s) it targets, its format, and its
   **licensing/copyright status** (published-with-permission, openly licensed, status unclear, or
   clearly proprietary).
4. **Decide reuse vs. adapt vs. rewrite**:
   - Clearly open-licensed or the user owns it → reuse directly, or adapt wording/context to fit.
   - Published academic scale with unclear or restrictive licensing → **don't reproduce it
     verbatim**. Treat it as a model of what a good item at that waypoint looks like, and write an
     original item with the same intent and difficulty, in your own wording — this is the same
     paraphrase-not-reproduce principle that applies to any copyrighted text.
   - Nothing suitable found for a given waypoint → draft a new item there.
5. Tag every item in the final bank as **new**, **adapted** (from what source), or **reused** (from
   what source, with confirmed license), so the user knows what due diligence still remains before
   publishing or administering the instrument.

This search doubles as a second jingle-jangle check at the item level: if an existing instrument's
items look like they're targeting a different construct than you intended despite sharing
vocabulary, that's a jingle signal worth taking back to Step 1.

### Choosing item format(s)

Pick based on the construct and the setting, not habit:
- **Multiple-choice / selected-response** — fast to score, good for well-defined content
  knowledge; weak at eliciting reasoning or process.
- **Open/constructed response** — richer evidence of reasoning; needs a real outcome space (Block
  3) and trained scorers.
- **Performance tasks / portfolios / projects** — good for complex, applied constructs; expensive
  to administer and score.
- **Rating scales / self-report items** — good for attitudes, self-perceptions; watch for social
  desirability and acquiescence bias as construct-irrelevant variance.
- **Observation checklists / interviews** — good for young children, clinical or behavioral
  constructs where self-report isn't reliable.
- **Log-file / behavioral trace data** — good for process constructs (e.g., collaboration,
  problem-solving strategy); requires an instrumented environment.

Multiple formats can coexist in one instrument if they all target the same construct map.

### Construct-relevant vs. descriptive features

For each item, ask: which features are there *because* they move a respondent along the
construct, and which are just incidental context? Two failure modes to watch for:

- **Construct-irrelevant variance** — something about the item makes it harder or easier for
  reasons that have nothing to do with the construct. Example: a math item wrapped in a
  paragraph of unnecessary text penalizes weak readers regardless of math ability.
- **Construct underrepresentation** — the item set as a whole misses part of the construct.
  Example: all items only tap the middle of the construct map, so the instrument can't tell apart
  respondents at the low or high extremes.

Both are threats to validity (definitional uncertainty) — flag them explicitly in the design
document rather than discovering them after the instrument ships.

### Coverage check

Before finalizing the item bank:
- Every waypoint on the construct map should have items (or item-response opportunities) that can
  distinguish it from its neighbors.
- The extremes need coverage too — an instrument with only "middle" items compresses everyone into
  the center of the scale and can't do its job at the tails.
- Draft more items than you need per waypoint; expect some to be cut after piloting or item-quality
  screening in Block 4.

## Block 3 — Outcome space

The outcome space is the set of **ordered, exhaustive categories** that raw responses get sorted
into, then scored. Roots: Marton's phenomenography (categorizing qualitatively different ways
people respond to something).

### Building a scoring guide

For each item or item family:
1. Write **category definitions** — plain-language descriptions of what response belongs in each
   category.
2. Map each category explicitly to a **construct-map waypoint**. This link is what makes a score
   meaningful, not just a count.
3. Collect **exemplar responses** (2–3 per category) — ideally from real or piloted responses, not
   invented ones.
4. Write a short **rater-training note**: common edge cases, how to break ties between adjacent
   categories, how much inference vs. literal reading is expected.

### Quality checklist

A good outcome space is:
- **Well-defined** — another person could apply it and land on the same category most of the time.
- **Research-based** — grounded in responses you've actually seen (pilot data, prior literature),
  not armchair guessing about how people "should" respond.
- **Context-specific** — tuned to this item set and domain, not a generic rubric copy-pasted from
  elsewhere.
- **Finite and exhaustive** — a manageable number of categories, and every plausible response has
  a home (including a "none of the above / off-task" catch-all if needed).
- **Ordered** — categories line up with the waypoint order from Block 1. If two categories can't be
  cleanly ordered relative to each other, that's a signal to either merge them or revisit whether
  the construct map needs an ordered-partition structure (see `construct-map-guide.md`).

### Flag for later

Note any categories you're unsure about ordering, any items where scoring will likely have low
inter-rater agreement, and any places where the outcome space had to compress information from the
construct map (e.g., collapsing two waypoints into one scoring category for practicality). These
become the first things to check once real data comes in during Block 4.

**See also:** `construct-map-guide.md` (the waypoints these items and categories are built
against); `measurement-model-selection.md` (how scored responses get combined and checked against
the map empirically).
