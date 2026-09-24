"""Score a blind sort against the answer key.

    python3 blind_sort_score.py answer_key.json sorter.csv [--round 1] [--state fbb-state.json] [--json]

sorter.csv is the blind-sorter agent's output, header:
    vignette_id,waypoint,runner_up,confidence

Reports overall accuracy, a confusion table (true x sorted), and a per-waypoint verdict:
    clean     every vignette of this waypoint sorted back to it
    confused  some vignettes went elsewhere; names the waypoint(s) they went to and whether
              the confusion is between ADJACENT waypoints (sharpen or merge) or distant ones
              (the continuum itself may be in doubt)

With --state, the result is written into the state file under construct_map.stress_test.rounds.
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

UNPLACED = "UNPLACED"


def read_sort(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "vignette_id" not in rows[0] or "waypoint" not in rows[0]:
        raise ValueError("sorter CSV needs columns vignette_id,waypoint")
    return {r["vignette_id"].strip(): r for r in rows}


def score(answer_key, sort_rows):
    order = answer_key["waypoint_order"]
    pos = {w: i for i, w in enumerate(order)}
    key = answer_key["key"]

    confusion = defaultdict(Counter)
    log = []
    for vid, true_wp in key.items():
        row = sort_rows.get(vid)
        got = (row["waypoint"].strip() if row else "") or UNPLACED
        if got not in pos:
            got = UNPLACED
        confusion[true_wp][got] += 1
        log.append({
            "vignette_id": vid,
            "true": true_wp,
            "sorted": got,
            "match": got == true_wp,
            "runner_up": (row.get("runner_up") or "").strip() if row else "",
            "confidence": (row.get("confidence") or "").strip() if row else "",
        })

    extra = sorted(set(sort_rows) - set(key))
    n = len(key)
    correct = sum(e["match"] for e in log)

    per_waypoint = []
    for w in order:
        total = sum(confusion[w].values())
        hits = confusion[w][w]
        wrong = {g: c for g, c in confusion[w].items() if g != w}
        entry = {"waypoint": w, "n": total, "correct": hits}
        if total == 0:
            entry["status"] = "no_vignettes"
        elif not wrong:
            entry["status"] = "clean"
        else:
            entry["status"] = "confused"
            entry["confused_with"] = [
                {
                    "waypoint": g,
                    "count": c,
                    "distance": None if g == UNPLACED else abs(pos[g] - pos[w]),
                }
                for g, c in sorted(wrong.items(), key=lambda kv: -kv[1])
            ]
        per_waypoint.append(entry)

    pairs = Counter()
    for e in log:
        if not e["match"] and e["sorted"] != UNPLACED:
            pairs[tuple(sorted((e["true"], e["sorted"]), key=pos.get))] += 1
    confusion_pairs = [
        {"pair": list(p), "count": c, "adjacent": abs(pos[p[0]] - pos[p[1]]) == 1}
        for p, c in pairs.most_common()
    ]

    if correct == n:
        verdict = "clean: every vignette sorted back to its waypoint"
    elif confusion_pairs and all(p["adjacent"] for p in confusion_pairs):
        verdict = "adjacent confusion: sharpen the named waypoint pair(s) or merge them"
    elif confusion_pairs:
        verdict = "non-adjacent confusion: revisit whether this is one ordered continuum"
    else:
        verdict = "unplaced vignettes only: rewrite those vignettes before blaming the waypoints"

    return {
        "n_vignettes": n,
        "n_correct": correct,
        "accuracy": round(correct / n, 3) if n else None,
        "verdict": verdict,
        "per_waypoint": per_waypoint,
        "confusion_pairs": confusion_pairs,
        "confusion_table": {w: dict(confusion[w]) for w in order},
        "unknown_ids_in_sort": extra,
        "log": log,
    }


def write_state(state_path, round_no, result):
    p = Path(state_path)
    state = json.loads(p.read_text()) if p.exists() else {}
    st = state.setdefault("construct_map", {}).setdefault("stress_test", {})
    rounds = [r for r in st.get("rounds", []) if r.get("round") != round_no]
    rounds.append({"round": round_no, **{k: v for k, v in result.items() if k != "log"}})
    st["rounds"] = sorted(rounds, key=lambda r: r["round"])
    p.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def print_report(res, order):
    print(f"Accuracy: {res['n_correct']}/{res['n_vignettes']} ({res['accuracy']:.0%})")
    print(f"Verdict:  {res['verdict']}\n")
    cols = order + [UNPLACED]
    print("true \\ sorted  " + "  ".join(f"{c:>8}" for c in cols))
    for w in order:
        row = res["confusion_table"][w]
        print(f"{w:<14} " + "  ".join(f"{row.get(c, 0):>8}" for c in cols))
    print()
    for e in res["per_waypoint"]:
        if e["status"] == "clean":
            print(f"  {e['waypoint']}: clean ({e['correct']}/{e['n']})")
        elif e["status"] == "confused":
            where = ", ".join(f"{c['waypoint']} x{c['count']}" for c in e["confused_with"])
            print(f"  {e['waypoint']}: confused ({e['correct']}/{e['n']}) -> {where}")
        else:
            print(f"  {e['waypoint']}: no vignettes")
    if res["unknown_ids_in_sort"]:
        print(f"\nIgnored ids not in the key: {', '.join(res['unknown_ids_in_sort'])}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("answer_key")
    ap.add_argument("sorter_csv")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--state", help="state JSON to record this round in")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    key = json.loads(Path(args.answer_key).read_text())
    res = score(key, read_sort(args.sorter_csv))
    if args.state:
        write_state(args.state, args.round, res)
    if args.json:
        json.dump(res, sys.stdout, indent=2)
        print()
    else:
        print_report(res, key["waypoint_order"])


if __name__ == "__main__":
    main()
