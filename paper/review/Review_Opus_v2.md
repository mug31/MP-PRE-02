# Review Paper oleh Reviewer AI (Opus), putaran 2

> Dijalankan 16 November 2026 setelah revisi A dan B (commit c7f9cee), dengan prompt review dari dosen yang sama
> persis dengan putaran 1 (`Review_Opus.md`). Reviewer adalah agen baru tanpa konteks sesi kerja, hanya membaca
> PDF render dari `paper/Paper_PRE02_Pustaka_Data.docx` (11 halaman), tanpa akses ke berkas lain atau web.
> Isi di bawah adalah keluaran reviewer apa adanya.

---

# Hasil review naskah "Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas" (Jurnal Pustaka Data, 11 halaman)

Saya membaca semua halaman 1–11, termasuk Tabel 1–9 dan Gambar 1–4. Halaman 11 kosong dan hanya berisi header dan footer.

**Penilaian ringkas:** naskah ini tergolong baik secara metodologis untuk ukuran studi dengan data sintetis. Validasinya leave-one-subproject-out, kalibrasinya dievaluasi per subproyek, ada uji bootstrap dengan koreksi Holm, dan keterbatasannya dilaporkan terbuka. Kelemahan utamanya ada tiga:
- Data sepenuhnya sintetis dan dibangkitkan oleh simulator penulis sendiri, sehingga ada risiko sirkularitas.
- Tidak ada baseline EVM/SPI. Padahal bagian Pendahuluan menempatkan EVM sebagai pendekatan konvensional yang hendak diperbaiki.
- Abstrak dan Kesimpulan mengklaim probabilitas dapat dikalibrasi ulang pada proyek berjalan. Namun skenario itu hanya diuji sebagai batas atas yang memakai label subproyek uji (ECE 0,0271, subbab 3.3).

**Rekomendasi:** revisi mayor.

---

## 1. Topic

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dengan bidang teknik informatika | 4 | Topiknya pemodelan prediktif dengan ML (LR, RF, GB, NN), kalibrasi probabilitas, dan sistem peringatan dini untuk proyek implementasi ERP (Bab 1, subbab 2.4). Ini masuk ranah informatika terapan dan rekayasa perangkat lunak. Unsur manajemen proyeknya dominan, tetapi kontribusi komputasinya jelas. | Tegaskan di Pendahuluan posisi studi dalam informatika, misalnya *predictive analytics* untuk manajemen proyek perangkat lunak/ERP. Jelaskan juga bahwa kerangka ini berpotensi diimplementasikan sebagai modul dalam sistem informasi manajemen proyek. |
| Kejelasan dan fokus topik | 4 | Fokusnya jelas: probabilitas keterlambatan di atas 5% dari baseline, terkalibrasi, dan diuji pada subproyek yang tidak pernah dilihat model (RQ1–RQ3, hlm. 3). Judulnya tidak mencerminkan dua unsur inti, yaitu kalibrasi dan peringatan dini, dan tidak menyebut ML maupun data sintetis. | Ubah judul agar memuat unsur kunci. Contoh: "Prediksi dan Kalibrasi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas untuk Sistem Peringatan Dini Berbasis Data Simulasi". |
| Nilai kebaruan atau kontribusi | 3 | Kebaruannya ada pada evaluasi kalibrasi lintas proyek (pooled ECE 0,056 vs rata-rata ECE per subproyek 0,1615) dan pembangkitan data dari dokumen PMP. Namun keempat algoritmanya standar tanpa *tuning*. Data sintetis berasal dari satu portofolio. Temuan bahwa kalibrasi tidak berpindah saat *base rate* berbeda sudah dikenal dalam literatur *dataset shift*/*prior shift*, yang tidak dibahas. | Posisikan kebaruan secara eksplisit terhadap literatur *label shift*/*prior probability shift* dan *transportability* model risiko. Tambahkan kontribusi metodologis yang lebih kuat, misalnya skema rekalibrasi bertahap yang realistis, yaitu memakai data awal proyek berjalan tanpa label akhir. |
| Potensi dampak akademik atau praktis | 3 | Implikasi praktisnya menarik: zona Hijau/Kuning/Merah, 56,7% iterasi terlambat sudah diperingatkan pada titik 25%, dan contoh P-FNE-03 dengan waktu tindak 165 hari (hlm. 8). Namun semua hasil berasal dari simulasi dan belum ada validasi pada proyek nyata, sehingga dampaknya masih potensial. | Tambahkan setidaknya studi kasus kecil dengan data realisasi, atau validasi eksternal pada dataset publik penjadwalan proyek, misalnya instans PSPLIB/RCMPSP dengan data aktual bila tersedia. Diskusikan juga biaya peringatan palsu (38% pada θ*, Tabel 8) dari sisi pengambil keputusan. |

