"""Unit checks for the plugin scripts.  Run: python3 -m unittest discover -s scripts/tests"""
import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import blind_sort_score  # noqa: E402
import render_dashboard  # noqa: E402
import shuffle_vignettes  # noqa: E402

EXAMPLE = HERE.parent.parent / "skills" / "design" / "references" / "example-state.json"

SPEC = {
    "waypoints": [
        {"id": "W1", "label": "low", "definition": "d1"},
        {"id": "W2", "label": "mid", "definition": "d2"},
        {"id": "W3", "label": "high", "definition": "d3"},
    ],
    "vignettes": [{"waypoint": w, "text": f"{w} case {i}"} for w in ("W1", "W2", "W3") for i in range(3)],
}


def sort_csv(assign):
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    w = csv.writer(fh)
    w.writerow(["vignette_id", "waypoint", "runner_up", "confidence"])
    for vid, wp in assign.items():
        w.writerow([vid, wp, "", "high"])
    fh.close()
    return fh.name


class Shuffle(unittest.TestCase):
    def test_packet_hides_the_key(self):
        packet, key = shuffle_vignettes.build(SPEC, seed=1)
        blob = json.dumps(packet)
        self.assertNotIn('"waypoint":', blob)
        self.assertEqual(len(packet["vignettes"]), 9)
        self.assertEqual(set(key["key"]), {v["vignette_id"] for v in packet["vignettes"]})

    def test_seed_is_reproducible_and_shuffles(self):
        a, _ = shuffle_vignettes.build(SPEC, seed=3)
        b, _ = shuffle_vignettes.build(SPEC, seed=3)
        self.assertEqual(a, b)
        texts = [v["text"] for v in a["vignettes"]]
        self.assertNotEqual(texts, [v["text"] for v in SPEC["vignettes"]])

    def test_unknown_waypoint_rejected(self):
        bad = {"waypoints": SPEC["waypoints"], "vignettes": [{"waypoint": "W9", "text": "x"}]}
        with self.assertRaises(ValueError):
            shuffle_vignettes.build(bad)


class Score(unittest.TestCase):
    def setUp(self):
        _, self.key = shuffle_vignettes.build(SPEC, seed=5)

    def test_perfect_sort_is_clean(self):
        res = blind_sort_score.score(self.key, blind_sort_score.read_sort(sort_csv(self.key["key"])))
        self.assertEqual(res["accuracy"], 1.0)
        self.assertTrue(all(p["status"] == "clean" for p in res["per_waypoint"]))
        self.assertTrue(res["verdict"].startswith("clean"))

    def test_adjacent_confusion_flagged(self):
        assign = dict(self.key["key"])
        w2 = [v for v, w in assign.items() if w == "W2"]
        assign[w2[0]] = "W3"
        res = blind_sort_score.score(self.key, blind_sort_score.read_sort(sort_csv(assign)))
        self.assertEqual(res["n_correct"], 8)
        self.assertEqual(res["confusion_pairs"], [{"pair": ["W2", "W3"], "count": 1, "adjacent": True}])
        self.assertTrue(res["verdict"].startswith("adjacent"))
        w2_entry = next(p for p in res["per_waypoint"] if p["waypoint"] == "W2")
        self.assertEqual(w2_entry["status"], "confused")

    def test_distant_confusion_and_unplaced(self):
        assign = dict(self.key["key"])
        w1 = [v for v, w in assign.items() if w == "W1"]
        assign[w1[0]] = "W3"
        assign[w1[1]] = "UNCODABLE"
        del assign[w1[2]]
        res = blind_sort_score.score(self.key, blind_sort_score.read_sort(sort_csv(assign)))
        self.assertTrue(res["verdict"].startswith("non-adjacent"))
        self.assertEqual(res["confusion_table"]["W1"].get("UNPLACED"), 2)

    def test_state_round_written_and_replaced(self):
        state = Path(tempfile.mkdtemp()) / "fbb-state.json"
        res = blind_sort_score.score(self.key, blind_sort_score.read_sort(sort_csv(self.key["key"])))
        blind_sort_score.write_state(state, 1, res)
        blind_sort_score.write_state(state, 1, res)
        rounds = json.loads(state.read_text())["construct_map"]["stress_test"]["rounds"]
        self.assertEqual(len(rounds), 1)
        self.assertNotIn("log", rounds[0])


class Dashboard(unittest.TestCase):
    def test_example_state_renders_all_panels(self):
        state = json.loads(EXAMPLE.read_text())
        out = render_dashboard.render(state)
        for needle in ("Panel 1", "Panel 2", "Panel 3", "<svg", "<details", "Reasoning about variability",
                       "nothing reusable found", "coverage gap"):
            self.assertIn(needle, out)

    def test_stress_badges_from_scored_round(self):
        state = json.loads(EXAMPLE.read_text())
        spec = {"waypoints": state["construct_map"]["waypoints"],
                "vignettes": [{"waypoint": w["id"], "text": w["id"]} for w in state["construct_map"]["waypoints"] for _ in range(2)]}
        _, key = shuffle_vignettes.build(spec, seed=2)
        assign = dict(key["key"])
        w2 = next(v for v, w in assign.items() if w == "W2")
        assign[w2] = "W3"
        res = blind_sort_score.score(key, blind_sort_score.read_sort(sort_csv(assign)))
        state["construct_map"]["stress_test"]["rounds"] = [{"round": 1, **res}]
        out = render_dashboard.render(state)
        self.assertIn("⚠ Confused with W3", out)
        self.assertIn("✓ No confusion", out)
        self.assertIn("added &#x27;no quantity or pattern named&#x27;", out)

    def test_empty_state_and_escaping(self):
        out = render_dashboard.render({"project": {"construct": "<b>x</b>"}})
        self.assertIn("&lt;b&gt;x&lt;/b&gt;", out)
        self.assertIn("Construct map not drafted yet", out)
        self.assertNotIn("<svg", out)
        self.assertIn("Not yet run — completes in Block 2", out)

    def test_venn_labels_stay_inside_canvas(self):
        import re
        state = json.loads(EXAMPLE.read_text())
        rel = ["jangle", "related", "jingle", "none", "related", "jingle"]
        state["literature"]["constructs"] = [{"name": f"C{i}", "relationship": r} for i, r in enumerate(rel)]
        svg = render_dashboard.venn("ours", state["literature"]["constructs"])
        for y in re.findall(r'<text x="[-\d.]+" y="([-\d.]+)"', svg):
            self.assertTrue(0 < float(y) <= render_dashboard.VH, y)


if __name__ == "__main__":
    unittest.main()
