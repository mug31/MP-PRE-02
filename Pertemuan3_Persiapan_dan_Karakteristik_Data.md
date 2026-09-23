# DOKUMENTASI PERSIAPAN & KARAKTERISTIK DATA (PERTEMUAN 3)
## Topik Riset: PRE-02 — Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas
**Studi Kasus:** Portofolio Modul Super ERP Farm Nation Enterprise (FNE) 2026  
**Berkas Data:** `MP-PRE-02-github/dataset_pre02_fne.csv`  

---

## 1. Identifikasi Sumber Data

Data yang digunakan dalam penelitian ini merupakan data empiris-simulatif yang diekstraksi secara langsung dari repositori resmi proyek berskala korporat **Super ERP Farm Nation Enterprise (FNE) 2026** yang tersimpan pada folder `MP_sumber_data/`.

### 1.1 Rincian Dokumen Sumber
Ekstraksi data didasarkan pada integrasi informasi dari:
1. **Kerangka Acuan Kerja (KAK):** `2026 KAK Proyek Farm Nation Enterprise.docx` (14 Bab) yang menetapkan ruang lingkup 12 fase dan 15 *milestone gates*.
2. **8 Dokumen Project Management Plan (PMP):**
   - `P-FNE-01`: Foundation & Core Platform
   - `P-FNE-02`: Core Agricultural Operations
   - `P-FNE-03`: Supply Chain & Procurement
   - `P-FNE-04`: Production & Manufacturing
   - `P-FNE-05`: Commerce, Sales & Logistics
   - `P-FNE-06`: Finance & HCM
   - `P-FNE-07`: Intelligence & Decision Platform
   - `P-FNE-08`: Advanced & Autonomous Enterprise
3. **8 Dokumen Software Requirements Specification (SRS):** Spesifikasi teknis entitas modul, arsitektur microservices, dan integrasi antar-subproyek.

---

## 2. Proses Pengumpulan Data & Penentuan Unit Analisis

Unit analisis dalam penelitian ini adalah **modul kerja tingkat operasional (*task/activity module*)** yang memiliki karakteristik:
1. Memiliki estimasi durasi dan beban jam kerja (*person-hours*) yang jelas dalam WBS.
2. Melibatkan alokasi tenaga ahli pengembang bersama (*shared developers*) lintas modul.
3. Terikat dalam rantai dependensi dengan modul lain (*predecessor-successor links*).
4. Berada pada titik pengawasan dan evaluasi (*monitoring & evaluation checkpoint*).

Dari total ratusan task mikro di 8 sub-proyek, dipilih **26 aktivitas inti (*core module tasks*)** yang paling strategis dan merepresentasikan variasi tingkat risiko, utilisasi, dan dependensi lintas sistem FNE.

---

## 3. Kamus Data & Dokumentasi Preprocessing

### 3.1 Struktur Variabel (Kamus Data)

| No | Kolom | Tipe Data | Deskripsi Operasional | Skala Pengukuran |
| :---: | :--- | :---: | :--- | :---: |
| 1 | `Task_ID` | String | Pengenal unik aktivitas (ACT-001 s.d ACT-026) | Nominal |
| 2 | `Sub_Project` | String | Kode sub-proyek induk (P-FNE-01 s.d P-FNE-08) | Nominal |
| 3 | `Task_Name` | String | Nama fungsionalitas modul perangkat lunak | Deskriptif |
| 4 | `Planned_Duration_Days` | Integer | Rencana durasi pelaksanaan dalam hari kerja | Rasio (10–25 hari) |
| 5 | `Planned_Effort_Hours` | Integer | Estimasi total jam kerja tim pengembang | Rasio (80–200 jam) |
| 6 | `Predecessor_Count` | Integer | Jumlah modul prasyarat langsung yang harus selesai sebelumnya | Diskrit (0–5 modul) |
| 7 | `Resource_Utilization_Rate` | Float | Rasio pemanfaatan developer terhadap kapasitas normal | Rasio (0.85–1.25) |
| 8 | `Risk_Score` | Float | Nilai probabilitas x dampak risiko dari Risk Register | Kontinu (0.18–0.50) |
| 9 | `SPI_Value` | Float | *Schedule Performance Index* ($EV / PV$) saat monitoring | Rasio (0.79–0.98) |
| 10 | `Change_Request_Count` | Integer | Frekuensi modifikasi kebutuhan yang disetujui | Diskrit (0–4 usulan) |
| 11 | `Status_Delay` | Integer | Status keterlambatan aktual ($1 = \text{Terlambat}, 0 = \text{Tepat Waktu}$) | Biner (0/1) |

### 3.2 Prosedur Preprocessing & Pembersihan Data
1. **Audit Missing Values:** Tidak ditemukan nilai kosong (*zero missing values*) pada ke-26 baris dan 11 kolom.
2. **Pengecekan Outlier & Range Sanitization:**
   - Seluruh nilai `Planned_Duration_Days` berada dalam rentang wajar siklus *sprint* enterprise (10 hingga 25 hari).
   - Nilai `SPI_Value` berkisar antara 0.79 hingga 0.98, mencerminkan variasi dinamika monitoring di mana tidak ada modul yang mengalami deviasi ekstrim abnormal.
