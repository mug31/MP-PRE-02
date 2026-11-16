# Review Paper oleh Reviewer AI (Sonnet), putaran 2

> Dijalankan 16 November 2026 setelah revisi A dan B (commit c7f9cee), dengan prompt review dari dosen yang sama
> persis dengan putaran 1 (`Review_Sonnet.md`). Reviewer adalah agen baru tanpa konteks sesi kerja, hanya membaca
> PDF render dari `paper/Paper_PRE02_Pustaka_Data.docx` (11 halaman), tanpa akses ke berkas lain atau web.
> Isi di bawah adalah keluaran reviewer apa adanya.

---

# Review: "Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas" (Jurnal Pustaka Data, 11 hlm.)

Penilaian hanya dari isi PDF. Skala 1-5 (5 = sangat baik). Catatan format: hlm. 11 kosong, dan ada ruang kosong besar di hlm. 6 (kolom kanan) dan hlm. 7 (bagian bawah).

Ringkasan singkat: naskah ini jujur dan kuat secara analitis. Pelaporan negatifnya (GB tidak konsisten antarsubproyek, ECE per subproyek 0,1615 jauh di atas ECE gabungan 0,056, Platt/isotonic tidak membantu) patut dipuji. Kelemahan utamanya ada di tiga hal. Data sepenuhnya sintetis dan dibangkitkan oleh simulator yang parameternya (f, peluang CR) diasumsikan. Sebagian hasil penting hanya muncul di teks tanpa tabel atau gambar. Daftar pustaka dan penyajian kebaruan belum kokoh.

## 1. Topic

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dengan teknik informatika | 4,5 | Pembelajaran mesin (LR, RF, GB, NN), kalibrasi probabilitas, simulasi, dan sistem peringatan dini adalah inti informatika/sains data (Bag. 2.4-2.5, Gambar 3-4). Domain proyek ERP menambah relevansi rekayasa sistem informasi. | Tegaskan di Pendahuluan kontribusi bagi informatika (metodologi evaluasi ML pada data sintetis dan pergeseran distribusi antarproyek), bukan hanya manajemen proyek. |
| Kejelasan dan fokus topik | 4 | Fokus pada probabilitas terkalibrasi dengan RQ1-RQ3 (hlm. 3). Namun judul "Multi Sumber Daya Terbatas" ambigu (multi-resource atau multi-project). Hlm. 3 dan 9 mengakui bahwa pemakaian sumber daya antarsubproyek tidak dimodelkan, jadi judul dan framing "multiproyek" lebih besar daripada cakupan nyata. | Perjelas judul, misalnya "...Proyek dengan Sumber Daya Terbatas: Studi Simulasi Portofolio ERP", dan tambahkan kata "sintetis/simulasi". |
| Nilai kebaruan atau kontribusi | 3,5 | Kebaruan terletak pada evaluasi kalibrasi dengan validasi leave-one-subproject-out dan temuan bahwa kalibrasi tidak berpindah antarproyek. Namun data sintetis dari simulator buatan sendiri membuat temuan sebagian merupakan fungsi simulator. Klaim "kerangka sistem peringatan dini" terlalu besar dibanding bukti. | Turunkan klaim "kerangka". Posisikan sebagai studi metodologis atau bukti konsep. Tunjukkan perbandingan dengan Monte Carlo schedule risk analysis atau EVM-SPI sebagai pembanding. |
| Potensi dampak akademik/praktis | 3,5 | Dampak praktis jelas (zona Hijau/Kuning/Merah, Tabel 8, Gambar 4). Tetapi tanpa data nyata, probabilitas tidak boleh dibaca sebagai peluang absolut (disebut di 3.7), sehingga dampak praktis masih konseptual. Pada ambang Youden, 38% iterasi tepat waktu mendapat peringatan palsu (Tabel 8). | Validasi pada minimal satu proyek nyata atau data historis. Tambahkan analisis biaya peringatan palsu vs keterlambatan terlewat. |

