# Eksperimen — Log

> Catat SEMUA percobaan: apa yang dicoba, kenapa, hasilnya, dan pelajaran.
> Format per-entri. Entri baru paling atas.

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