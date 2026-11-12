# BAB V PEMBAHASAN

> **Status draf:** versi awal Pertemuan 7 (November 2026). Bab ini menafsirkan hasil Bab IV, membandingkannya dengan
> penelitian terdahulu, serta menguraikan implikasi dan keterbatasan. Penjelasan sebab-akibat didukung bukti di
> `04_implemen_desain_eksperimen/hasil_analisis/bukti_pembahasan/` (disebut "Bukti E1–E8"). Analisis E5 bersifat
> *post-hoc* dan tidak mengubah hasil utama. Rujukan hanya memakai klaim yang sudah dicek di
> `02_Studi Literatur/Verifikasi_Literatur.md`; rujukan dengan catatan kredibilitas ditandai ⚠️.

---

## 5.1 Ringkasan Temuan

Penelitian ini bertujuan membangun model yang memprediksi probabilitas keterlambatan proyek dari kondisi aktual
pada tahap *monitoring*, sebagai dasar sistem peringatan dini. Temuan utamanya:

| No | Temuan | Dasar |
| :---: | :--- | :--- |
| 1 | *Gradient Boosting* tanpa kalibrasi tambahan memberi probabilitas paling akurat dan paling terkalibrasi (Brier 0,1718; ECE 0,0560; ROC-AUC 0,815) | H3 diterima |
| 2 | Model berbasis pohon (RF, GB) lebih akurat daripada *Logistic Regression*; *Neural Network* justru kalah dari pembanding naif | H2 diterima, H4 ditolak |
| 3 | Kalibrasi Platt/Isotonic tidak memperbaiki LR, RF, dan GB | H5 ditolak |
| 4 | Keunggulan model nyata pada gabungan seluruh iterasi, tetapi tidak konsisten di setiap subproyek | Uji Wilcoxon (Tabel 4.6) |
| 5 | Ketepatan prediksi naik tajam seiring berjalannya proyek (ROC-AUC GB 0,725 → 0,782 → 0,915) | Tabel 4.8 |
| 6 | Indeks kinerja jadwal (SPI) adalah variabel paling berpengaruh; risiko belum dimitigasi, frekuensi CR, dan pergeseran *dependency* hampir tidak menambah informasi pada GB | Tabel 4.12 |

Benang merah yang muncul berulang di bagian-bagian berikut adalah **perbedaan karakter antarsubproyek**. Sebagian
besar kelemahan model (kalibrasi yang gagal berpindah, kasus P-FNE-08, inkonsistensi antarsubproyek) bersumber dari
model yang harus memprediksi subproyek yang tidak pernah dilihatnya.

## 5.2 Mengapa Model Berbasis Pohon Unggul (H2, H3)

RF dan GB mengungguli LR karena hubungan antara kondisi proyek dan keterlambatan tidak linear. Pengaruh SPI terhadap
peluang terlambat, misalnya, jauh lebih kuat di titik 75% (ρ Spearman −0,786) daripada di titik 25% (ρ −0,435)
(Bukti E6), sehingga efeknya bergantung pada fase proyek. Pohon keputusan menangkap interaksi seperti ini tanpa harus
dirumuskan lebih dulu. Pola "RF ≈ GB > LR" juga dilaporkan pada domain lain, misalnya prediksi kebutuhan perawatan
armada dengan AUC RF 0,855 dan XGBoost 0,853 dibanding LR 0,822 (Grzelak et al., 2026), dan model *ensemble* GB/RF
dilaporkan lebih akurat daripada *classifier* tunggal pada proyek perangkat lunak (Mandapatti, 2026 ⚠️ ukuran data
tidak dilaporkan).

