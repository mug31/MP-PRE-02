# Log Pelaksanaan Eksperimen PRE-02

Luaran Pertemuan 5 — *log pelaksanaan eksperimen*. Dokumen ini mencatat eksekusi pipeline, luaran
yang dihasilkan, serta hasil verifikasi replikasi.

---

## 1. Identitas Eksekusi

| Butir | Keterangan |
| :--- | :--- |
| Skrip yang dijalankan | `04_implemen_desain_eksperimen/experiment_pipeline.py` |
| Dataset masukan | `dataset_pre02_fne.csv` (26 baris × 7 fitur + 1 label) |
| Perintah | `python experiment_pipeline.py` |
| Seed acak | 42 (dikunci pada partisi fold, bootstrap Random Forest, subsample Gradient Boosting, dan inisialisasi bobot MLP) |
| Lingkungan verifikasi | Python 3.12.14, NumPy 2.5.3, Matplotlib 3.11.2 (Linux) |
| Durasi eksekusi | ± 43 detik |
| Status akhir | Berhasil (exit code 0, tanpa keluaran galat) |
| Tanggal verifikasi replikasi | 23 September 2026 |

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
   **MLP Neural Network tanpa kalibrasi** (Brier 0.0127).
8. **Threshold analysis** — ambang optimal Youden `θ* = 0.7789` (J = 1.000; sensitivity 1.000;
   specificity 1.000).
9. **Validasi pembanding** — hold-out stratified 80:20 (n_train = 21, n_test = 5), bersifat indikatif.
10. **Ekspor luaran** — 4 tabel CSV, 3 grafik PNG, dan 1 dokumen ringkasan temuan.

### Ringkasan metrik yang tercetak saat eksekusi

| Model | Kalibrasi | ROC-AUC | Brier | Log Loss | ECE | Akurasi | F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | Raw | 1.0000 | 0.0273 | 0.1158 | 0.0570 | 96.2% | 0.9697 |
| Logistic Regression (Baseline) | Platt | 1.0000 | 0.0317 | 0.1427 | 0.0749 | 96.2% | 0.9697 |
| Logistic Regression (Baseline) | Isotonic | 0.9656 | 0.0724 | 1.4366 | 0.0746 | 92.3% | 0.9375 |
| Random Forest | Raw | 0.9875 | 0.0421 | 0.1446 | 0.0812 | 92.3% | 0.9375 |
| Random Forest | Platt | 1.0000 | 0.0696 | 0.2418 | 0.1224 | 96.2% | 0.9697 |
| Random Forest | Isotonic | 0.9156 | 0.0801 | 2.6700 | 0.0881 | 92.3% | 0.9375 |
| Gradient Boosting | Raw | 0.9031 | 0.0973 | 0.4888 | 0.1011 | 88.5% | 0.9032 |
| Gradient Boosting | Platt | 0.8656 | 0.0936 | 0.3491 | 0.0714 | 88.5% | 0.9032 |
| Gradient Boosting | Isotonic | 0.8781 | 0.1007 | 2.7513 | 0.0592 | 88.5% | 0.9032 |
| **MLP Neural Network** | **Raw** | **1.0000** | **0.0127** | **0.0341** | **0.0233** | **96.2%** | **0.9697** |
| MLP Neural Network | Platt | 1.0000 | 0.0216 | 0.1150 | 0.0990 | 96.2% | 0.9697 |
| MLP Neural Network | Isotonic | 1.0000 | 0.0138 | 0.0356 | 0.0234 | 96.2% | 0.9697 |

---

## 3. Luaran yang Dihasilkan

| Berkas | Isi | SHA-256 (16 karakter awal) |
| :--- | :--- | :--- |
| `tabel_metrik_evaluasi.csv` | Metrik 12 kombinasi model × kalibrasi (5-fold CV) | `e442386a63d3a801` |
| `tabel_metrik_holdout_80_20.csv` | Metrik pembanding hold-out 80:20 | `b0af5c1e032f2b5e` |
| `tabel_feature_importance.csv` | Bobot MDI 7 fitur dari Random Forest | `58076aab26e85ad6` |
| `tabel_prediksi_probabilitas_task.csv` | P(Delay) per task dan zona EWS | `4cc680f8bb878199` |
| `kurva_roc_perbandingan.png` | Kurva ROC 4 algoritma | `02cf64a20b8b2210` |
| `kurva_kalibrasi_probabilitas.png` | Diagram reliabilitas (5 bin) | `97f72398451dc135` |
| `feature_importance_comparison.png` | Diagram batang feature importance | `05dae53133e8ac4a` |
| `00_RINGKASAN_TEMUAN_EKSPERIMEN.md` | Ringkasan temuan yang digenerate dari angka hasil | `0574413500bea603` |

---

## 4. Verifikasi Replikasi

Pipeline dijalankan ulang pada 23 September 2026 di direktori terpisah menggunakan salinan skrip dan
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
