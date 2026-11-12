# BAB VI KESIMPULAN DAN SARAN

> **Status draf:** versi awal Pertemuan 7 (November 2026). Semua angka berasal dari Bab IV dan Bab V.

---

## 6.1 Kesimpulan

Penelitian ini membangun model yang memprediksi probabilitas keterlambatan lebih dari 5% dari *baseline* pada
delapan subproyek Super ERP Farm Nation Enterprise dengan sumber daya terbatas, berdasarkan kondisi proyek pada titik
*monitoring* 25%, 50%, dan 75%. Data historis dibangkitkan melalui simulasi iterasi random berbasis dokumen PMP dan
model diuji per subproyek. Kesimpulannya:

1. **Model terbaik.** *Gradient Boosting* tanpa kalibrasi tambahan menghasilkan probabilitas paling akurat dan paling
   terkalibrasi: Brier Score 0,1718 [0,1672; 0,1762], BSS 0,367 terhadap pembanding naif, ECE 0,0560, dan ROC-AUC
   0,815. Keunggulannya atas LR, RF, dan NN signifikan pada gabungan seluruh iterasi (H3 diterima).
2. **Perbandingan model.** *Random Forest* lebih akurat daripada *Logistic Regression* (H2 diterima). LR lebih akurat
   daripada pembanding naif, tetapi probabilitasnya terlalu ekstrem saat diterapkan ke subproyek baru (H1 diterima
   sebagian). *Neural Network* terlalu yakin dan kalah dari pembanding naif (H4 ditolak).
3. **Kalibrasi.** Platt scaling dan isotonic regression tidak memperbaiki LR, RF, maupun GB (H5 ditolak), karena
   pemetaan kalibrasi yang dipelajari dari proyek lain tidak berlaku untuk proyek baru.
4. **Waktu peringatan.** Ketepatan prediksi naik seiring berjalannya proyek (ROC-AUC GB 0,725; 0,782; 0,915 pada titik
   25%, 50%, 75%). Pada ambang 0,485, 56,7% proyek yang akhirnya terlambat sudah diperingatkan pada seperempat jadwal
   dan 81,0% sampai titik 75%, dengan peringatan palsu kumulatif 38,0% yang sebagian besar berupa proyek yang nyaris
   terlambat.
5. **Variabel penting.** SPI adalah variabel paling berpengaruh. Pergeseran *dependency*, frekuensi CR, dan risiko
   belum dimitigasi hampir tidak menambah informasi setelah SPI diketahui.
6. **Keterbatasan generalisasi.** Keunggulan antarmodel tidak konsisten di setiap subproyek, dan prediksi meleset jauh
   pada subproyek yang karakternya berbeda dari subproyek lain (P-FNE-08, BSS −0,414).

## 6.2 Kontribusi

| Kontribusi | Bentuk |
| :--- | :--- |
| Kerangka peringatan dini berbasis probabilitas | Model GB + zona Hijau (< 0,35), Kuning (0,35–0,65), Merah (≥ 0,65) yang kinerjanya diukur per titik *monitoring* |
| Evaluasi kalibrasi pada konteks multiproyek | Brier, BSS, ECE, *calibration intercept/slope*, dekomposisi Murphy, dan uji kalibrasi pasca-latih dengan validasi per subproyek |
| Temuan metodologis | Kalibrasi probabilitas keterlambatan bersifat khas per proyek; validasi acak akan menyembunyikan masalah ini |
| Prosedur pembangkitan data dari PMP | Simulasi jadwal, antrean sumber daya, *change request*, dan risiko yang setiap parameternya dirujuk ke dokumen PMP; dapat dipakai ulang untuk portofolio lain |

## 6.3 Saran

### 6.3.1 Saran praktis untuk manajer proyek

1. Gunakan probabilitas GB sebagai dasar zona tindakan. Zona Kuning cocok untuk pemantauan intensif dan tindakan
   ringan, zona Merah untuk tindakan mahal seperti penambahan sumber daya atau eskalasi ke Sponsor.
2. Perlakukan peringatan pada titik 25% sebagai sinyal awal untuk memperketat pemantauan; keputusan besar sebaiknya
   menunggu konfirmasi pada titik 50%.
3. Untuk proyek yang sangat berbeda dari proyek historis, terutama proyek berdurasi pendek, baca probabilitas model
   dengan hati-hati.

### 6.3.2 Saran penelitian lanjutan

| No | Saran | Alasan |
| :---: | :--- | :--- |
| 1 | Validasi dengan data realisasi proyek FNE setelah proyek berjalan | Data penelitian ini hasil simulasi |
| 2 | Kalibrasi ulang bertahap menggunakan data awal proyek yang sedang berjalan | Kalibrasi dari proyek lain tidak berpindah, sedangkan kalibrasi dengan data proyek sendiri menurunkan ECE secara drastis (Bab V, 5.4) |
| 3 | Menambah jumlah proyek dan memasukkan variabel karakter proyek (misalnya durasi *baseline*, ukuran tim) | Model gagal mengekstrapolasi ke subproyek yang berbeda (P-FNE-08) |
| 4 | Memodelkan perambatan keterlambatan antarsubproyek dan aturan antrean selain FCFS | Gap *delay propagation* baru terjawab sebagian |
| 5 | Menyetel *hyperparameter* dan menambahkan *early stopping* pada NN | NN terlalu yakin pada konfigurasi tetap |
| 6 | Memakai *dependency* dan risiko untuk prediksi tahap perencanaan, sebelum SPI tersedia | Nilai prediktif keduanya hilang setelah SPI diketahui |
