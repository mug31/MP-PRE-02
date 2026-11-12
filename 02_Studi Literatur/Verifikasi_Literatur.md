# Verifikasi Literatur PRE-02

> Dicek 12 November 2026 sebelum Pertemuan 7 (pembahasan). Sumber pengecekan: Crossref API, DataCite API, doi.org,
> arXiv API, Zenodo API, Semantic Scholar API, halaman penerbit, dan teks lengkap PDF bila terbuka. Berkas
> `Tinjauan Pustaka.md`, `Pertemuan2_Matriks_Literatur.md`, `Research gap.md`, dan draf Bab II awalnya **tidak diubah**;
> koreksi di bawah perlu diterapkan oleh tim.
>
> **Pembaruan:** koreksi sudah diterapkan ke `Tinjauan Pustaka.md`, `Pertemuan2_Matriks_Literatur.md`,
> `Sintesis Naratif.md`, `Research gap.md`, dan `Pertemuan2_Draft_Tinjauan_Pustaka.md` atas persetujuan tim.
> No. 19 dan No. 20 dihapus dari matriks; Bimantara (No. 12) tetap dipertahankan dengan catatan.

## Arti status

| Status | Arti |
| :---: | :--- |
| ✅ | Metadata benar dan klaim yang dicek sesuai sumber |
| 🟡 | Paper ada, tetapi ada metadata yang perlu dikoreksi atau klaim yang belum/tidak bisa dicek |
| ❌ | Paper tidak ditemukan, atau klaim di matriks bertentangan dengan isi paper |

Tingkat pengecekan klaim: **teks lengkap** (PDF dibaca), **abstrak** (hanya abstrak), **–** (tidak ada akses).

---

## Ringkasan

| Kelompok | Jumlah | ✅ | 🟡 | ❌ |
| :--- | ---: | ---: | ---: | ---: |
| Matriks No. 1–28 | 28 | 10 | 16 | 2 |
| Rujukan metode Bab III | 13 | 11 | 2 | 0 |

**Yang paling penting diperbaiki sebelum dikutip di Bab II/V**

| No | Rujukan | Masalah | Tindakan |
| :---: | :--- | :--- | :--- |
| 26 | Niculescu-Mizil & Caruana (2005) | Matriks menulis RF menghasilkan probabilitas terdistorsi. Paper justru menyatakan **neural net, bagged trees, random forest, dan logistic regression terkalibrasi baik**; yang terdistorsi adalah **boosted trees/stumps dan SVM** | Koreksi kolom temuan kunci |
| 22 | Wauters & Vanhoucke (2016) | Matriks menulis "khususnya SVR dan ANN". Lima metode di paper: decision tree, bagging, random forest, boosting, SVM (tanpa ANN). Temuan: AI mengungguli EVM/ES **hanya jika data latih dan uji mirip** | Koreksi temuan kunci |
| 21 | Batselier & Vanhoucke (2015) | Matriks menulis "Earned Schedule lebih stabil di akhir proyek". Abstrak mengevaluasi tiga teknik: perluasan EVM dengan *rework*, perluasan dengan *activity sensitivity*, dan EDM(t); EDM(t) setara metode EVM terbaik | Koreksi temuan kunci |
| 23 | Choetkiertikul et al. (2017) | Matriks menulis metode "Deep Learning (RNN/LSTM)". Paper memakai **faktor risiko + classifier** (8 proyek open source), memprediksi tingkat **dan peluang** keterlambatan; rata-rata precision 79%, recall 61%, F 68%, AUC 83% | Koreksi metode & output (bukan murni biner) |
| 28 | Cabanillas et al. (2014) | Matriks menulis metrik "Alert Timeliness, False Alarm Rate, Brier Score". Paper (BPM 2014, makalah pendek) memakai **SVM** untuk mengklasifikasi eksekusi tugas aman/anomali pada kasus *smart logistics*; tidak ada Brier Score maupun false alarm rate | Hapus metrik itu; jangan dikutip sebagai rujukan Brier |
| 25 | Browning & Yassine (2010) | Klaim "bottleneck sumber daya bersama memicu efek domino" tidak ada di abstrak. Isi paper: 20 *priority rule* pada 12.320 problem RCMPSP; aturan populer bisa berkinerja buruk; aturan terbaik berbeda untuk tujuan proyek vs portofolio | Ubah temuan kunci sesuai abstrak, atau cek teks lengkap |
| 20 | Editorial IJACSEAI (2026) | Tidak ditemukan sama sekali (judul, jurnal, maupun ISSN 3143-438X) | **Buang** dari matriks |
| 12 | Bimantara et al. (2025) | Daftar pustaka berisi rujukan yang tampak fiktif (Breiman 2023, DOI XGBoost palsu); DOI artikel tidak terdaftar; angka di matriks tidak cocok dengan abstrak | **Buang** dari matriks |
| 16 | Saurav & Shafi (2022) | Bukan model ML: studi **kuesioner** (292 responden) dengan regresi atas persepsi responden | Koreksi kolom metode; turunkan relevansinya |

