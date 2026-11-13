# Review Paper oleh Reviewer AI (Sonnet)

> Dijalankan 13 November 2026 dengan prompt review dari dosen. Reviewer adalah agen baru tanpa konteks sesi kerja,
> hanya membaca PDF render dari `paper/Paper_PRE02_Pustaka_Data.docx` (8 halaman), tanpa akses ke berkas lain atau
> web. Isi di bawah adalah keluaran reviewer apa adanya.

---

# Review Paper "Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas" (Jurnal Pustaka Data, 8 halaman)

Penilaian hanya berdasarkan isi PDF. Skala 1-5, dengan 5 sebagai sangat baik. Penilaian dibuat ketat.

**Kesan umum.** Naskah ini kuat secara teknis. Ia menyajikan baseline naif, evaluasi leave-one-subproject-out (LOSO), BSS dan ECE, uji hipotesis, dan analisis kasus (P-FNE-08, paradoks Simpson). Kelemahan utamanya ada di tiga hal.
- (a) Seluruh data adalah data simulasi yang parameternya ditentukan penulis, sehingga validitas eksternal sangat lemah.
- (b) Struktur tidak mengikuti format yang diminta. Tidak ada subbab Tinjauan Pustaka, rumusan masalah eksplisit, atau bagian Keterbatasan tersendiri, dan Pembahasan menyatu dengan Hasil.
- (c) Ada inkonsistensi statistik (Holm vs p = 0,039) dan kendala reproduktibilitas.

## 1. Topic

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dengan teknik informatika | 4 | Prediksi probabilistik berbasis machine learning (LR, RF, GB, NN), kalibrasi, dan simulasi untuk sistem peringatan dini proyek implementasi ERP. Domainnya sistem informasi dan manajemen proyek TI, sehingga relevan, tetapi kontribusi pada inti informatika (algoritma atau model baru) terbatas karena hanya membandingkan model yang sudah ada. | Tegaskan kontribusi informatikanya, misalnya pipeline simulasi-ke-prediksi, protokol evaluasi LOSO, atau sistem peringatan dini sebagai artefak perangkat lunak. |
| Kejelasan dan fokus topik | 4 | Fokus jelas: probabilitas keterlambatan >5% dari baseline pada tahap monitoring 25/50/75% (Abstrak, Bagian 1). Judul "Multi Sumber Daya Terbatas" ambigu karena tidak jelas apakah maksudnya multi-proyek dengan sumber daya terbatas. Pembahasan kadang melebar ke banyak temuan sekunder (Simpson, sensitivitas, zona peringatan). | Perbaiki judul, misalnya "...Proyek Multi-Subproyek dengan Sumber Daya Bersama Terbatas". Pertahankan satu pertanyaan utama. |
| Nilai kebaruan atau kontribusi | 3 | Kebaruan terletak pada kombinasi evaluasi kalibrasi, validasi lintas subproyek, dan simulasi dari PMP (Bagian 1, paragraf 4). Setiap komponennya sudah dikenal, dan hasil yang dilaporkan sebagian berupa temuan negatif atau tidak konsisten. Data simulasi membuat klaim kebaruan sulit dibedakan dari artefak simulator. | Nyatakan kebaruan secara tegas dan terukur. Tunjukkan bahwa hasil tidak sekadar artefak simulator, dengan satu validasi pada data nyata atau sekurangnya studi sensitivitas yang lengkap. |
| Potensi dampak akademik/praktis | 3 | Potensi praktis nyata, yaitu zona Hijau/Kuning/Merah dan contoh P-FNE-03 dengan 165 hari kerja untuk tindakan korektif (Bagian 3.5). Namun tanpa data realisasi, dampak praktis belum teruji. Dampak akademik terbatas pada satu portofolio, delapan subproyek, dan satu organisasi. | Tambahkan validasi pada proyek berjalan atau data publik, serta deskripsi cara integrasi ke praktik PMO. |