## 2. Abstract

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Kejelasan tujuan dan ruang lingkup | 4 | Tujuan jelas (memprediksi peluang >5% lewat baseline dan menguji kalibrasi pada proyek tak terlihat). Cakupan sintetis dan delapan subproyek disebut. | Sebut eksplisit bahwa tidak ada validasi data nyata dan bahwa hanya satu portofolio yang dipakai. |
| Pernyataan masalah ringkas | 3,5 | Kalimat pembuka ("peluang, bukan label") baik. Celah penelitian (kalibrasi lintas proyek dan ketiadaan data historis) tidak dinyatakan eksplisit. | Tambahkan satu kalimat celah: model prediksi keterlambatan dilaporkan dengan metrik daya beda, jarang diuji kalibrasinya pada proyek baru. |
| Paparan singkat hasil eksperimen | 4,5 | Metrik utama dilaporkan (Brier 0,172, ECE 0,056, ROC-AUC 0,815; ECE per subproyek 0,162; ROC-AUC 0,725 ke 0,915; 56,7%). Angka konsisten dengan Tabel 4, 7, dan 8. | Kurangi jumlah angka. Pilih 3-4 yang paling penting. |
| Penjabaran temuan utama dan kontribusi | 4 | Temuan utama (GB gabungan terbaik tetapi tidak konsisten, NN tanpa early stopping buruk, kalibrasi tidak berpindah) jelas. Kontribusi ("dapat menjadi dasar sistem peringatan dini berzona") agak kuat bila dibanding bukti sintetis. | Lunakkan klaim dan tegaskan kontribusi metodologis. |
| Kejelasan dan keringkasan narasi | 3 | Abstrak ganda (Inggris dan Indonesia) masing-masing ±200+ kata dan padat istilah (ECE, BSS, leave-one-subproject-out, isotonic). Sulit dibaca sekilas. | Pangkas menjadi ±150-200 kata per bahasa. Hindari singkatan yang belum didefinisikan (ECE, ROC-AUC) di abstrak. |

## 3. Introduction + Literature Review

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Definisi dan deskripsi istilah kunci | 3,5 | ERP, EVM, SPI, ROC dijelaskan (hlm. 2). Kalibrasi dijelaskan dengan contoh 0,8 yang baik. Brier, ECE, Platt, isotonic, dan permutation importance baru muncul di Metode tanpa pengenalan di Pendahuluan. "Super ERP Farm Nation Enterprise" tidak dijelaskan. | Tambahkan paragraf definisi "probabilitas terkalibrasi" dan "sistem peringatan dini berzona". Beri konteks portofolio studi. |
| Kejelasan latar belakang dan urgensi | 3,5 | Alur masalah (keterlambatan ERP, sumber daya bersama, EVM deterministik, ML) logis. Urgensi lebih bersifat argumen konseptual daripada bukti empiris. | Tambahkan data prevalensi keterlambatan proyek ERP/TI dari laporan atau survei yang kredibel. |
| Penyajian fakta pendukung relevansi | 3 | Hampir tidak ada statistik kuantitatif tentang skala keterlambatan. Klaim "keterlambatan terus berulang" disandarkan pada [1], yang berjudul analisis kinerja stakeholder ERP, dan tidak tampak berkaitan langsung. | Gunakan sumber statistik kegagalan atau keterlambatan proyek yang relevan dan ganti [1] (yang juga tampak sitasi mandiri) bila tidak mendukung. |
| Kejelasan rumusan masalah | 4 | RQ1-RQ3 dirumuskan jelas (hlm. 3), tetapi muncul setelah celah dan berupa satu paragraf padat. Hipotesis H1-H5 baru muncul di Bag. 2.5, jauh dari RQ. | Pisahkan RQ dalam daftar dan pindahkan hipotesis ke dekat RQ. |
| Pernyataan kebaruan (novelty) | 3 | Kontribusi utama dan pendukung disebut (hlm. 3), tetapi tidak ada kalimat kebaruan yang membedakan dari karya terdekat ([12] hibrida simulasi-ML). Istilah "kerangka" melebihi isi. | Tulis eksplisit: "Berbeda dari [12] yang ..., penelitian ini ...". |
| Sintesis literatur dan celah | 4,5 | Tabel 1 plus tiga celah (kalibrasi belum jadi evaluasi utama, dependensi sumber daya jarang dimodelkan, data historis tidak tersedia) sangat tajam. Kritik bahwa angka tertinggi berasal dari data kecil ([8], [11]) bagus. | Tambahkan kolom jumlah data dan skema validasi pada Tabel 1. Sintesis literatur kalibrasi lebih luas dan literatur Monte Carlo schedule risk. |
| Referensi relevan dan terkini | 3 | Banyak sumber 2025-2026 dari jurnal kurang dikenal ([1], [9] tesis, [11], [27], [28]). [27] (pemeliharaan armada logistik) dipakai mendukung klaim boosting dan agak jauh domainnya. Literatur inti manajemen risiko jadwal (QSRA/Monte Carlo) dan metode kalibrasi modern tidak ada. | Ganti atau perkuat dengan jurnal terindeks (Scopus/WoS). Tambahkan literatur schedule risk analysis, kalibrasi (beta/temperature), dan conformal prediction. |
| Hubungan logis literatur dengan tujuan | 4,5 | Setiap celah di hlm. 2 diterjemahkan ke RQ dan desain (LOSO untuk celah 1, simulasi sumber daya untuk celah 2 dan 3). | Buat pemetaan celah, RQ, dan hipotesis dalam satu tabel kecil. |

