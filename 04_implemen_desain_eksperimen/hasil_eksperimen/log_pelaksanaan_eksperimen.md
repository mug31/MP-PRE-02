# Log Pelaksanaan Eksperimen PRE-02

Luaran Pertemuan 5 — *log pelaksanaan eksperimen*. Dokumen ini mencatat eksekusi pipeline, luaran
yang dihasilkan, serta hasil verifikasi replikasi.

---

## 1. Identitas Eksekusi

| Butir | Keterangan |
| :--- | :--- |
| Skrip yang dijalankan | `04_implemen_desain_eksperimen/experiment_pipeline.py` |
| Dataset masukan | `dataset_pre02_fne_v3.csv` (26 baris × 7 fitur + 1 label; revisi durasi & effort hasil penelusuran ulang ke PMP) |
| Perintah | `python experiment_pipeline.py` |
| Seed acak | 42 (dikunci pada partisi fold, bootstrap Random Forest, subsample Gradient Boosting, dan inisialisasi bobot MLP) |
| Lingkungan verifikasi | Python 3.12.14, NumPy 2.5.3, Matplotlib 3.11.2 (Linux) |
| Durasi eksekusi | ± 22 detik |
| Status akhir | Berhasil (exit code 0, tanpa keluaran galat) |
| Tanggal verifikasi replikasi | 30 September 2026 (eksekusi ulang atas dataset v3) |

---

## 2. Tahapan yang Tercatat Selama Eksekusi

1. **Pemuatan data** — 26 baris task modul Super ERP FNE terbaca; distribusi kelas Delay = 1 sebanyak
   16 task (61.5%) dan Delay = 0 sebanyak 10 task (38.5%).
2. **Partisi Stratified 5-Fold** — rasio kelas dipertahankan pada setiap lipatan; ±5 task uji per lipatan.
3. **Standardisasi per fold** — `StandardScaler` dilatih hanya pada data latih tiap lipatan.
4. **Pelatihan 4 model** — Logistic Regression, Random Forest, Gradient Boosting, dan MLP Neural Network.
5. **Kalibrasi** — Platt Scaling dan Isotonic Regression dilatih pada inner 3-fold di dalam data latih,
   menghasilkan 12 kombinasi model × kalibrasi.
6. **Evaluasi out-of-fold** — ROC-AUC, Brier Score, Log Loss, ECE (5 bin), akurasi, recall, specificity, F1.
7. **Pemilihan model rekomendasi** — kombinasi dengan Brier Score terendah:
   **MLP Neural Network tanpa kalibrasi** (Brier 0.0007).
8. **Threshold analysis** — ambang optimal Youden `θ* = 0.4830` (J = 1.000; sensitivity 1.000;
   specificity 1.000).
9. **Validasi pembanding** — hold-out stratified 80:20 (n_train = 21, n_test = 5), bersifat indikatif.
10. **Ekspor luaran** — 4 tabel CSV, 3 grafik PNG, dan 1 dokumen ringkasan temuan.

### Ringkasan metrik yang tercetak saat eksekusi

| Model | Kalibrasi | ROC-AUC | Brier | Log Loss | ECE | Akurasi | F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | Raw | 1.0000 | 0.0254 | 0.1133 | 0.0943 | 96.2% | 0.9697 |
| Logistic Regression (Baseline) | Platt | 0.9938 | 0.0290 | 0.1336 | 0.0798 | 96.2% | 0.9697 |
| Logistic Regression (Baseline) | Isotonic | 0.9156 | 0.0772 | 2.6603 | 0.0736 | 92.3% | 0.9375 |
| Random Forest | Raw | 0.9938 | 0.0391 | 0.1367 | 0.0640 | 92.3% | 0.9375 |
| Random Forest | Platt | 0.9938 | 0.0459 | 0.1780 | 0.1040 | 92.3% | 0.9375 |
| Random Forest | Isotonic | 0.9188 | 0.0769 | 2.6569 | 0.0769 | 92.3% | 0.9375 |
| Gradient Boosting | Raw | 0.9375 | 0.0931 | 0.4789 | 0.0977 | 88.5% | 0.9032 |
| Gradient Boosting | Platt | 0.8813 | 0.0889 | 0.3278 | 0.0709 | 88.5% | 0.9032 |
| Gradient Boosting | Isotonic | 0.8625 | 0.1120 | 2.7878 | 0.0749 | 88.5% | 0.9091 |
| **MLP Neural Network** | **Raw** | **1.0000** | **0.0007** | **0.0079** | **0.0075** | **100.0%** | **1.0000** |
| MLP Neural Network | Platt | 1.0000 | 0.0164 | 0.1049 | 0.0947 | 100.0% | 1.0000 |
| MLP Neural Network | Isotonic | 1.0000 | 0.0016 | 0.0114 | 0.0106 | 100.0% | 1.0000 |

---

## 3. Luaran yang Dihasilkan

| Berkas | Isi | SHA-256 (16 karakter awal) |
| :--- | :--- | :--- |
| `tabel_metrik_evaluasi.csv` | Metrik 12 kombinasi model × kalibrasi (5-fold CV) | `4dfc4d131ac93e33` |
| `tabel_metrik_holdout_80_20.csv` | Metrik pembanding hold-out 80:20 | `670eaf192e5b7fd4` |
| `tabel_feature_importance.csv` | Bobot MDI 7 fitur dari Random Forest | `69ed9addfaaa492d` |
| `tabel_prediksi_probabilitas_task.csv` | P(Delay) per task dan zona EWS | `8ccde14365256982` |
| `kurva_roc_perbandingan.png` | Kurva ROC 4 algoritma | `5d2f2cfca4e686ab` |
| `kurva_kalibrasi_probabilitas.png` | Diagram reliabilitas (5 bin) | `d41795c1e733b259` |
| `feature_importance_comparison.png` | Diagram batang feature importance | `f8a9a4bb72f10a0b` |
| `00_RINGKASAN_TEMUAN_EKSPERIMEN.md` | Ringkasan temuan yang digenerate dari angka hasil | `70e620bdd96330da` |

---

## 4. Verifikasi Replikasi

Pipeline dijalankan ulang pada 30 September 2026 di direktori terpisah menggunakan salinan skrip dan
dataset yang sama. Kedelapan berkas luaran dibandingkan terhadap berkas yang tersimpan di repositori:

- Empat berkas CSV dan dokumen ringkasan: **identik** (perbandingan isi).
- Tiga berkas grafik PNG: **identik** (perbandingan byte per byte).

Dengan demikian eksperimen bersifat **deterministik dan dapat direplikasi penuh** pada konfigurasi
seed 42. Pemeriksaan ini juga menegaskan bahwa seluruh angka pada dokumen ringkasan, draft Bab III,
dan slide presentasi berasal dari eksekusi yang sama.

---

## 5. Catatan Pelaksanaan

- Eksekusi tidak memunculkan peringatan konvergensi maupun galat numerik.
- Seluruh model diimplementasikan ulang dengan NumPy; hasil Logistic Regression, Platt, Isotonic, dan
  perhitungan ROC-AUC telah dicocokkan terhadap scikit-learn pada tahap pengembangan pipeline.
- Ukuran sampel yang kecil (N = 26) membuat tiap lipatan uji hanya berisi ±5 task; keterbatasan ini
  dicatat pada `00_RINGKASAN_TEMUAN_EKSPERIMEN.md` bagian Catatan Keterbatasan.

---

tags #paper #mp #academic #research #eksperimen
