# Block 4 in depth: choosing a measurement model

The measurement model places persons and item-response thresholds on **one interval (logit)
scale**, which is then read as a **Wright map** — the empirical test of the construct map from
Block 1.

## Decision tree

Walk these questions in order; stop at the first match.

1. **Is there one construct or several strands?**
   - One construct → continue to Q2.
   - Several strands to be reported together → **multidimensional model (MRCM)**. Each strand gets
     its own scale; a composite/derived score can be added if the design calls for it (needs a
     multilevel model — flag this early, it's a bigger analysis lift).

2. **Are items scored right/wrong (dichotomous) or on an ordered multi-point scale (polytomous)?**
   - Dichotomous → **Rasch model**.
   - Polytomous (e.g., a 0–3 rubric score) → **Partial Credit Model** (or Rating Scale Model if all
     items share the same category structure).

3. **Do person or item characteristics need to be modeled explicitly** (e.g., checking for group
   differences / DIF, modeling growth over time, or explaining item difficulty from item
   features)?
   - Yes → use the **explanatory IRT** framing (person/item predictors as covariates in a
     generalized linear/nonlinear mixed model) layered on top of whichever base model Q1/Q2
     selected.
   - No → the descriptive (no-predictor) version of that model is enough for now.

4. **Do you suspect discontinuous, stage-like development** rather than smooth continuous growth
   (e.g., a conceptual "leap" rather than gradual accumulation)?
   - Yes → consider **Saltus** or a confirmatory mixture IRT model instead of (or alongside) the
     standard model.

5. **Do some items share a common stimulus or context that could make their responses locally
   dependent** (e.g., several questions about the same reading passage, or repeated ratings by the
   same rater)?
   - Yes → use an **item bundle / Rasch testlet** model (shared stimulus) or a **rater bundle**
     model (shared rater) to absorb that dependence rather than ignoring it.

6. **Do you want cut-scores or performance levels set directly on the construct map** (e.g., for
   certification or placement)?
   - Yes → note **construct-mapping standard setting** as the Block-4 follow-on step once the model
     is fit.

Most instruments only need Q1–Q2; Q3–Q6 are refinements to flag now and revisit once real data is
in hand.

## Reading the Wright map

Once the model is fit (this is typically a separate analysis step, not part of design), the Wright
map places persons and item-response thresholds on the same scale:

- Each construct-map **waypoint becomes a band** — a range of threshold locations — not a single
  point, because the items meant to target that waypoint won't land at exactly the same place.
- **Check the empirical order** of thresholds against the hypothesized waypoint order. This is the
  core validity check for the whole instrument.
- **Where they clash** (e.g., two waypoints' items interleave instead of separating cleanly),
  that's a signal to **revise the construct map or the item set**, not to force-fit the data. This
  feedback loop — data revising theory, theory guiding the next round of items — is the point of
  the four-building-block method, not a failure of it.

## What to include in the design document at this stage

Even before any data exists, the design document should state:
- Which model (from the decision tree above) is planned, and why.
- Any dependence structure expected (testlets, rater bundles) that the analysis will need to
  handle.
- What "looking right" would mean on a future Wright map — i.e., restate the hypothesized waypoint
  order from Block 1 as a concrete, checkable prediction.

**See also:** `construct-map-guide.md` (the waypoint order being tested); `items-and-outcome-space.md`
(what's being scored and fed into this model).
