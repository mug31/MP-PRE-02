# Review Paper oleh Reviewer AI (Opus)

> Dijalankan 13 November 2026 dengan prompt review dari dosen. Reviewer adalah agen baru tanpa konteks sesi kerja,
> hanya membaca PDF render dari `paper/Paper_PRE02_Pustaka_Data.docx` (8 halaman), tanpa akses ke berkas lain atau
> web. Isi di bawah adalah keluaran reviewer apa adanya.

---

# Hasil Review Naskah

**Judul:** *Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas*
**Jurnal tujuan:** Jurnal Pustaka Data
**Bahan review:** hanya PDF naskah, 8 halaman. Seluruh halaman dibaca, termasuk Tabel 1–6 dan Gambar 1–4.

**Rekomendasi:** **Revisi Mayor.**

Naskah ini rapi dan analisis statistiknya di atas rata-rata: ada *bootstrap* per iterasi, koreksi Holm, Wilcoxon per subproyek, dan analisis paradoks Simpson. Namun ada empat masalah pokok:

1. Klaim kebaruan pertama (sumber daya bersama di portofolio multiproyek) tidak didukung metode, karena simulasi dijalankan per subproyek dan perambatan antarsubproyek tidak dimodelkan.
2. Tidak ada *baseline* EVM/SPI, padahal EVM dikritik di Pendahuluan.
3. Klaim "paling terkalibrasi" bertumpu pada ECE gabungan (0,0560). Rata-rata ECE GB per subproyek ternyata 0,1615.
4. Keputusan hipotesis H3 dan H5 terlalu digeneralisasi. Selain itu, nilai p Wilcoxon 0,039 secara matematis tidak mungkin lolos koreksi Holm atas 17 uji.

---

## 1. Topik

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dengan bidang teknik informatika | 4 | Topiknya penerapan *machine learning* (LR, RF, GB, NN dengan scikit-learn [16]) untuk manajemen proyek implementasi ERP (Pendahuluan, hlm. 2; Bag. 2.4, hlm. 3). Ini masuk lingkup informatika terapan dan "Analisa Teknologi" di jurnal ini. Namun inti masalahnya penjadwalan proyek (domain manajemen proyek/teknik industri), dan sisi informatikanya (rekayasa data, sistem peringatan dini sebagai perangkat lunak) belum ditonjolkan. | Tegaskan kontribusi informatikanya: arsitektur sistem peringatan dini, *pipeline* data dari PMP, dan bagaimana model dipasang di sistem informasi manajemen proyek. Sebutkan juga kaitannya dengan rekayasa perangkat lunak/ERP. |
| Kejelasan dan fokus topik | 4 | Fokusnya jelas, yaitu memprediksi **probabilitas** (bukan label) keterlambatan >5% dan mengevaluasi kalibrasinya (Abstrak, hlm. 1). Masalahnya ada di judul. Frasa "Proyek Multi Sumber Daya Terbatas" ambigu: bisa dibaca *multi-resource* atau *multi-project*. Kata "kalibrasi" dan "peringatan dini", yang menjadi nilai jual utama, tidak muncul di judul. | Perjelas judul, misalnya: "Prediksi dan Kalibrasi Probabilitas Keterlambatan pada Portofolio Multiproyek dengan Sumber Daya Terbatas: Studi Simulasi". Tulis "multiproyek"/"multisumber" serangkai sesuai PUEBI. |
| Nilai kebaruan atau kontribusi | 3 | Ada tiga klaim kebaruan (hlm. 2, kolom kanan). Klaim yang paling bernilai adalah evaluasi apakah kalibrasi bisa berpindah antarsubproyek (Bag. 3.3). Tetapi klaim pertama, "memodelkan keterbatasan sumber daya bersama" di portofolio multiproyek, bertentangan dengan Bag. 2.2 ("menjalankan setiap subproyek 1.000 kali") dan Bag. 3.6 ("perambatan keterlambatan antarsubproyek belum dimodelkan"). Data juga sintetis, dari satu portofolio. | Selaraskan klaim kebaruan dengan yang benar-benar dilakukan. Ada dua pilihan: (a) modelkan perebutan sumber daya lintas subproyek, atau (b) hapus/lunakkan klaim pertama. Jadikan temuan "kalibrasi tidak berpindah antarproyek" sebagai kontribusi utama. |
| Potensi dampak akademik atau praktis | 3 | Zona Hijau/Kuning/Merah dan Tabel 6 (deteksi kumulatif) punya nilai praktis bagi manajer proyek. Dampaknya terbatas karena: data berasal dari simulasi atas rencana, bukan realisasi; hanya ada 8 subproyek dari satu portofolio; dan model gagal di P-FNE-08 (BSS −0,414, hlm. 5). | Tambahkan validasi pada data realisasi (meskipun kecil) atau dataset proyek publik. Diskusikan biaya peringatan palsu (38–50,5%, Tabel 6) secara operasional. |