## 2. Abstract

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Kejelasan tujuan dan ruang lingkup penelitian | 4 | Tujuannya jelas: memprediksi probabilitas keterlambatan >5% dan menguji kalibrasinya pada proyek yang tidak dipakai melatih. Ruang lingkupnya juga disebut: 8 subproyek, 24.000 observasi, tiga titik monitoring (hlm. 1). | Sebut eksplisit bahwa variabel terikatnya biner dan bahwa besaran keterlambatan tidak dicakup. Pembatasan ini baru muncul di subbab 2.3. |
| Pernyataan masalah disampaikan secara ringkas | 4 | Kalimat pembuka "Manajer proyek membutuhkan peluang keterlambatan, bukan sekadar label berisiko" ringkas dan tajam. Masalah ketiadaan data historis juga dinyatakan. | Tambahkan satu frasa yang menyebut mengapa kalibrasi lintas proyek menjadi masalah, yaitu *base rate* keterlambatan berbeda antarproyek. |
| Paparan singkat hasil eksperimen | 4 | Angka utama lengkap: Brier 0,172, ECE 0,056, ROC-AUC 0,815, ECE per subproyek 0,162, ROC-AUC 0,725→0,915, dan 56,7%. | Kurangi angka yang tidak esensial. Tambahkan rentang ketidakpastian, misalnya CI 95% Brier GB, agar klaim "paling akurat" terukur. Sebut bahwa selisih GB vs RF kecil (0,0043). |
| Penjabaran temuan utama dan kontribusinya | 3 | Kalimat akhir "dapat menjadi dasar sistem peringatan dini berzona, dengan syarat dikalibrasi ulang menggunakan data proyek yang sedang berjalan" melampaui bukti. Rekalibrasi pada subproyek sendiri (ECE 0,0271, subbab 3.3) memakai label subproyek uji dan diakui hanya batas atas. Temuan NN tanpa *early stopping* juga lebih merupakan artefak konfigurasi daripada temuan substantif. | Lunakkan klaim rekalibrasi, misalnya "berpotensi … bila tersedia data proyek berjalan; skenario ini baru diuji sebagai batas atas". Ganti kalimat tentang NN dengan temuan yang lebih bermakna, misalnya dominasi SPI atau paradoks antarsubproyek. |
| Kejelasan dan keringkasan narasi abstrak | 3 | Abstrak padat angka (lebih dari 12 nilai numerik) sehingga sulit dibaca. Abstrak bahasa Indonesia juga sarat istilah asing bercetak miring (*baseline*, *monitoring*, *change request*, *early stopping*). | Batasi 150–200 kata dengan struktur latar–tujuan–metode–hasil–implikasi. Pakai padanan Indonesia bila ada: garis dasar, pemantauan, permintaan perubahan, penghentian dini. |

