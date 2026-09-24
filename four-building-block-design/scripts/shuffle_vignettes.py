"""Build a blind-sort packet from labelled vignettes, and keep the answer key apart.

Input (JSON):
    {
      "waypoints": [{"id": "W1", "label": "...", "definition": "..."}, ...],   # low -> high
      "vignettes": [{"waypoint": "W1", "text": "..."}, ...]
    }

Outputs, in --out-dir:
    sort_packet.json   waypoint definitions + shuffled vignettes with opaque ids.
                       This is the ONLY file the blind-sorter agent may see.
    answer_key.json    vignette id -> true waypoint. Never give this to the sorter.

    python3 shuffle_vignettes.py vignettes.json --out-dir stress_test/round1 [--seed 7]
"""
import argparse
import json
import random
import sys
from pathlib import Path


def build(spec, seed=None):
    waypoints = spec["waypoints"]
    ids = [w["id"] for w in waypoints]
    if len(set(ids)) != len(ids):
        raise ValueError("waypoint ids must be unique")
    vignettes = spec["vignettes"]
    for v in vignettes:
        if v["waypoint"] not in ids:
            raise ValueError(f"vignette points to unknown waypoint {v['waypoint']!r}")

    rng = random.Random(seed)
    order = list(range(len(vignettes)))
    rng.shuffle(order)
    width = max(2, len(str(len(vignettes))))

    packet_items, key = [], {}
    for n, i in enumerate(order, start=1):
        vid = f"V{n:0{width}d}"
        packet_items.append({"vignette_id": vid, "text": vignettes[i]["text"]})
        key[vid] = vignettes[i]["waypoint"]

    # Waypoints go in construct order (the order is part of the theory being tested);
    # vignettes carry no waypoint and their ids follow the shuffled order.
    packet = {
        "waypoints": [
            {"id": w["id"], "label": w.get("label", ""), "definition": w["definition"]}
            for w in waypoints
        ],
        "vignettes": packet_items,
    }
    answer_key = {"waypoint_order": ids, "key": key}
    return packet, answer_key


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vignettes")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)

    spec = json.loads(Path(args.vignettes).read_text())
    packet, answer_key = build(spec, args.seed)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "sort_packet.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False))
    (out / "answer_key.json").write_text(json.dumps(answer_key, indent=2, ensure_ascii=False))

    per = {}
    for wp in answer_key["key"].values():
        per[wp] = per.get(wp, 0) + 1
    thin = [w for w in answer_key["waypoint_order"] if per.get(w, 0) < 2]
    print(f"{len(packet['vignettes'])} vignettes over {len(packet['waypoints'])} waypoints")
    print(f"packet (give to blind-sorter): {out / 'sort_packet.json'}")
    print(f"answer key (keep):             {out / 'answer_key.json'}")
    if thin:
        print(f"WARNING: fewer than 2 vignettes for {', '.join(thin)}", file=sys.stderr)


if __name__ == "__main__":
    main()
