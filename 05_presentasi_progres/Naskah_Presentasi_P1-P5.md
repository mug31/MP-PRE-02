# Naskah Presentasi PRE-02 — Progres Pertemuan 1–5

Naskah per slide untuk `PRE02_Presentasi_Progres_Pertemuan1-5.pptx` (17 slide).
Target durasi **±15 menit**. Kalimat bertanda ❝ ❞ boleh diucapkan apa adanya; sisanya poin yang
perlu tersampaikan dengan bahasa sendiri.

Persiapan tanya-jawab dan istilah teknis ada di [[Guideline_Presentasi_Pertemuan1-5]].

**Aturan utama:** semua angka yang disebut di bawah ini sudah dicocokkan dengan berkas hasil di
`04_implemen_desain_eksperimen/hasil_eksperimen/`. Kalau ragu pada suatu angka, lebih baik bilang
"detailnya ada di dokumen hasil" daripada menebak.

---

## Pembagian peran (opsional)

| Bagian | Slide | Pembicara |
| :--- | :---: | :--- |
| Pembuka, P1, P2 | 1–7 | Lead author (narasi dan literatur) |
| P3, P4, P5 | 8–16 | Penanggung jawab data dan eksperimen |
| Penutup | 17 | Salah satu, disepakati sebelumnya |

Kalau dibawakan satu orang, jalankan saja urut dari slide 1 sampai 17.

---

## Slide 1 — Sampul  ·  ±40 detik

❝ Selamat pagi, Bapak/Ibu. Kami dari tim PRE-02 akan menyampaikan progres penelitian Pertemuan 1
sampai 5 sekaligus. Judulnya: Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas,
dengan studi kasus portofolio delapan modul Super ERP Farm Nation Enterprise tahun 2026. ❞

Kalimat kunci yang sebaiknya diucapkan di awal:

❝ Inti penelitian kami satu kalimat: kami tidak sekadar menebak sebuah pekerjaan akan terlambat atau
tidak, tapi menghitung seberapa besar peluangnya, dan memastikan angka peluang itu bisa dipercaya. ❞

---

## Slide 2 — Peta progres dan pemenuhan output  ·  ±1 menit

- Jelaskan bahwa lima pertemuan menjawab lima pertanyaan berurutan: apa masalahnya, apa celah
  penelitiannya, datanya apa, bagaimana mengujinya, dan apa hasilnya.
- Tunjuk kolom "Output yang diminta" — tegaskan bahwa kolom itu disalin dari dokumen Rencana Progress
  Penelitian, dan kolom sebelahnya adalah berkas yang benar-benar sudah ada di repositori.

❝ Slide ini kami pakai sebagai daftar periksa. Setiap baris adalah output yang diminta silabus, dan
di sebelahnya berkas yang sudah kami hasilkan. Semua tautannya tersedia di repositori GitHub kami. ❞

---

## Slide 3 — P1: Latar belakang dan masalah  ·  ±1 menit

- Kiri: FNE menjalankan 8 sub-proyek ERP terintegrasi secara paralel, berbagi developer yang terbatas,
  dan antar-modul saling bergantung.
- Kanan: status risiko selama ini hanya label Low, Medium, High.

❝ Masalahnya, label seperti "risiko sedang" tidak memberi tahu Project Manager kapan harus bertindak.
Tidak ada ambang yang jelas. Akibatnya tindakan korektif biasanya baru diambil setelah keterlambatan
terjadi. Yang dibutuhkan adalah angka peluang antara 0 sampai 1 yang bisa dijadikan pemicu tindakan. ❞

---

## Slide 4 — P1: Tujuan, manfaat, batasan  ·  ±1 menit

- Dua tujuan: (1) model yang memprediksi probabilitas keterlambatan pada fase monitoring dan
  evaluation; (2) early warning system berbasis ambang probabilitas.
- Manfaat dan kontribusi: peringatan dini yang terkalibrasi, dasar keputusan berbasis risiko, dan
  kerangka monitoring prediktif yang bisa diintegrasikan ke sistem manajemen proyek.
- Batasan yang penting disebut sendiri: **hanya fase monitoring dan evaluation**, data dari dokumen
  KAK, PMP, dan SRS, empat algoritma, serta unit analisis berupa task/modul — bukan keseluruhan proyek.

---

## Slide 5 — P1: Variabel penelitian  ·  ±1,5 menit

Ini slide yang paling sering ditanya, jadi sampaikan pelan.

- Kolom kiri variabel konseptual dari deskripsi penelitian, kolom tengah kolom dataset yang benar-benar
  tersedia.
- Lima variabel terpetakan langsung: progres aktual → `SPI_Value`, utilisasi → `Resource_Utilization_Rate`,
  risiko → `Risk_Score`, perubahan → `Change_Request_Count`, dependency → `Predecessor_Count`.
