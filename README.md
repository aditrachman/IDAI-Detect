# IDAI-Detect

> Deteksi teks AI berbahasa Indonesia — rule-based multi-sinyal, transparan dengan penjelasan per kalimat.

Tidak seperti detector black-box (Turnitin AI, GPTZero) yang bias ke Bahasa Inggris dan cuma kasih angka tanpa alasan, IDAI-Detect menganalisis kombinasi sinyal linguistik yang sudah divalidasi pada sampel teks Indonesia asli, lalu menandai kalimat-kalimat yang mencurigakan beserta alasannya.

## Fitur

- **9 sinyal linguistik** — hipotesis awal yang diuji pada 5 sampel nyata (4 teks AI, 1 teks manusia), **belum tervalidasi skala besar**
- **Skor agregat + breakdown per sinyal** — verdict `AI` / `abu-abu` / `manusia`
- **Highlight per kalimat** dengan alasan spesifik (em dash prosa, kalimat penutup analitik, enumerasi sistematis, hedging, transisi kaku, puffery, dst.)
- **Web app sederhana**: paste teks atau upload file `.txt` / `.docx` / `.pdf`
- **CLI** untuk analisis batch
- **Self-check jujur**: `--self-check` menguji SEMUA sampel di `data/` dan exit code 1 kalau ada yang gagal (bukan cherry-pick)

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

> ⚠️ Self-check menguji SEMUA sampel (AI harus verdict AI, manusia harus manusia) dan
> exit code 1 kalau ada yang gagal. Dengan dataset kecil saat ini, kegagalan itu
> **disengaja dan jujur** — sinyal bahwa kalibrasi bobot/threshold masih pekerjaan terbuka.

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

> ⚠️ **Status validasi: hipotesis awal dari 5 sampel (4 AI, 1 manusia) — BUKAN tervalidasi skala besar.**
> Semua bobot & threshold di bawah bersifat **provisional**, didapat dari n=5 sampel dan
> berisiko overfit. Wajib dikalibrasi ulang dengan dataset M4 (subset Indonesia, ~2.000+
> sampel) di Milestone 3/6 sebelum hasilnya bisa diklaim.

| Sinyal | Bobot | Status (n=5) |
|---|---|---|
| Em dash prosa (—) | 0.35 | Hipotesis kuat: AI 1.4–6.8 / 1.000 kata vs 1 sampel manusia (0). Tahan edit manual |
| Kalimat penutup analitik | 0.20 | Muncul di 2 case study AI; 1 baseline manusia belum banding |
| Enumerasi sistematis | 0.15 | Muncul kuat di 1 case study; belum teruji lintas gaya |
| Burstiness rendah | 0.05 | Terkonfirmasi 2 detector, tapi noise di dokumen tabel-heavy |
| Hedging, transisi, puffery, kontras, basa-basi | @0.05 | Lemah / belum teruji — butuh sampel lebih banyak |

**Kondisi baseline saat ini (self-check strict, 20 Agu 2026):** 2 dari 4 sampel AI lolos,
2 gagal (1 abu-abu, 1 salah klasifikasi manusia) — rata-rata skor AI 0.345 vs manusia 0.057.
Ini baseline yang jujur: bobot/threshold belum layak, kalibrasi adalah pekerjaan terbuka (Milestone 6).

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