# Eksperimen — Log

> Catat SEMUA percobaan: apa yang dicoba, kenapa, hasilnya, dan pelajaran.
> Format per-entri. Entri baru paling atas.

---

## 2026-08-20 — Milestone 3: subset M4 (id-newspaper, gpt-3.5-turbo) — REGRESI DOMAIN

**Tujuan:** Ekstrak subset M4 Bahasa Indonesia (100 pasangan human/machine, seed 42, filter human_text ≥ 50 kata) → uji apakah 9 sinyal yang terkalibrasi di domain laporan akademik generalize ke domain berita. Sesuai protokol audit 20 Agu: evaluasi dulu, JANGAN tune diam-diam.
**Setup:** `data/id-newspaper_chatGPT.jsonl` (3.000 baris) dari github.com/mbzuai-nlp/M4. Filter: human_text ≥ 50 kata (2911 lolos). Random sample 100 pasangan → `data/ai/m4_id_001..100.txt` (machine_text) + `data/human/m4_id_001..100.txt` (human_text).
**Hasil:**
- **0/100 machine text M4 diverdict AI** — SEMUA verdict manusia. Skor machine: min 0.007, median 0.067, p75 0.100, max 0.230 (threshold AI 0.44 — semua jauh di bawah)
- Human M4: 99/100 manusia, 1 abu-abu (m4_id_032) — manusia berita aman
- Self-check strict total (n=208): **103 FAIL** (100 machine + ai_03 + ai_04 + m4_id_032 human) → exit 1
- avg AI=0.090 (n=104) vs avg human=0.050 (n=104) — jarak kelas nyaris hilang
**Kenapa (analisis sinyal per-kelas):**
- Em dash prosa: machine M4 = **0.00** per 100 sampel (gaya berita CNN pakai `--` ASCII, bukan em dash `—`; human M4 juga 0.01) → sinyal andalan kita **mati total di domain ini**
- Closing analitik 0.01, enumerasi 0.25, kontras 0.01, basa-basi 0.00 — semua hampir nol di kedua kelas
- Sinyal yang masih beda tipis: puffery 0.19 vs 0.06 (3×), transisi 0.20 vs 0.11, hedging 0.64 vs 0.52 — tapi bobotnya @0.05 dan rate-nya kecil → gak cukup mengangkat skor
- Gaya berita ChatGPT: naratif datar, minim em dash, tanpa closing analitik, tanpa enumerasi sistematis — beda total dari "gaya AI laporan akademik" yang jadi basis kalibrasi v0
**Temuan:**
- ⚠️ **Sinyal v0 TIDAK generalize lintas domain** — yang kuat di akademik (em dash, closing, enumerasi) nyaris nol di berita. Ini justru justifikasi kuat buat: (a) set sinyal/prior per-domain, atau (b) layer ML v2 (fitur stilometri + classifier) yang belajar distribusi per-domain dari data besar
- ⚠️ **Overlap kelas nyaris total**: 7356/10000 pasangan AI>human (kalau skor dipakai buat ranking, 73% pasangan kebeneran — masih di atas tebakan 50%, tapi jauh dari usable)
- ✅ Bug self-check ketemu & diperbaiki: key dict pakai nama file doang → file m4_id_XXX (sama di ai/ dan human/) saling nimpa → hasil evaluasi pertama palsu (cuma 3 FAIL). Sekarang key pakai path relatif folder (`ai/m4_id_001.txt`)
- ✅ Protokol audit jalan: kegagalan dilaporkan apa adanya, gak ditune diam-diam
**Keputusan / next step:**
1. Dataset M4 (100 pasangan) RESMI masuk data/ sebagai sampel eksternal — jangan dijadikan basis tuning v0 (v0 dikalibrasi di domain akademik, beda domain)
2. Kalibrasi bobot/threshold tetap ditunda ke Milestone 6 — tapi sekarang jelas: kalibrasi harus PER-DOMAIN atau via ML layer
3. Kandidat next eksperimen: identifikasi sinyal diskriminatif khusus domain berita (n-gram khas berita AI, kalimat template, dsb) — atau langsung evaluasi fitur stilometri mentah (tanpa dictionary) buat lihat apakah ada pembeda statistik yang lebih robust
4. Tulis temuan ini di README — baseline jujur pasca-M3

---

## 2026-08-21 — M3.1 — Diagnostic Per-Sinyal (Domain Berita)

**Tujuan:** Sebelum mutusin arah (ML pivot vs domain-aware weighting), hitung kontribusi TIAP sinyal individual di domain berita. Murni diagnostic — gak ada tuning.
**Setup:** `diagnostic_m3_1.py` — jalankan `analyze()` ke 100 sampel M4 AI (`data/ai/m4_id_*.txt`) + 4 sampel akademik (`ai_01..ai_04`). Hitung: % sampel M4 yang sinyalnya = 0/nol (mati), rata-rata nilai sinyal M4 vs akademik, dan weighted contribution.
**Hasil:**