## 2. Abstract

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Kejelasan tujuan dan ruang lingkup | 4 | Tujuan (prediksi probabilitas selesai >5% di atas baseline), objek (delapan subproyek Super ERP Farm Nation), data (24.000 observasi), dan validasi (LOSO) disebut jelas. | Sebutkan bahwa tujuan kedua adalah mengevaluasi kalibrasi dan menentukan ambang peringatan. Tegaskan secara eksplisit bahwa data bersifat simulasi sintetis. |
| Problem statement ringkas | 3 | Kalimat pembuka "manajer proyek perlu tahu seberapa besar peluang terlambat, bukan sekadar label" adalah motivasi yang baik. Namun celah penelitian (EVM deterministik, kalibrasi belum diuji lintas proyek) tidak dinyatakan. | Tambahkan satu kalimat celah, misalnya "kalibrasi pada prediksi keterlambatan proyek belum dievaluasi lintas proyek". |
| Paparan singkat hasil eksperimen | 4 | Angka lengkap tersedia (Brier 0,172, BSS 0,367, ECE 0,056, AUC 0,815; AUC 0,725 menjadi 0,915; 56,7% pada 25%). | Sertakan selang kepercayaan atau pernyataan bahwa keunggulan tidak konsisten per subproyek (Bagian 3.4). Angka yang dipamerkan tampak lebih meyakinkan daripada hasil per subproyek. |
| Penjabaran temuan utama dan kontribusi | 3 | Temuan disebut, tetapi kontribusi tidak dirumuskan. Abstrak tidak menyebut keterbatasan utama (data simulasi, hasil per subproyek tidak konsisten). | Tambahkan kalimat kontribusi dan satu kalimat keterbatasan. |
| Kejelasan dan keringkasan narasi | 3 | Padat, tetapi satu paragraf memuat terlalu banyak angka. Versi Inggris dan Indonesia ada sehingga halaman 1 penuh. Istilah "neural network terlalu yakin" dalam bahasa Inggris tidak dijelaskan (overconfident). | Pecah menjadi struktur latar-tujuan-metode-hasil-simpulan dan kurangi angka. Pastikan kedua versi identik isinya. |

## 3. Introduction + Literature Review

Catatan struktural: tidak ada subbab tinjauan pustaka terpisah. Tinjauan pustaka diintegrasikan dalam Bagian 1 (halaman 2).

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Definisi dan deskripsi istilah kunci | 3 | ERP, EVM, dan PMP didefinisikan sekilas. Kalibrasi dijelaskan dengan contoh (probabilitas 0,8 berarti sekitar 80% proyek terlambat). SPI baru didefinisikan di Tabel 1. ECE, BSS, dan reliability diagram tidak diperkenalkan di Pendahuluan. | Tambahkan paragraf definisi: keterlambatan (>5% baseline), kalibrasi, skor probabilistik, dan earned schedule/SPI. |
| Kejelasan latar belakang dan urgensi | 3 | Alur dari keterlambatan ERP ke EVM, ML, lalu kalibrasi masuk akal. Urgensi lebih bersifat argumentatif. Tidak ada angka dampak keterlambatan ERP atau biaya salah peringatan. | Tambahkan data kuantitatif dari laporan industri atau survei yang kredibel. |
| Penyajian fakta pendukung relevansi studi | 3 | Fakta berasal dari studi terdahulu (AUC 0,83 [5], AUC 0,997 pada 100 data [7]). Rujukan [1] (analisis stakeholder ERP, karya rekan penulis) tidak mendukung klaim keterlambatan. Beberapa klaim kuat ("sering menjadi penyebab kegagalan") bersandar pada satu sumber. | Ganti atau tambahkan rujukan primer tentang kegagalan dan keterlambatan proyek ERP. Kurangi swa-sitasi yang tidak relevan. |
| Kejelasan rumusan masalah | 2 | Tidak ada pertanyaan penelitian atau rumusan masalah. Hanya "Penelitian ini bertujuan..." di akhir Bagian 1. Hipotesis H1-H5 baru muncul di Bagian 2.5 (halaman 3-4), jauh dari pendahuluan. | Tuliskan 2-3 pertanyaan penelitian (RQ) di Pendahuluan dan pindahkan hipotesis ke sana, dengan pemetaan RQ ke hipotesis ke tabel hasil. |
| Pernyataan kebaruan | 3 | Ada pernyataan eksplisit: "Kebaruan penelitian ini terletak pada tiga hal". Namun klaim "masih jarang" dan "belum dievaluasi sistematis" tidak didukung penelusuran sistematis. | Jelaskan strategi pencarian literatur, atau lunakkan klaim. Bedakan kebaruan metodologis dan empiris. |
| Sintesis literatur dan celah | 3 | Ada tiga celah yang jelas (portofolio multi-sumber daya, kalibrasi lintas proyek, data historis tak tersedia). Namun tinjauan lebih berupa daftar studi (cloud ERP [7], Bayesian [6], dsb.) daripada sintesis, serta tidak ada tabel atau perbandingan. Literatur RCPSP, simulasi Monte Carlo risiko jadwal, earned schedule, dan konformal/probabilistik prediksi tidak dibahas. | Tambahkan subbab Tinjauan Pustaka dengan tabel perbandingan (domain, data, metrik, kalibrasi) dan bahas pendekatan probabilistik klasik (PERT/Monte Carlo, earned schedule). |
| Referensi relevan dan terkini | 3 | Rujukan [11], [12], [19]-[22] relevan untuk kalibrasi. Sebagian terkini (2022-2026), tetapi beberapa [7], [9], [26], [28] berasal dari jurnal yang kredibilitasnya perlu dipastikan. [10] adalah tesis. [26] (pemeliharaan armada) dan [27] (kuari) kurang dekat dengan topik. | Prioritaskan jurnal terindeks (Scopus/Q1-Q2) dan kurangi sumber tangensial. |
| Hubungan logis literatur dengan tujuan | 3 | Alur dari "metrik hanya mengukur diskriminasi" ke "kalibrasi diperlukan" ke tujuan penelitian cukup logis. Hubungan ke "model diuji pada subproyek yang tidak pernah dilihat" dan ke "data historis dari simulasi" kurang didukung literatur. | Tambahkan rujukan tentang validasi lintas domain dan simulasi sebagai pembangkit data (misal data sintetis dalam proyek). |

