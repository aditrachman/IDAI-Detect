#!/usr/bin/env python3
"""IDAI-Detect rule engine v0 — deteksi teks AI Bahasa Indonesia (rule-based multi-sinyal).

Sinyal dari validasi (lihat ../Pola dan Sinyal.md):
  terkonfirmasi kuat: em dash prosa, kalimat penutup analitik, enumerasi sistematis,
  burstiness rendah, transisi mekanis. Dictionary: puffery, hedging, kontras, basa-basi.
Bobot & threshold masih kasar (hasil validasi 5 sampel) — kalibrasi di Milestone 6.
ponytail: typo-manusia & narasi-kegagalan belum diimplementasi (susah rule-based,
kandidat ML layer v2).

Usage:
  python3 rule_engine.py <file.txt> [<file2.txt> ...]
"""

import re
import statistics
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------- preprocessing

_END = re.compile(r"[.!?…]+")


def split_sentences(line: str) -> list[str]:
    """Pecah satu baris jadi kalimat (min 4 kata, biar label pendek kebuang)."""
    return [s.strip() for s in _END.split(line) if len(s.split()) >= 4]


def prose_sentences(text: str) -> list[str]:
    """Kalimat prosa naratif: buang header/label pendek & baris mirip tabel.

    ponytail: heuristik baris — baris pendek tanpa .!? = label/header, baris
    dengan rasio digit tinggi = tabel. Gagal kalau dokumen tabelnya 1 baris
    panjang padat; upgrade: detect w:tbl di docx via python-docx.
    """
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line.split()) <= 4 and not _END.search(line):
            continue  # header/label
        digits = sum(c.isdigit() for c in line) / max(len(line), 1)
        if digits > 0.3:
            continue  # baris tabel (banyak angka)
        out.extend(split_sentences(line))
    return out


def _rate(count: int, total_words: int) -> float:
    return count * 1000 / total_words if total_words else 0.0


# ---------------------------------------------------------------- sinyal

EM_DASH = "—"

# kalimat terakhir paragraf yang merangkum ulang ("hasil ... menunjukkan bahwa ...")
_CLOSING = re.compile(
    r"\b(hasil|kesimpulan|secara keseluruhan|dengan demikian|dari uraian|"
    r"berdasarkan (?:hasil|pembahasan|analisis))"
    r".{0,80}\b(menunjukkan|dapat disimpulkan|terlihat|terbukti|memberikan gambaran)\b",
    re.I,
)

_ENUM_ORD = re.compile(r"^\s*(pertama|kedua|ketiga|keempat|kelima|keenam|terakhir)\b[,.\s]", re.I)
_ENUM_NUM = re.compile(r"^\s*(\d+|[a-z])[.)]\s+[A-Z]", re.I)

_HEDGING = ["cenderung", "kemungkinan", "umumnya", "pada umumnya", "sebagian besar",
            "dapat dikatakan", "dapat disimpulkan", "sebaiknya", "diharapkan", "mungkin"]

_TRANSISI = ["selain itu", "di sisi lain", "dengan demikian", "oleh karena itu",
             "berdasarkan hal tersebut", "lebih lanjut", "selanjutnya", "dalam hal ini",
             "pada dasarnya", "jika dilihat", "secara keseluruhan"]

_PUFFERY = ["memainkan peran", "menjadi bukti", "kunci utama", "sangat penting",
            "penting untuk dicatat", "perlu diingat", "di era digital", "lanskap",
            "menjadi solusi", "peran penting", "bukti nyata", "tidak dapat dipungkiri"]

_KONTRAS = re.compile(r"\bbukan\s+.{1,40}?\b(tapi|melainkan)\b", re.I)

_BASABASI = ["semoga membantu", "jika ada pertanyaan", "silahkan tanya", "jangan ragu",
             "semoga bermanfaat", "jika ada pertanyaan lain"]


def signal_em_dash(sents, total_words) -> float:
    """Em dash di prosa per 1.000 kata. Baseline: manusia 0, AI 1.5-12."""
    n = sum(s.count(EM_DASH) for s in sents)
    return min(_rate(n, total_words) / 2.0, 1.0), n


def signal_closing(sents) -> float:
    """Kalimat penutup analitik: kalimat terakhir baris yang merangkum analisis."""
    # rekonstruksi paragraf: kalimat yang diikuti akhir baris di teks asli
    # ponytail: pakai posisi "kalimat terakhir dari runtutan yang sama" via flag dari prose_sentences
    matched = 0
    total = len(sents)
    for i, s in enumerate(sents):
        if _CLOSING.search(s):
            matched += 1
    return min(matched / max(total, 1) * 6.0, 1.0), matched  # 1/6 kalimat aja udah penuh


def signal_enumeration(sents) -> float:
    """Enumerasi sistematis: Pertama/Kedua..., 1. 2. 3. di awal kalimat."""
    n = sum(1 for s in sents if _ENUM_ORD.match(s) or _ENUM_NUM.match(s))
    return min(n / 4.0, 1.0), n