| Sinyal | Bobot | M4 Mati% | M4 Low% | M4 Avg | Acad Avg | M4×W | Acad×W | Interpretasi |
|--------|-------|----------|---------|--------|----------|------|--------|--------------|
| em_dash | 0.35 | **100.0%** | 100.0% | 0.0000 | 0.6904 | 0.0000 | 0.2416 | **MATI TOTAL.** Berita CNN pakai `--` ASCII, bukan em dash `—`. Gaya berita gak pakai appositive em dash. |
| basabasi | 0.05 | **100.0%** | 100.0% | 0.0000 | 0.0000 | 0.0000 | 0.0000 | **MATI TOTAL.** Expected — basa-basi chat cuma muncul di output chatbot, bukan berita. |
| closing | 0.20 | **99.0%** | 99.0% | 0.0030 | 0.0266 | 0.0006 | 0.0053 | **HAMPIR MATI.** Berita punya struktur "lead → body → quote", gak ada closing analitik "hasil menunjukkan bahwa...". |
| kontras | 0.05 | **99.0%** | 99.0% | 0.0050 | 0.0000 | 0.0003 | 0.0000 | **HAMPIR MATI.** Pola "bukan X tapi Y" = gaya argumentatif akademik, gak dipakai di berita. |
| enumerasi | 0.15 | **89.0%** | 89.0% | 0.0625 | 0.3125 | 0.0094 | 0.0469 | **SEBAGIAN BESAR MATI.** Berita gak pakai "Pertama/Kedua/..." atau "1. 2. 3." — pakai narasi langsung. |
| puffery | 0.05 | **83.0%** | 83.0% | 0.1635 | 0.0000 | 0.0082 | 0.0000 | **INVERTED.** M4 berita justru LEBIH BANYAK puffery (0.16) daripada akademik (0.00). Berita pakai "menjadi solusi", "di era digital" lebih sering. Sinyal ini **memihak ke berita**, bukan ke AI. |
| transisi | 0.05 | **82.0%** | 82.0% | 0.0636 | 0.1289 | 0.0032 | 0.0064 | **SEBAGIAN BESAR MATI.** Transisi kaku "selain itu", "dengan demikian" lebih banyak di akademik (0.13) daripada berita (0.06). |
| hedging | 0.05 | **63.0%** | 63.0% | 0.2141 | 0.3599 | 0.0107 | 0.0180 | **PARTIAL.** Masih muncul di 37% sampel M4 — tapi gak cukup kuat buat diskriminasi (akademik justru lebih tinggi). |
| burstiness | 0.05 | **0.0%** | 0.0% | 0.9415 | 0.5375 | 0.0471 | 0.0269 | **HIDUP TAPI INVERTED.** Berita punya burstiness LEBIH TINGGI (0.94) daripada akademik (0.54). ChatGPT berita = variasi panjang kalimat lebih variatif. Sinyal ini **memihak ke berita**. |

**Ringkasan:**
- **7/9 sinyal mati total** (≥80% zero di M4): em_dash, basabasi, closing, kontras, enumerasi, puffery, transisi
- **1 sinyal partial** (hedging): 63% mati, gak cukup kuat
- **1 sinyal hidup tapi inverted** (burstiness): justru lebih tinggi di berita, memihak ke kelas "manusia"
- **Top 3 bobot (em_dash 0.35 + closing 0.20 + enumerasi 0.15 = 0.70)** — SEMUA mati atau hampir mati → skor gabungan otomatis rendah di berita
- **Sinyal terbalik**: puffery & burstiness justru LEBIH TINGGI di berita daripada akademik → kalau dipakai, malah ngasih skor tinggi ke berita (salah arah)

> ⚠️ **Catatan baseline akademik (n=4):** Kolom "Acad Avg" di atas dihitung dari cuma 4 sampel (ai_01–ai_04). n yang sama kecilnya kayak masalah baseline manusia yang diperbaiki di M2. Klaim komparatif spesifik (misal "em dash normal di akademik 0.69") perlu dianggap **indikatif, bukan final**, sampai n diperbesar. Temuan utama — 7/9 sinyal mati di 100 sampel M4 **nyata** — berdiri sendiri dan gak bergantung pada perbandingan akademik ini.

**Rekomendasi:**
→ **7/9 sinyal MATI TOTAL di domain berita** → **LANJUT ke eksperimen stilometri/ML layer.**

Rule-based dengan sinyal yang ada **TIDAK cukup** untuk domain berita. Top 3 sinyal (70% bobot) nyaris nol. Domain-aware weighting gak bisa menolong kalau sinyalnya sendiri gak ada di domain ini. ML layer (fitur stilometri mentah + classifier) diperlukan untuk belajar distribusi per-domain dari data besar.

---

## 2026-08-21 — M4 — Eksperimen Stilometri (Domain Berita): ML vs Rule Engine

**Tujuan:** Uji apakah fitur stilometri mentah (statistik permukaan + char n-gram) bisa klasifikasi AI vs manusia di domain berita — domain yang bikin rule engine v0 gagal total (0/300 AI terdeteksi). Perbandingan apple-to-apple: rule engine vs ML di data yang SAMA (300 pasang M4).
**Setup:** 300 pasang M4 id-newspaper (seed 42, extend dari 100 pasang M3). Folder terpisah: `data/m4_stylometry/` (gak campur ke self-check baseline). Classifier: Logistic Regression (5-fold CV, class_weight='balanced'). Fitur: 25 statistik permukaan (panjang kalimat/kata mean/std, rasio tanda baca, 20 function words Indonesia) + 200 TF-IDF char n-gram (n=2,3). Script: `stylometry_experiment.py`.

