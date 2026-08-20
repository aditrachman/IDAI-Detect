# PRD: Deteksi Teks Berbahasa Indonesia Buatan AI

**Codename sementara:** IDAI-Detect
**Status:** Draft persiapan (pra-skripsi)
**Penyusun:** Muhammad Aditya Rachman
**Terakhir diupdate:** 18 Agustus 2026 (update: dataset publik + related work)

---

## 1. Latar Belakang & Masalah

Sejak LLM (ChatGPT, Claude, Gemini, dll) makin gampang diakses, makin banyak teks — mulai dari tugas kuliah, artikel, sampai konten media sosial — yang ditulis AI tapi diakui sebagai tulisan manusia. Tools detector yang ada sekarang (Turnitin AI, GPTZero, dll) punya masalah:

- Mayoritas dilatih dan dioptimalkan untuk **teks Bahasa Inggris**
- Sifatnya **black-box** — cuma kasih skor persentase tanpa alasan yang jelas
- Studi menunjukkan akurasi deteksi manusia (dan bahkan beberapa tool) terhadap teks AI itu **tidak reliabel** kalau cuma mengandalkan satu sinyal (contoh: em dash overuse)

**Gap yang mau diisi:** belum ada tool deteksi teks AI yang (a) fokus ke Bahasa Indonesia, (b) transparan soal alasan kenapa suatu teks dicurigai AI, dan (c) dibangun dari kombinasi banyak sinyal linguistik, bukan cuma satu heuristik.

## 2. Tujuan Proyek

### Tujuan jangka pendek (proyek/prototype)
- Membangun sistem yang bisa menganalisis teks Bahasa Indonesia dan memberi skor keyakinan "kemungkinan ditulis AI"
- Sistem memberi **penjelasan per-kalimat**, bukan cuma angka
- Jadi portfolio project yang bisa dipakai/didemoin

### Tujuan jangka panjang (menuju skripsi)
- Jadi dasar penelitian ilmiah dengan kontribusi orisinal: dataset & model deteksi teks AI berbahasa Indonesia
- Punya metodologi evaluasi yang bisa dipertanggungjawabkan secara akademik

## 3. Target Pengguna

| Persona | Kebutuhan |
|---|---|
| Dosen/asdos (termasuk kamu sendiri) | Ngecek tugas mahasiswa yang dicurigai full-AI |
| Mahasiswa | Self-check sebelum submit, biar tau bagian mana yang "kebacaan AI" |
| Editor/penulis konten | Ngecek naskah sebelum publish |

*(Prioritas pertama: use case akademik, karena paling relevan sama posisi kamu sebagai asdos dan paling mudah dapat data uji)*

## 4. Scope

### In-scope (v1 / prototype)
- Input: teks paste langsung atau upload dokumen (.txt, .docx, .pdf)
- Analisis rule-based multi-sinyal (lihat §6)
- Skor agregat + breakdown per kategori sinyal
- Highlight kalimat/paragraf yang berkontribusi ke skor
- Web app sederhana (Next.js frontend + FastAPI backend)

### Out-of-scope (v1)
- Deteksi real-time / API publik berskala besar
- Dukungan bahasa selain Indonesia
- Watermarking atau deteksi berbasis model generator tertentu (misal fingerprint khusus GPT vs Claude)
- Mobile app

### Kemungkinan scope v2 (kalau lanjut ke skripsi)
- Layer ML/statistik (bukan cuma rule-based) — misal fitur stilometri + classifier
- Dataset kurasi sendiri: teks manusia vs AI Bahasa Indonesia
- Studi evaluasi dengan ground truth & metrik akademik (precision/recall/F1)

## 5. Rumusan Masalah Awal (buat nanti dijembatani ke skripsi)

1. Sinyal linguistik apa saja dari "Signs of AI Writing" yang **valid diterapkan** ke teks Bahasa Indonesia? (banyak pola di sumber aslinya bias ke Bahasa Inggris)
2. Seberapa akurat pendekatan rule-based multi-sinyal dibanding pendekatan statistik (misal TF-IDF + classifier) untuk teks Indonesia?
3. Bagaimana cara memberi confidence score yang transparan dan bisa dijelaskan (explainable), bukan black-box?

