#!/usr/bin/env python3
"""M3.1 — Diagnostic Per-Sinyal: analisis kontribusi tiap sinyal di domain berita.

Baca semua sampel M4 AI (data/ai/m4_id_*.txt) + sampel akademik (ai_01..ai_04),
hitung % mati, rata-rata nilai, dan ranking sinyal.
"""

import statistics
from pathlib import Path
from engine.rule_engine import analyze, WEIGHTS

DATA_DIR = Path(__file__).resolve().parent / "data"
SINYAL = list(WEIGHTS.keys())

def load_samples():
    """Load M4 AI + academic AI samples."""
    m4_ai = []
    for f in sorted((DATA_DIR / "ai").glob("m4_id_*.txt")):
        text = f.read_text(encoding="utf-8")
        m4_ai.append(("m4", f.name, text))

    academic_ai = []
    for f in sorted((DATA_DIR / "ai").glob("ai_0*.txt")):
        text = f.read_text(encoding="utf-8")
        academic_ai.append(("academic", f.name, text))

    return m4_ai, academic_ai

def analyze_batch(samples):
    """Run analyze() on each sample, return list of result dicts."""
    results = []
    for domain, name, text in samples:
        r = analyze(text)
        results.append({"domain": domain, "name": name, "result": r})
    return results

def compute_diagnostic(results_m4, results_academic):
    """Compute per-signal diagnostic metrics."""
    diagnostic = {}

    for sig in SINYAL:
        # M4 values
        m4_values = [r["result"]["signals"].get(sig, 0.0) for r in results_m4]
        # Academic values
        acad_values = [r["result"]["signals"].get(sig, 0.0) for r in results_academic]

        # % mati (value <= 0.05)
        m4_dead_pct = sum(1 for v in m4_values if v <= 0.05) / len(m4_values) * 100
        # % sangat rendah (value <= 0.10)
        m4_low_pct = sum(1 for v in m4_values if v <= 0.10) / len(m4_values) * 100

        m4_mean = statistics.mean(m4_values) if m4_values else 0
        acad_mean = statistics.mean(acad_values) if acad_values else 0

        # Weighted contribution (value * weight)
        m4_weighted = [r["result"]["signals"].get(sig, 0.0) * WEIGHTS[sig] for r in results_m4]
        acad_weighted = [r["result"]["signals"].get(sig, 0.0) * WEIGHTS[sig] for r in results_academic]
        m4_weighted_mean = statistics.mean(m4_weighted) if m4_weighted else 0
        acad_weighted_mean = statistics.mean(acad_weighted) if acad_weighted else 0

        diagnostic[sig] = {
            "weight": WEIGHTS[sig],
            "m4_dead_pct": round(m4_dead_pct, 1),
            "m4_low_pct": round(m4_low_pct, 1),
            "m4_mean": round(m4_mean, 4),
            "acad_mean": round(acad_mean, 4),
            "m4_weighted_mean": round(m4_weighted_mean, 4),
            "acad_weighted_mean": round(acad_weighted_mean, 4),
        }

    return diagnostic

def main():
    print("=" * 60)
    print("M3.1 — Diagnostic Per-Sinyal (Domain Berita)")
    print("=" * 60)

    m4_ai, academic_ai = load_samples()
    print(f"\nSampel M4 AI: {len(m4_ai)} | Sampel Akademik AI: {len(academic_ai)}")

    results_m4 = analyze_batch(m4_ai)
    results_academic = analyze_batch(academic_ai)

    # Verdict summary
    m4_correct = sum(1 for r in results_m4 if r["result"]["verdict"] == "AI")
    print(f"M4 verdict AI: {m4_correct}/{len(results_m4)} ({m4_correct/len(results_m4)*100:.0f}%)")

    diag = compute_diagnostic(results_m4, results_academic)

    # Sort by m4_dead_pct descending (most dead first)
    ranked = sorted(diag.items(), key=lambda x: (-x[1]["m4_dead_pct"], x[1]["m4_mean"]))

    print("\n" + "─" * 60)
    print(f"{'Sinyal':<12} {'Bobot':>6} {'M4 Mati%':>9} {'M4 Low%':>8} "
          f"{'M4 Avg':>8} {'Acad Avg':>9} {'M4*W':>7} {'Acad*W':>7}")
    print("─" * 60)

    for sig, d in ranked:
        print(f"{sig:<12} {d['weight']:>6.2f} {d['m4_dead_pct']:>8.1f}% {d['m4_low_pct']:>7.1f}% "
              f"{d['m4_mean']:>8.4f} {d['acad_mean']:>9.4f} {d['m4_weighted_mean']:>7.4f} {d['acad_weighted_mean']:>7.4f}")

    print("─" * 60)

    # Count dead signals
    dead_count = sum(1 for _, d in ranked if d["m4_dead_pct"] >= 80)
    low_count = sum(1 for _, d in ranked if d["m4_dead_pct"] >= 50)
    alive_count = len(SINYAL) - dead_count

    print(f"\nRingkasan: {dead_count}/{len(SINYAL)} sinyal mati (≥80% zero), "
          f"{low_count}/{len(SINYAL)} rendah (≥50% zero), {alive_count} masih hidup")

    # Recommendation
    print("\n" + "═" * 60)
    print("REKOMENDASI:")
    if dead_count >= 6:
        print(f"→ {dead_count}/9 sinyal MATI TOTAL di domain berita.")
        print("  → LANJUT ke eksperimen stilometri/ML layer.")
        print("  Rule-based dengan sinyal yang ada TIDAK cukup untuk domain berita.")
    elif dead_count <= 3:
        print(f"→ Cuma {dead_count}/9 sinyal yang mati, sisanya masih hidup tapi under-weighted.")
        print("  → COBA domain-aware weighting dulu (lebih murah, masih rule-based).")
        print("  Pivot ML bisa ditunda sampai domain-aware weight gagal.")
    else:
        print(f"→ {dead_count}/9 sinyal mati — antara domain-aware weighting DAN ML diperlukan.")
        print("  → Mulai dengan domain-aware weighting, siapkan ML sebagai fallback.")
    print("═" * 60)

    # Save raw data for Eksperimen.md
    print("\n\n--- RAW DATA FOR EKSPERIMEN.MD ---")
    for sig, d in ranked:
        print(f"| {sig} | {d['weight']:.2f} | {d['m4_dead_pct']:.1f}% | {d['m4_low_pct']:.1f}% | "
              f"{d['m4_mean']:.4f} | {d['acad_mean']:.4f} | {d['m4_weighted_mean']:.4f} | {d['acad_weighted_mean']:.4f} |")

if __name__ == "__main__":
    main()