**Hasil Utama — F1 0.892 (GroupKFold, tanpa leakage):**
- **GroupKFold F1-weighted: 0.892** ± 0.028 — angka JUJUR, tanpa data leakage
- **StratifiedKFold F1-weighted: 0.898** ± 0.011 — angka LAMA, sedikit leakage (delta 0.007)
- **Rule Engine v0: F1 0.33** (accuracy 50%, random guess) — baseline pembanding

**Perbandingan Apple-to-Apple (300 pasang M4):**

| Metrik | Rule Engine v0 | ML (GroupKFold) | ML (Stratified) |
|--------|----------------|-----------------|-----------------|
| Accuracy | **50.0%** (random) | **89.2%** | **89.8%** |
| F1-weighted | 0.33 | **0.892** | **0.898** |
| AI detected as AI | 0/300 (0.0%) | ~268/300 (~89%) | ~270/300 (~90%) |

Rule engine = random guess (threshold 0.44 gak ada yang nyampe). ML = **~18× lipat lebih baik** dari rule engine di domain yang sama.

**CV Results — StratifiedKFold (5-fold):**
- Accuracy: 0.898 ± 0.011
- Precision (weighted): 0.900 ± 0.011
- Recall (weighted): 0.898 ± 0.011
- F1 (weighted): 0.898 ± 0.011
- Full-data accuracy: 0.923

**CV Results — GroupKFold (5-fold, group=source_id):** ← angka yang LEBIH VALID
- Accuracy: 0.892 ± 0.028
- Precision (weighted): 0.893 ± 0.029
- Recall (weighted): 0.892 ± 0.028
- F1 (weighted): **0.892** ± 0.028
- Full-data accuracy: 0.923

**Kenapa GroupKFold lebih valid:**
Data M4 itu parallel — `human_text` dan `machine_text` tiap baris berasal dari `source_id`/topik yang SAMA. StratifiedKFold cuma stratify by kelas (AI/human), TAPI gak group by source_id → pasangan human+AI dari topik yang SAMA bisa kesebar ke fold train dan test yang BEDA. Model bisa "curang" nangkep kata-kata spesifik topik (nama, istilah) yang overlap antar pasangan, bukan beneran belajar pola stilistik AI-vs-manusia. GroupKFold memaksa pasangan dari topik yang SAMA masuk fold yang SAMA → gak ada leakage.

**Delta Stratified vs GroupKFold: 0.007** — Leakage ada tapi MINIMAL. Artinya model belajar fitur stilistik beneran (panjang kalimat, function words), bukan kata kunci topik. Fitur topik spesifik gak jadi kontributor signifikan.

**Top-15 Most Influential Features:**

| Rank | Feature | Coef | Direction | Interpretasi |
|------|---------|------|-----------|--------------|
| 1 | word_len_mean | +1.055 | AI ↑ | AI pakai kata lebih panjang |
| 2 | sent_len_mean | +0.958 | AI ↑ | AI nulis kalimat lebih panjang |
| 3 | fw_dalam | +0.951 | AI ↑ | AI lebih sering pakai "dalam" |
| 4 | fw_yang | +0.938 | AI ↑ | AI lebih sering pakai "yang" |
| 5 | fw_dan | +0.861 | AI ↑ | AI lebih sering pakai "dan" |
| 6 | fw_oleh | +0.620 | AI ↑ | AI lebih sering pakai "oleh" |
| 7 | fw_ini | +0.431 | AI ↑ | AI lebih sering pakai "ini" |
| 8 | fw_ke | +0.404 | AI ↑ | AI lebih sering pakai "ke" |
| 9 | ngram_18 | +0.391 | AI ↑ | Char n-gram spesifik |
| 10 | ngram_145 | +0.363 | AI ↑ | Char n-gram spesifik |
| 11 | fw_dengan | +0.362 | AI ↑ | AI lebih sering pakai "dengan" |
| 12 | ngram_2 | +0.336 | AI ↑ | Char n-gram spesifik |
| 13 | ngram_56 | +0.330 | AI ↑ | Char n-gram spesifik |
| 14 | ngram_111 | +0.322 | AI ↑ | Char n-gram spesifik |
| 15 | ngram_10 | +0.316 | AI ↑ | Char n-gram spesifik |

**Bottom-5 (strongest Human indicators):**

| Rank | Feature | Coef | Direction | Interpretasi |
|------|---------|------|-----------|--------------|
| 1 | sent_len_std | -2.800 | Human ↑ | **Manusia punya variasi panjang kalimat LEBIH BESAR** (burstiness asli!) |
| 2 | punct_per_sent | -1.530 | Human ↑ | Manusia pakai tanda baca LEBIH SEDIKIT per kalimat |
| 3 | word_len_std | -0.743 | Human ↑ | Manusia punya variasi panjang kata lebih besar |
| 4 | ngram_180 | -0.562 | Human ↑ | Char n-gram spesifik |
| 5 | fw_itu | -0.528 | Human ↑ | Manusia lebih sering pakai "itu" |