## 4. Methodology

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Deskripsi jenis dan sumber data | 3 | Sumber data dijelaskan: dokumen PMP, 337 aktivitas, 171 risiko (148 disimulasikan), 24.000 observasi (Bagian 2.1-2.2, Tabel 1-2). Data seluruhnya sintetis. Tidak ada deskripsi sebaran durasi (distribusi apa), sehingga fungsi pembangkit tidak jelas. Nilai f = 0,4 dipilih agar median P-FNE-08 sesuai (5,3% vs 5,3% dokumen), yaitu kalibrasi ke satu subproyek. Peluang CR 0,10 dan dampak diasumsikan tanpa dasar. | Berikan tabel parameter simulasi dengan sumbernya, justifikasi f dan peluang CR, dan uji sensitivitas dalam tabel (bukan hanya kalimat di Bagian 3.6). Nyatakan bahwa data sintetis berarti model mempelajari asumsi simulator. |
| Kejelasan desain eksperimen/pendekatan analitis | 4 | Desain jelas: 4 model, 3 kalibrasi, LOSO 8 lipatan, metrik Brier/BSS/ECE/AUC, bootstrap 2.000, Holm, Wilcoxon (Bagian 2.4-2.5). Namun pembagian "diratakan" dalam 24.000 observasi yang saling berkorelasi (1.000 iterasi x 3 titik per subproyek) bukan sampel independen. | Jelaskan unit analisis. Gunakan bootstrap berlapis (subproyek, iterasi) atau uji dengan struktur klaster. |
| Kejelasan prosedur langkah demi langkah | 3 | Simulasi dijelaskan baik (aturan first come first served, Persamaan 1). Namun urutan pelatihan-kalibrasi-evaluasi kurang jelas: "Kalibrator dilatih dalam lipatan per subproyek di data latih" ambigu (cross-validation dalam lipatan? ukuran sampel kalibrasi?). Tidak ada diagram alur atau algoritma. Fitur X1-X7 belum ditunjukkan cara penghitungannya untuk X6/X7. | Tambahkan diagram alur pipeline dan pseudocode. Jelaskan skema pemisahan data kalibrasi dan pelatihan. |
| Kesesuaian metode dengan rumusan masalah | 4 | Kalibrasi, LOSO, dan ambang Youden/zona cocok dengan tujuan. Ketiadaan rumusan masalah membuat pemetaan implisit. Tidak ada baseline non-ML (misal SPI sederhana, EVM, atau Monte Carlo atas rencana) sehingga klaim melampaui EVM belum teruji. | Tambahkan baseline EVM/SPI-threshold dan Monte Carlo murni. |
| Validitas dan kemungkinan replikasi | 2 | Hyperparameter ditetapkan tetap tanpa tuning (RF kedalaman 3, GB 100 tahap), benih acak tidak disebut, tidak ada pernyataan ketersediaan kode atau data, dokumen PMP tidak tersedia. Validitas eksternal rendah karena data sintetis. Ambang 0,35/0,65 untuk zona tidak dijustifikasi. Hipotesis ditentukan sebelum eksperimen (baik) tetapi tidak ada pra-registrasi. | Sediakan repositori (kode, parameter simulasi, benih acak), laporkan versi scikit-learn, lakukan tuning dalam nested CV, dan jelaskan dasar ambang zona. |

