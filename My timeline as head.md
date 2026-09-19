Sebagai **Lead Author / Penanggung Jawab Paper**, peranmu sangat krusial! Kamu adalah "sutradara" yang menyusun narasi ilmiah, menentukan struktur paper, dan memberi arahan teknis kepada Teman B (bagian data) agar hasil kodingannya sesuai dengan kebutuhan Bab 1 sampai Bab 4/5.

Karena target kalian adalah maju **sekali sekaligus untuk Progress 1–5 dalam 1 minggu**, berikut adalah **pembagian peran & alur kerja konkret** yang bisa kamu lakukan hari demi hari:

---

- [ ] 
### 🗓️ Roadmap Kerja Kamu (Lead Author) dalam 1 Minggu

#### **Hari 1–2: Penguncian Bab 1 & Penyusunan Bab 2 (Studi Literatur)**

- **Yang Kamu Kerjakan**:
    1. **Bab 1 (Pendahuluan)**: Pindahkan poin-poin Latar Belakang, Tujuan, Manfaat, Batasan, dan Variabel dari slide **Progress 1** yang sudah kita buat sebelumnya ke dalam draf Word/Paper.
    2. **Bab 2 (Tinjauan Pustaka & Research Gap)**:
        - Cari 5–10 paper/jurnal terkait _Machine Learning for Project Delay / Schedule Overrun Prediction_.
        - Buat **Tabel Matriks Literatur** (Kolom: Penulis, Metode, Variabel, Hasil, Celah/Research Gap).
        - **Tuliskan _Research Gap_-nya**: Jelaskan bahwa penelitian PRE-02 kalian berfokus pada **probabilitas numerik terkalibrasi (0–1)** pada multiproyek ERP terintegrasi dengan keterbatasan sumber daya, bukan cuma klasifikasi biner biasa (Terlambat/Tidak).

---
- [ ] 
#### **Hari 3–4: Penyusunan Bab 3 (Metodologi) & Memberi Instroksi ke Teman B**

- **Yang Kamu Kerjakan**:
    1. **Tulis Bab 3 (Metodologi)**:
        - Jelaskan alur penelitian (dari ekstraksi data PMP, _preprocessing_, _training_ model, hingga evaluasi).
        - Jabarkan definisi operasional variabel \(X\) (fitur-fitur PMP) dan \(Y\) (target probabilitas).
    2. **Pengarahan ke Teman B**:
        - Berikan file **`dataset_pre02_fne.csv`** yang sudah diterbitkan tadi ke Teman B.
        - Minta Teman B untuk mengeksekusi model Machine Learning di Python menggunakan algoritma yang disepakati (misal: _Logistic Regression_ & _Random Forest_ `predict_proba`).
        - **Minta Output Spesifik dari Teman B**:
            - [ ] Tabel performa model (Akurasi, Precision, Recall, ROC-AUC Score, Brier Score).
            - [ ] Gambar **ROC Curve** & **Confusion Matrix**.
            - [ ] Gambar **Feature Importance** (grafik bar yang menunjukkan fitur mana yang paling memicu keterlambatan).

---
- [ ] 
#### **Hari 5: Bab 4 (Pembahasan & Interpretasi Hasil Eksperimen)**

- **Yang Kamu Kerjakan**:
    1. Ambil tabel dan grafik hasil olahan dari Teman B.
    2. **Tuliskan Narasi Hasilnya di Bab 4**:
        - Jelaskan seberapa akurat model memprediksi keterlambatan (misal: _"Model Random Forest menghasilkan ROC-AUC sebesar 0.88..."_).
        - Bahas _Feature Importance_-nya (misal: _"Fitur `Resource_Utilization_Rate` dan `Predecessor_Count` menjadi pemicu utama probabilitas keterlambatan proyek FNE..."_).
        - Berikan contoh kasus: tunjukkan 1–2 task dari dataset FNE yang memiliki nilai probabilitas keterlambatan tinggi (misal \(P > 0.75\)) beserta rekomendasi mitigasinya bagi Project Manager.

---
- [ ] 
#### **Hari 6–7: Finishing, Pembundelan Paper & Slide Presentasi Gabungan (Progress 1–5)**

- **Yang Kamu Kerjakan**:
    1. **Integrasi Paper**: Gabungkan Bab 1, Bab 2, Bab 3, dan Bab 4 menjadi 1 file naskah/paper yang rapi.
    2. **Buat Deck Slide Presentasi 1–5**: Susun slide presentasi ringkas (10–12 slide) untuk ditunjukkan ke dosen, dengan urutan:
        - _Slide 1–3_: Progress 1 (Latar Belakang, Tujuan, Variabel).
        - _Slide 4–5_: Progress 2 (Matriks Literatur & Research Gap).
        - _Slide 6–7_: Progress 3 (Struktur Dataset & Preprocessing).
        - _Slide 8–9_: Progress 4 (Desain Eksperimen & Flowchart ML).
        - _Slide 10–12_: Progress 5 (Hasil ROC-AUC, Feature Importance & Analisis Probabilitas).
    3. Simulasi presentasi bersama Teman B sebelum maju ke dosen.

---

### 📋 Checklist Perintah yang Bisa Kamu Berikan ke Teman B Hari Ini:

> _"Bro/Sist, ini file `dataset_pre02_fne.csv` yang mau kita pake. Tugas kamu di Python:_
> 
> 1. _Bagi data jadi Train (80%) dan Test (20%)._
> 2. _Jalankan model Logistic Regression sama Random Forest pake `predict_proba`._
> 3. _Tolong kirimin aku:_
>     - _Nilai ROC-AUC Score & Brier Score._
>     - _Plot grafik ROC Curve & Feature Importance._
>     - _Tabel hasil prediksi probabilitasnya (\(P(\text{Delay})\))._
> 
> _Nanti gambar sama angkanya bakal aku narasiin dan masukin ke Bab 3, Bab 4, sama Slide Presentasi Progress 1–5 kita."_

---

💡 Apakah kamu butuh bantuan untuk **menyiapkan draf naskah Bab 2 (Tabel Matriks Literatur & Research Gap)** atau **format outline laporan Bab 1–4** dulu untuk mulai mencicil ketikanmu?