- **Dua variabel tidak tersedia** dan diganti proksi: sisa waktu diganti `Planned_Duration_Days`,
  backlog diganti `Planned_Effort_Hours`.

❝ Dua variabel terakhir memang tidak tercatat di dokumen PMP, jadi kami gunakan proksi dan kami
sampaikan terbuka. Kalau nanti ada data monitoring harian, dua variabel itu bisa dipakai apa adanya. ❞

- Tutup dengan variabel terikat: P(Delay), kontinu 0 sampai 1; label pelatihannya biner 0/1.

**Transisi:** ❝ Setelah masalahnya jelas, kami cek apa yang sudah dikerjakan peneliti lain dan di mana
celahnya. ❞

---

## Slide 6 — P2: Matriks literatur  ·  ±1,5 menit

- Sebut jumlahnya: 28 referensi tertelaah, 8 di antaranya jadi paper inti yang ada di tabel ini.
- Jangan bacakan seluruh baris. Cukup tiga kelompok:
  1. **Fondasi jadwal** — Batselier & Vanhoucke (2015) menempatkan SPI sebagai indikator jadwal, tapi
     hasilnya deterministik, satu angka estimasi.
  2. **Machine learning untuk delay** — Wauters & Vanhoucke (2016), Choetkiertikul dkk. (2017), dan
     Gondia dkk. (2020); luarannya durasi atau kelas diskret, dan kalibrasinya tidak diuji.
  3. **Kalibrasi dan peringatan dini** — Niculescu-Mizil & Caruana (2005) dan Guo dkk. (2017) adalah
     dasar Brier Score, Platt, Isotonic, dan ECE; Cabanillas dkk. (2014) untuk monitoring prediktif.
- Sebutkan bahwa kolom Sumber berisi tautan DOI yang bisa langsung dibuka dari slide.

---

## Slide 7 — P2: Research gap dan posisi PRE-02  ·  ±1 menit

Empat kartu, sebut singkat satu per satu:

1. Sumber daya bersama dan dependensi dimodelkan terpisah, belum simultan.
2. Prediksi berhenti di level proyek atau epic, belum level modul.
3. Perambatan keterlambatan antar-modul belum dimodelkan eksplisit.
4. Evaluasi berhenti di akurasi dan AUC; kalibrasi jarang diuji.

❝ Posisi kami ada di potongan hijau paling bawah: probabilitas terkalibrasi, di level modul ERP,
dengan fitur utilisasi dan dependensi, lalu diterjemahkan jadi zona peringatan. ❞

**Kejujuran yang perlu disiapkan:** eksperimen kami menjawab penuh gap 2 dan 4; gap 1 dan 3 baru
terjawab sebagian, lewat fitur utilisasi dan jumlah predecessor di level task. Sampaikan ini kalau
ditanya, jangan mengklaim keempatnya tuntas.

**Transisi:** ❝ Untuk mengisi celah itu kami butuh data task yang punya jadwal, beban developer, dan
dependensi. ❞

---

## Slide 8 — P3: Sumber data dan preprocessing  ·  ±1 menit

- Empat langkah: identifikasi sumber, pengumpulan, cleaning, transformasi.
- Sumber: KAK proyek FNE 2026, 8 dokumen PMP, 8 dokumen SRS.
- **Sebut sendiri sifat datanya:** empiris-simulatif — disusun dari dokumen perencanaan, bukan log
  historis banyak proyek.
- Empat kartu bawah: 26 task × 7 fitur, distribusi 16 banding 10, nol missing value, dan penyeimbangan
  cukup dengan stratifikasi tanpa SMOTE.

❝ Standardisasi kami latih hanya dari data latih di setiap lipatan, supaya tidak ada informasi data
uji yang bocor ke proses pelatihan. ❞

---

## Slide 9 — P3: Karakteristik data  ·  ±1,5 menit

- Tabel kiri: statistik deskriptif tujuh fitur, dihitung ulang langsung dari CSV.
- Kartu kanan, tiga pola yang sudah diverifikasi:
  - Seluruh 15 task dengan utilisasi ≥ 1,05 terlambat; dari 11 task sisanya hanya 1 yang terlambat.
  - Seluruh 14 task dengan SPI ≤ 0,88 terlambat.
  - 5 dari 6 task dengan predecessor ≥ 3 terlambat.

**Bagian terpenting di seluruh presentasi** — ucapkan sendiri sebelum ditanya:

❝ Ada satu hal yang perlu kami sampaikan terbuka. Pada dataset ini SPI hampir memisahkan kedua kelas
sendirian: task yang terlambat punya SPI 0,79 sampai 0,90, yang tepat waktu 0,91 sampai 0,98. Jadi
kalau nanti di hasil ada metrik yang mendekati sempurna, penyebab utamanya adalah keteraturan dokumen
perencanaan ini, bukan semata keunggulan algoritmanya. ❞

**Transisi:** ❝ Karena datanya hanya 26 task, desain eksperimennya harus hati-hati supaya hasilnya
tidak menipu. ❞

---

## Slide 10 — P4: Flow eksperimen  ·  ±1 menit

Runut enam kotak: muat data → bagi 5 lipatan berstrata → standardisasi per lipatan → latih 4 model →
kalibrasi → evaluasi dan ekspor luaran.

❝ Seluruh alur ini ada dalam satu skrip, `experiment_pipeline.py`, dengan seed 42 dikunci, sehingga
siapa pun bisa menjalankan ulang dan mendapat angka yang persis sama. Kami sudah membuktikannya. ❞

---

## Slide 11 — P4: Lima skenario dan parameter kontrol  ·  ±1 menit

- Skenario 1–4 adalah empat algoritma sesuai desain eksperimen: Logistic Regression sebagai baseline,
  Random Forest, Gradient Boosting, dan MLP dengan output sigmoid.
- Skenario 5 adalah analisis kalibrasi: output mentah dibandingkan dengan Platt Scaling dan Isotonic
  Regression.
- Variabel kontrol: partisi data, seed, urutan fitur, dan prosedur standardisasi dibuat identik.

❝ Karena semua dikontrol sama, perbedaan hasil hanya berasal dari algoritma dan teknik kalibrasinya. ❞

---

## Slide 12 — P4: Protokol validasi dan metrik  ·  ±1 menit

- Kiri, empat hal yang menjaga hasil tetap jujur: 5-fold berstrata, tanpa kebocoran data, kalibrator
  dilatih pada inner 3-fold, hold-out 80:20 sebagai pembanding, dan seed terkunci.
- Kanan, metrik dibagi dua dimensi:
  - **Kualitas probabilitas:** Brier Score, Log Loss, calibration curve, dan ECE.
  - **Kemampuan diskriminasi:** ROC-AUC, recall, specificity, F1.

❝ Pembagian dua dimensi ini penting. Akurasi hanya melihat benar atau salah di ambang 0,5, sedangkan
Brier Score menilai seberapa dekat angka peluangnya dengan kenyataan. Model bisa akurat tapi angka
peluangnya tidak bisa dipercaya. ❞

**Transisi:** ❝ Desain itu kami jalankan, dan ini hasilnya. ❞

---

## Slide 13 — P5: Hasil evaluasi 5-fold  ·  ±1,5 menit

- Jangan bacakan 12 baris. Tunjuk baris yang disorot: **MLP tanpa kalibrasi**, Brier 0,0127, ECE 0,0233,
  Log Loss 0,0341, ROC-AUC 1,000.
- Sebut pembandingnya: Logistic Regression juga ROC-AUC 1,000 dengan Brier 0,0273; Gradient Boosting
  paling rendah dengan ROC-AUC 0,9031.
- Aturan pemilihan model ditetapkan **sebelum** eksperimen: Brier Score terendah.

❝ Kalau ditanya kenapa bukan Logistic Regression yang dipilih padahal lebih sederhana: rekomendasi
kami sebenarnya ganda. MLP untuk mesin peringatan dini otomatis karena deviasi probabilitasnya paling
kecil, dan Logistic Regression sebagai pendamping ketika PM perlu menjelaskan sebab-akibatnya secara
transparan ke manajemen. Dengan N = 26, selisih sekecil itu belum tentu signifikan. ❞

---

## Slide 14 — P5: Kurva ROC dan kalibrasi  ·  ±1 menit

- Kiri, kurva ROC: makin dekat ke sudut kiri atas makin baik.
- Kanan, diagram reliabilitas: makin dekat ke garis diagonal berarti angka peluangnya makin jujur.

❝ Temuan yang menarik, kalibrasi tambahan justru tidak membantu. Pada Logistic Regression, Random
Forest, dan MLP, Brier Score-nya malah naik setelah dikalibrasi. Hanya Gradient Boosting yang membaik,
dari 0,0973 menjadi 0,0936 dengan Platt. ❞

❝ Penjelasannya: model berbasis sigmoid seperti Logistic Regression dan MLP memang sudah menghasilkan
probabilitas yang terkalibrasi secara alami. Sementara kalibrator yang dilatih hanya dari sekitar 20
sampel justru menambah noise. Ini sejalan dengan Niculescu-Mizil dan Caruana tahun 2005, bahwa
Isotonic Regression butuh data besar. Jadi ini bukan kegagalan eksperimen, melainkan temuan. ❞