## 5. Preliminary Data / Result

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dan kualitas data hasil awal | 3 | Hasil cukup kaya (Tabel 2-6, Gambar 1-4), tetapi seluruhnya dari data sintetis. Proporsi terlambat antarsubproyek sangat berbeda (0,4% di P-FNE-02 sampai 98,9% di P-FNE-04, Tabel 2), yang menunjukkan simulator menghasilkan kondisi ekstrem. Itu menurunkan kualitas kasus uji lintas subproyek. Angka dalam Tabel 3-5 konsisten secara aritmetika (BSS, selisih Brier). | Evaluasi pada data nyata. Bahas apakah sebaran label ekstrem realistis. |
| Kejelasan penyajian visual | 3 | Tabel jelas, tetapi tata letak buruk: kolom terpotong ("Subproy ek", "Terlamb at", "Pemban ding naif", Tabel 2-3) dan Tabel 6 sempit. Gambar 1-4 terlalu kecil: legenda, label sumbu, dan label forest plot (Gambar 2) hampir tak terbaca. Gambar 3-4 padat. | Perbesar gambar (lebar satu kolom penuh atau dua kolom), perbesar font, dan ubah tabel agar tidak terpecah. Gunakan palet yang dapat dibedakan untuk buta warna. |
| Interpretasi awal terhadap hasil | 4 | Interpretasi cermat: non-linearitas SPI (korelasi Spearman -0,786 vs -0,435), NN terlalu yakin (27,2% prediksi ≤0,01 atau ≥0,99), miskalibrasi akibat perbedaan tingkat dasar (Bagian 3.2-3.3). Ada penjelasan alternatif yang saling melengkapi. Namun penjelasan GB dan log-loss ([15] vs [11]) masih spekulatif karena tidak diuji. | Uji penjelasan dengan eksperimen (misal GB dengan loss lain) atau tandai sebagai hipotesis. |
| Perbandingan dengan baseline/ekspektasi | 3 | Ada baseline naif dan BSS (Tabel 3), yang bagus. Baseline domain (EVM/SPI, Monte Carlo) tidak ada, dan perbandingan dengan penelitian lain (Bagian 3.6) dinyatakan tidak langsung sebanding. Hasil per subproyek (GB lebih akurat dari RF hanya pada 5 dari 8) melemahkan klaim keunggulan. | Tambahkan baseline domain dan tabel hasil per subproyek untuk metrik utama. |

## 6. Discussion

