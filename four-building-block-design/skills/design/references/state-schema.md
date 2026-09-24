# `fbb-state.json` schema

One file per construct, in the user's working folder. `scripts/render_dashboard.py` and
`scripts/blind_sort_score.py --state` read and write it. A filled example is in
`example-state.json`.

```jsonc
{
  "project": {
    "construct": "short name",
    "one_sentence": "definition in one sentence",
    "respondents": "", "setting": "", "decision": "",
    "neighbours": ["constructs ruled separate in Step 0"],
    "created": "YYYY-MM-DD", "updated": "YYYY-MM-DD"
  },
  "stages": {                      // b1..b4
    "b1": {"status": "not_started | in_progress | awaiting_gate | approved", "gate_note": ""}
  },
  "literature": {                  // B1 jingle-jangle check -> dashboard Panel 1
    "keywords": ["every phrasing searched"],
    "verdict": "one line",
    "constructs": [{
      "keyword": "", "name": "", "source": "citation or URL",
      "definition": "paraphrase, never verbatim",
      "relationship": "jangle | jingle | related | none",
      "action": "rename ours / sharpen distinction / adopt / adapt / proceed"
    }]
  },
  "construct_map": {               // B1 -> dashboard Panel 2
    "map_type": "respondent | item-response | full",
    "structure": "single continuum | multiple strands | ordered partition | latent classes",
    "waypoints": [                 // LOW -> HIGH
      {"id": "W1", "label": "", "cue": "optional, e.g. lowest", "definition": "", "example_respondent": ""}
    ],
    "expert_review": [{"reviewer": "content-expert | measurement-reviewer | equity-reviewer", "issues": "", "revisions": "", "applied": true}],
    "stress_test": {
      "rounds": [],                // written by blind_sort_score.py --state (one entry per round)
      "resolution": {"W2": "what was changed to fix confusion, per waypoint"}
    }
  },
  "items": {                       // B2 -> dashboard Panel 3 + Panel 2 examples
    "keywords": [], "verdict": "",
    "existing": [{"source": "", "description": "paraphrase", "waypoints": ["W2"], "format": "",
                  "license": "open | owned | unclear | restricted",
                  "decision": "reuse | adapt | inspired-by-rewrite | not used"}],
    "bank": [{"id": "I1", "text": "", "waypoints": ["W2"], "format": "",
              "origin": "new | adapted | reused", "source": "",
              "irrelevant_features": "construct-irrelevant variance risks"}]
  },
  "outcome_space": [{              // B3
    "item_family": "I1 or a family name",
    "categories": [{"score": 0, "waypoint": "W1", "description": "", "exemplars": [""]}],
    "rater_note": ""
  }],
  "measurement_model": {           // B4
    "model": "Rasch | PCM | MRCM | explanatory IRT | Saltus | testlet",
    "rationale": "", "software": "", "wright_map_check": "what order is predicted",
    "risks": [""]
  },
  "loopbacks": [{"from": "b4", "to": "b1", "reason": "", "date": ""}],
  "decisions": [{"stage": "b1", "decision": "", "decided_by": "user | proposed",
                 "evidence": "literature | synthetic | real_data", "date": ""}]
}
```

Keep waypoints ordered **low → high** in the file. The dashboard displays them high → low.