Temuan bahwa GB **tanpa** kalibrasi tambahan paling terkalibrasi tampak berbeda dengan Niculescu-Mizil dan Caruana
(2005), yang menemukan *boosted trees* mendistorsi probabilitas ke bentuk sigmoid sehingga perlu dikalibrasi.
Perbedaannya dapat dijelaskan dari cara model dilatih. *Boosting* yang mereka kaji tergolong metode pemaksimal
*margin*, sedangkan GB di penelitian ini meminimalkan *log-loss* secara bertahap (Friedman, 2001), yaitu fungsi
kerugian yang langsung menghukum probabilitas yang keliru. Ditambah pohon yang dangkal (kedalaman 2) dan *learning
rate* kecil, GB menghasilkan probabilitas yang tidak ekstrem: tidak ada satu pun prediksinya yang ≤ 0,01 atau ≥ 0,99
(Bukti E1). Sebaliknya, RF memiliki *calibration slope* 1,555, artinya probabilitasnya terlalu dekat ke tengah. Ini
sesuai dengan sifat RF yang merata-ratakan suara banyak pohon.

## 5.3 Logistic Regression dan Neural Network (H1, H4)

**LR.** H1 hanya diterima sebagian: LR lebih akurat daripada pembanding naif, tetapi *calibration slope*-nya 0,586
dan *intercept*-nya 0,155. Niculescu-Mizil dan Caruana (2005) menggolongkan LR sebagai model yang umumnya sudah
terkalibrasi. Bukti E3 menunjukkan keduanya tidak bertentangan. Pada data latih setiap lipatan, *slope* LR ≈ 1,00
dan *intercept* ≈ 0, artinya LR terkalibrasi sempurna di dalam subproyek yang dilihatnya. Begitu diterapkan ke
subproyek uji, *intercept* menyebar dari −2,777 (P-FNE-07, terlalu tinggi) sampai +3,361 (P-FNE-04, terlalu rendah).
Jadi miskalibrasi LR bukan sifat bawaan LR, melainkan akibat perbedaan tingkat keterlambatan dasar antarsubproyek
yang tidak tertangkap oleh tujuh variabel.

**NN.** H4 ditolak dengan arah berlawanan: NN kurang akurat daripada LR, bahkan kalah dari pembanding naif (BSS
−0,053). Penyebabnya adalah keyakinan berlebih (*overconfidence*), sesuai temuan Guo et al. (2017) tentang jaringan
saraf modern. Sebanyak 27,2% prediksi NN bernilai ekstrem (≤ 0,01 atau ≥ 0,99), dan 31,6% dari prediksi ekstrem itu
salah arah (Bukti E1). Satu prediksi "pasti telat" yang ternyata tepat waktu menghasilkan hukuman *Log Loss* yang
sangat besar. Prediksi ekstrem yang salah itu saja menyumbang 1,005 dari total *Log Loss* NN 1,639. NN tetap
memiliki daya beda (ROC-AUC 0,696), tetapi angka probabilitasnya tidak dapat dipercaya. Hasil ini berbeda dengan
Kannan et al. (2022), yang menemukan MLP dan LR terbaik untuk memprediksi keterlambatan produksi (F-measure 0,973).
Perbedaannya wajar: data mereka berasal dari satu perusahaan dan dua mesin, sedangkan di sini model diuji pada
subproyek yang tidak pernah dilihat. *Hyperparameter* NN juga ditetapkan sebelum eksperimen tanpa penyetelan,
sehingga kinerja NN di sini adalah batas bawah, bukan potensi terbaiknya.

## 5.4 Mengapa Kalibrasi Tambahan Gagal (H5)

Platt dan Isotonic memperburuk ECE pada LR, RF, dan GB, dan hanya memperbaiki NN yang keluaran mentahnya paling buruk.
Ada dua penjelasan yang saling melengkapi.

1. **Model yang sudah terkalibrasi tidak butuh kalibrasi lagi.** Niculescu-Mizil dan Caruana (2005) menunjukkan
   bahwa Platt scaling pada model yang sudah terkalibrasi justru mendorong probabilitas menjauhi 0 dan 1, dan
   isotonic regression mudah *overfit* bila data kalibrasi sedikit. GB mentah sudah memiliki ECE terkecil (0,0560),
   sehingga ruang perbaikannya kecil dan risiko perburukannya besar.
