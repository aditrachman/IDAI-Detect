#!/usr/bin/env python3
"""M4 — Eksperimen Stilometri: klasifikasi AI vs manusia di domain berita.

Fitur: statistik permukaan + function words Indonesia + TF-IDF char n-gram.
Classifier: Logistic Regression (5-fold CV, class_weight='balanced').
Baseline comparison: rule engine v0 di data yang sama.
"""

import re
import statistics
from pathlib import Path
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, GroupKFold, cross_validate
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack

DATA_DIR = Path(__file__).resolve().parent / "data" / "m4_stylometry"

# ──────────────────────────── Indonesian function words (top-20)
# Frequency list dari korpus Bahasa Indonesia umum
INDO_FUNCTION_WORDS = [
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan",
    "untuk", "pada", "adalah", "akan", "juga", "sudah", "tidak",
    "dalam", "oleh", "karena", "ada", "lebih",
]

# ──────────────────────────── Feature extraction

def split_sentences(text):
    """Pecah teks jadi kalimat."""
    return [s.strip() for s in re.split(r'[.!?…]+', text) if len(s.strip().split()) >= 3]

def extract_features(text):
    """Ekstrak fitur statistik permukaan dari satu teks."""
    sents = split_sentences(text)
    words = text.split()
    total_words = len(words)

    # Sentence length
    sent_lens = [len(s.split()) for s in sents] if sents else [0]
    sent_len_mean = statistics.mean(sent_lens)
    sent_len_std = statistics.stdev(sent_lens) if len(sent_lens) > 1 else 0

    # Word length
    word_lens = [len(w) for w in words] if words else [0]
    word_len_mean = statistics.mean(word_lens)
    word_len_std = statistics.stdev(word_lens) if len(word_lens) > 1 else 0

    # Punctuation ratio per sentence
    punct_counts = [len(re.findall(r'[^\w\s]', s)) for s in sents] if sents else [0]
    punct_per_sent = statistics.mean(punct_counts) if punct_counts else 0

    # Function word frequency (per 1000 words)
    fw_counts = {}
    text_lower = text.lower()
    for fw in INDO_FUNCTION_WORDS:
        count = len(re.findall(r'\b' + re.escape(fw) + r'\b', text_lower))
        fw_counts[f"fw_{fw}"] = count * 1000 / total_words if total_words else 0

    return {
        "sent_len_mean": sent_len_mean,
        "sent_len_std": sent_len_std,
        "word_len_mean": word_len_mean,
        "word_len_std": word_len_std,
        "punct_per_sent": punct_per_sent,
        **fw_counts,
    }

# ──────────────────────────── Load data

def load_texts():
    """Load all M4 texts, return (texts, labels, ids, source_ids).
    source_id = stem filename (m4_id_XXX) — shared between AI and human pair.
    """
    texts, labels, ids, source_ids = [], [], [], []
    for f in sorted((DATA_DIR / "ai").glob("m4_id_*.txt")):
        texts.append(f.read_text(encoding="utf-8"))
        labels.append(1)  # AI
        ids.append(f.stem)
        source_ids.append(f.stem)  # m4_id_001 — same for AI & human pair
    for f in sorted((DATA_DIR / "human").glob("m4_id_*.txt")):
        texts.append(f.read_text(encoding="utf-8"))
        labels.append(0)  # Human
        ids.append(f.stem)
        source_ids.append(f.stem)  # m4_id_001 — same for AI & human pair
    return texts, np.array(labels), ids, np.array(source_ids)

# ──────────────────────────── Rule engine baseline