## 3. Introduction + Literature Review

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Definisi dan deskripsi istilah kunci/topik | 4 | EVM, EV, PV, SPI, ROC-AUC, dan proyek multi sumber daya terbatas didefinisikan (hlm. 2). Konsep kalibrasi dijelaskan dengan contoh intuitif ("probabilitas 0,8 baru bermakna bila sekitar 80%…"). | Definisikan secara formal *resource-constrained multi-project scheduling* (RCMPSP) dan "kalibrasi lintas proyek". Jelaskan juga perbedaan diskriminasi dan kalibrasi lebih awal. |
| Kejelasan latar belakang dan urgensi penelitian | 3 | Latar belakangnya logis. Urgensinya hanya didukung satu rujukan [1], yaitu studi SNA pemangku kepentingan ERP oleh sebagian penulis sendiri, yang relevansinya terhadap klaim keterlambatan lemah. Tidak ada data besaran masalah, misalnya tingkat keterlambatan proyek ERP. | Tambahkan bukti empiris tentang frekuensi dan dampak keterlambatan proyek ERP/TI dari studi atau survei bereputasi. Ganti atau lengkapi [1] dengan sumber yang langsung membahas keterlambatan. |
| Penyajian fakta yang mendukung relevansi studi | 3 | Tabel 1 menyajikan fakta studi terdahulu, termasuk kritik bahwa AUC 0,997 berasal dari 100 data [8]. Fakta tentang kerugian akibat keterlambatan atau kebutuhan industri akan probabilitas terkalibrasi belum disajikan. | Tambahkan fakta kuantitatif tentang biaya atau frekuensi keterlambatan. Sertakan juga rujukan bahwa keputusan berbasis ambang memerlukan probabilitas terkalibrasi, misalnya dari bidang prediksi risiko klinis [21]. |
| Kejelasan rumusan masalah | 4 | RQ1–RQ3 (hlm. 3) spesifik dan dapat diuji. | RQ3 menggabungkan dua pertanyaan, yaitu waktu/ambang dan variabel penentu. Pisahkan menjadi RQ3 dan RQ4 agar pemetaan ke hasil (subbab 3.5) lebih rapi. |
| Pernyataan novelty penelitian | 3 | Kontribusi utama dan pendukung dinyatakan eksplisit (hlm. 3). Namun klaim "kerangka sistem peringatan dini … terkalibrasi" tidak sepenuhnya didukung hasil, karena probabilitas tidak terkalibrasi per subproyek (ECE 0,1615). | Rumuskan novelty sebagai "evaluasi kalibrasi lintas proyek yang menunjukkan bahwa kalibrasi gabungan menyesatkan". Ini memang yang dibuktikan. Jangan merumuskannya sebagai "kerangka terkalibrasi". |
| Sintesis literatur dan identifikasi research gap | 4 | Tabel 1 merangkum 8 studi dengan domain, data, dan metrik. Tiga celah dirumuskan jelas (hlm. 2): kalibrasi belum dievaluasi, dependensi dan sumber daya jarang dimuat, dan ketiadaan data historis. | Sintesis belum mencakup simulasi Monte Carlo/*schedule risk analysis* klasik dan literatur *dataset shift*. Tambahkan juga kolom "validasi" di Tabel 1 (acak, per proyek, atau temporal) karena ini inti argumen. |
| Referensi relevan dan terkini | 3 | Ada rujukan 2022–2026 ([6], [8], [10]–[12], [27], [28]). Namun beberapa sumbernya berkualitas rendah atau sulit diverifikasi: tesis magister [9], jurnal kurang dikenal tanpa DOI [11], IJSREM [28]. Rujukan langsung tentang kalibrasi di manajemen proyek tidak ada. | Ganti [11] dan [28] dengan publikasi bereputasi. Tambahkan studi kalibrasi dan *dataset shift* terbaru serta studi ML penjadwalan proyek di jurnal seperti IJPM, Automation in Construction, atau IEEE TSE. |
| Hubungan logis antara literatur dan tujuan penelitian | 4 | Alurnya runtut: keterbatasan EVM, ML terbukti tetapi tanpa kalibrasi, simulasi + ML, lalu tujuan. Celah 1 terhubung ke RQ2 dan celah 3 ke prosedur data. | Celah 2 (dependensi dan perebutan sumber daya) tidak terhubung ke RQ mana pun. Hasilnya pun menunjukkan dependensi hampir tidak menambah informasi. Hubungkan celah ini ke RQ3 secara eksplisit. |

## 4. Methodology

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Deskripsi lengkap jenis dan sumber data | 4 | Sumber datanya jelas: dokumen PMP 8 subproyek, 337 aktivitas, 171 risiko, dan 148 yang disimulasikan beserta alasan pengecualiannya (subbab 2.1). Statistik per subproyek ada di Tabel 3. | Sajikan ringkasan karakteristik per subproyek: jumlah aktivitas, jumlah peran/sumber daya, kepadatan jaringan, dan jumlah risiko. Jelaskan apakah dokumen PMP dapat diakses atau dideskripsikan cukup untuk replikasi. |
| Kejelasan desain eksperimen atau pendekatan analitis | 4 | Desain LOSO 8 lipatan, kalibrator dengan *group CV* 3 lipatan, hipotesis H1–H5, bootstrap per iterasi, dan koreksi Holm sudah jelas (subbab 2.4–2.5). | Tambahkan diagram alur metodologi (simulasi → fitur → LOSO → kalibrasi → evaluasi → ambang). Jelaskan apakah titik monitoring dimasukkan sebagai fitur, karena X2 sisa waktu bergantung pada T yang berbeda per subproyek. |
| Kejelasan prosedur langkah demi langkah | 3 | Banyak detail simulasi belum dijelaskan: distribusi durasi aktivitas (deterministik atau stokastik), cara risiko dipetakan ke aktivitas (acak?), kalender kerja, cara EV(t) dihitung untuk X1 dan X3, dan cara X7 diukur. Persamaan (3) memakai notasi ŷ untuk proporsi aktual, terbalik dari konvensi. Dekomposisi *reliability*/*resolution* disebut di subbab 2.5 tetapi tidak dilaporkan di hasil. | Tambahkan pseudocode simulasi. Lengkapi definisi operasional X1–X7 dengan rumus. Seragamkan notasi ECE. Laporkan atau hapus dekomposisi Brier. |
| Kesesuaian metode dengan rumusan masalah | 3 | Metode umumnya sesuai RQ, tetapi ada empat masalah. (a) Tidak ada baseline EVM/SPI, padahal ini pembanding paling relevan menurut Pendahuluan. (b) Hiperparameter tidak di-*tuning* dan NN tanpa *early stopping* (1000 epoch), sehingga perbandingan antarmodel bias terhadap NN. (c) RF dengan kedalaman 3 sangat dangkal. (d) Uji Wilcoxon dengan n=8 secara matematis tidak mungkin lolos Holm (p min 0,0039 > 0,0029, hlm. 4), sehingga uji itu tidak informatif. | Tambahkan baseline SPI-only, misalnya logistik dengan SPI saja atau aturan T/SPI > 1,05T. Lakukan *nested* LOSO untuk *tuning* atau setidaknya *early stopping* standar. Ganti Wilcoxon dengan pendekatan yang punya daya uji, misalnya model efek campuran atau bootstrap hierarkis subproyek–iterasi. |
| Validitas dan replikasi metodologi | 3 | Seed, versi scikit-learn, dan hiperparameter dilaporkan, dan itu positif. Namun kode dan data hanya "tersedia atas permintaan" (hlm. 4) dan dokumen PMP tidak publik. Nilai f = 0,4 juga dipilih dengan mencocokkan P-FNE-08, yang kemudian dipakai sebagai subproyek uji (diakui di subbab 2.2). | Unggah kode, data sintetis, dan konfigurasi simulasi ke repositori publik ber-DOI (Zenodo/GitHub). Pilih f tanpa memakai subproyek yang dievaluasi, atau laporkan hasil dengan P-FNE-08 dikeluarkan. |

