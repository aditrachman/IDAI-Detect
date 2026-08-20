# Referensi

> Kumpulan paper, artikel, dan sumber pola. Tambahin link + 1-2 baris ringkasan kenapa relevan.

## Pola & heuristik (dari PRD)

- [ ] **Wikipedia: Signs of AI Writing (WikiProject AI Cleanup)** — sumber pola awal 9 kategori
- [ ] **Freeburg, E.M. (2026). *The Last Fingerprint: How Markdown Training Shapes LLM Prose*** — dasar teori em dash / markdown artifacts
- [ ] **VERMILLION framework** — linguistic markers of AI-generated communication
- [ ] **Studi keterbatasan manusia mendeteksi teks AI (Indiana Capital Chronicle, 2025)** — justifikasi kenapa butuh tool

## Related work (WAJIB baca + citasi)

- [ ] **Implementation of the BiLSTM Model for Detecting AI-Generated Indonesian Text**, Jurnal Teknologi Informatika dan Komputer (2026) — ⭐ riset Indonesia paling relevan, pembanding utama. Bi-LSTM + CRISP-DM, 5.008 sampel (manusia: scraping jurnalistik + SINTA 4; AI: parafrase ChatGPT & Gemini). Positioning kita: rule-based + explainability / hybrid, bukan black-box
- [x] **Wang, Y. et al. (2024). *M4: Multi-Generator, Multi-Domain, and Multi-Lingual Black-Box Machine-Generated Text Detection*. EACL 2024.** — ⭐ sumber dataset utama (github.com/mbzuai-nlp/M4); subset Indonesia (id-newspaper, gpt-3.5-turbo) dipakai di Milestone 3. Best Resource Paper Award EACL 2024
- [ ] **Roy, R. et al. (2026). *A Comprehensive Dataset for Human vs. AI Generated Text Detection* (Defactify)** — pembanding metodologi, baseline akurasi 58.35%
- [ ] **RAID Benchmark (2024)** — 7 bahasa termasuk Indonesia, multi-domain multi-LLM

## Dataset

- [x] **Wang, Y. et al. (2024). *M4: Multi-Generator, Multi-Domain, and Multi-Lingual Black-Box Machine-Generated Text Detection*. EACL 2024 (Best Resource Paper Award).** github.com/mbzuai-nlp/M4 — ⭐ dataset utama; subset Indonesia dipakai di Milestone 3: `data/id-newspaper_chatGPT.jsonl` (domain berita, source id_newspapers_2018, generator gpt-3.5-turbo, 3.000 baris parallel human/machine). Citation request eksplisit di README repo mereka — WAJIB dicitasi di skripsi/paper.
- [ ] **AI-TEXT-DETECTION-PILE** — huggingface.co (artem9k) — 1.39M sampel, baseline/benchmark
- [ ] **Defactify Text Dataset** — huggingface.co/datasets/Rajarshi-Roy-research/Defactify_Text_Dataset — 73k sampel NYT
- [ ] **HC3** — HuggingFace — referensi metodologi (Inggris/Cina)

## Buat dicari (masih open)

- Isi & metode eksak paper BiLSTM 2026 — harus dibaca detail buat cari celah positioning yang lebih tajam
- Paper M4 versi lengkap (metodologi, hasil per bahasa)