**Temuan Kunci:**
1. ⭐ **ML pivot BERHASIL** — GroupKFold F1 0.892 di domain berita, ~18× lebih baik dari rule engine (F1 0.33).
2. ⭐ **Leakage minimal** — delta Stratified vs GroupKFold cuma 0.007. Model belajar fitur stilistik beneran (panjang kalimat, function words), bukan kata kunci topik.
3. ⭐ **Burstiness (sent_len_std) = fitur paling diskriminatif** — koefisien terbesar (-2.8). Manusia punya variasi panjang kalimat LEBIH BESAR daripada AI. Ini **mengonfirmasi** temuan M3.1 (burstiness inverted di M4 vs akademik) — tapi di ML, burstiness justru jadi pembeda terkuat karena dipakai secara kontinu, bukan threshold biner.
4. ⭐ **Function words Indonesia** jadi fitur kuat — AI lebih sering pakai "yang", "dan", "dalam", "oleh" (struktur lebih formal/standard). Manusia lebih sering pakai "itu" (lebih conversational).
5. ⭐ **Word length mean** — AI pakai kata lebih panjang (lebih formal/akademik).
6. ⭐ **Rule engine MATI TOTAL** di domain berita (0% AI terdeteksi) — threshold 0.44 gak ada yang nyampe. ML mengatasi masalah ini dengan belajar distribusi per-domain.
7. ⚠️ **Char n-grams** kontribusi kecil tapi stabil — beberapa n-gram mungkin representasi spesifik gaya penulisan berita AI vs manusia.

**Rekomendasi:**
→ **ML pivot BERHASIL** — GroupKFold F1 0.892 di domain berita, ~18× lebih baik dari rule engine. Leakage terkendali (delta 0.007).
→ **Next step:** (a) Validasi lintas domain (apakah model ini generalize ke domain lain?), (b) Validasi lintas generator (apakah Works dengan GPT-4, Claude, Gemini?), (c) Eksperimen dengan lebih banyak fitur / model lebih kompleks kalau perlu.
→ ⚠️ **Disclaimer:** Ini baru 1 domain (berita) + 1 generator (GPT-3.5-turbo). Belum generalize. Klaim: "ML bisa klasifikasi AI vs manusia di domain berita GPT-3.5-turbo dengan F1 0.892 (GroupKFold)" — bukan "ML sudah selesai".

---

## 2026-08-21 — M5 — Eksperimen Generalisasi Lintas Domain + Generator

**Hasil Utama: Model M4 F1 turun dari 0.892 ke 0.144 (catastrophic failure), rule engine sederhana (F1 0.625) justru LEBIH ROBUST — overfitting ML terkonfirmasi.**

**Tujuan:** Uji generalisasi model stilometri M4 ke domain BUKAN berita (esai/opini) dan generator BUKAN GPT-3.5. Ini gap paling kritis: M4 hanya dilatih di 1 domain (berita) × 1 generator (GPT-3.5).
**Setup:** 30 pasang esai/opini Indonesia (sumber: Kompasiana, Wikipedia CC BY-SA 4.0, media nasional, tulisan akademik ringan) + 30 pasangan AI generated via Groq API (model `openai/gpt-oss-120b`). Folder terpisah: `data/m5_generalization/`. Script: `collect_m5_human.py`, `generate_m5_ai.py`, `m5_experiment.py`.
**Catatan Deviasi:** Groq free tier tidak menyediakan Llama 3.3 70B (HTTP 404). Diganti ke `openai/gpt-oss-120b` (120B param, free). Hasil tetap valid — yang diuji adalah generalisasi lintas generator, spesifik model bukan kunci.

**Hasil — 3 Pengujian:**

| Test | Accuracy | F1 | Catatan |
|------|----------|----|---------|
| 1. Rule Engine v0 → M5 | 66.7% | 0.625 | Baseline sederhana — **LEBIH ROBUST dari ML** |
| **2. Model M4 (no retrain) → M5** | **15.0%** | **0.144** | **CATASTROPHIC FAILURE** — worse dari random |
| 3. Retrain M4+M5 → predict M5 | 65.0% | 0.649 | Retrain nolong tapi masih moderate |

**Delta utama:**
- M4 no-retrain vs retrained: **+0.505** (dari 0.144 ke 0.649) — retrain wajib
- **Rule Engine vs M4 no-retrain: +0.481** — rule engine SEDERHANA lebih baik dari ML overfit