2. **Kalibrasi tidak berpindah antarproyek.** Kalibrator di penelitian ini dilatih dari subproyek lain. Bukti E2
   menguji ini secara langsung. Platt yang dilatih dari tujuh subproyek lain menaikkan rata-rata ECE per subproyek
   GB dari 0,1615 menjadi 0,2046. Sebaliknya, Platt "oracle" yang dilatih pada subproyek itu sendiri menurunkannya
   menjadi 0,0271. Artinya pemetaan kalibrasi sangat khas per proyek: yang dipelajari dari proyek lain tidak cocok
   untuk proyek baru.

Implikasinya, kalibrasi ulang paling bermanfaat bila dilakukan dengan data dari **proyek yang sama**, misalnya setelah
beberapa titik *monitoring* awal tersedia. Pilihan ini tidak dapat diuji dengan desain sekarang dan menjadi saran
penelitian lanjutan.

## 5.5 Generalisasi Antarproyek dan Kasus P-FNE-08

Keunggulan antarmodel signifikan pada gabungan 24.000 observasi, tetapi hanya H3f yang konsisten antarsubproyek
menurut uji Wilcoxon. Sebagai contoh, GB lebih akurat daripada RF hanya pada 5 dari 8 subproyek. Pola ini sejalan
dengan Wauters dan Vanhoucke (2016): metode AI mengungguli metode EVM/ES hanya bila data latih dan data uji mirip,
dan keunggulannya menurun saat keduanya berbeda. Kedelapan subproyek FNE memang berbeda jauh: proporsi terlambat
berkisar 0,4%–98,9% dan *baseline* 62–232 hari kerja (Bukti E4).

**P-FNE-08** adalah contoh paling jelas. GB memprediksi rata-rata 14,7%, padahal 54,0% iterasinya terlambat, sehingga
BSS-nya −0,414. Bukti E4 menunjukkan dua hal yang membuat subproyek ini unik:

| Ciri | P-FNE-08 | Subproyek lain |
| :--- | :--- | :--- |
| *Baseline* | 62 hari kerja (terpendek) | 120–232 hari |
| Ambang telat 5% dalam hari | 3,1 hari | 6,0–11,6 hari |
| Rata-rata utilisasi sumber daya | 0,048 (terendah) | 0,133–1,000 |

Karena ambangnya hanya 3,1 hari, keterlambatan rata-rata 3,4 hari sudah cukup membuat lebih dari separuh iterasi
berlabel terlambat. Keterlambatan absolut P-FNE-07 serupa (3,8 hari), tetapi ambangnya 6,4 hari, sehingga hanya 13,2%
iterasinya terlambat. Di sisi lain, utilisasi sumber daya pada data gabungan berkorelasi positif dengan keterlambatan
(ρ 0,289), tetapi di dalam subproyek tidak (median ρ −0,054; Bukti E6). Hubungan ini datang dari perbedaan
antarsubproyek, bukan dari dinamika proyek. Model yang belajar "utilisasi rendah = aman" lalu salah menilai P-FNE-08.

Dugaan awal bahwa masalahnya adalah skala fitur dalam hari absolut **tidak didukung**. Analisis *post-hoc* E5, yang
menormalkan sisa waktu dan pergeseran *dependency* terhadap *baseline*, hanya menggeser BSS P-FNE-08 dari −0,414 ke
−0,377 dan menurunkan kinerja P-FNE-07 (BSS 0,194 → 0,062). Penjelasan yang paling sesuai dengan bukti: P-FNE-08
berada di luar rentang kombinasi kondisi yang dilihat model dari tujuh subproyek lain, dan dengan hanya tujuh
subproyek latih model tidak dapat mengekstrapolasi dengan baik.

## 5.6 Variabel yang Berpengaruh

SPI adalah satu-satunya variabel yang menaikkan Brier Score di kedelapan lipatan saat diacak. Ini sejalan dengan
peran sentral indikator kinerja jadwal berbasis EVM dalam peramalan durasi proyek (Batselier & Vanhoucke, 2015).
SPI pada dasarnya merangkum hasil semua gangguan yang sudah terjadi sampai hari *monitoring*.

