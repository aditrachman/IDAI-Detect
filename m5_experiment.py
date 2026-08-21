#!/usr/bin/env python3
"""M5 — Eksperimen Generalisasi Lintas Domain + Generator.

3 pengujian:
1. Rule engine v0 (baseline)
2. Model M4 (no retrain) → predict M5 data
3. Model retrained M4+M5 → predict M5 data
"""

import re
import statistics
import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_validate
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack, vstack, csr_matrix

# ──────────────────────────── Paths
M4_DIR = Path(__file__).resolve().parent / "data" / "m4_stylometry"
M5_DIR = Path(__file__).resolve().parent / "data" / "m5_generalization"
M4_SCRIPT = Path(__file__).resolve().parent / "stylometry_experiment.py"

# ──────────────────────────── Function words (SAMA dengan M4)
INDO_FUNCTION_WORDS = [
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan",
    "untuk", "pada", "adalah", "akan", "juga", "sudah", "tidak",
    "dalam", "oleh", "karena", "ada", "lebih",
]

# ──────────────────────────── Feature extraction (SAMA dengan M4)
def split_sentences(text):
    return [s.strip() for s in re.split(r'[.!?…]+', text) if len(s.strip().split()) >= 3]

def extract_features(text):
    sents = split_sentences(text)
    words = text.split()
    total_words = len(words)
    sent_lens = [len(s.split()) for s in sents] if sents else [0]
    word_lens = [len(w) for w in words] if words else [0]
    punct_counts = [len(re.findall(r'[^\w\s]', s)) for s in sents] if sents else [0]
    fw = {}
    text_lower = text.lower()
    for f in INDO_FUNCTION_WORDS:
        c = len(re.findall(r'\b' + re.escape(f) + r'\b', text_lower))
        fw[f"fw_{f}"] = c * 1000 / total_words if total_words else 0
    return {
        "sent_len_mean": statistics.mean(sent_lens),
        "sent_len_std": statistics.stdev(sent_lens) if len(sent_lens) > 1 else 0,
        "word_len_mean": statistics.mean(word_lens),
        "word_len_std": statistics.stdev(word_lens) if len(word_lens) > 1 else 0,
        "punct_per_sent": statistics.mean(punct_counts) if punct_counts else 0,
        **fw,
    }

# ──────────────────────────── Loaders
def load_m4():
    texts, labels, ids, source_ids = [], [], [], []
    for f in sorted((M4_DIR / "ai").glob("m4_id_*.txt")):
        texts.append(f.read_text(encoding="utf-8"))
        labels.append(1); ids.append(f.stem); source_ids.append(f.stem)
    for f in sorted((M4_DIR / "human").glob("m4_id_*.txt")):
        texts.append(f.read_text(encoding="utf-8"))
        labels.append(0); ids.append(f.stem); source_ids.append(f.stem)
    return texts, np.array(labels), ids, np.array(source_ids)

def load_m5():
    texts, labels, ids, source_ids = [], [], [], []
    for f in sorted((M5_DIR / "ai").glob("essay_*.txt")):
        texts.append(f.read_text(encoding="utf-8"))
        labels.append(1); stem = f.stem; ids.append(stem); source_ids.append(stem)
    for f in sorted((M5_DIR / "human").glob("essay_*.txt")):
        texts.append(f.read_text(encoding="utf-8"))
        labels.append(0); stem = f.stem; ids.append(stem); source_ids.append(stem)
    return texts, np.array(labels), ids, np.array(source_ids)

def build_features(texts, tfidf=None, scaler=None, fit=False):
    """Build combined feature matrix."""
    feat_dicts = [extract_features(t) for t in texts]
    feature_names = list(feat_dicts[0].keys())
    X_stat = np.array([[d[f] for f in feature_names] for d in feat_dicts])

    if fit:
        tfidf = TfidfVectorizer(analyzer="char", ngram_range=(2, 3), max_features=200)
        X_tfidf = tfidf.fit_transform(texts)
        scaler = StandardScaler()
        X_stat_scaled = scaler.fit_transform(X_stat)
    else:
        X_tfidf = tfidf.transform(texts)
        X_stat_scaled = scaler.transform(X_stat)

    X_combined = hstack([csr_matrix(X_stat_scaled), X_tfidf])
    return X_combined, tfidf, scaler, feature_names

# ──────────────────────────── Test 1: Rule Engine
def test_rule_engine(texts, labels, name):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from engine.rule_engine import analyze

    preds = [1 if analyze(t)["verdict"] == "AI" else 0 for t in texts]
    preds = np.array(preds)
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average='weighted', zero_division=0)
    print(f"\n{'='*60}")
    print(f"TEST 1: Rule Engine v0 — {name}")
    print(f"{'='*60}")
    print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")
    print(classification_report(labels, preds, target_names=["Human", "AI"], zero_division=0))
    return acc, f1

