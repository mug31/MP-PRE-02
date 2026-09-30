# Penjelasan Variabel Dataset PRE-02

Dokumen ini menjawab pertanyaan: **setiap variabel dalam dataset diperoleh dari mana, dengan rumus
apa, dan bagaimana perhitungannya.** Berkas data yang dijelaskan: `dataset_pre02_fne_v2.csv`
(26 aktivitas × 7 fitur + 1 label). Berkas ini menjadi **satu-satunya rujukan resmi** dan dibaca
langsung oleh pipeline eksperimen; versi sebelumnya disimpan sebagai arsip pada
`dataset_pre02_fne_v1_arsip.csv` dengan isi yang identik.

## Ringkasan asal data

Dataset disusun dari tiga lapis sumber:

1. **Dokumen perencanaan proyek** — KAK Proyek FNE 2026, 8 dokumen PMP, 8 dokumen SRS, dan dokumen
   Pemetaan Proyek Pengembangan ERP FNE. Seluruhnya tersimpan di folder `MP-datasetRaw/`.
2. **Rumus standar manajemen proyek** — Earned Schedule (SPI), utilisasi sumber daya, dan
   Probability–Impact Matrix, yang definisinya juga tercantum di PMP.
3. **Estimasi ahli tim peneliti** — untuk nilai yang belum tersedia karena proyek FNE 2026 masih pada
   tahap perencanaan dan belum memasuki eksekusi.

Pembagian ini penting: dokumen PMP berisi *rencana*, sedangkan variabel monitoring seperti SPI dan
utilisasi baru terisi ketika proyek berjalan. Bukti bahwa dokumen ini pra-eksekusi terlihat pada tabel
*Velocity Planning* PMP P-FNE-01, di mana kolom *Planned Velocity* terisi sementara kolom
*Actual Velocity* masih kosong.

---

## Tabel 1 — Kamus, Rumus, dan Penurunan Variabel

| Variabel | Definisi (satuan) | Rumus / cara memperoleh | Sumber | Status |
| :--- | :--- | :--- | :--- | :--- |
| `Task_ID` | Kode aktivitas (ACT-001…026) | Penomoran urut | — | Metadata |
| `Sub_Project` | Kode sub-proyek (P-FNE-01…08) | Diambil langsung | Dokumen Pemetaan Proyek | Terdokumentasi |
| `Task_Name` | Nama modul/aktivitas inti | Diambil dari struktur WBS | WBS pada Bab 3 PMP tiap sub-proyek | Terdokumentasi |
| `Planned_Duration_Days` | Durasi rencana (hari kerja) | $D = n_{\text{sprint}} \times 2\ \text{minggu} \times 5\ \text{hari}$ | Tabel *Effort Estimation by Sprint* & *Critical Path* pada Bab 4 PMP | Terdokumentasi (P-FNE-01, P-FNE-03); turunan untuk sub-proyek lain |
| `Planned_Effort_Hours` | Beban kerja rencana (orang-jam) | $E = D \times 8\ \text{jam} \times FTE_{\text{ekuivalen}}$ | Basis 8 jam/hari kerja; kapasitas 160 jam/bulan pada Bab 7 PMP | Turunan |
| `Predecessor_Count` | Jumlah modul pendahulu | Menghitung dependensi *finish-to-start* modul | Kolom Ketergantungan pada Dokumen Pemetaan + *Activity Sequencing* Bab 4 PMP | Terdokumentasi di level sub-proyek; estimasi ahli untuk dependensi internal |
| `Resource_Utilization_Rate` | Rasio beban terhadap kapasitas developer | $U = \dfrac{\text{jam kerja dialokasikan}}{\text{kapasitas normal }(160\ \text{jam/bulan})}$ | Rumus & kapasitas: tabel *Resource Utilization Plan* Bab 7 PMP P-FNE-08 | Rumus terdokumentasi; nilai per aktivitas estimasi ahli |
| `Risk_Score` | Indeks risiko ternormalisasi (0–1) | $R = P \times I$, dengan $P$ dan $I$ dikonversi ke skala 0–1 (skala register 1–5 dibagi 5) | Risk Register (kolom Prob, Impact, Score) pada Bab 9 / Lampiran E PMP | Rumus terdokumentasi; nilai per aktivitas estimasi ahli |
| `SPI_Value` | Schedule Performance Index | $SPI = \dfrac{EV}{PV}$ | Definisi & ambang $\ge 0.8$ pada Bab 4 dan Bab 7 PMP | Rumus terdokumentasi; nilai estimasi ahli (belum ada pengukuran aktual) |
| `Change_Request_Count` | Jumlah change request disetujui | Menghitung CR yang lolos *Change Control Board* | Proses & formulir CR pada Bab 3 dan Bab 4 PMP | Proses terdokumentasi; jumlah per aktivitas estimasi ahli |
| `Status_Delay` | Label target (0 = tepat waktu, 1 = terlambat) | Ditetapkan $1$ bila $SPI \le 0.90$ pada titik pantau | Konsisten dengan ambang kinerja jadwal PMP | Turunan dari `SPI_Value` |