## 4. Methodology

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Deskripsi jenis dan sumber data | 3,5 | 337 aktivitas, 171 risiko (148 disimulasikan), 8 subproyek, 24.000 observasi, variabel X1-X7 (Tabel 2), label >5%. Namun dokumen PMP tidak dapat diverifikasi pembaca. Distribusi durasi, jenis dan jumlah sumber daya, dan ukuran per subproyek tidak dirinci. | Tambahkan tabel profil subproyek (jumlah aktivitas, risiko, sumber daya). Lampirkan ringkasan atau potongan PMP anonim. |
| Kejelasan desain eksperimen | 4 | Desain LOSO (tujuh latih, satu uji), prediksi out-of-fold, kalibrator dengan CV 3-lipatan di data latih, bootstrap 2.000 dengan Holm atas 17 uji: matang. Kelemahan: tidak ada tuning, satu seed, dan f dipilih dengan P-FNE-08, yang juga subproyek uji (diakui, hlm. 3). | Gunakan beberapa seed. Pilih f tanpa melibatkan subproyek uji (misalnya nested). |
| Kejelasan prosedur langkah demi langkah | 3,5 | Persamaan (1), kelas CR, aturan FCFS, dan titik monitor 25/50/75% jelas. Tidak ada diagram alur atau pseudocode. Detail alokasi sumber daya dan resolusi konflik antaraktivitas singkat. Log loss dipakai di Tabel 4 tetapi tidak didefinisikan di 2.5. | Tambahkan diagram alur pipeline dan pseudocode simulasi. Definisikan log loss. |
| Kesesuaian metode dengan rumusan masalah | 4 | RQ1 dijawab Brier/BSS, RQ2 dijawab ECE/slope plus kalibrasi LOSO, RQ3 dijawab ROC-AUC per titik, Youden, dan permutation importance. Uji Wilcoxon n=8 tidak mungkin signifikan setelah Holm (p minimum 0,0039 > 0,0029), sehingga dayanya nol sejak awal. | Ganti dengan pendekatan hierarkis atau laporkan ukuran efek dan CI antarsubproyek. |
| Validitas dan replikasi | 3 | Positif: versi scikit-learn 1.9.1 dan seed 42 disebut. Negatif: kode dan data hanya "tersedia atas permintaan" (hlm. 4). Validitas eksternal rendah karena latih dan uji dari simulator yang sama (sirkularitas). X2 (T-t) pada titik tetap secara implisit mengodekan T. | Publikasikan kode dan data di repositori. Diskusikan sirkularitas dan potensi kebocoran identitas subproyek lewat X2. |