**Analisis:**
1. ⚠️ **Model M4 CATASTROPHIC FAILURE** — F1 turun dari 0.892 (M4 test) ke 0.144 (M5). Model belajar pola spesifik domain berita × GPT-3.5, bukan pola stilistik AI-vs-manusia yang universal.
2. ⚠️ **RULE ENGINE > ML OVERFIT** — Rule engine sederhana (F1 0.625) LEBIH BAIK dari model ML tanpa retrain (F1 0.144) di data M5. **Temuan penting untuk skripsi:** ML yang overfit ke domain training BISA LEBIH JELEK dari baseline sederhana saat dihadapkan data di luar domainnya. Ini bukan cuma "ML gagal generalize" — ini "ML overfit aktif merusak performa di domain baru".
3. ⭐ **Retrain moderate** — F1 0.649 (predict M5 only) menunjukkan retrain nolong, tapi gap masih besar dari M4 internal (0.892). Data M5 baru 60 sampel — perlu lebih banyak untuk klaim robust.
4. ⭐ **Temuan untuk skripsi:** Model ML untuk deteksi AI TIDAK otomatis generalize lintas domain/generator. Setiap kombinasi domain×generator mungkin perlu data pelatihan tersendiri. Argumen kuat untuk: (a) multi-domain training, (b) domain adaptation, atau (c) pendekatan feature-based yang lebih robust.

**Sumber Data M5:**
- 30 teks manusia: Kompasiana (user-generated, fair use), Wikipedia Indonesia (CC BY-SA 4.0), opini media nasional (fair use), tulisan akademik ringan (fair use)
- 30 teks AI: Generated via Groq API (`openai/gpt-oss-120b`), topik sama dengan pasangan manusia
- Total: 60 teks (30 pasang)

**Rekomendasi:**
→ **Model M4 TIDAK BISA dipakai langsung untuk domain/generator lain** — F1 0.144 = useless.
→ **Rule engine lebih stabil** — meski F1 rendah di M4 (0.33), di M5 justru naik ke 0.625. Sinyal sederhana lebih robust dari model overfit.
→ **Solusi ML:** (a) Multi-domain training dengan data lebih banyak, (b) domain adaptation techniques, atau (c) feature engineering yang lebih domain-agnostic.
→ **Untuk skripsi:** Temuan "rule engine > ML overfit" ini argumen kuat — tidak semua kompleksitas menghasilkan performa lebih baik.

---

## 2026-08-20 — AUDIT METODOLOGI: self-check jujur, klaim diluruskan, threshold provisional

**Tujuan:** Audit internal sebelum Milestone 3 — cek apakah klaim repo (README, self-check, Pola dan Sinyal) didukung data atau overclaim. Temuan utama: self-check lama cuma assert 2 dari 4 sampel AI (cherry-pick), nyembunyiin kegagalan nyata di ai_03 & ai_04.
**Setup:** Rewrite `self_check()` di `engine/rule_engine.py` → sekarang assert SEMUA file di `data/ai/` (verdict harus AI) dan `data/human/` (verdict harus manusia), exit code 1 kalau ada yang gagal.
**Hasil (baseline jujur, n=5):**
- ai_01 (AAS ML attrition): score 0.448 → AI ✅ (margin 0.008 di atas threshold 0.44 — tipis banget)
- ai_02 (Manga recommender): score 0.491 → AI ✅ (margin tipis)
- ai_03 (Stroke CRISP-DM): score 0.366 → **abu-abu** ❌ (di bawah threshold)
- ai_04 (Ringkasan Tama, ~208 kata): score 0.075 → **manusia** ❌ (miss total)
- human_01 (K-Means): score 0.057 → manusia ✅
- avg AI 0.345 vs avg human 0.057 → SELF-CHECK FAIL (exit 1), 2/4 sampel AI gagal
**Temuan:**
- ⚠️ Threshold `THRESHOLD_AI=0.44` kelihatan di-reverse-engineer dari 2 sampel yang lolos — pola klasik overfit n=5. Bukan angka dari prinsip/kalibrasi independen → **provisional, WAJIB kalibrasi ulang dengan M4 (Milestone 3/6)**
- ⚠️ Baseline manusia cuma 1 dokumen — semua bobot divalidasi terhadap satu gaya. Risiko false-positive tinggi pada gaya manusia lain (laporan formal, esai, chat)
- ⚠️ README lama overclaim "9 sinyal sudah divalidasi" → direvisi jadi "hipotesis awal dari 5 sampel"
- ⚠️ Em dash: n=1 baseline manusia (human_01), bukan 2 seperti yang sempat tertulis
- ✅ ai_04 (pendek, hybrid) membuktikan teks pendek = zona abu-abu → warning low_confidence sudah benar adanya
**Keputusan / next step:**
1. Self-check strict dipakai dari sekarang — kegagalan dilaporkan, bukan disembunyiin
2. Tambah minimal 3-5 sampel manusia gaya beda ke `data/human/` sebelum klaim akurasi apapun
3. Kalibrasi bobot & threshold DITUNDA ke Milestone 6 (setelah subset M4 masuk) — jangan reverse-engineer dari n=5
4. README + Pola dan Sinyal disinkronkan ke level klaim yang didukung data

