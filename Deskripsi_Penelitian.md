## 1. Deskripsi Penelitian

Penelitian ini bertujuan untuk membangun model yang dapat memprediksi probabilitas suatu proyek akan mengalami keterlambatan berdasarkan kondisi aktual pada tahap monitoring dan evaluasi.

Berbeda dengan pendekatan klasifikasi yang hanya memberikan label risiko, model ini menghasilkan probabilitas numerik yang menunjukkan seberapa besar kemungkinan proyek terlambat. Probabilitas ini memberikan informasi yang lebih kaya bagi project manager untuk pengambilan keputusan.

Model ini berfungsi sebagai early warning system yang dapat memperingatkan project manager ketika probabilitas keterlambatan suatu proyek melewati ambang batas tertentu, sehingga tindakan korektif dapat segera diambil.

---

## 2. Variabel Penelitian

### Variabel Bebas (Features):
Kondisi aktual proyek pada tahap monitoring yg meliputi:
* Progres actual dibandingkan rencana
* Sisa waktu hingga deadline
* Backlog yang tersisa
* Tingkat utilisasi sumber daya
* Jumlah risiko yang belum dimitigasi
* Frekuensi perubahan yang terjadi
* Kinerja dependency dengan proyek lain

### Variabel Terikat (Target):
* Probabilitas keterlambatan yang bernilai antara 0 dan 1.

---

## 3. Metodologi Penelitian

Penelitian menggunakan pendekatan supervised learning untuk klasifikasi probabilistik. Data historis dari proyek-proyek sebelumnya dikumpulkan dengan label apakah proyek tersebut mengalami keterlambatan atau tidak.

Model yang digunakan adalah model yang menghasilkan probabilitas, seperti:
* Logistic Regression
* Random Forest dengan predict_proba
* Gradient Boosting dengan predict_proba
* Neural Network dengan output sigmoid

Setiap model dilatih dengan data training dan menghasilkan probabilitas keterlambatan untuk data baru.

---

## 4. Desain Eksperimen

Jenis eksperimen yang digunakan adalah eksperimen prediksi probabilitas dengan pendekatan berbagai algoritma.

### Eksperimen Pertama: Logistic Regression
* **Tujuan:** Membangun model baseline yang menghasilkan probabilitas terkalibrasi dengan baik.
* **Input:** Data training dengan fitur-fitur kondisi proyek dan label keterlambatan.
* **Proses:** Pelatihan regresi logistik.
* **Output:** Model dengan probabilitas keterlambatan.

### Eksperimen Kedua: Random Forest dengan predict_proba
* **Tujuan:** Meningkatkan akurasi prediksi probabilitas.
* **Input:** Data training yang sama.
* **Proses:** Pelatihan Random Forest.
* **Output:** Model dengan estimasi probabilitas dari frekuensi pohon.

### Eksperimen Ketiga: Gradient Boosting dengan predict_proba
* **Tujuan:** Mencapai kalibrasi probabilitas terbaik.
* **Input:** Data training.
* **Proses:** Pelatihan Gradient Boosting.
* **Output:** Model dengan probabilitas terkalibrasi.

### Eksperimen Keempat: Neural Network dengan output sigmoid
* **Tujuan:** Menangkap pola non-linear untuk prediksi probabilitas.
* **Input:** Data training dengan arsitektur jaringan.
* **Proses:** Pelatihan Neural Network.
* **Output:** Model dengan probabilitas keterlambatan.

### Eksperimen Kelima: Analisis Kalibrasi Probabilitas
* **Tujuan:** Memastikan probabilitas yang dihasilkan akurat dan terkalibrasi.
* **Input:** Probabilitas prediksi dan hasil aktual.
* **Proses:** Analisis calibration curve.
* **Output:** Rekomendasi model dengan kalibrasi terbaik.

---

## 5. Metrik Evaluasi

### Metrik Evaluasi:
* Brier Score yang mengukur akurasi probabilitas
* Log Loss atau cross-entropy
* Area Under ROC Curve untuk kemampuan diskriminasi
* Calibration curve untuk menilai kalibrasi probabilitas
* Expected Calibration Error

### Analisis Tambahan:
* Threshold analysis untuk menentukan ambang batas peringatan dini yang optimal.

---

## 6. Kontribusi Ilmiah

* Kontribusi utama penelitian ini adalah menghasilkan early warning system yang memberikan probabilitas keterlambatan secara kuantitatif dan terkalibrasi.
* Penelitian ini membantu project manager dalam mengidentifikasi proyek yang berisiko tinggi secara lebih dini.
* Selain itu, penelitian ini menyediakan informasi probabilitas yang dapat digunakan untuk pengambilan keputusan berbasis risiko.
* Kontribusi lainnya adalah menyediakan kerangka monitoring prediktif yang dapat diintegrasikan ke dalam sistem manajemen proyek.