#!/usr/bin/env python3
"""Ekstrak 300 pasang M4 id-newspaper (seed 42) → data/m4_stylometry/.

Extend dari 100 pasang lama (seed 42 tetap, 100 lama termasuk di dalam 300 baru).
Filter: human_text ≥ 50 kata. Simpan ke folder terpisah dari self-check baseline.
"""

import json
import random
from pathlib import Path

SEED = 42
N_PAIRS = 300
MIN_WORDS = 50
JSONL_PATH = Path(__file__).resolve().parent / "data" / "id-newspaper_chatGPT.jsonl"
OUT_DIR = Path(__file__).resolve().parent / "data" / "m4_stylometry"

def main():
    # Load JSONL
    records = []
    with open(JSONL_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    print(f"Total records: {len(records)}")

    # Filter: human_text ≥ 50 kata
    filtered = []
    for r in records:
        human_text = r.get("human_text", "")
        if len(human_text.split()) >= MIN_WORDS:
            filtered.append(r)

    print(f"Filtered (human_text ≥ {MIN_WORDS} words): {len(filtered)}")

    # Random sample 300 (seed 42)
    random.seed(SEED)
    sampled = random.sample(filtered, min(N_PAIRS, len(filtered)))
    print(f"Sampled: {len(sampled)}")

    # Save
    ai_dir = OUT_DIR / "ai"
    human_dir = OUT_DIR / "human"
    ai_dir.mkdir(parents=True, exist_ok=True)
    human_dir.mkdir(parents=True, exist_ok=True)

    for i, r in enumerate(sampled, 1):
        fname = f"m4_id_{i:03d}.txt"
        (ai_dir / fname).write_text(r["machine_text"], encoding="utf-8")
        (human_dir / fname).write_text(r["human_text"], encoding="utf-8")

    print(f"Saved {len(sampled)} pairs to {OUT_DIR}")
    print(f"  ai:   {ai_dir}")
    print(f"  human: {human_dir}")

    # Verify first 100 overlap with original (if exists)
    orig_ai = Path(__file__).resolve().parent / "data" / "ai"
    if (orig_ai / "m4_id_001.txt").exists():
        match = 0
        for i in range(1, 101):
            fname = f"m4_id_{i:03d}.txt"
            old = (orig_ai / fname).read_text(encoding="utf-8")
            new = (ai_dir / fname).read_text(encoding="utf-8")
            if old == new:
                match += 1
        print(f"Overlap check (first 100 vs original): {match}/100 identical")

if __name__ == "__main__":
    main()