Tiga variabel lain hampir tidak menambah informasi pada GB. Bukti E6 menjelaskan penyebabnya untuk masing-masing.

| Variabel | Korelasi dengan label | Korelasi dengan SPI (dalam subproyek) | Tafsiran |
| :--- | :--- | :--- | :--- |
| $X_7$ Pergeseran *dependency* | Ada (median ρ 0,303 dalam subproyek) | Kuat (median ρ −0,687) | Informasinya **sudah terkandung dalam SPI**: keterlambatan pendahulu langsung menurunkan SPI |
| $X_6$ Frekuensi CR | Negatif pada data gabungan (ρ −0,159), positif di dalam subproyek (median ρ 0,324) | Kuat (median ρ −0,542) | **Paradoks Simpson** antarsubproyek; efek dalam proyek terserap SPI |
| $X_5$ Risiko belum dimitigasi | Positif pada data gabungan (ρ 0,278), hampir nol di dalam subproyek (median ρ 0,016) | Lemah | Hubungannya **antarproyek**, bukan dinamika dalam proyek; tidak berguna untuk memprediksi proyek baru |

Temuan ini perlu dibaca berdampingan dengan literatur yang menempatkan *dependency* sebagai pendorong utama
keterlambatan. Sivakumar dan Sobika (2026 ⚠️ 150 tugas, jurnal kurang kuat) melaporkan korelasi *dependency* dengan
keterlambatan r = 0,61, dan Kula et al. (2023) memakai *out-degree* dependensi sebagai faktor risiko. Hasil penelitian
ini **tidak membantah** bahwa *dependency* penting. Korelasinya dengan keterlambatan memang ada (ρ 0,303). Bedanya,
saat SPI sudah diketahui, pergeseran *dependency* tidak menambah informasi baru, karena efeknya sudah tercermin dalam
progres aktual. Pada tahap perencanaan sebelum ada SPI, seperti pada penelitian Sivakumar dan Sobika, *dependency*
tetap merupakan prediktor yang berguna.

## 5.7 Implikasi untuk Sistem Peringatan Dini

**Kapan peringatan dapat dipercaya.** ROC-AUC GB naik dari 0,725 (titik 25%) ke 0,915 (titik 75%), sejalan dengan
temuan Kula et al. (2023) bahwa prediksi keterlambatan makin akurat di fase akhir karena informasi makin banyak.
Konsekuensinya ada pertukaran: makin dini peringatan, makin banyak waktu bertindak, tetapi makin besar peluang
keliru.

| Ambang | Telat sudah diperingatkan pada titik 25% | Peringatan palsu kumulatif s.d. 75% | Cocok untuk |
| :--- | ---: | ---: | :--- |
| 0,35 (batas Kuning) | 67,7% | 50,5% | Pemantauan intensif, tindakan ringan |
| 0,485 ($\theta^*$ Youden) | 56,7% | 38,0% | Keseimbangan umum |
| 0,65 (batas Merah) | 40,0% | 22,0% | Tindakan mahal: *crashing*, eskalasi ke Sponsor |

Zona bertingkat yang dirancang (Hijau/Kuning/Merah) cocok dengan pola ini: zona Kuning menangkap lebih banyak proyek
bermasalah dengan tindakan murah, zona Merah lebih jarang keliru sehingga layak untuk tindakan mahal.

**Peringatan palsu tidak sepenuhnya "salah".** Proyek tepat waktu yang pernah diperingatkan ($\theta^*$) memiliki
median keterlambatan akhir 3,6% dari *baseline*, dan 67,3% di antaranya terlambat lebih dari 3%. Proyek tepat waktu
yang tidak pernah diperingatkan memiliki median 2,8% (Bukti E8). Jadi sebagian besar peringatan palsu adalah proyek
yang **nyaris** melewati ambang 5%. Bagi manajer proyek, peringatan seperti ini tetap berguna.

**Contoh kasus** (Bukti E7, GB + Raw, keduanya dari P-FNE-03 dengan ambang telat 11,0 hari):