def signal_burstiness(sents) -> float | None:
    """Homogenitas panjang kalimat. AI rendah (transisi mekanis). None kalau < 5 kalimat."""
    if len(sents) < 5:
        return None
    lens = [len(s.split()) for s in sents]
    ratio = statistics.stdev(lens) / statistics.mean(lens)
    # ponytail: threshold kasar, kalibrasi milestone 6 (noise di dokumen tabel-heavy)
    if ratio <= 0.40:
        return 1.0, ratio
    if ratio <= 0.55:
        return 0.5, ratio
    return 0.15, ratio


def signal_hedging(sents, total_words) -> float:
    n = sum(s.count(w) for s in sents for w in _HEDGING)
    return min(_rate(n, total_words) / 8.0, 1.0), n


def signal_transisi(sents, total_words) -> float:
    n = sum(s.count(w) for s in sents for w in _TRANSISI)
    reps = sum(1 for w in _TRANSISI if sum(s.count(w) for s in sents) > 2)
    score = min(_rate(n, total_words) / 10.0, 1.0) + 0.25 * min(reps, 2)
    return min(score, 1.0), n


def signal_puffery(sents, total_words) -> float:
    n = sum(s.count(w) for s in sents for w in _PUFFERY)
    return min(_rate(n, total_words) / 3.0, 1.0), n


def signal_kontras(sents) -> float:
    n = sum(1 for s in sents if _KONTRAS.search(s))
    return min(n / 2.0, 1.0), n


def signal_basabasi(sents) -> float:
    n = sum(s.count(w) for s in sents for w in _BASABASI)
    return min(n, 1.0), n


# ---------------------------------------------------------------- scoring

# bobot dari kekuatan validasi (kalibrasi kasar 5 sampel, milestone 6 nanti)
# em dash terkuat (3 sampel AI vs 0 manusia, tahan edit) → bobot tertinggi
WEIGHTS = {
    "em_dash": 0.35,
    "closing": 0.20,      # terkonfirmasi case #2 & #3
    "enumerasi": 0.15,    # case #2: 9× enumerasi sistematis
    "burstiness": 0.05,   # noise di dokumen tabel-heavy → bobot kecil
    "hedging": 0.05,      # lemah: human_01 malah lebih banyak hedging
    "transisi": 0.05,     # lemah: human_01 juga banyak transisi
    "puffery": 0.05,
    "kontras": 0.05,
    "basabasi": 0.05,
}

THRESHOLD_AI = 0.44
THRESHOLD_HUMAN = 0.25
MIN_WORDS_CONFIDENT = 300


def analyze(text: str) -> dict:
    """Analisis satu teks → dict hasil. API utama, dipakai CLI & FastAPI nanti."""
    sents = prose_sentences(text)
    total_words = sum(len(s.split()) for s in sents)

    signals = {}
    signals["em_dash"], signals["em_dash_n"] = signal_em_dash(sents, total_words)
    signals["closing"], signals["closing_n"] = signal_closing(sents)
    signals["enumerasi"], signals["enumerasi_n"] = signal_enumeration(sents)
    b = signal_burstiness(sents)
    signals["burstiness"], signals["burstiness_ratio"] = (b if b else (0.0, None))
    signals["hedging"], signals["hedging_n"] = signal_hedging(sents, total_words)
    signals["transisi"], signals["transisi_n"] = signal_transisi(sents, total_words)
    signals["puffery"], signals["puffery_n"] = signal_puffery(sents, total_words)
    signals["kontras"], signals["kontras_n"] = signal_kontras(sents)
    signals["basabasi"], signals["basabasi_n"] = signal_basabasi(sents)

    # weighted sum dengan normalisasi bobot (skip sinyal yang gak punya nilai)
    active = {k: w for k, w in WEIGHTS.items() if signals.get(k) is not None}
    total_w = sum(active.values())
    score = sum(signals[k] * w for k, w in active.items()) / total_w

    low_confidence = total_words < MIN_WORDS_CONFIDENT
    if score >= THRESHOLD_AI:
        verdict = "AI"
    elif score <= THRESHOLD_HUMAN:
        verdict = "manusia"
    else:
        verdict = "abu-abu"

    return {
        "verdict": verdict,
        "score": round(score, 3),
        "words_analyzed": total_words,
        "low_confidence": low_confidence,
        "signals": {k: v for k, v in signals.items() if isinstance(v, (int, float))},
    }


# ---------------------------------------------------------------- per-kalimat (buat UI highlight)

FLAG_RULES = [
    ("em_dash", lambda s: EM_DASH in s, "Tanda pisah (—) dipakai di prosa — pola khas AI"),
    ("closing", lambda s: bool(_CLOSING.search(s)), "Kalimat penutup analitik — merangkum ulang analisis"),
    ("enumerasi", lambda s: bool(_ENUM_ORD.match(s) or _ENUM_NUM.match(s)), "Enumerasi sistematis (Pertama/Kedua... atau 1. 2. 3.)"),
    ("hedging", lambda s: any(w in s for w in _HEDGING), "Kata hati-hati/hedging berulang"),
    ("transisi", lambda s: any(w in s for w in _TRANSISI), "Transisi kaku (selain itu, dengan demikian...)"),
    ("puffery", lambda s: any(w in s for w in _PUFFERY), "Frasa lebay/puffery"),
    ("kontras", lambda s: bool(_KONTRAS.search(s)), "Kontras 'bukan X tapi Y'"),
    ("basabasi", lambda s: any(w in s for w in _BASABASI), "Basa-basi sisa chat"),
]