## 6. Kategori Fitur/Sinyal yang Akan Dideteksi

Diadaptasi dari Wikipedia "Signs of AI Writing" + riset pendukung, disesuaikan konteks Bahasa Indonesia:

| Kategori | Contoh Pola | Metode Deteksi |
|---|---|---|
| Puffery / frasa lebay | "memainkan peran penting", "menjadi bukti nyata" | Dictionary matching |
| Kalimat penutup analitik | Ringkasan ulang di akhir paragraf | Pattern matching + posisi kalimat |
| Kontras "bukan X, tapi Y" | Negative parallelism | Regex pattern |
| Basa-basi sisa chat | "semoga membantu", "jika ada pertanyaan lain" | Dictionary matching |
| Formatting berlebihan | Bold/list/heading tidak konsisten | Structural parsing (kalau input markdown/docx) |
| Tanda pisah (—) berlebihan | Frekuensi em dash relatif terhadap panjang teks | Statistical count + threshold |
| Hedging berlebihan | "cenderung", "kemungkinan", "dapat dikatakan" berulang | Dictionary + frequency |
| Transisi kaku/berulang | "selain itu", "di sisi lain" dipakai pola tetap | N-gram repetition check |
| Homogenitas struktur kalimat | Panjang kalimat terlalu seragam (rendah burstiness) | Statistik (variance panjang kalimat) |

**Catatan penting:** tiap sinyal dikasih bobot berbeda dan dikombinasi jadi skor agregat — bukan single-flag verdict. Ini sesuai temuan riset bahwa 1 sinyal doang gak reliabel.

## 7. Arsitektur Teknis (Rencana Awal)

```
Frontend (Next.js 15)
  └─ Upload/paste teks → kirim ke backend

Backend (FastAPI, Python)
  ├─ Text preprocessing (cleaning, sentence splitting)
  ├─ Rule Engine
  │    ├─ Dictionary-based matcher (puffery, hedging, basa-basi)
  │    ├─ Regex pattern matcher (kontras, transisi)
  │    └─ Statistical analyzer (em dash freq, sentence variance)
  ├─ Scoring Aggregator (weighted sum → confidence score)
  └─ Response: skor total + breakdown per kategori + highlight per kalimat

(v2, opsional) ML Layer
  └─ TF-IDF/embedding + classifier terlatih dari dataset kurasi
```

### 7.1 Strategi Agregasi Skor (keputusan desain, 18 Agu 2026)

**Tahap 1 (v1): Weighted voting STATIS**
- Bobot tiap sinyal ditentukan manual dari hasil validasi pola (Milestone 1) — pola yang terbukti kuat dapat bobot lebih besar
- Transparan & gampang di-tuning — nyambung sama positioning explainability
- Alasan gak pakai meta-model di v1: belum ada dataset labeled buat melatihnya

**Tahap 2 (v2): Meta-model logistic regression**
- Dilatih di ATAS fitur sinyal (bukan teks mentah): input = skor tiap sinyal, output = probabilitas AI
- Keuntungan: belajar bobot optimal + bias tiap detector, probabilitas terkalibrasi buat confidence score, koefisien tetap bisa dijelaskan (explainability terjaga — kontras sama random forest yang black-box)
- Sinyal "perplexity" masuk v2 (butuh model bahasa, bukan rule-based)
- Catatan: jangan bangun multi-agent system terpisah di v1 — cukup modul analyzer dalam satu proses. Multi-agent = scope creep di tahap ini

### 7.2 Kontrak Modul Analyzer & Telemetry (keputusan desain, 18 Agu 2026 — diskusi Raya × Gemini)

**Kontrak output tiap analyzer (Strategy Pattern, Modular Monolith di FastAPI):**
```json
{
  "module_name": "LexicalStats",
  "raw_score": 0.85,
  "confidence": 0.9,
  "evidence": ["High exact-word repetition", "Low variance in sentence length"]
}
```
- Aggregator cuma weighted voting dari `raw_score` × bobot statis
- `evidence` langsung dipakai frontend buat explainability