## 5. Preliminary Data / Result

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dan kualitas data hasil awal | 3,5 | Konsistensi internal sangat baik (rata-rata Tabel 7 cocok dengan Tabel 4, BSS cocok, Tabel 8 cocok dengan Gambar 4). Namun data sintetis dengan parameter asumsi (f=0,4, CR 0,10). Tabel 9 menunjukkan ECE GB berubah 0,029 hingga 0,114 dan proporsi terlambat 26,9% hingga 75,1% hanya karena f. | Lakukan sensitivitas pada seluruh model, bukan hanya GB. Tambahkan sensitivitas peluang CR. |
| Kejelasan penyajian visual | 3,5 | Tabel dan gambar umumnya rapi (Gambar 3, 4, Tabel 8). Kekurangan: Tabel 5 hanya memuat Brier mentah, padahal teks melaporkan Brier Platt/Isotonic GB (0,1860/0,1880). Tabel 6 hanya memuat sebagian dari 17 uji dan labelnya (H1a, H3a, dst.) tidak sama dengan Gambar 2. Gambar 1 tanpa jumlah observasi per interval dan CI. Hasil NN early stopping, importance, AUC per subproyek (>0,68), dan slope/intercept hanya di teks. | Tambahkan tabel untuk hasil-hasil yang hanya di teks, samakan label, tambahkan histogram jumlah per bin di Gambar 1. |
| Interpretasi awal | 4 | Interpretasi cermat: penyebab miskalibrasi (perbedaan tingkat dasar antarsubproyek), analisis P-FNE-08, paradoks Simpson untuk frekuensi CR, dan peran SPI. Beberapa penjelasan spekulatif dan diakui belum diuji (hlm. 5). Kalimat tentang peringatan palsu ("umumnya terjadi pada iterasi yang terlambat", hlm. 8) ambigu. | Perjelas kalimat itu (maksudnya iterasi tepat waktu yang hampir terlambat). Uji penjelasan boosting vs log loss dengan eksperimen kecil. |
| Perbandingan dengan baseline/ekspektasi | 3,5 | Ada pembanding naif dan LR (Tabel 4) serta perbandingan dengan [8], [9], [5] yang dinyatakan tidak setara. Tidak ada baseline domain (ambang SPI sederhana, ramalan EVM, atau Monte Carlo), padahal SPI adalah variabel dominan. | Tambahkan baseline ambang SPI dan baseline Monte Carlo/EVM. |

## 6. Discussion

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Argumentasi atas temuan secara logis | 4,5 | Argumen berlapis dan didukung angka: ECE gabungan vs per subproyek (0,056 vs 0,1615), dua penjelasan kegagalan kalibrasi (Platt 0,1615 ke 0,2046 vs 0,0271 bila dilatih sendiri), kasus P-FNE-08 (BSS -0,414 menjadi -0,377 setelah normalisasi). | Tambahkan ringkasan temuan di awal pembahasan. |
| Hubungan hasil dengan literatur | 3,5 | Subbab 3.6 membandingkan [8], [9], [5] dan menjelaskan mengapa tidak setara. Penjelasan GB vs [13] cukup bernalar tetapi bersandar pada [27] yang lemah. | Perkuat dengan literatur kalibrasi dan prediksi proyek yang lebih relevan. |
| Relevansi dan kontribusi bagi keilmuan | 4 | Pesan "laporkan ECE per proyek, bukan hanya gabungan" dan "kalibrasi ulang di proyek berjalan" bernilai (3.7). | Generalisasikan ke guideline evaluasi untuk model prediksi proyek. |
| Kekuatan penalaran dan analisis kritis | 4,5 | Sangat baik: uji ulang NN dengan early stopping dilaporkan jujur (termasuk bahwa early stopping bawaan 10% data latih justru memburuk, Brier 0,238) dan keputusan hipotesis tidak diubah. Menyadari signifikansi pada data sintetis dan n=8. | Nyatakan bahwa p-value pada 24.000 observasi sintetis bergantung pada jumlah simulasi. Utamakan ukuran efek. |
| Kesesuaian hasil dengan tujuan/hipotesis | 4 | Tabel 6 memetakan H1-H5 (didukung/sebagian/ditolak). Konsisten dengan RQ. H1 ("terkalibrasi baik") tidak punya kriteria operasional yang jelas. | Definisikan kriteria numerik untuk "terkalibrasi baik" sebelum pengujian. |