Catatan struktural: Pembahasan tidak terpisah. Bagian 3 bernama "Hasil dan Pembahasan" dan Bagian 3.6 berisi perbandingan literatur.

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Argumentasi atas temuan secara logis | 3 | Argumen umumnya runtut. Ada inkonsistensi inferensi di Bagian 3.4. Tertulis bahwa Holm diterapkan atas 17 uji, tetapi p = 0,039 pada Wilcoxon dengan hanya 8 subproyek dianggap signifikan. Dengan Holm (p x 17) hasil itu tidak signifikan. Uji Wilcoxon eksak n = 8 punya p minimum 0,0078 (dua sisi). H3 dinyatakan "diterima" berdasarkan bootstrap gabungan padahal tidak konsisten per subproyek. | Perbaiki dan jelaskan: laporkan p terkoreksi Holm, dan nyatakan bahwa hanya satu uji yang signifikan sebelum koreksi (atau tidak sama sekali setelahnya). Turunkan klaim H2/H3 menjadi "didukung pada tingkat gabungan". |
| Hubungan hasil dengan literatur terdahulu | 3 | Hubungan dibuat: bertentangan dengan [11] untuk boosted trees, sejalan dengan [12] untuk NN, berbeda dengan [27] (Bagian 3.2, 3.6). Perbandingan dengan [5], [7], [10] diakui tidak langsung. Beberapa pembanding ([26], [28]) dipakai ringan. | Perkuat dengan tabel perbandingan dan diskusi mengapa hasil berbeda (domain, data sintetis, ukuran data). |
| Relevansi dan kontribusi pada bidang keilmuan | 3 | Temuan "kalibrasi pasca-latih tidak mentransfer antar proyek" relevan, dan penalaran bahwa miskalibrasi bersumber dari perbedaan tingkat dasar bukan model berguna. Namun karena data sintetis dan hanya delapan subproyek, generalisasi lemah dan kontribusi belum dijabarkan secara eksplisit. | Rumuskan kontribusi ke dalam 2-3 butir dan beri batas generalisasi. |
| Kekuatan penalaran dan analisis kritis | 4 | Analisis kritis cukup kuat: P-FNE-08 (BSS -0,414, utilisasi), analisis fitur ternormalisasi, paradoks Simpson pada frekuensi CR, nilai tambah dependensi hilang setelah SPI (Bagian 3.4-3.5). Poin minus: korelasi dipakai sebagai bukti mekanisme. | Hindari kesimpulan kausal dari korelasi dan tambahkan uji ablasi fitur. |
| Kesesuaian hasil dengan tujuan/hipotesis | 3 | Tujuan tercapai secara deskriptif. Status hipotesis (Tabel 5) bercampur: H1 "diterima sebagian" padahal slope 0,586 dan intercept 0,155 menandakan LR tidak terkalibrasi baik, dan H5 ditolak. Penggunaan "terima" untuk H2/H3 yang tidak konsisten per subproyek berlebihan. | Gunakan "didukung/tidak didukung" dan jelaskan batas. |

## 7. Statement of Limitation

Catatan struktural: tidak ada subbab tersendiri. Keterbatasan hanya satu paragraf di akhir Bagian 3.6 (halaman 6).

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Pengakuan atas keterbatasan | 3 | Diakui: data dibangkitkan dari rencana sehingga hanya berlaku untuk proyek yang sesuai asumsi simulasi, hanya delapan subproyek, satu aturan prioritas, dan antrean antarsubproyek tidak dimodelkan. Namun ancaman utama (tanpa data realisasi, parameter f dan peluang CR diasumsikan, label dan fitur berasal dari simulator yang sama, hyperparameter tidak dituning) tidak diakui. | Buat subbab "Keterbatasan" tersendiri dan tambahkan butir tersebut. |
| Dampak keterbatasan terhadap interpretasi | 2 | Dampak hampir tidak dibahas. Hanya sensitivitas (BSS tetap positif pada faktor mitigasi 0,2 dan 1,0, tetapi ECE memburuk menjadi 0,114) yang disebut tanpa tabel. Tidak dijelaskan bagaimana data sintetis memengaruhi klaim "GB paling terkalibrasi" atau ambang 0,485. | Tuliskan dampak tiap keterbatasan terhadap klaim yang bersangkutan dan sajikan hasil sensitivitas dalam tabel. |
| Kejelasan ruang lingkup yang tidak dicakup | 3 | Beberapa disebut (antarsubproyek, prioritas, data nyata di saran Kesimpulan). Tidak ada pernyataan ringkas tentang yang di luar cakupan (biaya, kualitas, jenis proyek lain, estimasi besaran keterlambatan). | Tambahkan paragraf "di luar cakupan". |