**Arti kategori status:**

- **Terdokumentasi** — nilainya dapat ditunjuk langsung pada dokumen sumber.
- **Turunan** — dihitung dengan rumus dari nilai yang terdokumentasi.
- **Estimasi ahli** — ditetapkan tim peneliti karena nilai aktual belum ada; termasuk kategori
  *expert judgment*, metode estimasi yang juga diakui PMBOK dan dipakai PMP FNE sendiri.

---

## Contoh perhitungan

Seluruh contoh memakai **ACT-002 — IAM & SSO Implementation (P-FNE-01)**, kecuali disebut lain.

**1. Durasi rencana.** PMP P-FNE-01 menempatkan modul IAM pada Sprint 1 (*Auth & MFA*) dan Sprint 2
(*RBAC & SSO*), masing-masing 2 minggu.

$$D = 2\ \text{sprint} \times 2\ \text{minggu} \times 5\ \text{hari kerja} = 20\ \text{hari}$$

**2. Beban kerja rencana.** Dihitung atas basis satu developer ekuivalen (*1 FTE*) dengan 8 jam kerja
efektif per hari:

$$E = 20\ \text{hari} \times 8\ \text{jam} \times 1{,}0 = 160\ \text{orang-jam}$$

**3. Utilisasi sumber daya.** Kapasitas normal satu developer adalah 160 jam per bulan (sesuai tabel
*Resource Utilization Plan* PMP P-FNE-08, di mana 1 FTE = 160 jam/bulan). Bila developer yang
mengerjakan modul ini juga menangani modul lain sehingga bebannya menjadi 176 jam:

$$U = \frac{176\ \text{jam}}{160\ \text{jam}} = 1{,}10$$

Nilai $U > 1{,}0$ berarti *over-allocation*; $U < 1{,}0$ berarti beban masih di bawah kapasitas.

**4. Skor risiko.** Risk register PMP menilai probabilitas dan dampak pada skala 1–5. Modul IAM dinilai
$P = 3$ dan $I = 3$, lalu dikonversi ke skala 0–1:

$$R = \frac{3}{5} \times \frac{3}{5} = 0{,}6 \times 0{,}6 = 0{,}36$$

**5. SPI.** Pada titik pantau, nilai pekerjaan yang terselesaikan (*Earned Value*) mencapai 88% dari
nilai pekerjaan yang direncanakan (*Planned Value*):

$$SPI = \frac{EV}{PV} = \frac{88}{100} = 0{,}88$$

**6. Jumlah predecessor.** Untuk **ACT-021 (P-FNE-07)**, dokumen Pemetaan mencatat P-FNE-07 bergantung
pada P-FNE-02, 03, 04, 05, dan 06, sehingga `Predecessor_Count` $= 5$.

**7. Jumlah change request.** Untuk **ACT-004 (API Gateway & Kafka)**, ditetapkan 3 change request yang
disetujui CCB, mencerminkan penyesuaian spesifikasi integrasi selama pengerjaan.

**8. Label keterlambatan.** ACT-002 memiliki $SPI = 0{,}88 \le 0{,}90$, sehingga
`Status_Delay` $= 1$ (terlambat).

---

## Asumsi, batasan, dan implikasinya

**a. Mengapa nilai monitoring tidak diambil langsung dari dokumen.**
KAK, PMP, dan SRS adalah dokumen perencanaan yang disusun sebelum proyek dieksekusi. Dokumen tersebut
menetapkan *bagaimana* SPI, utilisasi, dan change request akan dipantau — lengkap dengan rumus, ambang,
dan periodisasinya — tetapi belum memuat hasil pemantauannya. Karena itu nilai per aktivitas
ditetapkan melalui estimasi ahli yang konsisten dengan rentang dan ambang pada dokumen.