## 7. Statement of Limitation

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Pengakuan atas keterbatasan | 4,5 | Subbab 3.8 menyebut lima keterbatasan: data sintetis dengan SPI dominan, parameter asumsi (CR, f dengan Tabel 9), satu portofolio delapan subproyek, tanpa tuning, ambang diambil dari prediksi yang sama. Sangat jujur. | Pindahkan ke bagian tersendiri bila ketentuan jurnal menghendaki. |
| Dampak keterbatasan terhadap interpretasi | 4 | Dampak dikuantifikasi sebagian (Tabel 9, NN early stopping). Tidak dinyatakan dampaknya pada peringkat model dan klaim zona peringatan. | Tambahkan kalimat: kesimpulan mana yang kokoh dan mana yang rentan. |
| Kejelasan ruang lingkup yang tidak dicakup | 4 | Tersebar di 2.3 (besaran keterlambatan, biaya, waktu tidak diprediksi), 2.1 (CR dan risiko biaya tidak disimulasikan), dan 3.8 (dependensi antarsubproyek tidak dimodelkan). | Rangkum dalam satu paragraf "di luar cakupan". |

## 8. Conclusion

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Ringkasan kontribusi utama dan hasil | 4 | Jawaban RQ1-RQ3 lengkap dengan angka (Brier 0,1718, BSS 0,367, ROC-AUC 0,815, ECE 0,1615, 0,725 ke 0,915, 56,7%). | Kurangi angka dan sertakan hasil pengujian hipotesis (H1-H5). |
| Penegasan kembali pentingnya temuan | 3,5 | Ada rekomendasi praktis (zona Hijau/Kuning/Merah). Penegasan pentingnya temuan terhadap bidang masih tersirat. | Tutup dengan satu kalimat tentang implikasi utama (kalibrasi harus diuji lintas proyek). |
| Kesesuaian dengan rumusan masalah dan tujuan | 4,5 | Kesimpulan terstruktur mengikuti RQ1, RQ2, RQ3. | Pertahankan. |
| Saran riset selanjutnya | 4 | Konkret: data realisasi, kalibrasi ulang, sensitivitas CR, tuning per subproyek, beta calibration, penambahan proyek, dependensi antarsubproyek. | Urutkan berdasarkan prioritas dan sebut validasi data nyata sebagai langkah pertama. |

## 9. References & Bibliography

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Keterkinian dan relevansi | 3 | Banyak referensi 2025-2026, tetapi sebagian berkualitas atau relevansinya diragukan ([1], [9] tesis, [11], [27], [28]) dan [2], [3], [4] relatif lama (2010-2016) untuk topik ML. | Ganti sumber lemah dengan jurnal terindeks. Tambahkan literatur ML dan risiko jadwal 2020-2025. |
| Format sitasi konsisten dan sesuai standar | 3 | Teks bernomor gaya IEEE, daftar gaya APA bernomor (hibrida). Variasi: [18] memakai "dalam:" di daftar berbahasa Inggris, [8] dan [11] tanpa DOI, tata letak DOI [22] dan [23] berantakan, [9] tesis. | Pilih satu gaya (IEEE atau APA) sesuai template jurnal. Seragamkan DOI dan bahasa. |
| Referensi dalam teks cocok dengan daftar | 4,5 | Sitasi [1]-[28] terpakai berurutan dan tidak ada referensi yatim. Tidak ditemukan sitasi tanpa entri. | Verifikasi akhir setelah revisi daftar. |
| Keseimbangan klasik dan terbaru | 3,5 | Klasik tepat (Brier 1950, Murphy 1973, Youden 1950, Wilcoxon 1945, Holm 1979, Friedman 2001, Platt 1999). Terbaru kuat tetapi bermutu tidak merata. Literatur menengah (2018-2024) tentang kalibrasi dan prediksi proyek kurang. | Tambahkan literatur 2018-2024 yang bereputasi. |