**Telemetry & Data Shadowing (dari hari pertama v1):**
- Setiap analisis → simpan 1 baris log: `X1..Xn` (raw_score tiap analyzer), hasil voting, + kolom `ground_truth` KOSONG
- Storage: CSV internal / SQLite sederhana (BUKAN PostgreSQL — ini log fitur, bukan database produksi)
- JANGAN simpan teks asli di log otomatis — cukup fitur. Alasan: hemat storage + privasi pengguna. Teks asli + label cuma disimpen manual pas kurasi dataset skripsi
- Manfaat: pas v2, dataset training logreg udah kesedia otomatis tanpa ekstraksi ulang

**Kesamaan dengan stack yang sudah kamu kuasai:** mirip arsitektur VoxSwarm (FastAPI + Next.js + scoring/classifier), jadi banyak kerangka kerja yang bisa reuse.

## 8. Kebutuhan Data

Ini bagian tersulit dan paling krusial:

- **Sumber teks manusia:** artikel berita Indonesia, esai mahasiswa (dengan izin/anonim), forum/blog
- **Sumber teks AI:** generate dari berbagai LLM (ChatGPT, Claude, Gemini) dengan prompt beragam topik
- **Ukuran minimal untuk prototype:** ~200-300 sampel per kelas (manusia vs AI) sudah cukup untuk validasi awal rule-based
- **Untuk skripsi nanti:** perlu jauh lebih besar dan harus didokumentasikan metodologi kurasinya (ini jadi kontribusi ilmiah tersendiri)

### 8.1 Dataset Publik yang Bisa Dimanfaatkan (Ready to Use)

| Dataset | Cakupan Bahasa Indonesia | Isi | Link |
|---|---|---|---|
| **M4 Dataset** | Ya — korpus berita Indonesia (CNN Indonesia, 2018) | Data paralel human vs AI, generator: davinci-003, ChatGPT, GPT-4, Cohere, Dolly2, BLOOMz. ~2.000 training + 500 dev/test per sumber | github.com/mbzuai-nlp/M4 |
| **RAID Benchmark** | Ya — salah satu dari 7 bahasa yang dicakup (termasuk bahasa rendah-sumber daya) | Multi-domain, multi-LLM | Cek paper RAID2024 |
| **HC3 (Human ChatGPT Comparison Corpus)** | Tidak (fokus Inggris/Cina) | Referensi metodologi perbandingan human vs ChatGPT | HuggingFace |
| **AI-TEXT-DETECTION-PILE** | Tidak (dominan Inggris) | 1.392.011 sampel (manusia: 1.028.144, AI: 363.867) — bisa buat baseline/benchmark metodologi | HuggingFace (artem9k) |
| **Defactify Text Dataset** | Tidak (NYT articles) | 73.193 sampel, generator: Gemma-2-9b, Mistral-7B, Qwen-2-72B, LLaMA-8B, Yi-Large, GPT-4o | huggingface.co/datasets/Rajarshi-Roy-research/Defactify_Text_Dataset |

**Prioritas:** mulai dari **M4 Dataset** karena satu-satunya yang punya cakupan Bahasa Indonesia native dan sudah paralel (human vs AI). Dataset lain berguna sebagai pembanding metodologi atau kalau butuh data tambahan Bahasa Inggris untuk cross-lingual testing.

### 8.2 Related Work Penting — Wajib Dibaca & Dicitasi

**Ada penelitian Indonesia yang sudah menggarap topik serupa** — ini krusial buat positioning novelty skripsi kamu:

> Sebuah studi mengembangkan sistem deteksi teks Bahasa Indonesia buatan AI menggunakan Bi-LSTM, dengan metodologi CRISP-DM. Dataset: 5.008 baris teks — manusia dari scraping platform jurnalistik dan jurnal akademik terindeks SINTA 4, teks AI dari parafrase ChatGPT dan Google Gemini.
> — *Implementation of the BiLSTM Model for Detecting AI-Generated Indonesian Text*, Jurnal Teknologi Informatika dan Komputer (2026)