## 8. Conclusion

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Ringkasan kontribusi utama dan hasil | 4 | Ringkasan akurat dan konsisten dengan Abstrak (Brier 0,1718, BSS 0,367, ECE 0,0560, AUC 0,815; RF lebih baik dari LR; NN lebih buruk dari naif). Hasil hipotesis tidak diringkas satu per satu. | Tambahkan ringkasan status H1-H5. |
| Penegasan kembali pentingnya temuan | 3 | Ditegaskan sebagai dasar sistem peringatan dini berzona dan peran SPI. Pentingnya temuan kalibrasi lintas proyek kurang ditekankan, dan tidak ada penegasan terhadap keterbatasan data sintetis. | Tegaskan dampak bagi praktik dan teori, sambil menyebut kualifikasi. |
| Kesesuaian dengan rumusan masalah dan tujuan awal | 4 | Selaras dengan tujuan di Bagian 1 (membangun dan membandingkan model, mengevaluasi kalibrasi, menentukan ambang). Karena tidak ada RQ eksplisit, pencocokan hanya terhadap tujuan. | Setelah RQ dibuat, jawab tiap RQ secara berurutan. |
| Saran riset selanjutnya | 4 | Konkret: validasi dengan data realisasi, kalibrasi ulang bertahap, tambah subproyek dan variabel karakter proyek, dan pemodelan perambatan antarsubproyek. | Tambahkan metode kalibrasi alternatif (beta, conformal), baseline Monte Carlo, dan evaluasi di organisasi lain. |

## 9. References & Bibliography

| Item | Skor | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Keterkinian dan relevansi | 3 | Dari 28 rujukan, sekitar 9 berumur 2022-2026 ([1], [6], [7], [9], [10], [14], [26], [27], [28]). Tiga rujukan kalibrasi inti ([11] 2005, [12] 2017, [20] 2016) relevan. Beberapa rujukan baru berasal dari penerbit/jurnal yang kredibilitasnya perlu diverifikasi, satu adalah tesis [10], dan [1] kurang relevan dan merupakan swa-sitasi. Rujukan prediksi keterlambatan proyek ERP terkini yang kuat masih sedikit. | Tambah rujukan 2021-2026 dari jurnal terindeks tentang prediksi jadwal proyek dan kalibrasi probabilistik. Verifikasi DOI [7], [26], [28]. |
| Format sitasi konsisten dan sesuai standar | 2 | Teks memakai gaya numerik bracket (IEEE/Vancouver), sementara daftar memakai gaya APA (nama, tahun di depan). Banyak inkonsistensi: [17] memakai "dalam:" (Indonesia) dalam daftar berbahasa Inggris, nomor halaman tidak ada pada [26], [28] dan beberapa lain, format DOI bervariasi (ada "doi:" dan tidak berformat tautan), penulisan inisial dan judul tidak seragam, judul jurnal dan kapitalisasi tidak konsisten. Perataan justify membuat spasi aneh (misal [21], [22]). | Pilih satu gaya (IEEE atau APA) sesuai pedoman jurnal dan terapkan secara konsisten, termasuk DOI dan halaman. Gunakan alat pengelola referensi. |
| Rujukan dalam teks cocok dengan daftar | 4 | Pemeriksaan pada [1]-[28]: semua nomor dalam teks ada di daftar dan tidak ada rujukan yatim yang tampak. [15] dipakai untuk GB dan log-loss, [26] hanya sekali di 3.2. | Pastikan tiap rujukan dikutip sesuai klaim, terutama [1], [26], [28]. |
| Keseimbangan klasik dan terbaru | 3 | Ada rujukan klasik metodologi yang tepat (Brier 1950, Youden 1950, Wilcoxon 1945, Holm 1979, Efron 1993, Platt 1999, Friedman 2001), dan rujukan terbaru 2022-2026. Namun rujukan domain inti (EVM, penjadwalan sumber daya) hanya [2] 2010, [3] 2015 dan sisanya periode 2016-2020 sedikit. Sebagian besar literatur domain terbaru bersifat satu-dua studi per topik. | Seimbangkan: tambah literatur domain 2018-2024 dan kurangi rujukan tangensial. |

