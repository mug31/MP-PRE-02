# Matriks Literatur Ilmiah: PRE-02
## Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas

Dokumen ini memuat sintesis terstruktur dari **8 referensi ilmiah bereputasi internasional** (IEEE/ACM, Elsevier, Springer, ASCE, ICML) yang menjadi landasan teoritis, komparasi metodologis, serta penegasan *Research Gap* bagi penelitian **PRE-02**.

---

### Tabel Matriks Sintesis Literatur

| No | Penulis & Tahun | Judul Paper & Publikasi | Fokus & Ranah | Metode / Algoritma | Fitur / Variabel Input | Metrik Evaluasi Utama | Temuan Kunci | Keterbatasan / Research Gap terhadap PRE-02 |
|:---:|:---|:---|:---|:---|:---|:---|:---|:---|
| **1** | **Batselier & Vanhoucke (2015)** | *Evaluation of deterministic state-of-the-art forecasting approaches for project duration based on earned value management*<br>*(International Journal of Project Management / Elsevier)* | Manajemen Proyek Tradisional (EVM / ES) | Earned Value Management (EVM), Earned Schedule (ES), Earned Duration (ED) | Planned Value (PV), Earned Value (EV), Actual Cost (AC), Actual Time (AT), SPI, SPI(t) | Mean Absolute Percentage Error (MAPE), Mean Percentage Error (MPE) | Pendekatan Earned Schedule lebih stabil memprediksi durasi akhir proyek dibanding metrik EVM klasik pada akhir siklus proyek. | **Hanya deterministik (titik estimasi tunggal), mengabaikan dinamika non-linearitas, interdependensi antar-tugas, serta tidak menghasilkan probabilitas risiko.** |
| **2** | **Wauters & Vanhoucke (2016)** | *A comparative study of Artificial Intelligence methods for project duration forecasting*<br>*(Expert Systems with Applications, 46, 249–261 / Elsevier)* | Machine Learning vs EVM | Decision Tree, Bagging, Random Forest, Boosting, Support Vector Machine; pembanding: metode forecasting EVM | Metrik EVM berkala, durasi historis, topologi jaringan kerja (network topology) | ⚠️ Metrik akurasi forecasting (cek di paper: MAE/MAPE) | Model AI (khususnya SVR dan ANN) mengungguli formula matematis EVM tradisional dalam peramalan durasi akhir proyek. | **Fokus pada regresi durasi waktu (angka hari/minggu), bukan estimasi probabilitas keterlambatan untuk sistem peringatan dini (*early warning*).** |
| **3** | **Choetkiertikul et al. (2017)** | *Predicting the delay of issues with due dates in software projects*<br>*(Empirical Software Engineering / Springer)* | Rekayasa Perangkat Lunak & Proyek Agile | Random Forest dan classifier pembanding (prediksi tingkat keterlambatan issue); ⚠️ aspek *networked classification* berbasis link antar-issue ada di karya terpisah: Choetkiertikul et al. (2015), ASE | Karakteristik Issue/Task, dependency link network, estimasi story points, developer workload | Precision, Recall, F-measure, Area Under ROC Curve (AUC) | Keterkaitan dependensi antar-isu perangkat lunak (*task link*) secara signifikan meningkatkan akurasi deteksi keterlambatan. | **Keluaran model berupa klasifikasi biner diskret (Delay vs No Delay); tidak melakukan kalibrasi probabilitas kontinu dan metrik Brier Score.** |
| **4** | **Gondia et al. (2020)** | *Machine Learning Algorithms for Construction Projects Delay Risk Prediction*<br>*(Journal of Construction Engineering and Management, 146(1), 04019085 / ASCE)* | Analisis Risiko Proyek | Naive Bayes (NB), Decision Tree (C4.5 / CART) | Skor risiko operasional, kualifikasi kontraktor, frekuensi perubahan desain (*change requests*) | Overall Accuracy, Precision, Recall, Misclassification Rate | Algoritma *decision tree* mampu memetakan faktor dominan pemicu keterlambatan secara transparan dan mudah diinterpretasi. | **Menghasilkan kelas risiko kualitatif diskrit (Low, Medium, High) yang kaku dan tidak memodelkan perebutan sumber daya bersama (*shared resource constraints*).** |
| **5** | **Browning & Yassine (2010)** | *Resource-constrained multi-project scheduling: Priority rule performance revisited*<br>*(International Journal of Production Economics, 126(2), 212–228 / Elsevier)* | Multi-Project Scheduling (RCMPSP) | Analisis 20 *priority rule* heuristik pada 12.320 problem uji (karakteristik jaringan, distribusi & kontensi sumber daya) | Utilisasi sumber daya (*Resource Utilization Rate*), batasan kapasitas, dependensi lintas proyek | Project lateness & portfolio lateness (rata-rata keterlambatan per proyek & waktu penyelesaian portofolio) | Bottleneck pada sumber daya bersama (*shared critical resource*) memicu efek domino (*cascading delay*) di seluruh portofolio proyek. | **Pendekatan berbasis simulasi murni dan aturan heuristik statis, belum memanfaatkan model *predictive learning* berbasis machine learning.** |
| **6** | **Niculescu-Mizil & Caruana (2005)** | *Predicting good probabilities with supervised learning*<br>*(Proceedings of the 22nd International Conference on Machine Learning / ICML)* | Fondasi Kalibrasi Probabilitas | Logistic Regression, Random Forest, SVM, Naive Bayes, Platt Scaling, Isotonic Regression | Dataset benchmark empiris lintas domain | Brier Score, Log Loss, Calibration Curves (Reliability Diagrams) | Model ensemble pohon (Random Forest) dan SVM menghasilkan ranking baik namun probabilitas terdistorsi (*uncalibrated*); Logistic Regression menghasilkan probabilitas paling terkalibrasi alami. | **Studi berfokus pada fondasi machine learning teoretis murni; belum diterapkan secara spesifik pada kasus monitoring dan evaluasi portofolio proyek TI.** |
| **7** | **Guo et al. (2017)** | *On Calibration of Modern Neural Networks*<br>*(Proceedings of the 34th International Conference on Machine Learning / ICML)* | Evaluasi Kalibrasi Deep Learning | Modern Deep Neural Networks, Temperature Scaling, Vector Scaling | Fitur representasi non-linear, logits layer | Expected Calibration Error (ECE), Maximum Calibration Error (MCE), Negative Log-Likelihood | Neural Network modern cenderung terlalu percaya diri (*overconfident*) meskipun akurasinya tinggi, sehingga membutuhkan teknik kalibrasi probabilitas khusus. | **Riset diuji pada domain computer vision dan NLP standar; belum diintegrasikan ke sistem pemantauan proyek dengan dataset berskala terbatas.** |
| **8** | **Cabanillas et al. (2014)** | *Predictive Task Monitoring for Business Processes*<br>*(Business Process Management — BPM 2014, LNCS 8659, 424–432 / Springer)* | Monitoring Prediktif & Early Warning | ⚠️ Isi kolom metode, fitur, dan metrik baris ini belum terverifikasi terhadap paper asli; cek ulang sebelum dikutip | Sisa waktu (*time remaining*), backlog task tersisa, alokasi sumber daya proses | Alert Timeliness, False Alarm Rate, Brier Score | Kerangka monitoring prediktif yang menghitung probabilitas pelanggaran batas waktu mampu memicu tindakan mitigasi dini sebelum *deadline* terlewati. | **Model mengandalkan log proses sekuensial yang ketat; kurang adaptif terhadap lingkungan multiproyek dinamis dengan ketergantungan matriks seperti ERP.** |