## 5. Preliminary Data / Result

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Relevansi dan kualitas data hasil awal | 3 | Data relevan dan berukuran besar (24.000), tetapi sangat tidak seimbang antarsubproyek: P-FNE-02 0,4% terlambat dan P-FNE-04 98,9% (Tabel 3). Metrik per subproyek di kedua ekstrem itu tidak stabil. Ketiga observasi per iterasi saling bergantung. Data juga bersifat sintetis sehingga dominasi SPI merupakan konsekuensi struktur simulasi (diakui di subbab 3.8). | Laporkan jumlah kasus positif per lipatan dan CI untuk metrik per subproyek (Tabel 7). Tambahkan analisis yang mengeluarkan dua subproyek ekstrem. Tambahkan derau pelaporan progres pada simulasi agar lebih realistis. |
| Kejelasan penyajian visual (grafik/tabel) | 4 | Gambar 1–4 informatif dan bertanda CI. Ada beberapa masalah: label H3a–H5h di Gambar 2 tidak didefinisikan di Tabel 6 atau teks. Tabel 6 memakai baris judul hipotesis yang menyela data. Tabel 5 memuat "Brier Raw" tetapi tidak memuat Brier setelah kalibrasi. Tabel 4 tidak memuat CI. *Permutation importance* tidak divisualkan. Halaman 11 kosong. | Selaraskan label Gambar 2 dengan Tabel 6. Lengkapi Tabel 5 dengan Brier Platt/Isotonic dan Tabel 4 dengan CI. Tambahkan grafik *permutation importance*. Hapus halaman kosong. |
| Interpretasi awal terhadap hasil | 4 | Interpretasinya cermat. Contohnya: perbedaan ECE gabungan vs per subproyek dijelaskan sebagai saling menutupi antar-interval (hlm. 5), slope RF 1,555 ditafsirkan benar, dan kasus P-FNE-08 dianalisis (hlm. 7). Ada satu lompatan: keunggulan model pohon disimpulkan sebagai bukti hubungan non-linear hanya dari perbedaan korelasi Spearman antar-titik, padahal itu lebih tepat disebut efek interaksi dengan fase. | Uji klaim non-linearitas dengan LR yang diberi suku interaksi SPI × fase atau *spline*. Jelaskan perbedaan antara *specificity* 81,9% dan peringatan palsu kumulatif 38% (Tabel 8) agar tidak membingungkan. |
| Perbandingan dengan baseline atau ekspektasi sebelumnya | 3 | Baseline yang dipakai hanya pembanding naif (*base rate* data latih). Tidak ada pembanding EVM/SPI deterministik maupun metode simulasi klasik. Perbandingan dengan studi terdahulu (subbab 3.6) kualitatif dan tanpa angka berdampingan. | Tambahkan baseline EVM/SPI dan model satu variabel SPI. Sajikan tabel perbandingan kuantitatif dengan studi di Tabel 1, dengan catatan perbedaan skema validasi. |