## Saran umum: struktur

1. Kerangka IMRaD sudah ada (Pendahuluan, Metode, Hasil dan Pembahasan, Kesimpulan), tetapi tinjauan pustaka menyatu dengan Pendahuluan. Pisahkan atau beri subjudul "Penelitian Terkait".
2. Keterbatasan (3.8) dan sensitivitas (Tabel 9) sebaiknya menjadi bagian sendiri atau dirujuk jelas dari Metode.
3. Gabungkan Hasil dan Pembahasan dengan lebih terarah: tiap subbab berurutan RQ1, RQ2, RQ3, lalu hipotesis. Subbab 3.6 (perbandingan literatur) lebih cocok sebagai pembahasan.
4. Pindahkan hipotesis H1-H5 ke dekat RQ di Pendahuluan, dan sertakan kriteria operasionalnya.
5. Angkat hasil yang hanya di teks ke tabel atau gambar: NN early stopping, permutation importance, AUC per subproyek, slope/intercept semua model, Brier terkalibrasi (Tabel 5).
6. Tambahkan diagram alur pipeline (PMP ke simulasi ke fitur ke model ke kalibrasi ke zona).
7. Perbaiki tata letak: hlm. 11 kosong, ruang kosong di hlm. 6-7. Satu abstrak Inggris plus satu Indonesia cukup singkat.
8. Samakan label Tabel 6 dengan Gambar 2.

## Saran umum: bahasa

1. Terlalu banyak istilah Inggris dalam teks Indonesia (monitoring, baseline, out-of-fold, early stopping). Gunakan padanan Indonesia pada kemunculan pertama dan cetak miring konsisten.
2. Konsistensi istilah: "iterasi" dipakai untuk satu simulasi dan juga untuk observasi pada titik monitor. Bedakan "iterasi simulasi" dan "observasi". Seragamkan "peringatan palsu", "terlambat", dan "keterlambatan".
3. Beberapa kalimat panjang dan padat angka (3.3, 3.4), pecah menjadi kalimat pendek.
4. Kalimat ambigu: "Peringatan palsu umumnya terjadi pada iterasi yang terlambat" (hlm. 8) perlu diperjelas. Hindari klaim kuat ("sangat bergantung") tanpa kuantifikasi.
5. Konsistensi angka: koma desimal di teks Indonesia, titik di abstrak Inggris. Pastikan konsisten dalam gambar dan tabel.
6. Singkatan (ECE, BSS, SPI, CR, PMP, EVM) didefinisikan pada kemunculan pertama di teks utama. Abstrak sebaiknya tidak bergantung pada singkatan.
7. Ada kemungkinan ketidakkonsistenan yang perlu dijelaskan: target PMP-08 "20 minggu, P50 21 minggu" (hlm. 3) vs T=62 hari untuk P-FNE-08 (Tabel 3). Beri penjelasan satuan atau cakupan.

## Rekapitulasi skor rata-rata

| Kelompok | Rata-rata |
|---|---|
| 1. Topic (4 item) | 3,88 |
| 2. Abstract (5 item) | 3,80 |
| 3. Introduction + Literature Review (8 item) | 3,63 |
| 4. Methodology (5 item) | 3,60 |
| 5. Preliminary Data / Result (4 item) | 3,63 |
| 6. Discussion (5 item) | 4,10 |
| 7. Statement of Limitation (3 item) | 4,17 |
| 8. Conclusion (4 item) | 4,00 |
| 9. References & Bibliography (4 item) | 3,50 |
| Rata-rata total (rata-rata 9 kelompok) | 3,81 |
| Rata-rata total (42 item) | 3,79 |

Rekomendasi umum: revisi minor sampai mayor (kekuatan: analisis kritis dan kejujuran pelaporan; perbaikan prioritas: kebaruan eksplisit, baseline domain, data dan kode terbuka, hasil dalam teks dipindah ke tabel, pembaruan dan format daftar pustaka).