# label pendek buat UI (legend + tooltip)
FLAG_LABELS = {name: name.replace("_", " ") for name, _, _ in FLAG_RULES}


def flag_sentences(text: str) -> list[dict]:
    """Kalimat prosa + daftar sinyal yang kena — buat highlight di UI."""
    return [
        {"text": s, "flags": [name for name, test, _ in FLAG_RULES if test(s)]}
        for s in prose_sentences(text)
    ]


def _norm_key(s: str) -> str:
    """Normalisasi buat pencocokan kalimat: spasi 1x, buang tanda baca akhir."""
    return re.sub(r"\s+", " ", s).strip().rstrip(".!?…")


def paragraphs_with_flags(text: str) -> list[dict]:
    """Paragraf asli + per-kalimat flag, buat highlight inline di teks utuh."""
    flagged = {_norm_key(s["text"]): s["flags"] for s in flag_sentences(text) if s["flags"]}
    paras = []
    for p in re.split(r"\n{2,}", text):
        p = p.strip()
        if not p:
            continue
        parts = re.split(r"(?<=[.!?…])\s+", p)
        sents_ui = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            flags = flagged.get(_norm_key(part), [])
            sents_ui.append({"text": part, "flagged": bool(flags), "flags": flags})
        paras.append({"text": p, "sentences": sents_ui})
    return paras


# ---------------------------------------------------------------- CLI + self-check

def _fmt(r: dict) -> str:
    sig = " ".join(f"{k}={v:.2f}" for k, v in r["signals"].items() if isinstance(v, float) and k in WEIGHTS)
    warn = " ⚠️TEXT PENDEK" if r["low_confidence"] else ""
    return (f"{r['verdict']:>8}  score={r['score']:.3f}  kata={r['words_analyzed']:>5}{warn}\n"
            f"          {sig}")


def read_text(path: Path) -> str:
    """Baca .txt langsung, .docx via zipfile (stdlib, tanpa python-docx)."""
    if path.suffix.lower() == ".docx":
        xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
        xml = xml.replace("</w:p>", "\n")
        return re.sub(r"\n{3,}", "\n\n", re.sub(r"<[^>]+>", "", xml))
    if path.suffix.lower() == ".pdf":
        from PyPDF2 import PdfReader  # lazy import biar engine tetep portable
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    for path in argv:
        r = analyze(read_text(Path(path)))
        print(f"{path}:")
        print(_fmt(r))
    return 0


def self_check(data_dir: Path) -> int:
    """Self-check strict: SEMUA sampel di data/ai/ harus verdict AI, SEMUA di data/human/
    harus verdict manusia. Gagal → return 1 + daftar kegagalan (jujur, bukan disembunyiin).
    Sampel AI yang diverdict salah = sinyal bobot/threshold belum layak, bukan error yang
    boleh di-cherry-pick. Kalibrasi: Milestone 6 dengan data M4 (subset Indonesia).
    """
    results = {}
    for label, folder in [("AI", "ai"), ("HUMAN", "human")]:
        for f in sorted((data_dir / folder).glob("*.txt")):
            r = analyze(f.read_text(encoding="utf-8"))
            results[f.name] = r
            ok = r["verdict"] == ("AI" if label == "AI" else "manusia")
            print(f"{label:<6} {f.name}: score={r['score']:.3f} verdict={r['verdict']:<8} {'OK' if ok else 'FAIL'}")

    ai_scores = [r["score"] for n, r in results.items() if n.startswith("ai")]
    hu_scores = [r["score"] for n, r in results.items() if n.startswith("human")]
    avg_ai, avg_hu = sum(ai_scores) / len(ai_scores), sum(hu_scores) / len(hu_scores)
    print(f"\navg AI={avg_ai:.3f} vs avg human={avg_hu:.3f}")

    fails = [
        (n, "AI", r["verdict"]) for n, r in results.items()
        if n.startswith("ai") and r["verdict"] != "AI"
    ] + [
        (n, "HUMAN", r["verdict"]) for n, r in results.items()
        if n.startswith("human") and r["verdict"] != "manusia"
    ]
    if fails:
        print(f"\nSELF-CHECK FAIL — {len(fails)} sampel tidak sesuai label:")
        for n, label, verdict in fails:
            print(f"  FAIL {n} (label {label}) -> verdict {verdict}")
        print("Ini sinyal jujur: bobot/threshold belum layak. Kalibrasi di Milestone 6 (data M4).")
        return 1
    print("SELF-CHECK OK")
    return 0


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent.parent / "data"
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        raise SystemExit(self_check(data_dir))
    else:
        raise SystemExit(main(sys.argv[1:]))