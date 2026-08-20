# IDAI-Detect

> Deteksi teks AI berbahasa Indonesia — rule-based multi-sinyal, transparan dengan penjelasan per kalimat.

Tidak seperti detector black-box (Turnitin AI, GPTZero) yang bias ke Bahasa Inggris dan cuma kasih angka tanpa alasan, IDAI-Detect menganalisis kombinasi sinyal linguistik yang sudah divalidasi pada sampel teks Indonesia asli, lalu menandai kalimat-kalimat yang mencurigakan beserta alasannya.

## Fitur

- **9 sinyal linguistik** yang sudah divalidasi pada 5 sampel nyata (4 teks AI, 1 teks manusia)
- **Skor agregat + breakdown per sinyal** — verdict `AI` / `abu-abu` / `manusia`
- **Highlight per kalimat** dengan alasan spesifik (em dash prosa, kalimat penutup analitik, enumerasi sistematis, hedging, transisi kaku, puffery, dst.)
- **Web app sederhana**: paste teks atau upload file `.txt` / `.docx` / `.pdf`
- **CLI** untuk analisis batch

## Cara menjalankan

```bash
pip install fastapi uvicorn python-multipart jinja2 PyPDF2
python3 app.py
# buka http://localhost:8000
```

CLI:

```bash
python3 engine/rule_engine.py file1.txt file2.docx
```

Self-check pada sampel yang ada di `data/`:

```bash
python3 engine/rule_engine.py --self-check
```

## Struktur

```
app.py                     # web app FastAPI
engine/rule_engine.py      # rule engine v0 (CLI + library)
templates/index.html       # UI highlight per kalimat
data/
  ai/                      # sampel teks AI (ground truth terkoreksi)
  human/                   # sampel teks manusia
```

## Sinyal yang dideteksi

| Sinyal | Bobot | Status validasi |
|---|---|---|
| Em dash prosa (—) | 0.35 | ✅ Terkuat: AI 1.5–12 / 1.000 kata vs manusia 0 |
| Kalimat penutup analitik | 0.20 | ✅ Terkonfirmasi 2 case study |
| Enumerasi sistematis | 0.15 | ✅ Terkonfirmasi (Pertama/Kedua, 1. 2. 3.) |
| Burstiness rendah | 0.05 | ⚠️ Noise di dokumen tabel-heavy |
| Hedging, transisi, puffery, kontras, basa-basi | @0.05 | ⚠️ Lemah, butuh lebih banyak sampel |

Bobot & threshold masih kasar (kalibrasi lanjutan di roadmap).

## Roadmap

- [x] Milestone 1 — Riset & validasi pola (case study: laporan ML, manga recommender, CRISP-DM stroke)
- [x] Milestone 2 — Rule engine v0 (CLI + web app sederhana)
- [ ] Milestone 3 — Validasi skala besar (subset Bahasa Indonesia dari M4 dataset)
- [ ] Milestone 4 — Kalibrasi bobot & threshold
- [ ] (v2) Layer ML — fitur stilometri + classifier (kandidat: Bi-LSTM pembanding)

## Disclaimer

Alat ini memberi **indikasi**, bukan vonis. Skor rendah pada teks formal/akademik yang ditulis manusia masih mungkin terjadi — jangan dipakai sebagai satu-satunya dasar penilaian.

## Lisensi

Belum ditentukan.