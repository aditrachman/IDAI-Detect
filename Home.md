# IDAI-Detect — Home

> Deteksi teks berbahasa Indonesia buatan AI, transparan & explainable.
> Codename sementara: **IDAI-Detect** | Status: **Draft persiapan (pra-skripsi)**

## Apa ini

Tool analisis teks Bahasa Indonesia yang memberi skor keyakinan "kemungkinan ditulis AI" + penjelasan per-kalimat, berbasis kombinasi banyak sinyal linguistik (bukan single heuristic).

**Gap yang diisi:**
- Detector existing (Turnitin AI, GPTZero) bias ke teks Bahasa Inggris
- Black-box — cuma skor tanpa alasan
- Satu sinyal doang gak reliabel → butuh multi-sinyal

## Status

- [x] PRD draft (18 Agu 2026) — updated: dataset publik + related work ditemukan
- [x] Related work BiLSTM 2026 ditemukan → positioning: **rule-based + explainability** (beda dari Bi-LSTM black-box)
- [x] Dataset prioritas ditetapkan: **M4** (ada Bahasa Indonesia)
- [x] Milestone 1: Riset & validasi pola — 4 sampel AI + 1 manusia, 9 sinyal divalidasi, em dash = sinyal terkuat → [[Pola dan Sinyal]]
- [x] Milestone 2: Rule engine v0 — `engine/rule_engine.py` (CLI, stdlib-only, self-check ✅, kalibrasi bobot awal)
- [ ] Milestone 3: Sample data kecil (bisa pakai subset M4)
- [ ] Milestone 4: Backend FastAPI
- [ ] Milestone 5: Frontend Next.js
- [ ] Milestone 6: Testing & iterasi bobot
- [ ] (Opsional) Kurasi dataset besar + proposal skripsi

## Navigasi

- [[PRD]] — dokumen sumber proyek (latar belakang, scope, arsitektur, milestone)
- [[Pola dan Sinyal]] — daftar 9 kategori sinyal + status validasi untuk Bahasa Indonesia *(lagi dikerjain)*
- [[Dataset]] — sumber data teks manusia vs AI, etika, target ukuran
- [[Eksperimen]] — log eksperimen & iterasi
- [[Referensi]] — paper, artikel, sumber pola

## Pertanyaan riset utama

1. Sinyal linguistik apa dari "Signs of AI Writing" yang valid diterapkan ke Bahasa Indonesia?
2. Seberapa akurat rule-based multi-sinyal vs pendekatan statistik (TF-IDF + classifier)?
3. Gimana bikin confidence score yang explainable, bukan black-box?