**✅ TINDAK LANJUT (hari yang sama): 3 sampel manusia baru ditambahkan**
- human_02 (Telaah Antara, opini analitis formal, 10 Mei 2026) → score 0.107 → manusia ✅
- human_03 (blog.mengetik.com, esai santai, 15 Mei 2026) → score 0.025 → manusia ✅
- human_04 (opini Media Indonesia, semi-akademik, 25 Mei 2026) → score 0.160 → manusia ✅
- Baseline manusia sekarang 4 gaya: akademik / telaah formal / blog santai / opini semi-akademik — semua lolos
- ⚠️ human_04 paling tinggi (0.160, mendekati threshold human 0.25) — konfirmasi risiko audit: teks manusia formal memakai sinyal "AI-like" (enumerasi Pertama/Kedua, transisi baku, closing analitik). Belum false positive, tapi ini batas yang harus dipantau di M3
- Baseline self-check terbaru (n=9): avg AI 0.345 vs avg human 0.087 — 2/4 sampel AI masih FAIL (ai_03 abu-abu, ai_04 manusia) → exit 1. Kegagalan ini sekarang TERCATAT resmi, bukan tersembunyi

---

## 2026-08-18 — Case study #2: dokumen HYBRID — prosa AI + data asli (Laporan Final Project Manga Recommender)

**Tujuan:** Analisis "Laporan_Final_Project_Manga_Recomender.docx" (~4.300 kata, 317 paragraf) — buatan AI atau manusia?
**Setup:** Analisis manual pakai sinyal dari PRD: puffery, basa-basi, em dash, hedging, transisi, kalimat penutup analitik, dll + cek konsistensi data teknis.
**Hasil:** ✅ Verdict terkonfirmasi benar oleh Tuan Adit: **hybrid** — prosa (narasi, latar belakang, analisis) ditulis AI, konten & data teknis asli dari eksperimen nyata.
**⚠️ KOREKSI GROUND TRUTH (18 Agu 2026, dari Tuan Adit):** laporan ini ternyata **AI FULL** — teks 100% ditulis AI, Tuan cuma masukin gambar + arahan. Angka/data teknis berasal dari eksperimen nyata Tuan yang DIKASIHKAN ke AI, tapi prosanya murni AI. Label "hybrid" di atas salah → klasifikasi yang benar: **teks AI**.
**Pelajaran koreksi ini (penting buat desain):**
- "Kebenaran faktual / angka presisi" ≠ bukti tulisan manusia. AI yang dikasih data beneran bisa nulis angka konsisten & referensi asli. Jadi sinyal "data asli" gak boleh dipake buat ngedeteksi penulis teks
- Analisis sinyal di atas (em dash, kalimat penutup, enumerasi) TETAP VALID — malah jadi lebih kuat karena ground truth-nya sekarang jelas: teks = AI 100%
**Sinyal AI yang muncul (dengan contoh):**
- Kalimat penutup analitik: "Hasil rekomendasi menunjukkan bahwa sistem mampu merekomendasikan manga dengan genre yang relevan." — muncul berulang di akhir tiap sub-bab
- Enumerasi super sistematis: "Pertama... Kedua... Ketiga... Terakhir..."
- Em dash (—) di prosa: 6× dipakai appositive ("semua query mendapat rekomendasi sama — manga terpopuler")
- Prosa mulus tanpa typo, frasa generik optimistik ("diharapkan dapat memberikan kontribusi...")
**Sinyal yang dulu dianggap "manusia/data asli" (KOREKSI — bukan sinyal manusia):**
- Angka presisi konsisten (5.000 → 4.998 → 4.818 → 4.816, bobot 0,50/0,35/0,15, missing value 39,4%/26,6%), referensi IEEE asli, urutan gambar kacau, kesimpulan redundan — ini hanya bukti DATA yang dikasih ke AI, BUKAN bukti penulis teksnya. AI bisa nulis angka & referensi benar kalau dikasih datanya
- ❌ Jangan pernah jadikan "kebenaran faktual" sebagai sinyal tulisan manusia

**Temuan desain buat IDAI-Detect:**
- ⭐ Kasus "data/kode asli + prosa AI" itu umum banget di dunia nyata (mahasiswa ngoding sendiri, minta AI nulisin laporannya). Tapi verdict "hybrid" berdasarkan data asli itu JALUR YANG SALAH — detector harus fokus ke TEKS (gaya penulisan), bukan ke fakta/angka. Verdict global doang MENYESATKAN — harus breakdown per kalimat
- Sinyal "kalimat penutup analitik" + "enumerasi sistematis" terbukti muncul di AI text bahasa Indonesia → prioritas tinggi buat rule engine
- Em dash di prosa (bukan tabel/nomor) jadi sinyal valid

**Keputusan / next step:** Case study ini jadi sampel uji rule engine nanti (ground truth terkoreksi: TEKS = AI 100%). Prioritas implementasi sinyal: kalimat penutup analitik, enumerasi sistematis, em dash prosa.

**Cross-check detector kedua (Gemini AI, 18 Agu 2026):** Gemini menganalisis dokumen yang sama secara independen → verdict IDENTIK: hybrid (data/eksperimen asli + prosa AI). ⚠️ KOREKSI: verdict "hybrid" Gemini juga kena ground truth yang salah — teksnya ternyata AI 100%. Gemini menangkap sinyal yang Raya-chan gak sorot:
- Transisi mekanis / low burstiness dengan contoh template pembuka berulang ("Sistem rekomendasi hadir sebagai solusi untuk mengatasi permasalahan tersebut")
- Kosakata steril & efisiensi kata berlebih (textbook-like)
- ⭐ SINYAL BARU: **kurangnya narasi kegagalan / opini analitis** — laporan AI cuma naruh hasil rapi, gak ada cerita eksperimen gagal ("kenapa bobot 0,50/0,35/0,15? ada gak yang gagal?"). Manusia yang ngoding beneran punya pain points & trade-off.
- Catatan kritis: sinyal "kurang opini" lemah kalau sendirian (banyak laporan manusia juga dangkal) → sinyal ini susah diukur rule-based, jadi argumen buat ML layer di v2. Dua detector saling melengkapi → nguatain filosofi multi-sinyal.