| Iterasi | Probabilitas 25% / 50% / 75% | Zona | SPI 25% / 50% / 75% | Hasil akhir | Tafsiran untuk PM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 301 | 0,796 / 0,853 / 0,826 | Merah sejak 25% | 0,928 / 0,919 / 0,944 | Telat 11,7 hari (5,3%) | Peringatan Merah sejak seperempat jadwal memberi sekitar 165 hari kerja untuk *fast-tracking*, penambahan sumber daya, atau eskalasi (PMP-01 §8.4.3) |
| 216 | 0,630 / 0,694 / 0,635 | Kuning → Merah → Kuning | 0,956 / 0,937 / 0,949 | Telat 10,6 hari (4,8%), tepat waktu | Peringatan "palsu" pada proyek yang nyaris melewati ambang; tindakan korektif ringan di zona Kuning sudah memadai |

Penelitian EWS berbasis AI lain juga memakai model pohon untuk memberi sinyal sebelum deviasi jadwal membesar (Kumar
& Shrivas, 2025 ⚠️ jurnal multidisiplin kecil), dan monitoring prediktif saat *runtime* sudah diusulkan untuk proses
bisnis (Cabanillas et al., 2014). Kontribusi penelitian ini adalah menunjukkan bahwa probabilitas yang dipakai sebagai
dasar ambang perlu diuji kalibrasinya, dan bahwa kalibrasi itu bergantung pada kemiripan antarproyek.

## 5.8 Perbandingan dengan Penelitian Terdahulu

| Penelitian | Domain dan data | Validasi | Hasil dilaporkan | Hasil penelitian ini |
| :--- | :--- | :--- | :--- | :--- |
| Haekal et al. (2026) | Proyek *cloud* ERP, 100 data | Tidak dijelaskan per proyek | RF: AUC 0,997, akurasi 0,980 | GB: AUC 0,815; RF: AUC 0,818 |
| Choetkiertikul et al. (2017) | *Issue* 8 proyek *open source* | — | AUC rata-rata 0,83 | (lihat di atas) |
| Impivaara (2025) | Pesanan manufaktur, 3 tahun, satu perusahaan | — | LightGBM: AUC 0,943 | |
| Purnomo et al. (2025) | Pengiriman kurir, 10.999 data | — | RF/XGBoost: AUC 0,73 | |
| Balaji & Poyyamozhi (2026 ⚠️) | *Project Management Risk Dataset* (sumber tidak dijelaskan) | — | Brier 0,024 | GB: Brier 0,1718 |
| Mirjalili et al. (2025, *preprint*) | Jaringan proyek sintetis & *benchmark* (regresi durasi) | — | ECE 3,5–3,8% | GB: ECE 5,6% (klasifikasi) |

Angka-angka ini **tidak dapat dibandingkan langsung** karena domain, ukuran data, jenis target, dan cara validasinya
berbeda. ROC-AUC penelitian ini lebih rendah daripada Haekal et al. (2026) dan Impivaara (2025), tetapi diperoleh
dengan menguji setiap subproyek menggunakan model yang tidak pernah melihat subproyek tersebut. Validasi seperti ini
lebih ketat dan lebih mendekati pemakaian nyata pada proyek baru. Nilai ini berada di kisaran yang sama dengan
Choetkiertikul et al. (2017) pada data *issue* proyek perangkat lunak (AUC 0,83). Brier Score sulit dibandingkan karena nilainya
bergantung pada sebaran label: Brier 0,024 pada data dengan kelas yang hampir pasti akan jauh lebih mudah dicapai
daripada pada data dengan proporsi terlambat 44,8% seperti di sini. Itulah sebabnya penelitian ini melaporkan BSS
terhadap pembanding naif (0,367).

## 5.9 Posisi terhadap Research Gap

