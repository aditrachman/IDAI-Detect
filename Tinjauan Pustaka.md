# Tinjauan Pustaka: Posisi IDAI-Detect dibanding Riset yang Sudah Ada

> Rangkuman posisi IDAI-Detect setelah baca detail related work. Fokus: apa yang beda/unik, apa kelemahan yang perlu diakui.

---

## 1. Peta Riset Deteksi Teks AI (Indonesia)

| Riset | Metode | Dataset | Akurasi/F1 | Tahun | Catatan |
|-------|--------|---------|------------|-------|---------|
| **BiLSTM (Alif et al.)** | Bi-LSTM + Keras Embedding (64d) | 5.008 (jurnalistik + SINTA 4, ChatGPT + Gemini) | 78.24% acc, **93.77% manusia**, **62.62% AI akademik** | 2026 | Black-box, CRISP-DM, deployed Streamlit |
| **IndoBERT hoax (Nur et al.)** | IndoBERT + XAI | TurnBackHoax (1.116) + Mendeley (600) | 90–97% (hoax detection, bukan AI-text) | 2025 | SLR, hoax ≠ AI-text detection |
| **Topic-split (Alikhanov et al.)** | LR + BiLSTM + DistilBERT | HC3 + DAIGT v2 (124K) | LR 82.87%, BiLSTM 88.86%, DistilBERT 88.11% | 2026 | **Validasi independen** topic-based split → GroupKFold kita benar |
| **Cross-lingual (Agrahari et al.)** | MLDet (cross-lingual adaptation) | Multilingual benchmark | F1 0.707 macro | 2025 | Black-box, cross-lingual tapi gak interpretable |
| **IDAI-Detect (kita)** | Rule-based + LR stylometry (25 fitur + 200 TF-IDF n-gram) | M4 (300 pasang) + M5 (60 pasang) | **M4: F1 0.892**, **M5: F1 0.144 (no retrain)**, **0.649 (retrain)** | 2026 | Hybrid, explainable, tapi generalisasi lemah |

---

## 2. Apa yang BEDA/UNIK dari IDAI-Detect

### a) Pendekatan Hybrid (Rule-Based + ML)
- Riset lain: mayoritas pakai deep learning end-to-end (BiLSTM, BERT, DistilBERT) → black-box
- **Kita:** rule-based (9 sinyal linguistik) + ML (Logistic Regression stylometry) → bisa explain KENAPA teks dicurigai
- **Nilai tambah:** explainability. User bisa lihat sinyal mana yang nyala (burstiness, em dash, dll), bukan cuma "skor 0.87 → AI"

### b) Fokus pada Bahasa Indonesia
- Riset internasional (M4, RAID, HC3) mayoritas English-centric
- **Kita:** spesifik Indonesia, dengan fitur linguistik yang relevan (function words Indonesia: "yang", "dan", "di", dll)
- Tapi: BiLSTM Alif et al. juga Indonesia → kita gak sendirian di niche ini

### c) Transparansi Metodologi
- Banyak riset gak publish detail split data → susah reproduksi
- **Kita:** Eksperimen.md lengkap dari M1–M5, GroupKFold by source_id, data split documented
- **Validasi independen:** Alikhanov et al. (2026) pakai topic-based split → prinsip sama dengan GroupKFold kita

---

## 3. Kelemahan yang PERLU DIAKUI

### a) Generalisasi LEMAH (temuan M5)
- **Fakta:** Model M4 (F1 0.892 di berita) → F1 0.144 di esai (catastrophic failure)
- **Bandingin:** BiLSTM Alif et al. juga gagal di AI akademik (62.62% vs 93.77% manusia) — pola kegagalan MIRIP, beda domain = beda performa
- **Kesimpulan:** Overfitting domain bukan cuma masalah kita — ini masalah umum di deteksi teks AI

### b) Skala Data KECIL
- **Kita:** 300 pasang (M4) + 60 pasang (M5) = total 660 teks
- **BiLSTM:** 5.008 teks
- **Topic-split:** 124K teks (HC3 + DAIGT v2)
- **IndoBERT hoax:** 6.120 teks
- **Implikasi:** Klaim kita terbatas — belum robust buat generalisasi luas

### c) Akurasi di Bawah SOTA
- **Kita:** F1 0.892 (M4, in-domain) vs BiLSTM 88.86% acc (topic-split, harder evaluation)
- **IndoBERT hoax:** 92–97% (tapi task berbeda — hoax, bukan AI-text)
- **DistilBERT:** 88.11% + ROC-AUC 0.96
- **Kesimpulan:** Kita masih di bawah deep learning SOTA, tapi dengan keunggulan explainability

### d) Rule Engine GAK CUKUP
- **Fakta:** Rule engine F1 0.33 di M4 (random guess), 0.625 di M5 (lebih stabil tapi tetap rendah)
- **Kesimpulan:** Rule-based alone gak solusi — perlu ML, tapi ML perlu data lebih banyak

---

## 4. Celah Riset yang Bisa Diisi

| Celah | Status Kita | Peluang |
|-------|-------------|---------|
| **Explainability** | ✅ Punya (rule-based + per-signal breakdown) | Kembangkan: SHAP/LIME untuk ML features |
| **Cross-domain generalization** | ❌ Gagal (M5 F1 0.144) | Multi-domain training, domain adaptation |
| **Hybrid rule+ML** | 🟡 Belum eksperimen | Kombinasi skor rule + ML → potensi lebih stabil |
| **Bahasa Indonesia** | ✅ Fokus | Perluas ke more domains (akademik, media sosial, dll) |
| **Dataset public** | 🟡 M4 public, M5 manual collect | Manfaatkan TurnBackHoax + Mendeley untuk M6 |

---

## 5. Rekomendasi buat Skripsi

1. **Akui kelemahan jujur:** generalisasi lemah, data kecil, di bawah SOTA
2. **Highlight keunggulan:** explainability, hybrid approach, transparansi metodologi
3. **Positioning:** "Bukan yang paling akurat, tapi yang paling interpretable dan practical untuk user Indonesia"
4. **Citation wajib:** M4 (Wang et al. 2024), BiLSTM (Alif et al. 2026), topic-split (Alikhanov et al. 2026)
5. **Data governance:** catat sumber data jelas (M4 CC BY-SA, TurnBackHoax public, Mendeley CC BY 4.0)

---

## 6. Status Baca Paper

| Paper | Status | Catatan |
|-------|--------|---------|
| M4 (Wang et al. 2024) | ✅ [x] | Dataset utama, sudah dipakai |
| BiLSTM (Alif et al. 2026) | ✅ [x] | Detail: 78.24% acc, 93.77% manusia, 62.62% AI akademik |
| Topic-split (Alikhanov et al. 2026) | ✅ [x] | Validasi GroupKFold: 88.86% BiLSTM |
| Cross-lingual (Agrahari et al. 2025) | ✅ [x] | F1 0.707, cross-lingual adaptation |
| Systematic review hoax (Nur et al. 2025) | ✅ [x] | Dataset TurnBackHoax + Mendeley |
| Defactify (Roy et al. 2026) | ⬜ [ ] | Belum baca detail |
| RAID Benchmark (2024) | ⬜ [ ] | Belum baca detail |