---

## A. Matriks literatur No. 1–28

| No | Rujukan | Status | Metadata terverifikasi / koreksi | Klaim yang dicek | Tingkat | Catatan kredibilitas |
| :---: | :--- | :---: | :--- | :--- | :---: | :--- |
| 1 | Haekal et al. (2026) | 🟡 | Judul lengkap: *A Random-Forest-Based Framework for Predicting Schedule Achievement in Cloud Enterprise Resource Planning Projects Using the Critical Path Method and the Programme Evaluation and Review Technique*. Penulis: J. Haekal, R. Mu'min, S.A. Lesmana, N.E. Triana, Y.D. Suwandari, D. Rukmayadi, I.G. Prihanto. *South African Journal of Industrial Engineering* 37(2), 74–94, terbit 31 Agustus 2026. DOI tertulis 10.7166/37-2-3151 tetapi **belum bisa dibuka di doi.org** | ✅ RF vs NN; AUC 0,997; CA/F1/precision/recall 0,980; MCC 0,960; fitur 4M dari CPM/PERT. **Dataset hanya 100 data**; tidak ada Brier/kalibrasi | Teks lengkap | Jurnal ilmiah SAJIE (teknik industri). Isi kolom DOI; catat N = 100 |
| 2 | Mandapatti (2026) | 🟡 | Jaswanth Kumar Mandapatti, *Journal of Scalable Data Engineering and Intelligent Computing* 3(2), 65–69 (edisi Mei–Agu 2026, diterima Des 2025). DOI di PDF 10.17051/JSDEIC/03.02.09 **tidak terdaftar** (404) | ✅ angka hanya dari Gambar 1: GB akurasi 0,93, precision 0,92, recall 0,91, F1 ≈ 0,915. Ukuran dan sumber data **tidak dilaporkan** | Teks lengkap | Jurnal baru, DOI tidak terdaftar; lemah sebagai rujukan utama |
| 3 | Kula et al. (2023) | ✅ | Kula, Greuter, van Deursen, Gousios. ESEC/FSE 2023, hlm. 1012–1023. DOI 10.1145/3611643.3616328 | ✅ 4.040 epic, 270 tim ING; *out-degree* dependensi sebagai faktor risiko; propagasi keterlambatan antar-delivery disebut sebagai arah lanjutan | Teks lengkap | Konferensi bereputasi (ACM) |
| 4 | Sivakumar & Sobika R (2026) | 🟡 | Judul lengkap: *AI-Driven Predictive Analytics for Improving Project Planning: A Task-Level Analysis of Interdependencies and Decision Making*. IJSREM 10(7), Juli 2026. DOI 10.55041/IJSREM65902 (bisa dibuka) | ✅ RF Regression; R² 0,90; MSE ≈ 1,00; r dependensi 0,61, risiko 0,31, kompleksitas 0,27, durasi 0,05. **Hanya 150 observasi tugas** | Teks lengkap | IJSREM: jurnal multidisiplin berbiaya publikasi, kualitas *peer review* diragukan. Hanya sebagai pendukung |
| 5 | Mirjalili et al. (2025) | 🟡 | Penulis kedua **Behrad Braghi** (bukan "Barghi"). arXiv 2511.15003 | ✅ MAE 2,71, RMSE 3,97, R² 0,91–0,92 (TGN), ECE 3,5–3,8% (< 4%) | Teks lengkap | Preprint, belum *peer review* |
| 6 | Impivaara (2025) | ✅ | Vendela Impivaara (2025), tesis magister (*Diplomityö*), LUT University, School of Engineering Science, Industrial Engineering and Management. URN https://urn.fi/URN:NBN:fi-fe20251215119518 | ✅ Data pesanan 3 tahun di perusahaan produksi Finlandia; Microsoft Fabric AutoML; LightGBM terbaik: ROC-AUC 0,943, precision 0,747, recall 0,637, F1 0,687 | Abstrak (dibuka lewat browser) | Tesis magister |
| 7 | Kannan et al. (2022) | ✅ | Kannan, Abdul Halim, Ramakrishnan, Ismail, Wijaya. *Journal of Big Data* 9, art. 94. DOI 10.1186/s40537-022-00644-w | ✅ MLP & LR terbaik, F-measure 0,973; data produksi 6 bulan dua mesin | Abstrak | Jurnal Springer bereputasi |
| 8 | Fitzsimmons et al. (2022) | ✅ | Fitzsimmons, Lu, Hong, Brilakis. *ITcon* 27, 70–93. DOI 10.36680/j.itcon.2022.004 | ✅ 293.263 tugas dari 302 proyek; GMM-EBN + SVM + simulasi; 54,4% lebih akurat vs simulasi standar. "SE 16,7 minggu" belum dicek | Abstrak | Jurnal *open access* bereputasi |
| 9 | Kumar & Shrivas (2025) | 🟡 | Sebenarnya terbit di ***RICERCA, International Journal of Multidisciplinary Research and Innovation* 5(12), 8–16** (Des 2025); Zenodo 10.5281/zenodo.17898268 hanya salinan | ✅ RF, ANN, GB, LSTM dibandingkan dengan CPM/PERT/EVM; EWS. Metrik spesifik belum dicek | Abstrak | Jurnal multidisiplin kecil; pendukung saja |
| 10 | Balaji & Poyyamozhi (2026) | 🟡 | S. Balaji, N. Poyyamozhi. IJSRET 12(2), Mar–Apr 2026. DOI Zenodo **10.5281/zenodo.19483001** | ✅ TAM-Lite; akurasi 97,6%, precision 97,2%, recall 97,8%, F1 97,5%, **Brier 0,024**. Dataset: "Project Management Risk Dataset" (sumber tidak dijelaskan) | Teks lengkap | IJSRET: jurnal berbiaya publikasi, *peer review* diragukan. Jika dipakai sebagai satu-satunya rujukan "Brier di proyek software", sebutkan keterbatasannya |
| 11 | Grzelak et al. (2026) | ✅ | Judul lengkap: *Predictive Maintenance in Logistics Fleets: A Comparative Evaluation of Random Forest, XGBoost and Logistic Regression*. Grzelak, Voicu, Stoica, Vilau. *Logistics* 10(8), 183 | ✅ RF AUC 0,855 ≈ XGBoost 0,853 > LR 0,822; uji signifikansi CV. Topiknya kebutuhan perawatan, bukan keterlambatan | Abstrak | MDPI. Relevansi metodologis saja |
| 12 | Bimantara et al. (2025) | ❌ | Henri Caesar Bimantara, Abdul Rokim, Elkin Rilvani (Universitas Pelita Bangsa). *Jurnal Media Akademik* 3(7), terbit 27 Juli 2025. DOI tertulis 10.62281/v3i7.2629 **tidak terdaftar** (404) | ⚠️ Abstrak: RF, GB, SVR; **500 proyek** prefabrikasi 2020–2024 (bukan 100); GB terbaik dengan RMSE 2,3 hari (produksi) dan 1,8 hari (pengiriman); prediktor: kompleksitas, ketersediaan material, antrean. Angka di matriks (RMSE 0,513; R² 0,9687; MAPE 3,83%) tidak ada di abstrak | Abstrak (dibuka lewat browser) | **Daftar pustakanya memuat rujukan yang tampak fiktif**, misalnya "Breiman (2023), JMLR 45(2)" (Breiman wafat 2005) dan "Chen & Guestrin (2023), DOI 10.1145/acm.2023.xgboost"; kedua DOI tidak terdaftar. **Sebaiknya dibuang** |
| 13 | Restrepo Ramirez & Rua-Machado (2025) | ✅ | *Revista EIA* 22(44). DOI 10.24050/reia.v22i44.1861 | ✅ 6 model regresi termasuk RFR; deviasi 2,09% (progres) dan 11,05% (keterlambatan); 102 dan 81 data | Abstrak | Jurnal ilmiah |
| 14 | Ingole (2026) | ✅ | *International Journal of Creative and Open Research in Engineering and Management* 2(7), 1–9. DOI 10.55041/ijcope.v2i7.142 | ✅ SLR PRISMA 30 studi; RF/XGBoost akurasi > 85% | Abstrak | Jurnal kecil; SLR sebagai pendukung |
| 15 | Purnomo et al. (2025) | 🟡 | Judul lengkap: *Predictive Modeling of Delivery Delays in Transportation Using Machine Learning: A Comparative Study of Service Types*. Agus Purnomo, Nava Gia Ginasta, Syafrianita, Syafrial Fachri Pane. DIJEMSS 7(2), 1765–1779. DOI artikel **10.38035/dijemss.v7i2.5736** (di matriks hanya DOI edisi) | ✅ RF & XGBoost akurasi ≈ 65%, AUC 0,73; 10.999 data PT Pos Indonesia | Halaman artikel | Jurnal manajemen pendidikan & sosial; domain jauh |
| 16 | Saurav & Shafi (2022) | 🟡 | *Review of Applied Science and Technology*, hlm. 464–501. DOI 10.63125/dn8nkm85 | ⚠️ **Studi kuesioner** 292 responden; regresi atas persepsi kapabilitas ML, bukan model prediksi | Abstrak | Koreksi kolom metode |
| 17 | Khoshkonesh et al. (2026) | 🟡 | Judul benar: ***Bayesian-Monte Carlo Schedule Updating for Construction Digital Twins: A Probabilistic Framework for Dynamic Project Forecasting***. arXiv 2605.17608 | ✅ Bayesian updating + simulasi pada jaringan PSPLIB | Abstrak | Preprint |
| 18 | Soleymani et al. (2022) | ✅ | Judul lengkap: *Autonomous Resource Management in Construction Companies Using Deep Reinforcement Learning Based on IoT*. arXiv 2208.08087 | – | – | Preprint |
| 19 | [Penulis tidak tercantum] (2025) | 🟡 | Ditemukan di repositori Undip (eprints2.undip.ac.id/45987, berkas Sipil42.pdf). **Penulis dan tahun belum terbaca**: server repositori sedang galat basis data (12 Nov 2026) | ✅ LR, RFR, SVR; R = 0,957; MAE 136,569; RMSE 182,051; input jumlah lantai, luas, lokasi, fungsi bangunan | Abstrak | Skripsi; isi penulis/tahun sebelum dipakai |
| 20 | Editorial IJACSEAI (2026) | ❌ | **Tidak ditemukan**: judul, jurnal, dan ISSN 3143-438X tidak ada di indeks mana pun | – | – | **Buang** |
| 21 | Batselier & Vanhoucke (2015) | 🟡 | *Int. J. Project Management* 33(7), 1588–1596. DOI benar | ⚠️ Lihat tabel prioritas: tiga teknik (rework, activity sensitivity, EDM(t)) | Abstrak | Jurnal bereputasi |
| 22 | Wauters & Vanhoucke (2016) | 🟡 | *Expert Systems with Applications* 46, 249–261. DOI benar | ⚠️ Lihat tabel prioritas: DT, bagging, RF, boosting, SVM; unggul jika data latih–uji mirip | Abstrak | Jurnal bereputasi |
| 23 | Choetkiertikul et al. (2017) | 🟡 | *Empirical Software Engineering* 22(3), 1223–1263. DOI benar | ⚠️ Lihat tabel prioritas | Abstrak | Jurnal bereputasi |
| 24 | Gondia et al. (2020) | ✅ | *J. Construction Engineering and Management* 146(1), 04019085. DOI benar | ✅ Decision tree & naive Bayes untuk memprediksi tingkat keterlambatan | Abstrak | Jurnal bereputasi (ASCE) |
| 25 | Browning & Yassine (2010) | 🟡 | *Int. J. Production Economics* 126(2), 212–228. DOI benar | ⚠️ Lihat tabel prioritas | Abstrak | Jurnal bereputasi |
| 26 | Niculescu-Mizil & Caruana (2005) | 🟡 | ICML 2005, hlm. 625–632. DOI benar | ⚠️ Lihat tabel prioritas. Juga: Platt pada model yang sudah terkalibrasi baik justru mendorong probabilitas menjauhi 0 dan 1; isotonic lebih mudah *overfit* bila data kalibrasi sedikit | Teks lengkap | Rujukan fondasi |
| 27 | Guo et al. (2017) | ✅ | Guo, Pleiss, Sun, Weinberger. ICML 2017, PMLR 70, 1321–1330; arXiv 1706.04599 | ✅ Neural network modern cenderung *overconfident*; ECE | Abstrak | Rujukan fondasi |
| 28 | Cabanillas et al. (2014) | 🟡 | BPM 2014 (LNCS 8659), 424–432, makalah pendek. DOI 10.1007/978-3-319-10172-9_31 benar | ❌ Lihat tabel prioritas | Teks lengkap (preprint Univ. Sevilla) | Makalah pendek konferensi |