---

### Pemetaan Research Gap (Celah Penelitian) PRE-02

Berdasarkan sintesis matriks literatur di atas, posisi penelitian **PRE-02** diformulasikan untuk menjawab 3 keterbatasan utama:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            KONDISI RISET TERDAHULU                          │
│                                                                             │
│  [EVM Tradisional]         [ML Standar]                 [Simulasi RCMPSP]   │
│  • Hanya angka estimasi    • Hanya label biner          • Aturan heuristik  │
│    deterministik             (Delay / No-Delay)           statis            │
│  • Mengabaikan dinamika    • Probabilitas tidak diuji   • Tidak ada model   │
│    non-linear resource       apakah terkalibrasi          machine learning  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼ IDENTIFIKASI GAP
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Output Kategorial Kaku ──> PM tidak punya derajat keyakinan numerik      │
│ 2. Uncalibrated Models    ──> Probabilitas overconfident memicu alarm palsu │
│ 3. Isolated Project Scope ──> Mengabaikan ketergantungan sumber daya bersama│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼ NOVELTY & POSISI
┌─────────────────────────────────────────────────────────────────────────────┐
│                       POSISI PENELITIAN PRE-02                              │
│                                                                             │
│  ✓ Membangun model klasifikasi probabilistik kuantitatif kontinu (0 s.d 1) │
│  ✓ Mengintegrasikan metrik jadwal (SPI), utilisasi sumber daya, risiko,     │
│    dan dependensi lintas sub-proyek (Super ERP FNE)                         │
│  ✓ Menguji dan membandingkan kalibrasi model via Brier Score & ECE          │
│  ✓ Menentukan threshold optimal untuk Early Warning System terkalibrasi     │
└─────────────────────────────────────────────────────────────────────────────┘
```
