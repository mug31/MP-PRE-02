# RINGKASAN TEMUAN EKSPERIMEN PRE-02
## Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas

> Dokumen ini digenerate otomatis oleh `experiment_pipeline.py`; seluruh angka dan kalimat temuan diturunkan langsung dari hasil eksperimen.

**Dataset:** N = 26 task (16 Delay : 10 On-Time). **Protokol:** Stratified 5-Fold Cross-Validation, seed 42, standardisasi per fold, kalibrasi dilatih pada inner 3-fold di dalam fold training.

### 1. Tabel Kinerja Evaluasi 5-Fold Cross-Validation

| Model Algoritma | Kalibrasi | ROC-AUC | Brier Score | Log Loss | ECE | Akurasi | Recall | Specificity | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | Raw | 1.0000 | 0.0254 | 0.1133 | 0.0943 | 96.2% | 1.000 | 0.900 | 0.9697 |
| Logistic Regression (Baseline) | Platt | 0.9938 | 0.0290 | 0.1336 | 0.0798 | 96.2% | 1.000 | 0.900 | 0.9697 |
| Logistic Regression (Baseline) | Isotonic | 0.9156 | 0.0772 | 2.6603 | 0.0736 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Random Forest | Raw | 0.9938 | 0.0391 | 0.1367 | 0.0640 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Random Forest | Platt | 0.9938 | 0.0459 | 0.1780 | 0.1040 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Random Forest | Isotonic | 0.9188 | 0.0769 | 2.6569 | 0.0769 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Gradient Boosting | Raw | 0.9375 | 0.0931 | 0.4789 | 0.0977 | 88.5% | 0.875 | 0.900 | 0.9032 |
| Gradient Boosting | Platt | 0.8813 | 0.0889 | 0.3278 | 0.0709 | 88.5% | 0.875 | 0.900 | 0.9032 |
| Gradient Boosting | Isotonic | 0.8625 | 0.1120 | 2.7878 | 0.0749 | 88.5% | 0.938 | 0.800 | 0.9091 |
| **MLP Neural Network** | Raw | 1.0000 | 0.0007 | 0.0079 | 0.0075 | 100.0% | 1.000 | 1.000 | 1.0000 |
| MLP Neural Network | Platt | 1.0000 | 0.0164 | 0.1049 | 0.0947 | 100.0% | 1.000 | 1.000 | 1.0000 |
| MLP Neural Network | Isotonic | 1.0000 | 0.0016 | 0.0114 | 0.0106 | 100.0% | 1.000 | 1.000 | 1.0000 |

*Metrik klasifikasi (Akurasi, Recall, Specificity, F1) dihitung pada ambang batas 0.5. Baris tebal = model rekomendasi.*

### 2. Temuan Kunci

1. **Kekuatan Diskriminasi (ROC-AUC, output mentah):** ROC-AUC tertinggi dicapai oleh Logistic Regression (Baseline) dan MLP Neural Network (1.0000); terendah Gradient Boosting (0.9375).
2. **Kualitas Probabilitas sebelum kalibrasi:** Brier Score terendah dimiliki MLP Neural Network (Brier = 0.0007, ECE = 0.0075).
3. **Efek Kalibrasi (Brier Score Raw → Platt → Isotonic):**
   - Logistic Regression (Baseline): 0.0254 → 0.0290 → 0.0772
   - Random Forest: 0.0391 → 0.0459 → 0.0769
   - Gradient Boosting: 0.0931 → 0.0889 → 0.1120
   - MLP Neural Network: 0.0007 → 0.0164 → 0.0016
4. **Rekomendasi model dengan kalibrasi terbaik:** MLP Neural Network (tanpa kalibrasi) (Brier = 0.0007, ECE = 0.0075, Log Loss = 0.0079, ROC-AUC = 1.0000).
5. **Prediktor Dominan (Feature Importance RF, MDI):** dua fitur dengan bobot tertinggi adalah `SPI_Value` (0.335) dan `Risk_Score` (0.274).
6. **Threshold Analysis (Youden J):** pada model rekomendasi, ambang optimal θ* = 0.4830 (J = 1.000; Sensitivity = 1.000; Specificity = 1.000).
7. **Early Warning System (Hijau < 0.35, Kuning 0.35–0.65, Merah ≥ 0.65), model rekomendasi:** zona Merah menangkap 16 dari 16 modul yang aktual terlambat dengan 0 alarm palsu; zona Kuning berisi 0 modul terlambat dan 0 modul tepat waktu; 0 modul terlambat lolos ke zona Hijau.

### 3. Validasi Pembanding: Hold-out Stratified 80:20

n_train = 21, n_test = 5. Karena data uji hanya 5 task, hasil ini bersifat indikatif dan tidak dipakai untuk pemilihan model (detail: `tabel_metrik_holdout_80_20.csv`).

| Model Algoritma | Kalibrasi | ROC-AUC | Brier Score | Akurasi |
| :--- | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | Raw | 1.0000 | 0.0113 | 100.0% |
| Logistic Regression (Baseline) | Platt | 1.0000 | 0.0163 | 100.0% |
| Logistic Regression (Baseline) | Isotonic | 1.0000 | 0.0000 | 100.0% |
| Random Forest | Raw | 1.0000 | 0.0081 | 100.0% |
| Random Forest | Platt | 1.0000 | 0.0272 | 100.0% |
| Random Forest | Isotonic | 1.0000 | 0.0006 | 100.0% |
| Gradient Boosting | Raw | 1.0000 | 0.0000 | 100.0% |
| Gradient Boosting | Platt | 1.0000 | 0.0210 | 100.0% |
| Gradient Boosting | Isotonic | 1.0000 | 0.0035 | 100.0% |
| MLP Neural Network | Raw | 1.0000 | 0.0000 | 100.0% |
| MLP Neural Network | Platt | 1.0000 | 0.0074 | 100.0% |
| MLP Neural Network | Isotonic | 1.0000 | 0.0000 | 100.0% |

### 4. Catatan Keterbatasan

- Ukuran sampel sangat kecil (N = 26); tiap fold uji hanya berisi ±5 task, sehingga metrik memiliki varians tinggi.
- ROC-AUC ≈ 1.00 menunjukkan kelas hampir terpisah sempurna pada data empiris-simulatif ini; hasil perlu divalidasi pada data proyek riil sebelum digeneralisasi.
- Kalibrator dilatih pada ±20 sampel per fold; Isotonic Regression rawan overfitting pada ukuran ini, sehingga Platt Scaling lebih stabil secara teoretis (Niculescu-Mizil & Caruana, 2005).
- Pemilihan model rekomendasi dan θ* dilakukan pada prediksi out-of-fold yang sama dengan yang dilaporkan, sehingga estimasi kinerjanya sedikit optimistis.
