# 04_implemen_desain_eksperimen
## Capaian Pertemuan 4 (Implementasi Desain Eksperimen) dan Pertemuan 5 (Pelaksanaan Eksperimen) — versi 2
**Topik:** PRE-02 — Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas
**Studi Kasus:** 8 subproyek Super ERP Farm Nation Enterprise (FNE) 2026

Versi 2 (November 2026) menggantikan versi September 2026 setelah revisi dosen 7 Oktober 2026: data kini berasal
dari simulasi jadwal & risiko PMP (`../06_simulasi_iterasi/dataset_ml/`), bukan dataset 26 modul. Versi 1 tetap ada di
riwayat git.

---

### Struktur berkas

| Berkas | Isi | Status |
| :--- | :--- | :--- |
| [`01_Flow_dan_Skenario_Eksperimen.md`](01_Flow_dan_Skenario_Eksperimen.md) | **Desain eksperimen versi 2**: flowchart, variabel, Skenario 0–7, protokol validasi, hyperparameter, metrik, peringatan dini | Aktif |
| [`experiment_pipeline.py`](experiment_pipeline.py) | Script eksperimen versi 2 (scikit-learn): Skenario 0–7, validasi *leave-one-subproject-out*, kalibrasi, evaluasi, grafik, ringkasan otomatis | Aktif |
| [`uji_pipeline.py`](uji_pipeline.py) | Uji pipeline (desain Bagian 9.3): pemisahan data, pembanding naif, label acak, arah koefisien, konsistensi luaran, reproduksi | Aktif |
| [`hasil_eksperimen/`](hasil_eksperimen/) | Luaran eksperimen (tabel CSV, grafik, ringkasan, log) | Aktif (luaran Pertemuan 5) |
| [`analisis_data.py`](analisis_data.py) | Analisis data Pertemuan 6: CI *bootstrap*, uji hipotesis H1–H5, dekomposisi Brier, analisis ambang & deteksi dini, per subproyek, kepentingan fitur model rekomendasi | Aktif |
| [`uji_analisis.py`](uji_analisis.py) | Uji analisis: konsistensi dengan Pertemuan 5, metrik berbobot, kalibrasi logistik, CI, dekomposisi Brier, prosedur uji, ambang, reproduksi | Aktif |
| [`hasil_analisis/`](hasil_analisis/) | Luaran analisis (tabel CSV, grafik, ringkasan) | Aktif (luaran Pertemuan 6) |
| [`../draft/Bab_III_Metodologi_Penelitian.md`](../draft/Bab_III_Metodologi_Penelitian.md) | Draf Bab III versi baru (+ 3.11 hipotesis & teknik analisis) | Aktif (draf) |
| [`../draft/Bab_IV_Hasil_Penelitian.md`](../draft/Bab_IV_Hasil_Penelitian.md) | Draf Bab IV Hasil Penelitian | Aktif (draf) |
| [`02_Draft_Metodologi_Eksperimen_Bab3.md`](02_Draft_Metodologi_Eksperimen_Bab3.md) | Draf Bab III versi 1 (dataset 26 modul) | Arsip, digantikan `../draft/` |
| [`generate_pertemuan4_pptx.py`](generate_pertemuan4_pptx.py), [`PRE02_Pertemuan4_Implementasi_Desain_Eksperimen.pptx`](PRE02_Pertemuan4_Implementasi_Desain_Eksperimen.pptx) | Slide presentasi Pertemuan 4 versi 1 | Arsip; generator membaca berkas hasil versi 1 sehingga tidak kompatibel dengan luaran versi 2 |

---

### Cara menjalankan

```bash
pip install numpy pandas scikit-learn matplotlib joblib

# 1) Dataset (sudah tersedia; jalankan ulang hanya bila simulasi berubah) — dari folder 06_simulasi_iterasi/
python buat_dataset_ml.py
python uji_dataset_ml.py
python buat_dataset_ml.py --faktor-dampak 0.2 --keluaran dataset_ml/sensitivitas/dataset_ml_faktor_0.2.csv
python buat_dataset_ml.py --faktor-dampak 1.0 --keluaran dataset_ml/sensitivitas/dataset_ml_faktor_1.0.csv

# 2) Eksperimen — dari folder ini
python experiment_pipeline.py --sensitivitas   # Skenario 0–7, beberapa menit (paralel semua inti CPU)
python uji_pipeline.py --reproduksi            # uji pipeline + jalan ulang untuk reproduksi

# 3) Analisis data (Pertemuan 6) — dari folder ini, setelah langkah 2
python analisis_data.py                        # ± 3 menit
python uji_analisis.py --reproduksi            # uji analisis + jalan ulang untuk reproduksi
```

### Luaran di `hasil_eksperimen/`

