# Log Pelaksanaan Eksperimen PRE-02 (versi 2)

> Digenerate otomatis oleh `experiment_pipeline.py`.

- Waktu jalan: 2026-11-12 16:30, durasi total 269 detik
- Lingkungan: Python 3.13.15, scikit-learn 1.9.1, numpy 2.5.4, pandas 3.1.1, joblib 1.6.0
- Dataset: `06_simulasi_iterasi/dataset_ml/dataset_ml.csv` (MD5 `907f625a901fae02c39b83f0b035a28f`), 24000 baris
- Fitur (7): SPI_Jadwal, Sisa_Waktu_Hari, Backlog_Sisa_Persen, Utilisasi_Resource, Risiko_Belum_Dimitigasi, Frekuensi_CR, Pergeseran_Dependency_Hari
- Label: Telat_Lebih_5_Persen; grup validasi: Subproyek
- Seed: 42
- Pembagian luar: LeaveOneGroupOut (8 lipatan); pembagian dalam kalibrasi: GroupKFold(3) per subproyek
- Pemeriksaan otomatis: kolom & ukuran data sesuai kontrak; tidak ada subproyek uji di data latih; setiap baris diprediksi tepat satu kali

## Durasi per model × kalibrasi (8 lipatan, paralel)

- Pembanding Naif / Raw: 6.7 detik
- Logistic Regression / Raw: 0.5 detik
- Logistic Regression / Platt: 1.0 detik
- Logistic Regression / Isotonic: 0.8 detik
- Random Forest / Raw: 4.8 detik
- Random Forest / Platt: 13.1 detik
- Random Forest / Isotonic: 15.1 detik
- Gradient Boosting / Raw: 9.0 detik
- Gradient Boosting / Platt: 28.9 detik
- Gradient Boosting / Isotonic: 33.6 detik
- MLP Neural Network / Raw: 25.7 detik
- MLP Neural Network / Platt: 48.2 detik
- MLP Neural Network / Isotonic: 50.1 detik

## Model rekomendasi

Gradient Boosting + Raw (Brier terendah; seri: ECE, lalu Log Loss)

## Dataset sensitivitas

- faktor 0.4: `dataset_ml.csv` (MD5 `907f625a901fae02c39b83f0b035a28f`)
- faktor 0.2: `dataset_ml_faktor_0.2.csv` (MD5 `38bd59c96809f566bb340a682379db04`)
- faktor 1.0: `dataset_ml_faktor_1.0.csv` (MD5 `3960b8cd7bcc679f6c661a82a7c4cf06`)
