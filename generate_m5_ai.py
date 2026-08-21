#!/usr/bin/env python3
"""M5 — Generate pasangan AI dari teks manusia via Groq API (Llama/GPT-oss).

Rate limit: 30 req/min, ~1000/hari. 30 teks = aman, jeda 2s antar-request.
"""

import json
import time
from pathlib import Path
from groq import Groq

HUMAN_DIR = Path(__file__).resolve().parent / "data" / "m5_generalization" / "human"
AI_DIR = Path(__file__).resolve().parent / "data" / "m5_generalization" / "ai"
META_PATH = Path(__file__).resolve().parent / "data" / "m5_generalization" / "m5_human_metadata.json"
MODEL = "openai/gpt-oss-120b"

client = Groq()

def extract_topic(text):
    """Ambil topik dari header file."""
    for line in text.splitlines():
        if line.startswith("Topik:"):
            return line.replace("Topik:", "").strip()
    return "topik umum"

def generate_ai_text(topic, human_text):
    """Generate versi AI dari topik yang sama."""
    prompt = f"""Tulis esai/opini berbahasa Indonesia tentang topik berikut. Panjang 200-300 kata. Tulis gaya natural, jangan pakai template atau format kaku.

Topik: {topic}

Tulis esainya langsung, jangan pakai penjelasan atau thinking tags."""

    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Kamu adalah penulis esai Indonesia yang baik. Tulis natural, tidak kaku, tidak pakai template."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.8
    )
    content = r.choices[0].message.content
    # Bersihkan thinking tags kalau ada
    if "<think>" in content:
        import re
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    return content

def main():
    AI_DIR.mkdir(parents=True, exist_ok=True)

    # Load metadata
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    # Cek哪些 sudah ada
    existing = {f.stem for f in AI_DIR.glob("essay_*.txt")}
    print(f"Existing AI essays: {len(existing)}")

    success = 0
    failed = 0

    for i, m in enumerate(meta, 1):
        fname = f"essay_{i:03d}.txt"
        if fname.replace(".txt", "") in existing:
            print(f"[{i:02d}] SKIP (sudah ada): {fname}")
            success += 1
            continue

        human_path = HUMAN_DIR / fname
        if not human_path.exists():
            print(f"[{i:02d}] SKIP (file tidak ada): {fname}")
            continue

        content = human_path.read_text(encoding="utf-8")
        topic = extract_topic(content)
        # Ambil teks asli (tanpa header)
        lines = content.split("\n\n", 1)
        human_text = lines[1] if len(lines) > 1 else content

        print(f"[{i:02d}] Generating: {topic[:50]}...", end=" ", flush=True)
        try:
            ai_text = generate_ai_text(topic, human_text)
            words = len(ai_text.split())

            # Save
            out_content = f"Sumber: Groq API ({MODEL})\nTopik: {topic}\nPasangan dari: {m['source']}\n\n{ai_text}"
            (AI_DIR / fname).write_text(out_content, encoding="utf-8")
            print(f"OK ({words} kata)")
            success += 1

            # Rate limit jeda
            time.sleep(2.5)
        except Exception as e:
            print(f"FAIL: {e}")
            failed += 1
            time.sleep(5)  # longer jeda on error

    print(f"\nDone: {success} OK, {failed} FAILED")

    # Update metadata
    ai_meta = []
    for i, m in enumerate(meta, 1):
        fname = f"essay_{i:03d}.txt"
        ai_path = AI_DIR / fname
        if ai_path.exists():
            ai_meta.append({
                "file": fname,
                "source": f"Groq API ({MODEL})",
                "topic": m["topic"],
                "model": MODEL,
                "human_pair": m["file"]
            })
    ai_meta_path = AI_DIR.parent / "m5_ai_metadata.json"
    ai_meta_path.write_text(json.dumps(ai_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"AI metadata: {ai_meta_path}")

if __name__ == "__main__":
    main()
