# Pola dan Sinyal — Validasi untuk Bahasa Indonesia

> Status: **VALIDASI AWAL n=5 (4 AI, 1 manusia) — BELUM SKALA BESAR**
> ⚠️ 20 Agu 2026 (audit metodologi): semua status di bawah berdasar 5 sampel doang.
> Bobot & threshold di rule engine bersifat **PROVISIONAL** dan WAJIB dikalibrasi ulang
> begitu dataset M4 (subset Indonesia, ~2.000+ sampel) masuk di Milestone 3.
> Jangan pernah dibaca sebagai angka final.
> Sumber awal: Wikipedia "Signs of AI Writing" + riset pendukung.
> Tugas: cek satu-satu pola di bawah, mana yang **muncul di tulisan AI Bahasa Indonesia** dan mana yang **bias/gak relevan** (sumber aslinya bias ke Bahasa Inggris).

## Cara validasi

1. Ambil ~10 contoh teks AI Bahasa Indonesia (generate dari ChatGPT/Claude/Gemini, topik beragam)
2. Ambil ~10 teks manusia Bahasa Indonesia (berita, esai, blog)
3. Cek manual: apakah pola ini muncul lebih sering di teks AI?
4. Catat hasilnya di kolom **Status**

## Daftar sinyal

| # | Kategori | Contoh Pola | Status | Catatan Validasi |
|---|---|---|---|---|
| 1 | Puffery / frasa lebay | "memainkan peran penting", "menjadi bukti nyata" | ⬜ belum dicek | — |
| 2 | Kalimat penutup analitik | Ringkasan ulang di akhir paragraf | ✅ **terkonfirmasi** | Case study #2 & #3: *"Hasil rekomendasi menunjukkan...", "Hasil setiap model dibandingkan untuk memilih model terbaik..."* — muncul di akhir sub-bab laporan AI |
| 3 | Kontras "bukan X, tapi Y" | Negative parallelism | ⬜ belum dicek | — |
| 4 | Basa-basi sisa chat | "semoga membantu", "jika ada pertanyaan lain" | ⬜ belum dicek | — |
| 5 | Formatting berlebihan | Bold/list/heading tidak konsisten | ⬜ belum dicek | ⚠️ Lemah & rawan false positive — format jelek bisa dari pipeline rendering, bukan penulis. Kemungkinan dibuang dari v1 |
| 6 | Em dash (—) berlebihan | Frekuensi tanda pisah relatif panjang teks | ✅ **terkonfirmasi (3 sampel)** | ⭐ Baseline: AI 1,4 / 6,8 / **3,7** per 1.000 kata prosa vs MANUSIA **0** (human_01 — satu-satunya baseline manusia). ⚠️ n=1 baseline manusia, belum cukup buat klaim kuat. Catatan: em dash di sel tabel / rentang angka ("0,08 – 82,0") gak dihitung — cuma prosa. ⭐ **Bahkan setelah diedit manusia (case study #3), em dash-nya nyangkut** — sinyal paling tahan banting |
| 7 | Hedging berlebihan | "cenderung", "kemungkinan", "dapat dikatakan" | ⬜ belum dicek | — |
| 8 | Transisi kaku/berulang | "selain itu", "di sisi lain", "dengan demikian" | ⬜ belum dicek | Catatan: "di sisi lain" kurang natural di ID? Cek |
| 9 | Homogenitas panjang kalimat | Variance rendah (low burstiness) | ✅ **terkonfirmasi** | Cross-check 2 detector (Raya + Gemini): transisi mekanis & template pembuka berulang = sinyal kuat di AI text ID |
| 10 | **Kurang narasi kegagalan / opini analitis** *(baru, dari Gemini)* | Laporan cuma rangkum hasil rapi, gak ada cerita eksperimen gagal / trade-off keputusan ("kenapa bobot 0,50?") | ✅ terkonfirmasi (case study #2, teks AI 100%) | ⚠️ Lemah kalau sendirian — banyak laporan manusia juga dangkal. Susah diukur rule-based → kandidat ML layer v2 |

## Pola tambahan khusus Bahasa Indonesia (kandidat, perlu riset)

- Penerjemahan langsung idiom Inggris → Indonesia yang kaku (translationese)
- Penggunaan kata baku berlebihan di konteks santai (atau sebaliknya)
- Kalimat pasif berlebihan ("dapat dilakukan", "perlu diperhatikan")
- Kata serapan teknis yang dipaksakan ("memfasilitasi", "mengoptimalkan" berulang)
- Klik-klik frasa formal berulang di awal paragraf

## ⚠️ Sinyal KEBALIKAN (tanda manusia — untuk menurunkan skor AI)

⭐ Ditemukan dari human_01 (jurnal K-Means 2020) — kesalahan ini umum di tulisan manusia Indonesia, AI modern gak bikin:
- **Typo nyata**: "egent of social change" (harusnya agent), "tersetruktur", "peminataan", "bertangung jawab"
- **Kapitalisasi gak konsisten**: "Ahmad dwi tama saputra" (huruf kecil), "Npm." vs "NPM" (ai_04 — ⚠️ ternyata ini bagian header yang diketik manual, bukan prosa)
- **Bahasa santai di dokumen formal**: "matkul" (ai_04 — ⚠️ sama, header manual)
- **Artefak ketik manual**: label bold dempet sama definisi tanpa spasi — "a. SupportSupport merupakan..." (ai_04 — ⚠️ header/label manual). ⚠️ Validasi per konteks: sinyal ini cuma valid kalau bagian yang dicek emang ditulis orang itu sendiri
- **Grammar error**: "yang gunakan" (hilang imbuhan), "Jumlah data yang banyak tersebut maka sangat mungkin terjadi kesalahan"
- **Struktur kalimat berbelit/bertele-tele** (kebalikan dari "efisiensi kata" AI)
- **Repetisi berlebihan**: definisi diulang verbatim (abstract + abstrak), "K-Means Clustering" diulang terus
- **Format kutipan gak konsisten**: "(Selvia Tristianty Hidajat, 2016 ; 59)" — spasi aneh, format campur
- **Spasi aneh di sekitar tanda hubung**: "kelas - kelas", "kriteria – kriteria"
- ⚠️ Catatan: beberapa kesalahan bisa berasal dari pipeline PDF/rendering — tetap validasi per kasus. Tapi typo linguistik (egent, peminataan) itu murni kesalahan penulis → sinyal manusia kuat

## Keputusan yang udah diambil

- ⭐ **Kasus "data/kode asli + prosa AI" itu umum banget** (2 dari 2 sampel kita ternyata gitu): detector harus fokus ke TEKS (gaya penulisan), JANGAN pernah jadikan "kebenaran faktual / angka presisi" sebagai sinyal manusia — AI yang dikasih data bisa nulis angka bener
- ⚠️ **Verdict global "AI/human" menyesatkan** — harus breakdown per kalimat/bagian
- ✅ **"Kalimat penutup analitik" & "enumerasi sistematis"** terbukti muncul kuat di teks AI Bahasa Indonesia → prioritas tinggi
- ✅ **Em dash di prosa** (bukan di tabel/nomor/range) = sinyal valid
- ✅ **Burstiness rendah / transisi mekanis** terkonfirmasi 2 detector independen (Raya + Gemini) → prioritas tinggi
- ✅ **Sinyal baru #10 "kurang narasi kegagalan"** (dari Gemini) — kandidat buat ML layer v2, bukan rule-based
- ✅ **Agregasi skor: v1 = weighted voting statis (bobot dari validasi pola), v2 = meta-model logistic regression di atas fitur sinyal** (lihat PRD §7.1) — keputusan dari diskusi Raya × Gemini
- ✅ **Em dash prosa** = sinyal terkuat sejauh ini — 3 sampel AI: 1,4 / 6,8 / 3,7 per 1.000 kata vs manusia 0. ⭐ Tahan edit manual
- ✅ **Edited AI text (case study #3) tetap terdeteksi** — edit kecil manusia gak nyamarin em dash, struktur template, & nol typo
- ⚠️ **Dokumen tabel-heavy butuh preprocessing khusus** — pisah tabel vs prosa sebelum statistik kalimat (case study #3: sentence splitting kena noise sel tabel)
- ⚠️ **Teks pendek (< ~300 kata) = zona abu-abu** — statistik (em dash rate, burstiness) unreliable di sampel kecil; rule engine harus kasih peringatan confidence rendah (case study #4)
- ⭐ **HYBRID "kerangka manusia + prosa AI" itu pola umum** (2 dari 4 sampel AI: case #3 stroke & #4 Tama) — sinyal "manusia" sering cuma nempel di header/label manual, prosa-nya tetap AI. Rule engine harus fokus ke prosa naratif, kecualikan header/label/bullet pendek
- 📌 **Data validasi nyata**: `data/ai/` 4 sampel (ai_01 AAS ML ~3.135 kata, ai_02 Manga ~4.333 kata, ai_03 Stroke CRISP-DM ~1.600 kata edited, ai_04 ringkasan Tama ~208 kata hybrid) + `data/human/` 1 sampel (human_01 K-Means ~3.877 kata)

## Template entri validasi (copy buat tiap pola)

```markdown
### [Nama Pola]
- **Kapan dicek:** [tanggal]
- **Sumber pola:** [Wikipedia/paper/dll]
- **Contoh di teks AI ID:** [kutip 1-2 kalimat nyata]
- **Contoh di teks manusia ID:** [kutip, kalau ada]
- **Verdict:** ✅ valid / ⚠️ sebagian / ❌ gak relevan
- **Alasan:** ...
```