## 2. Abstract

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Kejelasan tujuan dan ruang lingkup penelitian | 4 | Tujuan (memprediksi probabilitas keterlambatan >5%) dan ruang lingkup (8 subproyek, 24.000 observasi, titik 25/50/75%) jelas (hlm. 1). Namun pembaca tidak tahu apa "Super ERP Farm Nation Enterprise" itu (organisasi nyata? kasus akademik?), dan sifat datanya yang sintetis baru tersirat di kalimat ketiga. | Sebutkan sejak awal bahwa ini studi berbasis simulasi atas dokumen rencana. Beri satu frasa konteks tentang portofolio tersebut. |
| Pernyataan masalah disampaikan secara ringkas | 5 | Kalimat pembukanya ringkas dan tajam: manajer butuh *seberapa besar peluang*, bukan sekadar label berisiko/tidak. | Pertahankan. Bisa ditambah setengah kalimat bahwa probabilitas yang tidak terkalibrasi menyesatkan, untuk menjembatani ke fokus kalibrasi. |
| Paparan singkat hasil eksperimen | 4 | Angka kuncinya ada: Brier 0,172, BSS 0,367, ECE 0,056, ROC-AUC 0,815; AUC naik dari 0,725 ke 0,915; 56,7% terdeteksi di titik 25%. Semuanya konsisten dengan Tabel 3 dan Tabel 6. Yang tidak disebut: selang kepercayaan, dan fakta bahwa keunggulan antarmodel tidak konsisten per subproyek (hlm. 5). | Tambahkan satu kalimat bahwa keunggulan GB signifikan pada data gabungan, tetapi tidak konsisten antarsubproyek. |
| Penjabaran temuan utama dan kontribusinya | 3 | Kontribusi tidak dinyatakan eksplisit sebagai kontribusi. Frasa "56,7% proyek yang akhirnya terlambat" sebenarnya merujuk ke *iterasi simulasi*, bukan proyek nyata, sehingga bisa menyesatkan. Keterbatasan penting (data sintetis, kegagalan di P-FNE-08, ECE per subproyek yang jauh lebih buruk) tidak disebut. | Ganti "proyek" dengan "iterasi simulasi" atau "skenario". Tutup abstrak dengan kalimat kontribusi dan implikasi, misalnya bahwa kalibrasi perlu dilakukan ulang per proyek. |
| Kejelasan dan keringkasan narasi abstrak | 4 | Panjangnya sekitar 200 kata dan alurnya runtut, tetapi padat angka. Kata kunci EN dan ID tidak sepadan: versi EN memuat "gradient boosting", versi ID memuat "keterlambatan proyek". Bentuk "pasca-latih" seharusnya "pascalatih". | Samakan daftar kata kunci di kedua bahasa. Kurangi angka yang tidak esensial (misalnya cukup Brier dan ECE). |