| Gap (`Research gap.md`) | Status | Penjelasan |
| :--- | :---: | :--- |
| 1. *Joint resource–dependency*: keterbatasan sumber daya dan dependensi belum dimodelkan bersamaan | **Terjawab** | Simulasi memodelkan antrean sumber daya bersama (FCFS) dan dependensi aktivitas sekaligus; model memakai utilisasi ($X_4$) dan pergeseran *dependency* ($X_7$) bersamaan. Kontribusi prediktif keduanya ternyata kecil setelah SPI diketahui (5.6) |
| 2. Probabilitas pada level modul ERP | **Sebagian** | Prediksi dibuat pada level **subproyek** (kelompok modul, misalnya *Finance & HCM*), bukan per modul |
| 3. *Delay propagation* antarmodul | **Sebagian** | Perambatan di dalam subproyek tertangkap lewat $X_7$ dan SPI. Perambatan **antarsubproyek** tidak dimodelkan (keterbatasan 3.13 butir 6) |
| 4. Kalibrasi probabilitas belum dievaluasi | **Terjawab** | Brier, BSS, ECE, *reliability diagram*, *calibration intercept/slope*, dekomposisi Murphy, dan uji kalibrasi Platt/Isotonic. Temuan baru: kalibrasi tidak berpindah antarproyek (5.4) |

## 5.10 Implikasi dan Keterbatasan

### 5.10.1 Implikasi teoretis

1. Untuk prediksi probabilitas keterlambatan, model yang dilatih dengan fungsi kerugian probabilistik (GB dengan
   *log-loss*) dapat terkalibrasi baik tanpa kalibrasi tambahan. Rekomendasi umum "selalu kalibrasi model pohon"
   (Niculescu-Mizil & Caruana, 2005) tidak berlaku untuk semua varian *boosting*.
2. Kalibrasi probabilitas pada data multiproyek bersifat khas per proyek. Evaluasi model prediksi keterlambatan perlu
   memakai validasi per proyek; validasi acak menyembunyikan masalah ini.
3. Setelah progres aktual (SPI) tersedia, variabel struktural seperti *dependency* dan risiko kehilangan sebagian besar
   nilai prediktifnya. Nilai variabel-variabel itu terletak di tahap sebelum progres teramati.

### 5.10.2 Implikasi praktis

1. Probabilitas GB dapat dipakai langsung sebagai dasar zona Hijau/Kuning/Merah, dengan catatan bahwa angkanya lebih
   dapat dipercaya mulai titik 50% jadwal.
2. Pada titik 25%, peringatan sebaiknya diperlakukan sebagai sinyal untuk memperketat pemantauan, bukan dasar
   tindakan mahal.
3. Untuk proyek yang karakternya sangat berbeda dari proyek historis (misalnya sangat pendek seperti P-FNE-08),
   probabilitas model perlu dibaca hati-hati atau dikalibrasi ulang dengan data proyek itu sendiri.

### 5.10.3 Keterbatasan

| No | Keterbatasan | Dampak terhadap temuan |
| :---: | :--- | :--- |
| 1 | Data historis dibangkitkan dengan simulasi berbasis PMP, bukan realisasi | Angka kinerja berlaku untuk proyek yang perilakunya sesuai asumsi simulasi |
| 2 | Hanya 8 subproyek | Uji konsistensi antarsubproyek berdaya rendah; generalisasi ke proyek lain terbatas (5.5) |
| 3 | Antrean sumber daya hanya memakai aturan FCFS | Browning dan Yassine (2010) menunjukkan kinerja penjadwalan multiproyek bergantung pada aturan prioritas, sehingga hasil dapat berubah dengan aturan lain |
| 4 | Faktor dampak risiko dikalibrasi hanya ke median PMP-08 | Analisis sensitivitas (Tabel 4.13) menunjukkan BSS tetap positif, tetapi kalibrasi memburuk saat dampak risiko lebih besar |
| 5 | *Hyperparameter* tidak disetel | Kinerja NN kemungkinan dapat diperbaiki |
| 6 | Selang kepercayaan hanya mencakup variasi antar-iterasi | Ketidakpastian akibat pemilihan subproyek tidak tercakup |
| 7 | Perambatan keterlambatan antarsubproyek tidak dimodelkan | Gap 3 hanya terjawab sebagian |