## 6. Discussion

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Argumentasi atas temuan secara logis | 4 | Argumen tentang kegagalan Platt/Isotonic lintas proyek (hlm. 6) disertai pembuktian tambahan: Platt per subproyek turun menjadi 0,0271 dan intercept LR menyebar −2,777 s.d. 3,361. Argumen ini meyakinkan. | Jadikan analisis *base rate shift* temuan sentral. Uji solusi praktis seperti penyesuaian *prior* atau koreksi intercept dengan *base rate* yang diestimasi dari dokumen PMP sebelum proyek berjalan. |
| Hubungan hasil dengan literatur terdahulu | 3 | Ada keterkaitan dengan [4], [6], [10], [13], [14], [27], [28]. Rujukan [27] tentang perawatan armada logistik kurang relevan sebagai pembanding. Hubungan dengan literatur *dataset shift* dan *transportability* model risiko, yang menjadi inti temuan RQ2, tidak dibahas. | Kaitkan temuan RQ2 dengan literatur *prior/label shift* dan validasi eksternal model prediksi klinis. Ganti [27] dengan studi manajemen proyek yang sebanding. |
| Relevansi dan kontribusi terhadap bidang keilmuan | 3 | Pesan "ECE gabungan menyembunyikan miskalibrasi per proyek" (subbab 3.7) berguna bagi peneliti. Namun karena semuanya berbasis simulasi satu portofolio, generalisasi kontribusinya terbatas. | Tambahkan subbab yang memisahkan kontribusi metodologis yang dapat digeneralisasi (protokol evaluasi) dari temuan spesifik simulasi (dominasi SPI). |
| Kekuatan penalaran dan analisis kritis | 4 | Penulis kritis terhadap hasilnya sendiri. Contohnya: H2/H3 hanya berlaku pada data gabungan (hlm. 7), analisis Simpson pada frekuensi CR (hlm. 8), dan pengakuan bahwa *early stopping* mengubah peringkat NN (hlm. 5). Namun analisis *early stopping* bersifat *post hoc*, dan rentang Brier 0,171–0,190 tidak jelas apakah per lipatan atau gabungan. | Perjelas satuan analisis *early stopping*. Pertimbangkan menjadikan konfigurasi dengan *early stopping* sebagai analisis utama yang direncanakan, atau sajikan keduanya berdampingan sejak awal agar perbandingan adil. |
| Kesesuaian hasil dengan tujuan atau hipotesis awal | 4 | Tabel 6 memetakan keputusan setiap hipotesis secara transparan. Kriteria "terkalibrasi baik" pada H1 dan ambang keputusan untuk intercept/slope tidak didefinisikan sebelumnya, sehingga label "didukung sebagian" terkesan subjektif. Isotonic pada H5 tidak muncul di Tabel 6. | Definisikan kriteria operasional H1 sejak subbab 2.5, misalnya CI intercept memuat 0 dan CI slope memuat 1. Masukkan semua 17 uji ke Tabel 6 atau ke lampiran. |