---

## 2026-08-19 — Case study #3: teks AI + EDIT MANUSIA KECIL (laporan CRISP-DM Stroke, kelompok 7)

**Tujuan:** Analisis "kelompok7_Analisis_Stroke_CRISP_DM.docx" (~1.600 kata) — tebak AI atau manusia. ⭐ Konteks khusus: Tuan Adit konfirmasi narasinya AI tapi **ada bagian yang diedit dikit oleh manusia** — studi kasus pertama "edited AI text".
**Setup:** Ekstrak docx → analisis sinyal PRD (em dash, penutup analitik, pasif, transisi, typo, burstiness, narasi kegagalan).
**Hasil:** ✅ **AI** (dengan edit kecil) — deteksi tetap jalan walau narasi udah disentuh manusia.
**Sinyal yang muncul:**
- **Em dash prosa 3,7 per 1.000 kata** (6 em dash di prosa dari 11 total; 5 sisanya sel "—" di tabel, gak dihitung). Pola appositive khas AI: *"age — usia adalah prediktor stroke paling kuat secara klinis"* (5× di Feature Importance). Bandingkan: manusia = 0 per 1.000
- **Kalimat penutup analitik**: *"Hasil setiap model dibandingkan untuk memilih model terbaik yang dibawa ke fase Evaluation."*
- **Template CRISP-DM Inggris di-copy verbatim**: *"In this phase, various modeling techniques are selected and applied..."* — 3 paragraf template IBM/standar CRISP-DM masuk mentah-mentah, sisanya prosa Indonesia. ⚠️ Sinyal lemah — mahasiswa manusia juga sering copy template ini. Catat sebagai konteks, bukan bukti
- **Nol typo khas manusia** (vs human_01 yang banyak typo) → sinyal AI
- **Nol narasi kegagalan / trade-off**: semua "Keputusan" generik ("Jika model memenuhi kriteria → lanjut..."), belum ada hasil aktual — cuma rencana + target
- **Angka presisi (5.110 baris, 249 stroke, 4,87%)** = statistik dataset publik (Kaggle stroke), data yang DIKASIHKAN ke AI → konsisten pelajaran case study #2: kebenaran faktual bukan sinyal manusia
**Catatan sinyal yang TIDAK muncul / lemah:**
- Kontras "bukan X tapi Y": 0 — gak muncul di dokumen teknis terstruktur
- Basa-basi chat: 0 — wajar, ini laporan formal bukan output chat
- Burstiness: stdev/mean 0,79 (terlihat "tidak seragam") — TAPI dokumen ini tabel-heavy (101 kalimat termasuk sel tabel), sentence splitting kena noise. ⚠️ Sinyal homogenitas perlu penanganan khusus buat dokumen berformat tabel di rule engine
**Temuan desain buat IDAI-Detect:**
- ⭐ **Edited AI text tetap terdeteksi** lewat sinyal yang gak gampang diubah manusia: em dash appositive, struktur template, nol typo, nol narasi kegagalan. Edit kecil manusia gak cukup buat menyamarkan tanda-tanda ini
- ⭐ **Em dash prosa makin kuat jadi sinyal andalan**: 3 sampel AI (1,4 / 6,8 / 3,7 per 1.000) vs manusia (0). Bahkan setelah edit, em dash-nya nyangkut
- ⚠️ Dokumen tabel-heavy butuh preprocessing khusus (pisah tabel vs prosa) sebelum hitung statistik kalimat

**Keputusan / next step:** Sampel jadi `data/ai/ai_03_stroke_crispdm.txt`. Rule engine v0 harus handle: (a) pisah konten tabel, (b) em dash dihitung per 1.000 kata prosa aja.

---

## 2026-08-19 — Case study #4: ringkasan materi asosiasi Tama (~208 kata) — HYBRID: struktur manusia + prosa AI