## B. Rujukan metode di Bab III

| Rujukan | Status | Metadata terverifikasi | Catatan |
| :--- | :---: | :--- | :--- |
| Brier (1950) | ✅ | *Monthly Weather Review* 78(1), 1–3. DOI 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 | |
| Platt (1999) | 🟡 | *Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods*, dalam Smola dkk. (ed.), *Advances in Large Margin Classifiers*, MIT Press | Sebagian sumber mencatat tahun 2000 dan halaman 61–74 belum terkonfirmasi; cek buku |
| Zadrozny & Elkan (2002) | ✅ | Proc. 8th ACM SIGKDD, 694–699. DOI 10.1145/775047.775151 | |
| Youden (1950) | ✅ | *Cancer* 3(1), 32–35. DOI 10.1002/1097-0142(1950)3:1<32::AID-CNCR2820030106>3.0.CO;2-3 | |
| Pedregosa et al. (2011) | ✅ | *JMLR* 12, 2825–2830 | |
| Friedman (2001) | ✅ | *Annals of Statistics* 29(5), 1189–1232. DOI 10.1214/aos/1013203451 | |
| Niculescu-Mizil & Caruana (2005) | ✅ | Lihat No. 26 | Metadata benar |
| Guo et al. (2017) | ✅ | Lihat No. 27 | |
| Efron & Tibshirani (1993) | ✅ | *An Introduction to the Bootstrap*, Chapman & Hall/CRC. DOI 10.1201/9780429246593 | |
| Holm (1979) | 🟡 | *Scandinavian Journal of Statistics* 6(2), 65–70; JSTOR stable 4615733 | Tidak punya DOI; pakai tautan JSTOR |
| Wilcoxon (1945) | ✅ | *Biometrics Bulletin* 1(6), 80–83. DOI 10.2307/3001968 | |
| Van Calster et al. (2016) | ✅ | *J. Clinical Epidemiology* 74, 167–176. DOI 10.1016/j.jclinepi.2015.12.005 | |
| Murphy (1973) | ✅ | *J. Applied Meteorology* 12(4), 595–600. DOI 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2 | |