---

## Slide 15 — P5: Feature importance  ·  ±1,5 menit

- Urutan bobot: `SPI_Value` 0,310 dan `Risk_Score` 0,307 di dua teratas, `Resource_Utilization_Rate`
  0,156 di posisi ketiga, dan `Predecessor_Count` hanya 0,021.

Ini titik rawan, karena judul penelitian menyoroti keterbatasan sumber daya. Jawab dua lapis:

❝ Pertama, secara jujur hasil ini belum mendukung kuat hipotesis kami: dua fitur teratas adalah fitur
jadwal dan risiko, menyumbang sekitar 62 persen. ❞

❝ Kedua, interpretasinya begini. Keterbatasan sumber daya adalah penyebab, sedangkan penurunan SPI
adalah manifestasinya. Faktanya seluruh 15 task dengan utilisasi di atas 1,05 berakhir terlambat —
varians utilisasi itu terserap ke dalam anjloknya SPI. Implikasi praktisnya, PM tidak bisa memantau
utilisasi secara terpisah, melainkan harus membaca dampak berantainya ke SPI. Pemisahan sebab dan
akibat ini yang akan kami uji pada data yang lebih besar. ❞

---

## Slide 16 — P5: Early warning system  ·  ±1,5 menit

- Zonasi operasional: Hijau di bawah 0,35, Kuning 0,35 sampai 0,65, Merah 0,65 ke atas.
- Hasil pada model rekomendasi: zona Merah berisi 16 task dan menangkap **16 dari 16** task yang
  benar-benar terlambat, tanpa alarm palsu. Zona Kuning berisi 1 task tepat waktu, yaitu ACT-018
  General Ledger dengan peluang 0,57. Tidak ada task terlambat yang lolos ke zona Hijau.
- Ambang optimal statistik dari analisis Youden J adalah 0,779, dilaporkan terpisah dari ambang
  operasional.

❝ Ambang 0,35 dan 0,65 adalah ambang tindakan manajerial yang kami tetapkan di tahap desain, bukan
hasil optimasi setelah melihat data. Ambang statistik 0,779 kami laporkan terpisah supaya jelas mana
yang keputusan desain dan mana yang temuan. ❞

- Tutup dengan tindakan tiap zona: Hijau pantau rutin, Kuning tinjau ulang alokasi developer, Merah
  eskalasi berupa crashing, fast-tracking, atau penyesuaian backlog.

**Transisi:** ❝ Hasilnya memang sangat bagus, tapi kami sadar kenapa bisa sebagus itu, dan justru itu
yang akan kami uji berikutnya. ❞

---

## Slide 17 — Keterbatasan dan rencana lanjutan  ·  ±1,5 menit

Sampaikan keterbatasan dengan nada tenang, bukan defensif:

1. N = 26, tiap lipatan uji hanya sekitar 5 task, jadi selisih kecil antar-model belum tentu signifikan.
2. ROC-AUC 1,000 terjadi karena data empiris-simulatif hampir terpisah sempurna oleh SPI — bukan
   jaminan kinerja pada proyek nyata.
3. Isotonic Regression rawan overfitting pada ukuran sampel ini.
4. Pemilihan model dan ambang dilakukan pada prediksi out-of-fold yang sama dengan yang dilaporkan,
   sehingga estimasinya sedikit optimistis.

Lalu rencana: Pertemuan 6 analisis mendalam dan uji signifikansi, Pertemuan 7 pembahasan dan
konfrontasi dengan literatur, Pertemuan 8 finalisasi paper IMRAD, serta validasi pada data proyek riil
berukuran di atas 100 sebagai agenda lanjutan.

❝ Sekian penyampaian progres Pertemuan 1 sampai 5 dari kami. Terima kasih, dan kami siap menerima
masukan. ❞

---

## Catatan teknis sebelum maju

- Buka file `.pptx` dengan PowerPoint atau LibreOffice Impress; tautan pada slide 6 baru aktif saat
  mode presentasi atau saat diklik dengan Ctrl.
- Kalau ada angka yang ingin dicek mendadak, buka `hasil_eksperimen/00_RINGKASAN_TEMUAN_EKSPERIMEN.md`
  — isinya digenerate otomatis dari hasil eksperimen.
- Jangan menjanjikan XGBoost atau variabel *linked module delay deviation*; keduanya tidak ada dalam
  eksperimen ini.
- Kalau ditanya sesuatu yang belum dikerjakan, jawab apa adanya dan masukkan ke rencana Pertemuan 6–8.
  Mengakui batas lebih aman daripada mengarang jawaban.

---

tags #paper #mp #academic #research #presentasi
