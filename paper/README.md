# paper/ — Luaran Pertemuan 8 (Finalisasi Paper)

Naskah untuk **Jurnal Pustaka Data** (Pustaka Galeri Mandiri, ISSN 2809-7483), mengikuti template
`Template_Pustaka_Data.doc`.

| Berkas | Isi | Disunting? |
| :--- | :--- | :--- |
| `naskah_sumber.md` | **Naskah yang disunting.** Sitasi ditulis `[@kunci]` | Ya, sunting di sini |
| `susun_paper.py` | Menomori sitasi sesuai urutan muncul, menyusun Daftar Rujukan dari kamus `RUJUKAN` (metadata dari `../02_Studi Literatur/Verifikasi_Literatur.md`), menomori gambar/tabel/rumus, lalu mengisi template asli | Tambah rujukan baru di `RUJUKAN` |
| `Paper_PRE02_Pustaka_Data.md` | Naskah final bersitasi nomor (hasil skrip) | Tidak |
| `Paper_PRE02_Pustaka_Data.docx` | **Naskah final yang sudah diisi langsung ke template asli** (kop jurnal, logo, header, footer, kolom, dan gaya paragraf template; rujukan bernomor otomatis gaya *Rujukan*) | Tidak |
| `Template_Pustaka_Data.doc` | Template asli Jurnal Pustaka Data yang diisi oleh skrip | Tidak |
| `buat_slide.js` | Pembuat slide (pptxgenjs) | Ya |
| `Presentasi_Hasil_PRE02.pptx` | Slide presentasi hasil penelitian, 12 slide | Tidak |

## Cara menjalankan

```bash
# gambar 1-4 versi satu kolom, panel (a) atas dan (b) bawah, dari CSV hasil eksperimen (butuh numpy, pandas, matplotlib)
python gambar_paper.py

# naskah (butuh pandoc, LibreOffice, python-docx, pillow, dan font Liberation Serif)
python susun_paper.py

# slide (butuh node + pptxgenjs; APPLY_THEME = scripts/apply_theme.js dari skill pptx)
NODE_PATH=<node_modules berisi pptxgenjs> APPLY_THEME=<path apply_theme.js> node buat_slide.js
```

## Ke Google Docs

Unggah `Paper_PRE02_Pustaka_Data.docx` ke Google Drive → klik kanan → **Buka dengan → Google Dokumen**.

## Sebelum submit

| No | Yang perlu dilakukan tim |
| :---: | :--- |
| 1 | Buka .docx di Word/Google Docs dan cek tata letak akhir (pemisah kolom dan posisi gambar bisa sedikit bergeser antara LibreOffice, Word, dan Google Docs) |
| 2 | Lengkapi afiliasi (template meminta jurusan dan nomor WhatsApp) dan baris *Submitted/Reviewed/Accepted* diisi redaksi |
| 3 | Cek ulang tiga DOI yang belum aktif di doi.org per 12 Nov 2026 (Haekal, Mandapatti, Ananta; lihat `Verifikasi_Literatur.md`). Di naskah, DOI Haekal dan Mandapatti tidak dicantumkan |
| 4 | Template meminta rujukan dikelola dengan Mendeley/Zotero; daftar di sini sudah urut dan lengkap, bisa diimpor bila redaksi memintanya |

## Checklist Pertemuan 8 (`progres_penelitian_MP.md`)

- [x] **Penyusunan paper lengkap (IMRAD):** struktur baku template (Pendahuluan, Metode Penelitian, Hasil dan Pembahasan, Kesimpulan), 7 halaman.
- [x] **Penyempurnaan bahasa ilmiah dan sitasi:** sitasi bernomor sesuai urutan muncul, semua rujukan terverifikasi, tanpa bullet di isi, kesimpulan tanpa sitasi.
- [x] **Abstrak dan daftar pustaka:** Abstract (196 kata) + Abstrak (177 kata), 28 rujukan.
- [x] **Paper ilmiah final** (draf siap tempel ke template) dan **slide presentasi hasil penelitian**.
