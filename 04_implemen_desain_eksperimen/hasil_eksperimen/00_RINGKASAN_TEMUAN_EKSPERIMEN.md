# RINGKASAN TEMUAN EKSPERIMEN PRE-02
## Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas

> Dokumen ini digenerate otomatis oleh `experiment_pipeline.py`; seluruh angka dan kalimat temuan diturunkan langsung dari hasil eksperimen.

**Dataset:** N = 26 task (16 Delay : 10 On-Time). **Protokol:** Stratified 5-Fold Cross-Validation, seed 42, standardisasi per fold, kalibrasi dilatih pada inner 3-fold di dalam fold training.

### 1. Tabel Kinerja Evaluasi 5-Fold Cross-Validation

| Model Algoritma | Kalibrasi | ROC-AUC | Brier Score | Log Loss | ECE | Akurasi | Recall | Specificity | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | Raw | 1.0000 | 0.0273 | 0.1158 | 0.0570 | 96.2% | 1.000 | 0.900 | 0.9697 |
| Logistic Regression (Baseline) | Platt | 1.0000 | 0.0317 | 0.1427 | 0.0749 | 96.2% | 1.000 | 0.900 | 0.9697 |
| Logistic Regression (Baseline) | Isotonic | 0.9656 | 0.0724 | 1.4366 | 0.0746 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Random Forest | Raw | 0.9875 | 0.0421 | 0.1446 | 0.0812 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Random Forest | Platt | 1.0000 | 0.0696 | 0.2418 | 0.1224 | 96.2% | 1.000 | 0.900 | 0.9697 |
| Random Forest | Isotonic | 0.9156 | 0.0801 | 2.6700 | 0.0881 | 92.3% | 0.938 | 0.900 | 0.9375 |
| Gradient Boosting | Raw | 0.9031 | 0.0973 | 0.4888 | 0.1011 | 88.5% | 0.875 | 0.900 | 0.9032 |
| Gradient Boosting | Platt | 0.8656 | 0.0936 | 0.3491 | 0.0714 | 88.5% | 0.875 | 0.900 | 0.9032 |
| Gradient Boosting | Isotonic | 0.8781 | 0.1007 | 2.7513 | 0.0592 | 88.5% | 0.875 | 0.900 | 0.9032 |
| **MLP Neural Network** | Raw | 1.0000 | 0.0127 | 0.0341 | 0.0233 | 96.2% | 1.000 | 0.900 | 0.9697 |
| MLP Neural Network | Platt | 1.0000 | 0.0216 | 0.1150 | 0.0990 | 96.2% | 1.000 | 0.900 | 0.9697 |
| MLP Neural Network | Isotonic | 1.0000 | 0.0138 | 0.0356 | 0.0234 | 96.2% | 1.000 | 0.900 | 0.9697 |

*Metrik klasifikasi (Akurasi, Recall, Specificity, F1) dihitung pada ambang batas 0.5. Baris tebal = model rekomendasi.*

### 2. Temuan Kunci

1. **Kekuatan Diskriminasi (ROC-AUC, output mentah):** ROC-AUC tertinggi dicapai oleh Logistic Regression (Baseline) dan MLP Neural Network (1.0000); terendah Gradient Boosting (0.9031).
2. **Kualitas Probabilitas sebelum kalibrasi:** Brier Score terendah dimiliki MLP Neural Network (Brier = 0.0127, ECE = 0.0233).
3. **Efek Kalibrasi (Brier Score Raw → Platt → Isotonic):**
   - Logistic Regression (Baseline): 0.0273 → 0.0317 → 0.0724
   - Random Forest: 0.0421 → 0.0696 → 0.0801
   - Gradient Boosting: 0.0973 → 0.0936 → 0.1007
   - MLP Neural Network: 0.0127 → 0.0216 → 0.0138
4. **Rekomendasi model dengan kalibrasi terbaik:** MLP Neural Network (tanpa kalibrasi) (Brier = 0.0127, ECE = 0.0233, Log Loss = 0.0341, ROC-AUC = 1.0000).
5. **Prediktor Dominan (Feature Importance RF, MDI):** dua fitur dengan bobot tertinggi adalah `SPI_Value` (0.310) dan `Risk_Score` (0.307).
6. **Threshold Analysis (Youden J):** pada model rekomendasi, ambang optimal θ* = 0.7789 (J = 1.000; Sensitivity = 1.000; Specificity = 1.000).
7. **Early Warning System (Hijau < 0.35, Kuning 0.35–0.65, Merah ≥ 0.65), model rekomendasi:** zona Merah menangkap 16 dari 16 modul yang aktual terlambat dengan 0 alarm palsu; zona Kuning berisi 0 modul terlambat dan 1 modul tepat waktu; 0 modul terlambat lolos ke zona Hijau.

### 3. Validasi Pembanding: Hold-out Stratified 80:20

n_train = 21, n_test = 5. Karena data uji hanya 5 task, hasil ini bersifat indikatif dan tidak dipakai untuk pemilihan model (detail: `tabel_metrik_holdout_80_20.csv`).

| Model Algoritma | Kalibrasi | ROC-AUC | Brier Score | Akurasi |
| :--- | :---: | :---: | :---: | :---: |
| Logistic Regression (Baseline) | Raw | 1.0000 | 0.0087 | 100.0% |
| Logistic Regression (Baseline) | Platt | 1.0000 | 0.0185 | 100.0% |
| Logistic Regression (Baseline) | Isotonic | 1.0000 | 0.0000 | 100.0% |
| Random Forest | Raw | 1.0000 | 0.0045 | 100.0% |
| Random Forest | Platt | 1.0000 | 0.0474 | 100.0% |
| Random Forest | Isotonic | 1.0000 | 0.0000 | 100.0% |
| Gradient Boosting | Raw | 1.0000 | 0.0000 | 100.0% |
| Gradient Boosting | Platt | 1.0000 | 0.0210 | 100.0% |
| Gradient Boosting | Isotonic | 1.0000 | 0.0033 | 100.0% |
| MLP Neural Network | Raw | 1.0000 | 0.0000 | 100.0% |
| MLP Neural Network | Platt | 1.0000 | 0.0088 | 100.0% |
| MLP Neural Network | Isotonic | 1.0000 | 0.0000 | 100.0% |

### 4. Catatan Keterbatasan

- Ukuran sampel sangat kecil (N = 26); tiap fold uji hanya berisi ±5 task, sehingga metrik memiliki varians tinggi.
- ROC-AUC ≈ 1.00 menunjukkan kelas hampir terpisah sempurna pada data empiris-simulatif ini; hasil perlu divalidasi pada data proyek riil sebelum digeneralisasi.
- Kalibrator dilatih pada ±20 sampel per fold; Isotonic Regression rawan overfitting pada ukuran ini, sehingga Platt Scaling lebih stabil secara teoretis (Niculescu-Mizil & Caruana, 2005).
- Pemilihan model rekomendasi dan θ* dilakukan pada prediksi out-of-fold yang sama dengan yang dilaporkan, sehingga estimasi kinerjanya sedikit optimistis.