## 7. Statement of Limitation

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Pengakuan atas keterbatasan penelitian | 4 | Subbab 3.8 memuat lima keterbatasan yang jujur: data sintetis, asumsi parameter, cakupan, tanpa *tuning*, dan ambang optimistis. Ada analisis sensitivitas f (Tabel 9). | Tambahkan keterbatasan yang belum disebut: (a) tidak ada baseline EVM, (b) ambang zona 0,35/0,65 tidak diturunkan secara empiris, (c) observasi berulang per iterasi, (d) label biner dengan ambang 5% tetap. |
| Dampak keterbatasan terhadap interpretasi hasil | 4 | Dampak setiap keterbatasan dijelaskan. Contohnya: SPI dominan karena struktur simulasi, nilai absolut metrik bergantung pada asumsi (ECE naik menjadi 0,114 pada f = 1,0), dan peringkat model dapat berubah. | Kuantifikasi dampak untuk parameter lain. Sensitivitas peluang CR 0,10 dan kelas kesulitan belum diuji. Tambahkan setidaknya satu tabel sensitivitas lagi. |
| Kejelasan ruang lingkup yang tidak dicakup | 3 | Sebagian ruang lingkup yang dikecualikan tersebar di beberapa tempat: besaran keterlambatan, biaya, dan waktu sampai keterlambatan (subbab 2.3), sumber daya antarsubproyek (subbab 2.1), dan risiko biaya. Tidak ada satu pernyataan ringkas. | Satukan daftar hal yang tidak dicakup dalam satu paragraf di subbab 3.8 atau di akhir Pendahuluan. |