---

## C. Dampak ke pembahasan (Pertemuan 7)

| Temuan verifikasi | Pemakaian di Bab V |
| :--- | :--- |
| Niculescu-Mizil & Caruana: LR, RF, dan NN umumnya terkalibrasi baik; Platt pada model yang sudah terkalibrasi bisa memperburuk ekor distribusi; isotonic mudah *overfit* | Mendukung hasil H5 (kalibrasi tidak membantu LR/RF/GB). Hasil LR (*slope* 0,586) dan NN (*overconfident*) berbeda dari temuan umum mereka → dibahas sebagai efek pergeseran antarsubproyek |
| Wauters & Vanhoucke: AI unggul hanya jika data latih dan uji mirip | Sejalan dengan temuan bahwa keunggulan model tidak konsisten antarsubproyek dan kasus P-FNE-08 |
| Haekal (AUC 0,997), Balaji (Brier 0,024), Mandapatti (akurasi 0,93) memakai data kecil/tidak jelas dan validasi acak | Dibandingkan secara hati-hati: angka kita lebih rendah, tetapi divalidasi per subproyek |
| Sivakumar (dependensi r = 0,61) dari 150 tugas di jurnal kurang kuat | Perbedaan dengan temuan kita (dependency lemah) dibahas, dengan catatan kekuatan buktinya |
| Kula: dependensi (*out-degree*) faktor risiko; propagasi keterlambatan masih arah lanjutan | Mendukung posisi gap *delay propagation* |
| Guo et al.: NN *overconfident* | Mendukung penjelasan H4 |

## D. Rujukan tambahan untuk paper (P8)

| Rujukan | Status | Metadata terverifikasi | Catatan |
| :--- | :---: | :--- | :--- |
| Ananta, Pamungkas & Ainul Yaqin (2026) | ✅ | *Analisis Domain Kinerja Stakeholder pada Proyek ERP Menggunakan Social Network Analysis*. Jurnal Pustaka Data 6(5), 833–847, terbit 31 Okt 2026. DOI 10.55382/jurnalpustakadata.v6i5.2152 (tertulis di situs jurnal, belum aktif di doi.org per 12 Nov 2026) | Dibuka langsung di situs jurnal (SINTA 5). Dosen pembimbing sebagai penulis ketiga; terbit di jurnal tujuan |
| Waridi, Fikri & Yaqin, *Memprediksi Keberhasilan Proyek ERP Menggunakan Indikator Kinerja Multi-Domain dan Machine Learning* | ❌ belum dipakai | Hanya ditemukan sebagai naskah template JACIS di ResearchGate; volume, nomor, dan tahun masih kosong | Belum terbit, jangan dikutip sebagai publikasi |

