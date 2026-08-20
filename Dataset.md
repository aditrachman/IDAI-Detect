# Dataset — Sumber Data & Etika

> Target prototype: ~200-300 sampel per kelas (manusia vs AI).
> Ini bagian tersulit — dokumentasi metodologi kurasi jadi kontribusi skripsi.

## 🎯 Prioritas: M4 Dataset (ready to use, ada Bahasa Indonesia!)

**Kenapa M4 duluan:** satu-satunya dataset publik dengan cakupan Bahasa Indonesia native + paralel human vs AI (korpus berita CNN Indonesia 2018, generator: davinci-003, ChatGPT, GPT-4, Cohere, Dolly2, BLOOMz). ~2.000 train + 500 dev/test per sumber.

- Link: github.com/mbzuai-nlp/M4
- [ ] Clone & inspeksi struktur data — cek split Indonesia, format, kualitas
- [ ] Ekstrak subset Bahasa Indonesia buat validasi rule engine (Milestone 3 bisa langsung pake ini, gak perlu scraping dulu!)

**Dataset pendukung (pembanding metodologi / cross-lingual):**
- RAID Benchmark — 7 bahasa termasuk Indonesia (cek paper RAID2024)
- AI-TEXT-DETECTION-PILE — 1.39M sampel, Inggris dominan, buat baseline/benchmark
- Defactify Text Dataset — 73k sampel NYT, baseline akurasi 58.35%
- HC3 — referensi metodologi human-vs-ChatGPT (Inggris/Cina)

## Teks Manusia (kurasi sendiri — untuk skripsi / data tambahan)

| Sumber | Contoh | Status | Catatan |
|---|---|---|---|
| Artikel berita Indonesia | Detik, Kompas, Antara | ✅ 1 sampel | human_02 (Telaah Antara, 10 Mei 2026). ⚠️ Antara punya klausul larang crawling otomatis — diambil manual 1 artikel buat riset pribadi, bukan training massal. Atribusi dicatat di sini |
| Esai mahasiswa (anonim) | Tugas kuliah (izin dulu) | ⬜ belum | WAJIB izin + anonimisasi |
| Forum/blog | Kaskus, blog pribadi | ✅ 1 sampel | human_03 (blog.mengetik.com, 15 Mei 2026 — esai santai) |
| Opini/kolom media | Media Indonesia dkk | ✅ 1 sampel | human_04 (opini Media Indonesia, 25 Mei 2026 — semi-akademik) |
| Tulisan sendiri | Tulisan Tuan Adit | ⬜ belum | Termudah & pasti "human" |

**Sampel manusia saat ini (20 Agu 2026):** human_01 (jurnal K-Means, akademik) + human_02 (telaah formal) + human_03 (blog santai) + human_04 (opini semi-akademik) — 4 gaya beda, semua verdict manusia di self-check strict. Masih butuh: chat casual, esai mahasiswa, tulisan sendiri.

## Teks AI

| Sumber | Status | Catatan |
|---|---|---|
| ChatGPT | ⬜ belum | Prompt beragam topik |
| Claude | ⬜ belum | — |
| Gemini | ⬜ belum | — |
| LLM lokal (kalau ada) | ⬜ belum | Bisa dokumentasi model + versi (penting buat reproducibility) |

## Etika & Integritas

- Esai mahasiswa: izin tertulis + anonim total (jangan simpan identitas)
- Dokumen bagaimana tiap sampel dibuat: prompt apa, model apa, versi apa
- Jangan pakai data yang dilindungi / berbayar tanpa izin
- Kalau publish dataset (skripsi), lampirkan metodologi kurasi lengkap

## Struktur penyimpanan (rencana)

```
data/
  human/
    001.txt
    002.txt
    ...
  ai/
    chatgpt_001.txt
    claude_001.txt
    gemini_001.txt
    ...
  metadata.csv   # sumber, tanggal, model/prompt (buat AI), anonim id
```

## Checklist

- [ ] Kumpulkan ~30 sampel dulu (mix semua sumber) buat validasi awal rule engine
- [ ] Metadata template disepakati
- [ ] Izin esai mahasiswa (kalau jadi)