## 8. Conclusion

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Ringkasan kontribusi utama dan hasil | 4 | Kesimpulan menjawab RQ1–RQ3 dengan angka kunci (hlm. 9). | Kurangi pengulangan angka yang sudah ada di abstrak. Fokus pada makna temuan. |
| Penegasan kembali pentingnya temuan | 3 | Pentingnya temuan "kalibrasi gabungan menyesatkan" kurang ditegaskan dan tenggelam di antara angka. Rekomendasi tindakan pada zona Merah bergantung pada probabilitas yang terbukti tidak terkalibrasi lintas proyek. | Tegaskan satu atau dua pesan utama bagi praktisi dan peneliti. Beri peringatan eksplisit bahwa zona hanya andal setelah rekalibrasi. |
| Kesesuaian dengan rumusan masalah dan tujuan awal | 4 | Ketiga RQ terjawab. Tujuan "kerangka sistem peringatan dini terkalibrasi" hanya tercapai sebagian, dan ini tidak dinyatakan terus terang. | Nyatakan bahwa tujuan probabilitas terkalibrasi pada proyek baru belum tercapai tanpa data proyek berjalan. |
| Saran untuk pengembangan riset selanjutnya | 4 | Saran rinci dan relevan: data realisasi, rekalibrasi bertahap, *tuning* per subproyek, pembanding EVM, kalibrasi beta, dan sumber daya antarsubproyek (hlm. 10). | Prioritaskan saran dan tautkan masing-masing ke keterbatasan spesifik. Pembanding EVM sebaiknya dikerjakan dalam revisi ini, bukan ditunda ke riset selanjutnya. |

## 9. References & Bibliography

| Item | Skor (1-5) | Justifikasi | Saran perbaikan |
|---|---|---|---|
| Keterkinian dan relevansi referensi | 3 | Sekitar 9 dari 28 rujukan berasal dari 2022–2026. Beberapa rujukan terbaru berkualitas meragukan: [9] tesis, [11] jurnal tanpa DOI, [28] IJSREM. [1] adalah sitasi diri yang relevansinya lemah. | Ganti sumber lemah dengan jurnal atau prosiding bereputasi. Tambahkan rujukan kalibrasi dan *dataset shift* 2020-an dan ML manajemen proyek 2023–2026. |
| Format sitasi konsisten dan sesuai standar | 3 | Gaya penomoran konsisten, tetapi detailnya tidak seragam: posisi tahun pada [18] (setelah editor), [9] memakai URN tanpa URL, [14] dan [17] tanpa DOI/URL, nama penulis "Ainul Yaqin, M." pada [1], dan pemenggalan DOI yang mengganggu pada [22] dan [23]. | Gunakan pengelola referensi (Zotero/Mendeley) dengan gaya resmi jurnal. Lengkapi DOI/URL dan seragamkan urutan elemen. |
| Referensi dalam teks cocok dengan daftar pustaka | 5 | Semua nomor [1]–[28] dirujuk dalam teks secara berurutan, dan tidak ada rujukan yang yatim. | Pertahankan. Periksa ulang setelah revisi bila rujukan ditambah. |
| Keseimbangan literatur klasik dan terbaru | 4 | Rujukan klasik metodologis tepat: Brier 1950, Youden 1950, Wilcoxon 1945, Holm 1979, Murphy 1973, Platt 1999, Zadrozny 2002, Friedman 2001. Rujukan terbaru domain juga ada. Porsi rujukan domain 2020–2026 dari sumber bereputasi masih kurang. | Tambah 4–6 rujukan domain bereputasi terkini. Pertimbangkan sumber asli ECE (Naeini dkk., 2015) di samping [14]. |

---

## Saran umum: struktur