**b. Mengapa utilisasi dapat melebihi 1,0 padahal PMP menunjukkan alokasi di bawah kapasitas.**
Tabel alokasi pada PMP P-FNE-08 menghasilkan utilisasi agregat maksimum 0,774 di level sub-proyek.
Namun **setiap PMP hanya mencatat alokasi di dalam sub-proyeknya sendiri**, sedangkan developer yang
sama menangani beberapa sub-proyek secara paralel. Utilisasi gabungan lintas sub-proyek tidak tercatat
pada dokumen mana pun. Nilai $U > 1{,}0$ dalam dataset merepresentasikan kondisi *shared developer*
lintas sub-proyek tersebut — dan justru ketiadaan pencatatan inilah salah satu celah yang diangkat
penelitian PRE-02.

**c. Konsekuensi metodologis dari penetapan label.**
Karena `Status_Delay` diturunkan dari kondisi $SPI \le 0{,}90$, aturan tersebut berlaku untuk seluruh
26 baris tanpa pengecualian. Akibatnya `SPI_Value` memiliki daya pisah yang sangat tinggi dan turut
menjelaskan mengapa metrik evaluasi pada Pertemuan 5 mendekati sempurna. Tindak lanjutnya: eksperimen
diulang **tanpa** `SPI_Value` sebagai fitur, sehingga model diuji pada kemampuan prediksi dini yang
sesungguhnya.

**d. Mengapa durasi aktivitas tidak selalu sama dengan panjang sprint.**
Satuan pada dokumen PMP adalah *sprint*, sedangkan satuan pada dataset adalah *modul*. Keduanya tidak
berkorespondensi satu-satu: sebuah sprint dapat memuat beberapa modul sekaligus, dan sebaliknya satu
modul dapat dikerjakan menyeberangi beberapa sprint bersama pekerjaan lain. Durasi pada dataset
mengacu pada rentang pengerjaan inti modul tersebut, bukan pada total panjang sprint yang memuatnya.
Tiga aktivitas berikut menunjukkan selisih terbesar dan dicatat sebagai butir peninjauan.

**e. Butir yang masih perlu ditinjau ulang.**

| Butir | Kondisi saat ini | Rencana peninjauan |
| :--- | :--- | :--- |
| Durasi ACT-001 | Dataset 10 hari; PMP P-FNE-01 mencatat Sprint 0 selama 1 minggu (5 hari) | Cakupan dataset mencakup penyiapan klaster K8s di luar Sprint 0; angka akan disinkronkan pada revisi dataset berikutnya |
| Durasi ACT-010 & ACT-011 | Dataset 25 hari; pemetaan sprint PMP P-FNE-03 memberi rentang berbeda | Tinjau ulang agregasi sprint ke modul |
| Basis `Planned_Effort_Hours` | Dihitung atas 1 FTE ekuivalen | Pertimbangkan basis ukuran tim penuh bila data alokasi per modul tersedia |

---

## Tabel 2 — Isi Dataset (`dataset_pre02_fne_v2.csv`, N = 26)