# ──────────────────────────── Test 2 & 3: ML Model
def test_ml_model(X_train, y_train, X_test, y_test, name, train_label=""):
    pipe = Pipeline([("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average='weighted', zero_division=0)
    print(f"\n{'='*60}")
    print(f"TEST: {name} — {train_label}")
    print(f"{'='*60}")
    print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")
    print(classification_report(y_test, preds, target_names=["Human", "AI"], zero_division=0))

    # Top-10 coefficients
    coefs = pipe.named_steps["clf"].coef_[0]
    top_idx = np.argsort(coefs)[::-1]
    print("Top-10 features:")
    for rank, idx in enumerate(top_idx[:10], 1):
        print(f"  {rank}. feat_{idx}: {coefs[idx]:+.4f}")
    return acc, f1, pipe

# ──────────────────────────── Main
def main():
    print("=" * 60)
    print("M5 — Eksperimen Generalisasi Lintas Domain + Generator")
    print("Domain: esai/opini (bukan berita) | Generator: GPT-oss-120b (bukan GPT-3.5)")
    print("=" * 60)

    # Load data
    m4_texts, m4_labels, m4_ids, m4_groups = load_m4()
    m5_texts, m5_labels, m5_ids, m5_groups = load_m5()
    print(f"\nM4: {len(m4_texts)} texts (berita × GPT-3.5)")
    print(f"M5: {len(m5_texts)} texts (esai × GPT-oss-120b)")

    # Build features
    X_m4, tfidf, scaler, feat_names = build_features(m4_texts, fit=True)
    X_m5, _, _, _ = build_features(m5_texts, tfidf=tfidf, scaler=scaler)

    all_names = feat_names + [f"ngram_{n}" for n in range(200)]

    # ── Test 1: Rule Engine on M5
    test_rule_engine(m5_texts, m5_labels, "M5 (esai, GPT-oss)")

    # ── Test 2: M4 model (no retrain) → predict M5
    print(f"\n{'#'*60}")
    print("# TEST 2: Model M4 (no retrain) → predict M5")
    print(f"{'#'*60}")
    acc2, f1_2, pipe2 = test_ml_model(
        X_m4, m4_labels, X_m5, m5_labels,
        "M5", "Train: M4 (berita×GPT-3.5) | Test: M5 (esai×GPT-oss)"
    )

    # ── Test 3: Retrain M4+M5 → predict M5 (GroupKFold)
    print(f"\n{'#'*60}")
    print("# TEST 3: Retrain M4+M5 → GroupKFold CV on M5")
    print(f"{'#'*60}")
    X_all = vstack([X_m4, X_m5])
    y_all = np.concatenate([m4_labels, m5_labels])
    groups_all = np.concatenate([m4_groups, m5_groups])

    cv = GroupKFold(n_splits=5)
    pipe = Pipeline([("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))])
    results = cross_validate(pipe, X_all, y_all,
                              cv=cv.split(X_all, y_all, groups_all),
                              scoring={"accuracy": "accuracy", "f1": "f1_weighted"},
                              return_train_score=False)

    acc3 = results["test_accuracy"].mean()
    f1_3 = results["test_f1"].mean()
    print(f"\n{'='*60}")
    print(f"TEST 3: Retrain M4+M5 (GroupKFold, n=5)")
    print(f"{'='*60}")
    print(f"Accuracy: {acc3:.4f} ± {results['test_accuracy'].std():.4f}")
    print(f"F1:       {f1_3:.4f} ± {results['test_f1'].std():.4f}")

    # Also train on full M4+M5 and predict M5 specifically
    pipe_full = Pipeline([("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))])
    pipe_full.fit(X_all, y_all)
    preds_m5 = pipe_full.predict(X_m5)
    acc_m5 = accuracy_score(m5_labels, preds_m5)
    f1_m5 = f1_score(m5_labels, preds_m5, average='weighted', zero_division=0)
    print(f"\nFull M4+M5 train → predict M5 only:")
    print(f"Accuracy: {acc_m5:.4f} | F1: {f1_m5:.4f}")
    print(classification_report(m5_labels, preds_m5, target_names=["Human", "AI"], zero_division=0))

    # ── Comparison summary
    print(f"\n{'='*60}")
    print("RINGKASAN PERBANDINGAN")
    print(f"{'='*60}")
    print(f"{'Test':<45} {'Accuracy':>10} {'F1':>10}")
    print(f"{'─'*65}")
    print(f"{'1. Rule Engine v0 → M5':<45} {'—':>10} {'—':>10}")
    print(f"{'2. Model M4 (no retrain) → M5':<45} {acc2:>10.4f} {f1_2:>10.4f}")
    print(f"{'3. Retrain M4+M5 (GroupKFold)':<45} {acc3:>10.4f} {f1_3:>10.4f}")
    print(f"{'3b. Retrain M4+M5 → predict M5':<45} {acc_m5:>10.4f} {f1_m5:>10.4f}")
    print(f"{'─'*65}")

    delta = f1_2 - f1_3
    print(f"\nDelta (M4 no-retrain vs retrained): {delta:+.4f}")
    if delta < -0.1:
        print("⚠️  OVERFITTING DOMAIN: Model M4 anjlok parah di domain baru tanpa retrain.")
    elif delta < -0.05:
        print("⚠️  Moderate domain gap: ada penurunan signifikan tapi masih usable.")
    else:
        print("✅ Generalisasi cukup baik: gap kecil antara no-retrain dan retrained.")

if __name__ == "__main__":
    main()