| Berkas | Isi |
| :--- | :--- |
| `00_RINGKASAN_TEMUAN_EKSPERIMEN.md` | Ringkasan semua skenario (digenerate otomatis dari angka) |
| `log_pelaksanaan_eksperimen.md` | Lingkungan, MD5 dataset, durasi tiap model, model rekomendasi (digenerate otomatis) |
| `tabel_metrik_evaluasi.csv` | Skenario 0–5: Brier, BSS, Log Loss, ECE, ROC-AUC, ambang Youden, recall, specificity, precision, F1, confusion matrix, penanda rekomendasi |
| `tabel_metrik_per_titik.csv` | Skenario 6: metrik per titik monitoring 25/50/75% |
| `tabel_metrik_per_subproyek.csv` | Metrik per subproyek uji |
| `tabel_zona_peringatan.csv` | Zona Hijau/Kuning/Merah & ambang θ* per subproyek × titik |
| `tabel_feature_importance.csv` | Koefisien LR, MDI RF, permutation importance RF |
| `tabel_sensitivitas.csv` | Skenario 7 |
| `tabel_prediksi_oof.csv` | Prediksi out-of-fold setiap baris untuk 13 kombinasi model × kalibrasi |
| `kurva_roc_perbandingan.png`, `kurva_kalibrasi_probabilitas.png`, `feature_importance_comparison.png`, `metrik_per_titik.png` | Grafik |

---

### Checklist Pertemuan 4 (`progres_penelitian_MP.md`)

- [x] **Implementasi metode sesuai instruksi:** 4 model probabilistik + kalibrasi Platt & Isotonic sesuai `Deskripsi_Penelitian.md`.
- [x] **Penyusunan skenario eksperimen:** Skenario 1–5 sesuai Deskripsi Penelitian + 0 (pembanding naif), 6 (per titik), 7 (sensitivitas).
- [x] **Parameter & variabel kontrol:** 7 fitur & label terdokumentasi; hyperparameter tetap; seed 42; validasi per subproyek.
- [x] **Flow eksperimen:** `01_Flow_dan_Skenario_Eksperimen.md` Bagian 2.
- [x] **Script/tools eksperimen:** `experiment_pipeline.py` + `uji_pipeline.py`.
- [x] **Draf bagian metodologi:** `../draft/Bab_III_Metodologi_Penelitian.md` (draf awal).

### Checklist Pertemuan 5

- [x] **Eksekusi eksperimen & pengumpulan luaran:** `hasil_eksperimen/`.
- [x] **Validasi awal hasil:** `uji_pipeline.py`.
- [x] **Dataset hasil eksperimen & log pelaksanaan:** `tabel_prediksi_oof.csv`, `log_pelaksanaan_eksperimen.md`.

### Luaran di `hasil_analisis/` (Pertemuan 6)

| Berkas | Isi |
| :--- | :--- |
| `00_RINGKASAN_ANALISIS.md` | Ringkasan semua analisis (digenerate otomatis dari angka) |
| `tabel_keputusan_hipotesis.csv` | Keputusan H1–H5, kriteria, rincian, konsistensi antarsubproyek |
| `tabel_uji_hipotesis.csv` | 17 uji selisih berpasangan: selisih, CI 95%, p bootstrap, p Holm, subproyek searah, p Wilcoxon |
| `tabel_uji_rekomendasi.csv` | Model rekomendasi vs kombinasi terbaik kedua (dua arah) |
| `tabel_ci_metrik.csv` | Brier, BSS, Log Loss, ECE, ROC-AUC, intercept & slope kalibrasi dengan CI 95% (13 kombinasi) |
| `tabel_ci_per_titik.csv`, `tabel_perubahan_antartitik.csv` | Metrik per titik monitoring dengan CI; perubahan antartitik dengan CI |
| `tabel_dekomposisi_brier.csv` | Reliability, resolution, uncertainty (Murphy) |
| `tabel_analisis_ambang.csv` | Recall, specificity, precision, F1 untuk ambang 0,05–0,95, θ*, 0,35, 0,65 (keseluruhan & per titik) |
| `tabel_deteksi_dini.csv` | Persentase kumulatif proyek telat yang sudah diperingatkan & peringatan palsu s.d. 25/50/75% |
| `tabel_analisis_subproyek.csv`, `tabel_profil_subproyek.csv` | Kinerja model rekomendasi per subproyek; rata-rata fitur per subproyek |
| `tabel_kepentingan_fitur_rekomendasi.csv` | Permutation importance model rekomendasi per lipatan |
| `grafik_uji_hipotesis.png`, `grafik_dekomposisi_brier.png`, `grafik_metrik_per_titik_ci.png`, `grafik_analisis_ambang.png`, `grafik_deteksi_dini.png` | Grafik |

### Checklist Pertemuan 6 (`progres_penelitian_MP.md`)

- [x] **Penerapan teknik analisis data:** CI *bootstrap* klaster, uji selisih berpasangan + Holm, Wilcoxon antarsubproyek, dekomposisi Murphy, intercept & slope kalibrasi (`analisis_data.py`).
- [x] **Pembuatan tabel & grafik:** `hasil_analisis/`.
- [x] **Pengujian hipotesis/evaluasi performa:** H1–H5, satu per eksperimen di `Deskripsi_Penelitian.md` §4 (`tabel_keputusan_hipotesis.csv`).
- [x] **Draft bagian results:** `../draft/Bab_IV_Hasil_Penelitian.md`.