1. **Hasil dan Pembahasan digabung.** Bab 3 terlalu panjang (8 subbab). Pertimbangkan memisahkan Bab 3 "Hasil" dari Bab 4 "Pembahasan", yang memuat perbandingan dengan literatur, implikasi, dan keterbatasan, bila templat jurnal mengizinkan.
2. **Tidak ada diagram alur metodologi.** Tambahkan satu gambar alur dari simulasi PMP sampai sistem zona di Bab 2.
3. **Analisis *early stopping* NN** (subbab 3.2) sebaiknya dipindah ke subbab analisis tambahan atau sensitivitas tersendiri agar tidak mengaburkan perbandingan utama.
4. **Pelabelan uji perlu diseragamkan.** Label H3a–H5h di Gambar 2 tidak muncul di Tabel 6. Semua 17 uji sebaiknya ditampilkan di satu tabel atau lampiran.
5. **Kelengkapan tabel.** Tabel 4 tanpa CI, Tabel 5 tanpa Brier pascakalibrasi, *permutation importance* tanpa tabel atau gambar, dan ROC-AUC per subproyek (diklaim > 0,68 di subbab 3.7) tidak disajikan.
6. **Unsur naskah yang hilang.** Halaman 11 kosong dan perlu dihapus. Tidak ada judul bahasa Inggris, pernyataan ketersediaan data/kode, ucapan terima kasih, atau pernyataan konflik kepentingan. Periksa ketentuan jurnal.
7. **Pemetaan RQ.** RQ3 sebaiknya dipecah, dan setiap subbab hasil diberi rujukan RQ eksplisit, misalnya "3.5 (RQ3)".

## Saran umum: bahasa

1. **Campuran istilah asing berlebihan.** Banyak istilah dicetak miring padahal ada padanan baku: *baseline* (garis dasar), *monitoring* (pemantauan), *early stopping* (penghentian dini), *change request* (permintaan perubahan), *subsample*, *dependency*. Gunakan padanan Indonesia dan sebut istilah asing sekali saat pertama muncul.
2. **Istilah "iterasi" ambigu.** Kata ini juga lazim berarti iterasi pelatihan. "Replikasi simulasi" atau "*run* simulasi" lebih tepat.
3. **Kalimat padat angka.** Di Abstrak dan Kesimpulan, beberapa kalimat memuat 3–5 angka sekaligus. Pecah kalimat dan pindahkan angka sekunder ke tabel.
4. **Ketepatan istilah statistik.** "Selang kepercayaan" sudah baik. Konsistenkan "probabilitas" vs "peluang" (keduanya dipakai bergantian) dan "terkalibrasi" vs "kalibrasi tambahan".
5. **Abstrak bahasa Inggris** sudah cukup baik. Perlu sedikit penyuntingan bahasa, misalnya "tests their calibration" menjadi "evaluates the calibration of these probabilities", dan "late runs were flagged" perlu dijelaskan rujukan ambangnya (θ* Youden).
6. **Ejaan.** Ejaan dan tanda desimal sudah konsisten (koma untuk bahasa Indonesia, titik untuk bahasa Inggris). Pertahankan.

---

## Rekapitulasi skor

| Kelompok | Jumlah item | Total skor | Rata-rata |
|---|---|---|---|
| 1. Topic | 4 | 14 | 3,50 |
| 2. Abstract | 5 | 18 | 3,60 |
| 3. Introduction + Literature Review | 8 | 28 | 3,50 |
| 4. Methodology | 5 | 17 | 3,40 |
| 5. Preliminary Data / Result | 4 | 14 | 3,50 |
| 6. Discussion | 5 | 18 | 3,60 |
| 7. Statement of Limitation | 3 | 11 | 3,67 |
| 8. Conclusion | 4 | 15 | 3,75 |
| 9. References & Bibliography | 4 | 15 | 3,75 |
| **Rata-rata total** | **42** | **150** | **3,57** (per item); 3,59 (rata-rata dari rata-rata kelompok) |

**Prioritas revisi:**
1. Tambahkan baseline EVM/SPI.
2. Lakukan *tuning* atau *early stopping* yang adil untuk semua model.
3. Uji rekalibrasi bertahap yang realistis tanpa label subproyek uji, atau lunakkan klaimnya di Abstrak dan Kesimpulan.
4. Buka kode dan data sintetis.
5. Ganti rujukan yang lemah.
6. Rapikan Tabel 4–6, Gambar 2, dan hapus halaman kosong.