def rule_engine_baseline(texts, labels):
    """Jalankan rule engine v0 di semua data, return predictions."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from engine.rule_engine import analyze

    preds = []
    scores = []
    for text in texts:
        r = analyze(text)
        preds.append(1 if r["verdict"] == "AI" else 0)
        scores.append(r["score"])

    preds = np.array(preds)
    labels = np.array(labels)

    acc = accuracy_score(labels, preds)
    print(f"\n{'='*60}")
    print("BASELINE: Rule Engine v0 (threshold 0.44)")
    print(f"{'='*60}")
    print(f"Accuracy: {acc:.4f} ({int(acc*len(labels))}/{len(labels)})")
    print(classification_report(labels, preds, target_names=["Human", "AI"], zero_division=0))

    # Per-class stats
    ai_mask = labels == 1
    human_mask = labels == 0
    print(f"AI detected as AI: {preds[ai_mask].sum()}/{ai_mask.sum()} ({preds[ai_mask].sum()/ai_mask.sum()*100:.1f}%)")
    print(f"Human detected as Human: {(preds[human_mask]==0).sum()}/{human_mask.sum()} ({(preds[human_mask]==0).sum()/human_mask.sum()*100:.1f}%)")

    return acc

# ──────────────────────────── Main experiment

def main():
    print("=" * 60)
    print("M4 — Eksperimen Stilometri (Domain Berita)")
    print("=" * 60)

    # Load
    texts, labels, ids, source_ids = load_texts()
    print(f"\nData: {len(texts)} texts ({labels.sum()} AI, {len(labels)-labels.sum()} Human)")
    print(f"Unique source_ids (topik): {len(np.unique(source_ids))}")

    # ── Rule engine baseline (apple-to-apple)
    rule_engine_baseline(texts, labels)

    # ── Fitur statistik permukaan
    print(f"\n{'='*60}")
    print("ML Experiment: Logistic Regression + Stylometric Features")
    print(f"{'='*60}")

    print("\nExtracting features...")
    feature_dicts = [extract_features(t) for t in texts]
    feature_names = list(feature_dicts[0].keys())
    X_stat = np.array([[d[f] for f in feature_names] for d in feature_dicts])
    print(f"Statistical features: {len(feature_names)}")

    # ── TF-IDF char n-gram
    tfidf = TfidfVectorizer(analyzer="char", ngram_range=(2, 3), max_features=200)
    X_tfidf = tfidf.fit_transform(texts)
    tfidf_names = [f"ngram_{n}" for n in range(X_tfidf.shape[1])]
    print(f"TF-IDF char n-gram features: {X_tfidf.shape[1]}")

    # ── Combine
    scaler = StandardScaler()
    X_stat_scaled = scaler.fit_transform(X_stat)
    from scipy.sparse import csr_matrix
    X_combined = hstack([csr_matrix(X_stat_scaled), X_tfidf])
    all_names = feature_names + tfidf_names

    print(f"Total features: {X_combined.shape[1]}")

    pipe = Pipeline([
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
    ])

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision_weighted",
        "recall": "recall_weighted",
        "f1": "f1_weighted",
    }

    # ── 5-Fold Stratified CV (SEBELUM — result lama, MUNGKIN ada leakage)
    print(f"\n{'='*60}")
    print("CV #1: StratifiedKFold (5-fold) — RESULT LAMA, MUNGKIN LEAKED")
    print(f"{'='*60}")
    cv_strat = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results_strat = cross_validate(pipe, X_combined, labels, cv=cv_strat, scoring=scoring, return_train_score=False)

    print(f"\n{'─'*60}")
    print(f"{'Metric':<15} {'Mean':>8} {'Std':>8}")
    print(f"{'─'*60}")
    for metric in ["accuracy", "precision", "recall", "f1"]:
        vals = results_strat[f"test_{metric}"]
        print(f"{metric:<15} {vals.mean():>8.4f} {vals.std():>8.4f}")
    print(f"{'─'*60}")

    # ── 5-Fold GroupKFold by source_id (BARU — fix leakage)
    print(f"\n{'='*60}")
    print("CV #2: GroupKFold (5-fold, group=source_id) — FIX LEAKAGE")
    print("Pasangan human+ai dari topik SAMA masuk fold SAMA.")
    print(f"{'='*60}")
    cv_group = GroupKFold(n_splits=5)
    results_group = cross_validate(pipe, X_combined, labels, cv=cv_group.split(X_combined, labels, source_ids),
                                    scoring=scoring, return_train_score=False)

    print(f"\n{'─'*60}")
    print(f"{'Metric':<15} {'Mean':>8} {'Std':>8}")
    print(f"{'─'*60}")
    for metric in ["accuracy", "precision", "recall", "f1"]:
        vals = results_group[f"test_{metric}"]
        print(f"{metric:<15} {vals.mean():>8.4f} {vals.std():>8.4f}")
    print(f"{'─'*60}")

    # ── Perbandingan
    f1_strat = results_strat["test_f1"].mean()
    f1_group = results_group["test_f1"].mean()
    delta = f1_strat - f1_group

    print(f"\n{'='*60}")
    print("PERBANDINGAN: StratifiedKFold vs GroupKFold")
    print(f"{'='*60}")
    print(f"{'Metrik':<15} {'Stratified':>12} {'GroupKFold':>12} {'Delta':>10}")
    print(f"{'─'*60}")
    for metric in ["accuracy", "precision", "recall", "f1"]:
        s = results_strat[f"test_{metric}"].mean()
        g = results_group[f"test_{metric}"].mean()
        d = s - g
        print(f"{metric:<15} {s:>12.4f} {g:>12.4f} {d:>+10.4f}")
    print(f"{'─'*60}")

    print(f"\nF1 leakage: {f1_strat:.4f} → {f1_group:.4f} (delta: {delta:+.4f})")
    if delta > 0.05:
        print(f"⚠️  LEAKAGE TERKONFIRMASI — F1 turun {delta:.3f} setelah fix.")
        print(f"   Angka yang JUJUR: GroupKFold F1 = {f1_group:.4f}")
    else:
        print(f"✅ Leakage minimal (delta < 0.05)")

    # ── Train on full data for coefficient analysis (tetap sama)
    print(f"\nTraining on full data for coefficient analysis...")
    clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    clf.fit(X_combined, labels)

    full_preds = clf.predict(X_combined)
    full_acc = accuracy_score(labels, full_preds)
    print(f"Full-data accuracy: {full_acc:.4f}")

    # ── Top-15 coefficients
    coefs = clf.coef_[0]
    top_idx = np.argsort(coefs)[::-1]

    print(f"\n{'='*60}")
    print("Top-15 Most Influential Features")
    print("(+ = condong AI, - = condong manusia)")
    print(f"{'='*60}")
    print(f"{'Rank':>4} {'Feature':<25} {'Coef':>10} {'Direction':<10}")
    print(f"{'─'*60}")

    for rank, idx in enumerate(top_idx[:15], 1):
        name = all_names[idx] if idx < len(all_names) else f"feat_{idx}"
        coef = coefs[idx]
        direction = "AI ↑" if coef > 0 else "Human ↑"
        print(f"{rank:>4} {name:<25} {coef:>10.4f} {direction:<10}")

    print(f"\n{'─'*60}")
    print("Bottom-5 (strongest Human indicators):")
    for rank, idx in enumerate(top_idx[-5:][::-1], 1):
        name = all_names[idx] if idx < len(all_names) else f"feat_{idx}"
        coef = coefs[idx]
        print(f"  {rank}. {name:<25} {coef:>10.4f}  Human ↑")

    # ── Summary (pakai GroupKFold sebagai angka utama)
    print(f"\n{'='*60}")
    print("RINGKASAN (pakai GroupKFold — angka JUJUR)")
    print(f"{'='*60}")
    print(f"Stratified F1 (LEAKED): {f1_strat:.4f}")
    print(f"GroupKFold F1 (JUJUR):  {f1_group:.4f}")
    print(f"Full-data accuracy: {full_acc:.4f}")
    if f1_group > 0.7:
        print("→ Model MENJANJIKAN di domain berita (GPT-3.5-turbo)")
        print("  Tapi: baru 1 domain 1 generator — belum generalize.")
    elif f1_group > 0.55:
        print("→ Model LEMAH tapi di atas tebakan — ada sinyal tapi tipis.")
        print("  Perlu feature engineering lebih atau model lebih kuat.")
    else:
        print("→ Model GAK LEBIH BAIK dari tebakan — fitur stilometri gak cukup.")
        print("  Pertimbangkan: data lebih banyak, fitur berbeda, atau pendekatan lain.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