**Implikasi untuk kamu:**
- Ini **bukan penghalang**, tapi validasi kalau topiknya legit dan diakui layak diteliti di Indonesia
- Wajib dicitasi di bagian tinjauan pustaka skripsi
- Celah pembeda yang masih terbuka: mereka pakai Bi-LSTM (black-box, deep learning), kamu bisa ambil sudut **rule-based + explainability** (kasih alasan per kalimat) atau **hybrid rule-based + statistical**, yang belum mereka garap
- Baseline akurasi di riset besar sejenis (dataset Defactify, non-Indonesia) cuma 58.35% — bukti bahwa masalah deteksi AI generatif ini emang masih jauh dari solved, ruang kontribusi masih besar

## 9. Metrik Keberhasilan (Prototype)

| Metrik | Target Awal |
|---|---|
| Precision (teks AI yang benar terdeteksi AI) | Belum ada baseline — kumpulkan dulu, evaluasi setelah v1 jalan |
| Recall | idem |
| False positive rate ke teks manusia formal/akademik | Diprioritaskan rendah (jangan sampai tuduh mahasiswa yang nulis formal) |
| Kejelasan explanation | Subjektif — user testing kecil (misal ke teman/dosen) |

## 10. Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| Sinyal dari Wikipedia bias ke Bahasa Inggris, gak semua relevan ke Indonesia | Validasi manual tiap pola sebelum diimplementasi, buang yang gak relevan |
| Dataset kecil bikin skor gak reliabel | Mulai rule-based dulu (gak butuh data training besar), ML nyusul kalau data cukup |
| False positive ke penulis non-native/formal | Kasih disclaimer jelas di UI: ini indikasi, bukan vonis |
| Scope creep ke fitur macam-macam | Kunci ke v1 scope dulu, semua ide tambahan masuk backlog v2 |

## 11. Milestone Kasar

1. **Riset & validasi pola** — cek satu-satu pola Wikipedia, mana yang applicable ke Bahasa Indonesia (perlu dicek manual dengan contoh nyata)
2. **Rule engine v0** — implementasi dictionary + regex matcher, tanpa UI dulu (CLI/notebook testing)
3. **Kumpulkan sample data kecil** — buat validasi manual rule engine
4. **Backend API** — FastAPI endpoint buat scoring
5. **Frontend** — UI upload/paste + visualisasi hasil
6. **Testing & iterasi bobot skor**
7. **(Opsional lanjut ke skripsi)** — kurasi dataset besar, proposal formal, rumusan masalah final

## 12. Referensi Awal

**Pola & heuristik:**
- Wikipedia: Signs of AI Writing (WikiProject AI Cleanup) — sumber pola awal
- Freeburg, E.M. (2026). *The Last Fingerprint: How Markdown Training Shapes LLM Prose* — dasar teori em dash
- VERMILLION framework (linguistic markers of AI-generated communication)
- Studi tentang keterbatasan manusia mendeteksi teks AI (Indiana Capital Chronicle, 2025) — jadi justifikasi kenapa butuh tool, bukan cuma insting

**Related work (wajib dicitasi):**
- *Implementation of the BiLSTM Model for Detecting AI-Generated Indonesian Text*, Jurnal Teknologi Informatika dan Komputer (2026) — riset Indonesia paling relevan, jadi pembanding utama
- Wang, Y. et al. (2023/2024). *M4: Multi-Generator, Multi-Domain, and Multi-Lingual Black-Box Machine-Generated Text Detection* — sumber dataset utama (github.com/mbzuai-nlp/M4)
- Roy, R. et al. (2026). *A Comprehensive Dataset for Human vs. AI Generated Text Detection* (Defactify) — pembanding metodologi & baseline akurasi

**Dataset:**
- M4 Dataset — github.com/mbzuai-nlp/M4
- AI-TEXT-DETECTION-PILE — huggingface.co (artem9k)
- Defactify Text Dataset — huggingface.co/datasets/Rajarshi-Roy-research/Defactify_Text_Dataset

---

*Dokumen ini adalah working draft. Belum untuk submit ke dospem — masih perlu validasi teknis dan diskusi kelayakan topik.*