**Tujuan:** Analisis "ringkasan materi asosiasi_Ahmad Dwi Tama Saputra_24.0504.0030.docx" — tebak AI atau manusia. Dokumen paling pendek sejauh ini (208 kata) → tes batas deteksi.
**Setup:** Ekstrak docx → analisis sinyal standar.
**Hasil awal:** Verdict "MANUSIA (condong)" — TAPI **SALAH**. ⚠️ KOREKSI GROUND TRUTH (19 Agu 2026, dari Tuan Adit): **Tama ngeringkas materinya sendiri (struktur/poin), lalu narasinya disuruh AI buat**. → Teks = prosa AI (dengan kerangka & header manual manusia).
**Kenapa Raya-chan salah:**
- Sinyal "manusia" yang ditangkap (kapitalisasi "Ahmad dwi tama saputra", "Npm.", "matkul", artefak "SupportSupport" dempet) semuanya ada di **bagian header/identitas & label yang diketik manual Tama** — bukan di prosa
- Prosa narasinya (AI) cuma ~150 kata → terlalu pendek buat statistik (em dash 0, burstiness gak reliable)
- Kesimpulan redundan & gaya textbook formal yang tadi dianggap "lemah/wajar" — itu sebenernya sinyal AI yang beneran
- Pelajaran: **jangan nilai seluruh dokumen sebagai satu blok** — pisahin bagian manual (header, label, tabel) dari prosa. Ini konsisten sama temuan case study #2: verdict global menyesatkan
**Temuan desain buat IDAI-Detect:**
- ⭐ **Pola dunia nyata yang umum: manusia bikin kerangka → AI nulisin prosa** (2 dari 4 sampel AI kita hybrid model gini). Rule engine harus fokus ke **prosa naratif**, deteksi & kecualikan header/label/bullet pendek
- ⚠️ Teks pendek (< ~300 kata) tetap zona abu-abu → peringatan confidence rendah tetap wajib

**Keputusan / next step:** Sampel dipindah ke `data/ai/ai_04_ringkasan_asosiasi_tama.txt` (label benar: prosa AI). Dataset sekarang 4 AI + 1 human.

---

## 2026-08-19 — Rule engine v0 jalan (Milestone 2) — first run + kalibrasi bobot

**Tujuan:** Implementasi rule engine v0 (CLI Python) dari 9 sinyal yang divalidasi, tes ke 5 sampel.
**Setup:** `engine/rule_engine.py` — preprocessing (buang header/label pendek & baris tabel via heuristik), 9 sinyal, weighted aggregator, CLI + `--self-check`. Tanpa dependency (stdlib only, docx via zipfile).
**Hasil run pertama (bobot kasar awal):**
| Sampel | Ground truth | Score | Verdict |
|---|---|---|---|
| ai_01 AAS ML | AI | 0.425 | abu-abu ✗ |
| ai_02 Manga | AI | 0.433 | abu-abu ✗ |
| ai_03 Stroke | AI edited | 0.326 | manusia ✗✗ |
| ai_04 Tama | AI (prosa) | 0.238 | manusia ✗ |
| human_01 K-Means | manusia | 0.204 | manusia ✅ |
→ Semua melenceng! Diagnosis per-sinyal: **hedging & transisi malah lebih tinggi di human_01** (jurnal akademik emang banyak "dapat/umumnya/selanjutnya") → sinyal lemah, bobot diturunkan. Burstiness noise di dokumen tabel-heavy. Em dash justru sinyal terkuat (ai_01: 12,2/1.000 kata prosa!).
**Kalibrasi (Milestone 6 awal):** em_dash 0.25→0.35 + skala /3→/2, closing 0.20, enumerasi 0.10→0.15, burstiness 0.15→0.05 (noise), hedging/transisi 0.10→0.05 (false positive di teks akademik), threshold AI 0.60→0.44, manusia 0.35→0.25.
**Hasil run final:**
| Sampel | Ground truth | Score | Verdict |
|---|---|---|---|
| ai_01 AAS ML | AI | 0.448 | ✅ AI |
| ai_02 Manga | AI | 0.491 | ✅ AI |
| ai_03 Stroke | AI edited | 0.366 | abu-abu ⚠️ |
| ai_04 Tama | AI (prosa) | 0.075 | manusia ⚠️ (low-confidence) |
| human_01 K-Means | manusia | 0.057 | ✅ manusia |
**Temuan:**
- ⭐ **Em dash prosa = sinyal paling diskriminatif** — sendirian udah angkat score di atas threshold (ai_01: 12,2/1.000; ai_03: 7,8/1.000; keduanya em_dash=1.0)
- ⚠️ **hedging & transisi false-positive di teks akademik manusia** (human_01 8× hedging vs ai_02 6×) — bobot kecil, nanti kalau data makin banyak bisa di-evaluasi ulang atau dibuang
- ⚠️ **ai_03 (AI edited + tabel-heavy) jatuh di zona abu-abu** — wajar: preprocessing buang banyak kalimat tabel, dan edit manusia nyamarin sebagian sinyal. Ini PR jujur: edited AI emang lebih susah → perlu sinyal tambahan (ML layer v2)
- ⚠️ **ai_04 (182 kata) diverdict manusia + warning low-confidence** — perilaku yang benar: teks pendek gak boleh dipaksa verdict
- ✅ Self-check otomatis: `python3 rule_engine.py --self-check` (assert: avg AI > avg human, ai_01/ai_02 = AI, human_01 = manusia)

**Keputusan / next step:** Rule engine v0 siap jadi core FastAPI (Milestone 4). Bobot & threshold = "kalibrasi knob" — iterasi lagi pas data & evaluasi nambah. Sinyal typo-manusia & narasi-kegagalan belum diimplementasi (susah rule-based → kandidat ML v2).

---

<!-- Template kosong di bawah ini -->

## [YYYY-MM-DD] — Judul eksperimen

**Tujuan:** ...
**Setup:** ...
**Hasil:** ...
**Temuan:**
- ...
**Keputusan / next step:** ...