| ID | Sub-Proyek | Nama Aktivitas | Durasi (hari) | Effort (jam) | Pred. | Utilisasi | Risk | SPI | CR | Delay |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| ACT-001 | P-FNE-01 | Infrastructure & K8s Cluster Setup | 10 | 80 | 0 | 0.85 | 0.25 | 0.98 | 0 | 0 |
| ACT-002 | P-FNE-01 | IAM & SSO Implementation | 20 | 160 | 1 | 1.1 | 0.36 | 0.88 | 2 | **1** |
| ACT-003 | P-FNE-01 | Master Data Management (MDM) 24 Entities | 20 | 180 | 1 | 1.05 | 0.3 | 0.9 | 1 | **1** |
| ACT-004 | P-FNE-01 | API Gateway & Kafka Event Bus Setup | 10 | 90 | 2 | 0.95 | 0.48 | 0.82 | 3 | **1** |
| ACT-005 | P-FNE-02 | Farm & Land Parcel Registration API | 15 | 120 | 1 | 0.9 | 0.2 | 0.96 | 0 | 0 |
| ACT-006 | P-FNE-02 | Crop Cycle Planning & Tracking Service | 20 | 160 | 2 | 1.15 | 0.36 | 0.86 | 2 | **1** |
| ACT-007 | P-FNE-02 | Harvest & Batch Quality Management | 15 | 110 | 1 | 0.88 | 0.24 | 0.97 | 1 | 0 |
| ACT-008 | P-FNE-02 | Mobile Offline Sync Engine | 15 | 130 | 2 | 1.2 | 0.4 | 0.8 | 2 | **1** |
| ACT-009 | P-FNE-03 | Supplier Portal & Performance Scorecard | 15 | 100 | 1 | 0.85 | 0.18 | 0.98 | 0 | 0 |
| ACT-010 | P-FNE-03 | Procurement & Purchase Order Workflow | 25 | 200 | 2 | 1.05 | 0.35 | 0.89 | 3 | **1** |
| ACT-011 | P-FNE-03 | Inventory & Warehouse Multi-Location API | 25 | 190 | 2 | 1.12 | 0.42 | 0.84 | 2 | **1** |
| ACT-012 | P-FNE-04 | Production Planning & Multi-Level BOM Engine | 20 | 160 | 3 | 1.1 | 0.36 | 0.87 | 2 | **1** |
| ACT-013 | P-FNE-04 | MRP Computation Engine | 15 | 130 | 2 | 1.15 | 0.4 | 0.83 | 1 | **1** |
| ACT-014 | P-FNE-04 | Production Costing & Asset Maintenance | 15 | 110 | 1 | 0.9 | 0.22 | 0.95 | 0 | 0 |
| ACT-015 | P-FNE-05 | Sales Order CRUD & Validation API | 15 | 120 | 2 | 0.92 | 0.25 | 0.96 | 1 | 0 |
| ACT-016 | P-FNE-05 | Customer 360 View & CRM Integration | 15 | 110 | 1 | 0.88 | 0.2 | 0.97 | 0 | 0 |
| ACT-017 | P-FNE-05 | Real-time Shipment & Logistics Tracking | 20 | 150 | 2 | 1.08 | 0.38 | 0.88 | 2 | **1** |
| ACT-018 | P-FNE-06 | General Ledger & Auto Journal Ingestion | 20 | 160 | 4 | 1.02 | 0.3 | 0.91 | 1 | 0 |
| ACT-019 | P-FNE-06 | Accounts Payable Three-Way Matching | 15 | 120 | 2 | 0.95 | 0.28 | 0.94 | 1 | 0 |
| ACT-020 | P-FNE-06 | Payroll Engine & HCM Attendance Sync | 20 | 170 | 1 | 1.1 | 0.36 | 0.85 | 2 | **1** |
| ACT-021 | P-FNE-07 | Data Lake & Warehouse CDC Ingestion Pipeline | 25 | 200 | 5 | 1.15 | 0.45 | 0.82 | 3 | **1** |
| ACT-022 | P-FNE-07 | Executive BI Dashboard & KPI Alerting | 20 | 150 | 2 | 0.9 | 0.22 | 0.96 | 1 | 0 |
| ACT-023 | P-FNE-07 | AI Demand & Crop Yield Forecasting Service | 25 | 190 | 3 | 1.18 | 0.42 | 0.84 | 2 | **1** |
| ACT-024 | P-FNE-08 | IoT Telemetry Streaming & Threshold Alerting | 20 | 160 | 2 | 1.2 | 0.48 | 0.81 | 2 | **1** |
| ACT-025 | P-FNE-08 | Digital Twin Farm & Machine State Sync | 20 | 160 | 3 | 1.12 | 0.36 | 0.88 | 1 | **1** |
| ACT-026 | P-FNE-08 | What-If Simulation Engine & Autonomous Recommendation | 25 | 200 | 4 | 1.25 | 0.5 | 0.79 | 4 | **1** |

**Distribusi label:** 16 aktivitas terlambat (61,5%) dan 10 aktivitas tepat waktu (38,5%).

**Pola yang terverifikasi pada dataset:** seluruh 15 aktivitas dengan utilisasi $\ge 1{,}05$ berstatus
terlambat, sementara dari 11 aktivitas di bawah ambang tersebut hanya 1 yang terlambat. Pola ini
konsisten dengan teori *bottleneck* sumber daya, namun perlu dibaca bersama catatan (c) di atas:
karena nilai utilisasi dan label sama-sama ditetapkan pada tahap penyusunan dataset, pola tersebut
belum dapat diperlakukan sebagai bukti empiris independen.

---

tags #paper #mp #academic #research #dataset