3. **Data Encoding & Separation:**
   - Kolom metadata (`Task_ID`, `Sub_Project`, `Task_Name`) dipisahkan sebagai atribut identifikasi dan tidak dimasukkan ke dalam matriks fitur pemodelan.
   - Matriks fitur $X$ berdimensi $26 \times 7$ dan vektor target $Y$ berdimensi $26 \times 1$.
4. **Standardisasi Fitur:**
   - Fitur numerik ditransformasikan menggunakan `StandardScaler` ($\mu=0, \sigma=1$) dalam protokol *cross-validation* guna memastikan stabilitas konvergensi algoritma *Logistic Regression* dan *Multi-Layer Perceptron*.

---

## 4. Deskripsi Karakteristik & Analisis Statistik Deskriptif

### 4.1 Statistik Deskriptif Variabel Masukan ($N = 26$)

| Variabel | Rata-rata ($\mu$) | Standar Deviasi ($\sigma$) | Nilai Minimum | Nilai Maksimum |
| :--- | :---: | :---: | :---: | :---: |
| `Planned_Duration_Days` | 18.46 | 4.42 | 10.00 | 25.00 |
| `Planned_Effort_Hours` | 146.54 | 35.55 | 80.00 | 200.00 |
| `Predecessor_Count` | 2.00 | 1.13 | 0.00 | 5.00 |
| `Resource_Utilization_Rate` | 1.038 | 0.125 | 0.850 | 1.250 |
| `Risk_Score` | 0.335 | 0.095 | 0.180 | 0.500 |
| `SPI_Value` | 0.890 | 0.062 | 0.790 | 0.980 |
| `Change_Request_Count` | 1.50 | 1.07 | 0.00 | 4.00 |

*Seluruh nilai pada tabel dihitung ulang langsung dari `dataset_pre02_fne.csv` (standar deviasi sampel, $ddof = 1$).*

### 4.2 Distribusi Variabel Terikat (Target Class Balance)
- **Kelas Terlambat (`Status_Delay = 1`):** 16 modul (**61.54%**)
- **Kelas Tepat Waktu (`Status_Delay = 0`):** 10 modul (**38.46%**)
- *Analisis:* Distribusi kelas tergolong seimbang secara moderat (*mildly imbalanced*), sehingga tidak memerlukan teknik *synthetic resampling* yang berlebihan (seperti SMOTE), melainkan cukup dikontrol menggunakan stratifikasi pada saat partisi (*Stratified K-Fold*).

### 4.3 Karakteristik Hubungan Fitur terhadap Keterlambatan
Analisis awal menunjukkan pola yang sangat konsisten dengan teori manajemen proyek PMBOK:
1. **Dampak Overload Pengembang:** Seluruh 15 aktivitas dengan `Resource_Utilization_Rate` $\ge 1.05$ berstatus terlambat (`Status_Delay = 1`), sedangkan dari 11 aktivitas di bawah ambang tersebut hanya 1 yang terlambat. Pola ini mengindikasikan beban kerja melebihi 100% sebagai pemicu utama kegagalan jadwal.
2. **Efek Dependensi Jaringan:** Dari 6 modul dengan `Predecessor_Count` $\ge 3$ (pada `P-FNE-04`, `P-FNE-06`, `P-FNE-07`, dan `P-FNE-08`), 5 di antaranya terlambat akibat akumulasi keterlambatan modul pendahulunya (*delay propagation*).
3. **Korelasi SPI:** Seluruh 14 modul dengan `SPI_Value` $\le 0.88$ tergolong terlambat, menegaskan relevansi indikator *Earned Schedule* sebagai prediktor kuat.
4. **Catatan Kritis — Separabilitas `SPI_Value`:** Pada dataset ini `SPI_Value` nyaris memisahkan kedua kelas secara tunggal (modul terlambat berada pada rentang 0.79–0.90, modul tepat waktu pada 0.91–0.98). Konsekuensinya, metrik diskriminasi pada eksperimen P5 berpotensi mendekati nilai sempurna bukan semata karena keunggulan algoritma, melainkan karena keteraturan dokumen perencanaan yang menjadi sumber data (bersifat empiris-simulatif). Karakteristik ini dilaporkan secara terbuka sebagai keterbatasan penelitian dan menjadi dasar agenda validasi pada data proyek riil berukuran $N > 100$.

### 4.4 Implikasi Ukuran Data ($N = 26$) terhadap Desain Eksperimen
Mengingat ukuran sampel yang kompak ($N = 26$):
1. Pengujian tidak dapat mengandalkan pemisahan *train-test* acak sederhana karena berisiko varians estimasi yang tinggi; oleh karena itu **Stratified 5-Fold Cross-Validation** ditetapkan sebagai standar utama.
2. Model dengan kapasitas parameter raksasa (seperti *Deep Neural Networks* ratusan layer) dihindari; sebaliknya, model yang digunakan adalah model dengan regularisasi ketat (*L2-penalized Logistic Regression*, *Shallow Random Forest*, dan *Compact MLP 16-8*).