## 3. Introduction + Literature Review

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Definisi dan deskripsi istilah kunci/topik | 3 | Kalibrasi didefinisikan dengan baik lewat contoh "probabilitas 0,8 …" (hlm. 2). Namun istilah "proyek multi sumber daya terbatas" (RCMPSP) tidak didefinisikan, SPI tidak dijabarkan saat pertama muncul (Tabel 1, hlm. 3), dan ROC-AUC tidak pernah diuraikan. EVM disebut, tetapi indikatornya tidak dijelaskan. | Tambahkan definisi singkat RCMPSP, SPI (=EV/PV), *Earned Schedule*, dan ROC-AUC. Uraikan setiap akronim saat pertama muncul di teks utama. |
| Kejelasan latar belakang dan urgensi penelitian | 4 | Alur paragrafnya logis: keterlambatan ERP, lalu sumber daya bersama, lalu keterbatasan EVM yang deterministik, lalu ML, lalu kebutuhan kalibrasi (hlm. 2). Urgensinya bertumpu pada argumen konseptual. | Perkuat urgensi dengan dampak nyata keterlambatan ERP, misalnya persentase proyek ERP yang terlambat atau kerugian biaya. |
| Penyajian fakta-fakta yang mendukung relevansi studi | 3 | Faktanya hanya kinerja model dari studi lain (ROC-AUC 0,83 [5], AUC 0,997 [7]). Klaim "keterlambatan merupakan masalah yang terus berulang" hanya didukung [1], sebuah studi SNA *stakeholder* yang relevansinya tidak langsung. Tidak ada statistik industri. | Tambahkan data empiris tingkat keterlambatan atau kegagalan proyek ERP dan TI dari sumber bereputasi. |
| Kejelasan rumusan masalah | 3 | Tidak ada rumusan masalah atau pertanyaan penelitian (RQ) yang eksplisit. Yang ada hanya paragraf tujuan (hlm. 2). Hipotesis H1–H5 baru muncul di Bag. 2.5 (hlm. 3–4) dan tidak dikaitkan dengan masalah di Pendahuluan. | Rumuskan RQ1–RQ3 di akhir Pendahuluan (akurasi model, kalibrasi dan keterpindahannya, waktu/ambang peringatan), lalu petakan H1–H5 ke masing-masing RQ. |
| Pernyataan kebaruan (novelty) penelitian | 4 | Kebaruan dinyatakan eksplisit dalam tiga poin (hlm. 2). Ini baik. Namun poin "simulasi atas PMP delapan subproyek nyata" lebih tepat disebut kekhasan data daripada kebaruan ilmiah, dan klaim celah pertama tidak terpenuhi oleh metode (lihat item 1.3). | Pisahkan kebaruan ilmiah dari kekhasan kasus, dan pastikan setiap klaim terbukti di Hasil. |
| Sintesis literatur terdahulu dan identifikasi celah (research gap) | 3 | Literatur disajikan berurutan seperti katalog ([4]–[10]), belum disintesis secara kritis. Celah pertama ("masih jarang") tidak disertai bukti penelusuran. Tidak ada tabel pembanding studi terdahulu (data, metode, metrik, validasi, ada/tidaknya kalibrasi). Literatur RCMPSP, *Earned Schedule*, dan *schedule risk analysis* berbasis Monte Carlo tidak dibahas. | Buat tabel sintesis studi terdahulu dan tunjukkan bahwa hampir tidak ada yang melaporkan kalibrasi atau validasi lintas proyek. Itulah celah yang paling kuat. Tambahkan literatur Monte Carlo SRA dan RCMPSP. |
| Referensi yang digunakan relevan dan terkini | 3 | Sebagian besar relevan, tetapi ada beberapa yang kualitasnya lemah: [10] tesis magister, [28] IJSREM, [9] jurnal yang kurang dikenal. [1] adalah sitasi diri penulis ketiga dengan topik tidak langsung. Literatur kalibrasi terbaru (pasca-2017) dan *dataset shift* belum ada. | Ganti atau lengkapi dengan artikel bereputasi 2021–2026 tentang prediksi keterlambatan dan kalibrasi/*distribution shift*. Kurangi sitasi diri yang tidak esensial. |
| Hubungan logis antara literatur dengan tujuan penelitian | 4 | Ada benang merah yang jelas: studi lain hanya mengukur diskriminasi [11][12], kalibrasi tidak dapat diasumsikan, sehingga tujuan penelitian ini mengevaluasi kalibrasi. Kaitan ke "sumber daya bersama" lebih lemah. | Hubungkan setiap celah langsung ke satu RQ, satu hipotesis, dan satu analisis. |

## 4. Methodology

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Deskripsi lengkap tentang jenis dan sumber data | 3 | Bag. 2.1 menyebut 337 aktivitas dan 171 risiko (148 disimulasikan). Namun tidak ada rincian per subproyek: jumlah aktivitas, jumlah peran dan kapasitas sumber daya, jumlah risiko. Konteks organisasi juga tidak dijelaskan (nyata atau kasus akademik, siapa penyusun PMP). Data disebut "historis", padahal sintetis, dan ini menyesatkan. | Tambahkan kolom aktivitas, sumber daya, dan risiko per subproyek di Tabel 2. Ganti istilah "data historis" dengan "data sintetis hasil simulasi". Jelaskan asal dan kualitas dokumen PMP. |
| Kejelasan desain eksperimen atau pendekatan analitis | 4 | Desainnya jelas dan kuat: simulasi 1.000 iterasi, tiga titik pantau, LOSO 8 lipatan, kalibrator dengan lipatan dalam, *bootstrap* 2.000 replikasi per iterasi utuh, Holm, dan Wilcoxon (Bag. 2.2–2.5). Persamaan (1)–(3) disajikan. | Tambahkan diagram alir penelitian (simulasi, ekstraksi fitur, LOSO, kalibrasi, evaluasi) agar desainnya mudah diikuti. |
| Kejelasan prosedur langkah demi langkah | 3 | Ada beberapa langkah yang tidak dijelaskan: (a) penskalaan fitur untuk LR dan NN; (b) detail pelatihan NN (optimizer, epoch, *early stopping*, regularisasi); (c) *seed* acak dan versi pustaka; (d) jenis *binning* ECE (lebar sama atau frekuensi sama); (e) metode *permutation importance* (hlm. 6) yang tidak ada di Metode; (f) data untuk menghitung θ\* Youden (jika memakai prediksi uji, ambangnya optimistis); (g) daftar 17 uji yang dikoreksi Holm. Notasi ŷ(B_m) − p̂(B_m) pada Pers. (3) juga tidak didefinisikan. | Lengkapi semua butir (a)–(g), bisa dalam tabel konfigurasi atau lampiran. Definisikan notasi Pers. (3) (frekuensi teramati dan rata-rata keyakinan). |
| Kesesuaian metode dengan rumusan masalah | 3 | Metodenya sesuai untuk pertanyaan kalibrasi. Ada dua ketidaksesuaian: (1) masalah "sumber daya bersama antarproyek" tidak dimodelkan karena simulasi per subproyek; (2) Pendahuluan memposisikan EVM sebagai pendekatan konvensional yang hendak dilampaui, tetapi EVM/*Earned Schedule* tidak dijadikan *baseline*. *Hyperparameter* ditetapkan tanpa *tuning* dan tanpa justifikasi, sehingga perbandingan model bisa bias, terutama untuk NN. | Tambahkan *baseline* berbasis SPI/*Earned Schedule*, misalnya aturan SPI<ambang atau prakiraan EAC(t) yang dikonversi ke probabilitas. Lakukan *nested tuning*, atau jelaskan alasan *hyperparameter* tetap. |
| Validitas dan replikasi metodologi dimungkinkan | 3 | Ada tiga hal yang mengganggu. Faktor f=0,4 dikalibrasi pada P-FNE-08 (Bag. 2.2), yang juga merupakan lipatan uji, sehingga ada risiko kebocoran dan sirkularitas. Probabilitas CR 0,10 dan distribusi kelas 60/30/10% tidak dijustifikasi. Label dan fitur berasal dari simulator yang sama, sehingga model sebenarnya mempelajari asumsi simulator (SPI dominan secara konstruksi). Dokumen PMP, kode, dan data tidak tersedia, sehingga replikasi sulit. | Kalibrasi f pada subproyek yang tidak dipakai menguji, atau laporkan hasil dengan f yang ditetapkan *a priori*. Tambahkan analisis sensitivitas untuk probabilitas CR. Sertakan pernyataan ketersediaan data/kode (repositori). |

## 5. Preliminary Data / Result

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dan kualitas data hasil awal | 3 | Hasil relevan dan dilaporkan dengan CI. Angka saling konsisten: BSS di Tabel 3 cocok dengan 1−Brier/0,2715, selisih di Tabel 5 cocok dengan Tabel 3, dan rata-rata Tabel 2 = 44,8%. Namun proporsi terlambat sangat timpang antarsubproyek (0,4% vs 98,9%, Tabel 2), sehingga hasil LOSO sangat dipengaruhi pergeseran *base rate*. Variabel X2 = T−t secara efektif mengodekan identitas subproyek. | Diskusikan dampak ketimpangan prevalensi. Uji model tanpa X2, atau dengan X2 yang dinormalisasi (proporsi waktu). Laporkan metrik per subproyek dalam tabel. |
| Kejelasan penyajian visual data (grafik/tabel) | 3 | Gambar 1, 2, dan 3 terlalu kecil: label sumbu dan legenda hampir tidak terbaca saat dicetak, dan judulnya berbahasa Inggris. Gambar 1 tidak menampilkan histogram jumlah prediksi per bin. Nama subproyek di Tabel 2 terpotong ("P-/FNE-01"). Judul Tabel 3 menyebut CI 95%, tetapi CI untuk BSS dan ECE tidak ada. Tabel 4 hanya memuat Brier "Raw", padahal Brier setelah Platt/Isotonic hanya disebut di teks. Teks menyebut *log loss* terkecil, tetapi *log loss* tidak ada di Tabel 3. | Perbesar gambar (satu kolom penuh atau lebar halaman), samakan bahasa label, dan tambahkan histogram prediksi. Perbaiki lebar kolom Tabel 2. Lengkapi Tabel 3 dengan CI semua metrik dan *log loss*, dan Tabel 4 dengan Brier untuk tiap kalibrasi. |
| Interpretasi awal terhadap hasil | 4 | Interpretasinya baik. *Slope* 1,555 pada RF ditafsirkan dengan benar sebagai *underconfident*. Perbedaan GB (*log-loss*) dengan *boosting* pemaksimal *margin* [11] dijelaskan. Proporsi prediksi ekstrem NN dihitung. Namun ada temuan penting yang tidak ditekankan: rata-rata ECE GB per subproyek 0,1615 (hlm. 5) jauh di atas ECE gabungan 0,0560, sehingga klaim "paling terkalibrasi" hanya berlaku pada tingkat gabungan. | Laporkan ECE per subproyek untuk semua model dan sesuaikan klaim di Abstrak dan Kesimpulan. Tegaskan bahwa kalibrasi gabungan menutupi miskalibrasi per proyek. |
| Perbandingan dengan baseline atau ekspektasi sebelumnya | 3 | Pembandingnya hanya *naive prevalence*. Pembanding naif dengan proporsi data latih adalah *baseline* lemah, karena prevalensi berbeda drastis antarsubproyek. Tidak ada *baseline* EVM/SPI. Perbandingan dengan literatur (Bag. 3.6) hanya memakai ROC-AUC dan diakui tidak setara. | Tambahkan *baseline* berbasis SPI/*Earned Schedule* dan model LR univariat dengan SPI. Bandingkan juga dengan ekspektasi analisis risiko kuantitatif PMP (P50/P80). |

## 6. Discussion

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Argumentasi atas temuan secara logis | 4 | Argumennya umumnya logis. Analisis paradoks Simpson pada frekuensi CR dan korelasi utilisasi (hlm. 5–6) bagus. Ada satu argumen yang lemah: kegagalan NN dijelaskan dengan "jaringan saraf modern" [12], padahal MLP 16–8 bukan jaringan dalam. Penyebab yang lebih mungkin adalah ketiadaan penskalaan, regularisasi, atau *early stopping*, dan ini tidak diuji. | Uji ulang NN dengan standardisasi dan *early stopping* sebelum menarik kesimpulan, atau batasi klaimnya. |
| Hubungan hasil dengan literatur terdahulu | 4 | Hasil dikaitkan dengan [3], [4], [6], [11], [12], [26], [27], dan [28], termasuk temuan yang berbeda ([11], [27]). Sebagian rujukan berasal dari domain lain (armada logistik [26], tambang [27]). | Bandingkan dengan studi kalibrasi pada domain manajemen proyek atau rekayasa perangkat lunak, dan dengan studi Monte Carlo SRA. |
| Relevansi dan kontribusi terhadap bidang keilmuan | 3 | Temuan bahwa kalibrasi tidak berpindah antarproyek berharga, tetapi belum dirumuskan sebagai kontribusi teoretis atau praktis yang jelas. Kontribusi bagi informatika (desain sistem) juga belum dibahas. | Tambahkan subbagian "Implikasi teoretis dan praktis", misalnya perlunya rekalibrasi per proyek dan *online calibration*. |
| Kekuatan penalaran dan kejelasan analisis kritis | 4 | Ada kritik diri yang baik: inkonsistensi antarsubproyek dan kasus P-FNE-08. Namun ada kelemahan statistik. Dengan n=8, nilai p minimum Wilcoxon eksak sekitar 0,0039 (satu arah) atau 0,0078 (dua arah), lebih besar dari 0,05/17 ≈ 0,0029. Akibatnya tidak ada uji Wilcoxon yang mungkin signifikan setelah Holm atas 17 uji, sehingga p=0,039 (hlm. 5) jelas p yang belum dikoreksi. Uji "Platt dilatih pada subproyek itu sendiri" yang menghasilkan ECE 0,0271 tampaknya juga dievaluasi *in-sample*. | Jelaskan apakah Holm diterapkan pada Wilcoxon, dan nyatakan keterbatasan daya uji n=8. Pastikan evaluasi Platt per subproyek memakai data *held-out* di dalam subproyek. |
| Kesesuaian hasil dengan tujuan atau hipotesis awal | 3 | Keputusan di Tabel 5 bertumpu pada *bootstrap* data gabungan, yang menganggap 8 subproyek tetap. H3 "Diterima" padahal GB hanya unggul atas RF di 5 dari 8 subproyek dan uji antarsubproyek tidak signifikan. H5 dirumuskan umum (Platt **atau** Isotonic menurunkan ECE), tetapi hanya diuji pada GB+Platt. Pada NN, Platt justru menurunkan ECE (0,2188 → 0,1417, Tabel 4), sehingga H5 "Ditolak" terlalu umum. | Bedakan keputusan pada tingkat gabungan dan antarproyek. Ubah H3 menjadi "diterima pada data gabungan, tidak konsisten antarproyek", dan H5 menjadi "ditolak untuk model pohon, diterima untuk NN". |

## 7. Statement of Limitation

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Pengakuan atas keterbatasan penelitian | 3 | Keterbatasan diakui (data dari rencana, 8 subproyek, satu aturan prioritas FCFS, tanpa perambatan antarsubproyek), tetapi hanya satu paragraf yang terselip di Bag. 3.6 (hlm. 6), bukan bagian tersendiri. | Buat subbagian "Keterbatasan" tersendiri yang terstruktur. |
| Dampak keterbatasan terhadap interpretasi hasil | 3 | Ada analisis sensitivitas untuk f (0,2 dan 1,0), dengan ECE memburuk menjadi 0,114. Tetapi tidak dijelaskan bagaimana sifat sintetis data dapat membesarkan dominasi SPI (yang secara konstruksi mencerminkan durasi tambahan), atau bagaimana asumsi CR 0,10 memengaruhi hasil. | Uraikan arah bias tiap keterbatasan (optimistis atau pesimistis). Tambahkan sensitivitas untuk probabilitas CR dan aturan prioritas lain. |
| Kejelasan ruang lingkup yang tidak dicakup oleh studi | 3 | Sebagian disebut (perambatan antarsubproyek, aturan prioritas). Hal lain tidak disebut: biaya, keterlambatan di bawah 5%, besaran keterlambatan (regresi), model temporal atau *survival analysis*, dan variabel manusia atau organisasi. | Nyatakan batas ruang lingkup secara eksplisit di Metode (delimitasi), bukan hanya di akhir. |

## 8. Conclusion

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Ringkasan kontribusi utama dan hasil penelitian | 4 | Ringkas dan memuat angka kunci (hlm. 6–7). Namun angka abstrak diulang hampir verbatim, dan frasa "kalibrasi … tidak berlaku untuk proyek baru" ditulis tanpa batasan konteks simulasi. | Kurangi pengulangan angka dan tekankan makna temuan. Tambahkan frasa "dalam konteks simulasi ini". |
| Penegasan kembali pentingnya temuan | 4 | Implikasi praktisnya ditegaskan: peringatan dini untuk memperketat pemantauan, dan tindakan mahal di zona Merah. | Tambahkan pentingnya temuan bagi peneliti, misalnya perlunya melaporkan kalibrasi per proyek. |
| Kesesuaian dengan rumusan masalah dan tujuan awal | 4 | Ketiga tujuan (model, kalibrasi, ambang peringatan) terjawab. Karena RQ tidak eksplisit, pemetaannya harus disimpulkan sendiri oleh pembaca. | Susun kesimpulan per RQ atau per hipotesis. |
| Saran untuk pengembangan riset selanjutnya | 4 | Sarannya konkret: data realisasi, rekalibrasi bertahap, menambah proyek dan variabel karakter, serta perambatan antarsubproyek (hlm. 7). | Tambahkan saran metodologis: *baseline* EVM/ES, *online/recalibration* Bayesian, *domain adaptation*, dan model sekuensial. |

## 9. References & Bibliography

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Keterkinian dan relevansi referensi | 3 | Dari 28 rujukan, sekitar 9 terbit 2021–2026 ([1], [6], [7], [9], [10], [14], [26], [27], [28]). Sisanya rujukan metodologi klasik, dan itu wajar. Namun sebagian rujukan terbaru berasal dari sumber yang kurang kuat ([9], [10] tesis, [28] IJSREM), dan [1] relevansinya tidak langsung. | Tambahkan rujukan jurnal bereputasi (Q1/Q2) terbaru tentang prediksi keterlambatan, *Earned Schedule*, kalibrasi, dan *dataset shift*. |
| Format sitasi konsisten dan sesuai standar | 3 | Formatnya umumnya seragam (Penulis. Tahun. Judul. Sumber. Vol(No): hlm. doi). Ada inkonsistensi: [17] menaruh tahun di akhir dan memakai "dalam:" bercampur "(Eds)". Pemakaian koma sebelum "&" tidak seragam ([4] dan [23] tanpa koma, [7] dengan koma). [16] memakai "et al." sedangkan yang lain mencantumkan semua penulis. Spasi rata kanan merusak tampilan DOI di [19], [21], dan [22]. | Seragamkan sesuai gaya selingkung Jurnal Pustaka Data. Perbaiki [17]. Atur rata kiri untuk daftar pustaka agar DOI tidak terpecah. |
| Referensi dalam teks cocok dengan daftar pustaka | 5 | Seluruh [1]–[28] dirujuk di teks secara berurutan, dan tidak ada rujukan yatim di kedua arah (dicek pada hlm. 2–6). | Pertahankan. |
| Keseimbangan antara literatur klasik dan terbaru | 4 | Seimbang. Rujukan klasik dipakai untuk landasan metode (Brier 1950, Youden 1950, Wilcoxon 1945, Holm 1979, Murphy 1973, Platt 1999), dan rujukan terbaru untuk aplikasi. Literatur kalibrasi modern pasca-2017 dan RCMPSP klasik (Kolisch, Kurtulus & Davis) belum ada. | Lengkapi dengan literatur kalibrasi modern dan literatur RCMPSP sebagai fondasi teoretis. |

---

## Saran umum: struktur

1. **Pisahkan Tinjauan Pustaka atau buat sintesis terstruktur.** Pendahuluan saat ini menggabungkan latar belakang dan katalog studi. Tambahkan tabel pembanding studi terdahulu dan akhiri Pendahuluan dengan RQ eksplisit, kontribusi, dan sistematika penulisan.
2. **Hipotesis jangan muncul tiba-tiba di Bag. 2.5.** Turunkan H1–H5 dari literatur di Pendahuluan atau Tinjauan Pustaka, dan petakan ke RQ.
3. **Lengkapi Metode** dengan diagram alir, tabel konfigurasi model (penskalaan, *seed*, versi pustaka, pelatihan NN), metode *permutation importance*, dan cara penentuan θ\*.
4. **Buat subbagian Keterbatasan tersendiri** (misalnya 3.7) dan pernyataan ketersediaan data/kode sebelum Daftar Rujukan.
5. **Tata letak:** banyak ruang kosong besar (hlm. 2 kolom kanan sebelum Bag. 2; hlm. 3 sebelum Bag. 2.3 dan 2.5; hlm. 4 sebelum Bag. 3 dan 3.3). Gambar 1–3 terlalu kecil. Tabel 2 terpotong. *Header* tidak konsisten ("Vol. x No. x" di hlm. 1 vs "Vol . x No. 1" di hlm. 2–8). Placeholder template (Submitted xx-xx-20xx, E-ISSN 9999-9999) tidak masalah untuk tahap submisi, tetapi spasi "Vol ." perlu diperbaiki.
6. **Konsistensi bahasa gambar:** judul dan legenda Gambar 1–4 berbahasa Inggris ("Reliability diagram — 4 model tanpa kalibrasi", "Efek kalibrasi … rekomendasi: Raw"), sedangkan naskah berbahasa Indonesia. Samakan.
7. **Tambahkan tabel metrik per subproyek** (Brier, ECE, AUC per model), karena inti temuan ada pada heterogenitas antarproyek.

## Saran umum: bahasa

1. Bahasa Indonesianya umumnya baku, padat, dan jelas. Kalimatnya efektif dan jarang bertele-tele. Ini kekuatan naskah.
2. **Ejaan PUEBI/EYD:** "multi sumber daya" menjadi "multisumber daya" (atau ubah struktur judul), "pasca-latih" menjadi "pascalatih". Bentuk "antarsubproyek" sudah benar.
3. **Istilah asing:** penulisan miring tidak konsisten. *baseline*, *monitoring*, *Brier score*, dan *log loss* dimiringkan, tetapi "Platt scaling" (Bag. 2.4) dan "ROC-AUC" tidak. "Hyperparameter" bisa diganti "hiperparameter". Tetapkan satu kebijakan: miringkan semua istilah asing yang belum diserap, atau gunakan padanan (misalnya "lipatan" untuk *fold*, yang sudah dipakai).
4. **Istilah yang menyesatkan:** "data historis" seharusnya "data sintetis/simulasi". "Proyek yang terlambat" pada hasil sebaiknya "iterasi/skenario simulasi yang terlambat". "Akurat" untuk Brier sebaiknya "akurasi probabilistik".
5. **Gaya:** hindari ungkapan informal seperti "NN kalah dari pembanding naif" (pakai "berkinerja lebih buruk daripada"), "terlalu yakin" (bisa dilengkapi istilah "*overconfident*" sekali), dan "eksperimen" bentuk jamak padahal hanya ada satu desain eksperimen.
6. **Akronim:** uraikan SPI, ROC-AUC, PMP, dan RCMPSP saat pertama muncul di teks utama, bukan di tabel.
7. **Notasi:** Pers. (3) memakai ŷ dan p̂ tanpa definisi, dan subskrip "naif" pada BSS bercampur bahasa. Definisikan semua simbol tepat setelah persamaan.
8. **Abstrak EN:** sudah cukup baik. Pertimbangkan *proofreading* oleh penutur asli, misalnya ganti "flagged at one quarter of the schedule" dengan "flagged by the 25% checkpoint", dan pastikan kata kuncinya sepadan dengan versi Indonesia.

---

## Rekapitulasi Skor

| Kelompok | Jumlah item | Total skor | Rata-rata |
|---|---|---|---|
| 1. Topic | 4 | 14 | 3,50 |
| 2. Abstract | 5 | 20 | 4,00 |
| 3. Introduction + Literature Review | 8 | 27 | 3,38 |
| 4. Methodology | 5 | 16 | 3,20 |
| 5. Preliminary Data / Result | 4 | 13 | 3,25 |
| 6. Discussion | 5 | 18 | 3,60 |
| 7. Statement of Limitation | 3 | 9 | 3,00 |
| 8. Conclusion | 4 | 16 | 4,00 |
| 9. References & Bibliography | 4 | 15 | 3,75 |
| **Total** | **42** | **148** | **3,52** (rata-rata per item; rata-rata dari 9 rata-rata kelompok juga 3,52) |

**Keputusan reviewer:** Revisi Mayor. Prioritas perbaikan:

1. Selaraskan klaim "sumber daya bersama multiproyek" dengan metode.
2. Tambahkan *baseline* EVM/*Earned Schedule*.
3. Laporkan dan tekankan ECE per subproyek. Rata-ratanya 0,1615 untuk GB, dibandingkan 0,0560 pada data gabungan.
4. Koreksi keputusan H3 dan H5, dan jelaskan koreksi Holm pada uji Wilcoxon.
5. Hilangkan kebocoran kalibrasi f yang dikalibrasi pada P-FNE-08.
6. Lengkapi detail replikasi (penskalaan, NN, *seed*, θ\*, *permutation importance*).
7. Perbaiki keterbacaan Gambar 1–3 dan kelengkapan Tabel 3–4.
8. Pisahkan bagian Keterbatasan.
