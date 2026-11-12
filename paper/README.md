# paper/ — Luaran Pertemuan 8 (Finalisasi Paper)

Naskah untuk **Jurnal Pustaka Data** (Pustaka Galeri Mandiri, ISSN 2809-7483), mengikuti template
`Template_Pustaka_Data.doc`.

| Berkas | Isi | Disunting? |
| :--- | :--- | :--- |
| `naskah_sumber.md` | **Naskah yang disunting.** Sitasi ditulis `[@kunci]` | Ya, sunting di sini |
| `susun_paper.py` | Menomori sitasi sesuai urutan muncul, menyusun Daftar Rujukan dari kamus `RUJUKAN` (metadata dari `../02_Studi Literatur/Verifikasi_Literatur.md`), menomori gambar/tabel, lalu membuat .md dan .docx | Tambah rujukan baru di `RUJUKAN` |
| `Paper_PRE02_Pustaka_Data.md` | Naskah final bersitasi nomor (hasil skrip) | Tidak |
| `Paper_PRE02_Pustaka_Data.docx` | Naskah final berformat template: Times New Roman 10 pt, judul 15 pt, A4 margin 25 mm, abstrak satu kolom, isi dua kolom (hasil skrip) | Tidak |
| `gaya_pustaka_data.docx` | Dokumen gaya untuk pandoc (hasil skrip) | Tidak |
| `buat_slide.js` | Pembuat slide (pptxgenjs) | Ya |
| `Presentasi_Hasil_PRE02.pptx` | Slide presentasi hasil penelitian, 12 slide | Tidak |

## Cara menjalankan

```bash
# naskah (butuh pandoc dan python-docx)
python susun_paper.py

# slide (butuh node + pptxgenjs; APPLY_THEME = scripts/apply_theme.js dari skill pptx)
NODE_PATH=<node_modules berisi pptxgenjs> APPLY_THEME=<path apply_theme.js> node buat_slide.js
```

## Ke Google Docs

Unggah `Paper_PRE02_Pustaka_Data.docx` ke Google Drive → klik kanan → **Buka dengan → Google Dokumen**.

## Sebelum submit

| No | Yang perlu dilakukan tim |
| :---: | :--- |
| 1 | Tempel isi ke file template asli agar kop jurnal, logo, dan tata letak dua kolom persis sama; rumus dibuat ulang dengan *equation editor* agar nomornya rata kanan |
| 2 | Lengkapi afiliasi (template meminta jurusan dan nomor WhatsApp) dan baris *Submitted/Reviewed/Accepted* diisi redaksi |
| 3 | Cek ulang tiga DOI yang belum aktif di doi.org per 12 Nov 2026 (Haekal, Mandapatti, Ananta; lihat `Verifikasi_Literatur.md`). Di naskah, DOI Haekal dan Mandapatti tidak dicantumkan |
| 4 | Template meminta rujukan dikelola dengan Mendeley/Zotero; daftar di sini sudah urut dan lengkap, bisa diimpor bila redaksi memintanya |

## Checklist Pertemuan 8 (`progres_penelitian_MP.md`)

- [x] **Penyusunan paper lengkap (IMRAD):** struktur baku template (Pendahuluan, Metode Penelitian, Hasil dan Pembahasan, Kesimpulan), 7 halaman.
- [x] **Penyempurnaan bahasa ilmiah dan sitasi:** sitasi bernomor sesuai urutan muncul, semua rujukan terverifikasi, tanpa bullet di isi, kesimpulan tanpa sitasi.
- [x] **Abstrak dan daftar pustaka:** Abstract (196 kata) + Abstrak (177 kata), 28 rujukan.
- [x] **Paper ilmiah final** (draf siap tempel ke template) dan **slide presentasi hasil penelitian**.
