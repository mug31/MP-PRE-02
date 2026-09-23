# 05_presentasi_progres

## Slide Presentasi Gabungan Progres Pertemuan 1–5

**Topik:** PRE-02 — Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas
**Studi Kasus:** Portofolio Modul Super ERP Farm Nation Enterprise (FNE) 2026
**Peruntukan:** sekali maju untuk menyampaikan progres Pertemuan 1 sampai 5 sekaligus (±15 menit).

---

### 📂 Berkas pada Folder Ini

| Berkas | Keterangan |
| :--- | :--- |
| `PRE02_Presentasi_Progres_Pertemuan1-5.pptx` | Dek presentasi 17 slide, format 16:9, gaya *Swiss Academic* mengikuti slide Pertemuan 4. |
| `generate_presentasi_p1_p5.py` | Script generator dek tersebut. |
| `Naskah_Presentasi_P1-P5.md` | Naskah bicara per slide (17 slide, ±15 menit) beserta pembagian peran dan kalimat transisi. |

Persiapan tanya-jawab, daftar istilah, dan rangkuman isi tiap pertemuan ada di
[[Guideline_Presentasi_Pertemuan1-5]].

---

### 🗂️ Peta Slide terhadap Output yang Diminta

| Slide | Isi | Output silabus yang dipenuhi |
| :---: | :--- | :--- |
| 1 | Sampul | — |
| 2 | Peta progres P1–P5 dan tabel pemenuhan output | Rekap seluruh pertemuan |
| 3–5 | Latar belakang, masalah, tujuan, manfaat, batasan, variabel penelitian | **P1:** slide rencana penelitian |
| 6–7 | Matriks 8 paper inti; empat lapis research gap dan posisi PRE-02 | **P2:** matriks literatur + draft tinjauan pustaka |
| 8–9 | Sumber data, preprocessing, statistik deskriptif, pola data | **P3:** dataset siap pakai, dokumentasi preprocessing, karakteristik data |
| 10–12 | Flow eksperimen, lima skenario dan parameter kontrol, protokol validasi dan metrik | **P4:** flow eksperimen, script/tools, draft metodologi |
| 13–16 | Hasil 5-fold CV, kurva ROC dan kalibrasi, feature importance, EWS dan threshold analysis | **P5:** dataset hasil eksperimen dan log pelaksanaan |
| 17 | Keterbatasan dan rencana Pertemuan 6–8 | Penutup |

Metrik evaluasi yang ditampilkan mengikuti Deskripsi Penelitian: Brier Score, Log Loss, ROC-AUC, *calibration curve*, ECE, serta *threshold analysis* sebagai analisis tambahan.

---

### 🚀 Cara Regenerasi Slide

```bash
uv run --with python-pptx python generate_presentasi_p1_p5.py
```

Seluruh angka pada slide P3 dan P5 dibaca langsung dari `dataset_pre02_fne.csv` dan folder
`04_implemen_desain_eksperimen/hasil_eksperimen/` saat script dijalankan. Jadi bila eksperimen
dijalankan ulang, cukup jalankan kembali script ini agar slide otomatis ikut terbarui — tidak ada
angka hasil yang ditulis manual di dalam script.