## Saran umum: struktur

1. Ikuti kerangka IMRaD yang eksplisit: Pendahuluan, Tinjauan Pustaka (subbab tersendiri dengan tabel sintesis), Metode, Hasil, Pembahasan, Keterbatasan, Kesimpulan. Saat ini Hasil dan Pembahasan digabung (Bagian 3) dan keterbatasan hanya satu paragraf di akhir 3.6.
2. Tambahkan rumusan masalah atau RQ di Pendahuluan, dan pindahkan hipotesis H1-H5 dari Bagian 2.5 ke sana. Petakan RQ ke hipotesis ke tabel hasil ke kesimpulan.
3. Nyatakan sejak Abstrak dan Pendahuluan bahwa data adalah sintetis. Tambahkan subbab validitas yang membahas ancaman (circularity simulator-model, parameter f dan CR yang diasumsikan).
4. Pindahkan hasil sensitivitas dan hasil per subproyek ke tabel utama, bukan hanya kalimat. Tambahkan diagram alur pipeline.
5. Perbaiki tata letak: ruang kosong besar di halaman 2-3 dan 5, halaman 8 hampir kosong, placeholder template (Vol. x, xx-xx-20xx) masih ada, tabel terpotong, dan gambar terlalu kecil.
6. Periksa konsistensi dan inferensi statistik: Holm vs p = 0,039 (Bagian 3.4), dan sebutkan unit independen.
7. Sediakan pernyataan ketersediaan kode dan data.

## Saran umum: bahasa

1. Bahasa Indonesia umumnya jelas dan akademik, tetapi banyak istilah Inggris tanpa padanan atau konsistensi: "terlalu yakin" (overconfident), "pembanding naif", "reliability diagram", "recall", "specificity", "change request". Pilih satu pendekatan: cetak miring konsisten untuk istilah asing, dan berikan padanan Indonesia pada kemunculan pertama.
2. Kalimat sering panjang dan padat angka (Abstrak, 3.4, 3.5). Pecah menjadi kalimat pendek dan pindahkan angka ke tabel.
3. Gunakan format angka konsisten: koma desimal di teks, tetapi gambar dan sebagian tabel memakai titik. Tulis "p = 0,039" dengan p miring dan format persamaan seragam (spasi "C = 1", "f = 0,4").
4. Hindari klaim berlebihan ("paling akurat dan paling terkalibrasi", "diterima") tanpa kualifikasi, dan gunakan bahasa hati-hati ("didukung pada data simulasi ini").
5. Istilah konsisten: "subproyek" vs "proyek" dan "ambang" vs "zona", serta konsistensi judul ("Multi Sumber Daya Terbatas").
6. Abstrak Inggris dan Indonesia perlu disamakan isinya, dan sebaiknya hapus salah satu bila pedoman jurnal tidak mensyaratkan keduanya.

## Rekapitulasi skor

| Kelompok | Jumlah item | Rata-rata |
|---|---|---|
| 1. Topic | 4 | 3,50 |
| 2. Abstract | 5 | 3,40 |
| 3. Introduction + Literature Review | 8 | 2,88 |
| 4. Methodology | 5 | 3,20 |
| 5. Preliminary Data / Result | 4 | 3,25 |
| 6. Discussion | 5 | 3,20 |
| 7. Statement of Limitation | 3 | 2,67 |
| 8. Conclusion | 4 | 3,75 |
| 9. References & Bibliography | 4 | 3,00 |

- **Rata-rata total, seluruh 42 item (jumlah skor 134):** 3,19 dari 5.
- **Rata-rata dari rata-rata kelompok:** 3,21.
- **Rekomendasi:** revisi mayor.

Prioritas revisi:
1. Pisahkan Tinjauan Pustaka, rumusan masalah, Pembahasan, dan Keterbatasan.
2. Nyatakan dan telaah dampak data sintetis, termasuk parameter f dan peluang CR.
3. Perbaiki inkonsistensi inferensi (Holm vs p = 0,039) dan lengkapi hasil per subproyek serta baseline domain.
4. Rapikan format referensi dan sediakan kode atau data untuk replikasi.
5. Perbaiki gambar dan tabel agar terbaca.
