Berikut adalah contoh penelusuran pelacakan sumber dokumen untuk **setiap kolom di baris ACT-001**:

---

### 📌 Contoh Pelacakan Sumber untuk Baris ACT-001

Data pada baris **ACT-001** berasal dari dokumen utama **`2026 PMP Super ERP Farm Nation Enterprise Foundation & Core Platform.docx`** (sub-proyek **P-FNE-01**). Berikut rincian lokasi dokumen, bab, dan cara mendapatkan setiap angkanya:

| Kolom | Nilai | Dokumen & Bab Sumber | Cara Memperoleh Angka / Rumus |
| :--- | :--- | :--- | :--- |
| **`Task_ID`** | **`ACT-001`** | **`Penjelasan_Variabel_Dataset.md`** | Kode unik pengenal aktivitas urutan ke-1 yang ditetapkan dalam dataset eksperimen. |
| **`Sub_Project`** | **`P-FNE-01`** | **PMP P-FNE-01** (Bab 1.2) | Kode resmi sub-proyek *Foundation & Core Platform* pada portofolio FNE. |
| **`Task_Name`** | **Infrastructure & K8s Cluster Setup** | **PMP P-FNE-01** (Bab 3.5 WBS Level 1-3) | Nama modul/aktivitas dari elemen WBS 1.1 (*Infrastructure & DevOps / Kubernetes Cluster*). |
| **`Planned_Duration_Days`** | **`5`** | **PMP P-FNE-01** (Bab 4.2 / 4.4 Jadwal) | Diambil dari durasi *Sprint 0 / Setup Infrastructure* selama 1 minggu kerja (5 hari kerja). |
| **`Planned_Effort_Hours`** | **`40`** | **PMP P-FNE-01** (Bab 7 Resource Management) | Dihitung dengan rumus konversi PMP: \\(\text{Durasi (5 hari)} \times 8\text{ jam/hari} \times 1.0\text{ FTE} = 40\text{ jam}\\). |
| **`Predecessor_Count`** | **`0`** | **PMP P-FNE-01** (Bab 4.2 *Activity Sequencing*) | Bernilai `0` karena merupakan modul fondasi paling awal di Fase 1 yang tidak membutuhkan *predecessor*. |
| **`Resource_Utilization_Rate`** | **`0.85`** | **PMP P-FNE-01** (Bab 7 *Resource Plan*) | Dihitung dari rasio jam kerja dialokasikan terhadap kapasitas normal (160 jam/bulan). Nilai \\(0.85 < 1.0\\) berarti alokasi pengembang masih aman. |
| **`Risk_Score`** | **`0.25`** | **PMP P-FNE-01** (Bab 8 / 9 *Risk Register*) | Hasil matriks probabilitas \\(\times\\) dampak (\\(P \times I\\)) pada *Risk Register* yang dikonversi ke skala \\(0.0–1.0\\). |
| **`SPI_Value`** | **`0.98`** | **PMP P-FNE-01** (Bab 4 & 7 Pemantauan EVM) | Nilai *Schedule Performance Index* (\\(\text{SPI} = \frac{EV}{PV}\\)) pada titik pemantauan. Angka \\(0.98\\) menunjukkan proyek berjalan hampir tepat sesuai jadwal. |
| **`Change_Request_Count`** | **`0`** | **PMP P-FNE-01** (Bab 3.1 & 4 *Change Control*) | Jumlah usulan perubahan lingkup yang diajukan ke *Change Control Board* (CCB) untuk modul ini. |
| **`Status_Delay`** | **`0`** | **Turunan Kinerja PMP** | Status biner target (\\(0 = \text{Tepat Waktu}\\)) karena nilai \\(\text{SPI\_Value } (0.98) > 0.90\\). |

---

### 💡 Panduan Praktis untuk Baris Lainnya
Jika Anda ingin memeriksa baris modul lainnya (misalnya **ACT-010** atau **ACT-021**):
1. Lihat kode kolom **`Sub_Project`** (misalnya `P-FNE-03` atau `P-FNE-07`).
2. Buka file **PMP** yang sesuai dengan kode sub-proyek tersebut.
3. Rujukan cepat untuk seluruh 26 baris dapat dilihat di file catatan **`Penjelasan_Variabel_Dataset.md`**.

---

🎯 *Apakah Anda ingin mencoba melacak baris aktivitas dari sub-proyek lain, seperti P-FNE-03 (Supply Chain) atau P-FNE-08 (Autonomous Enterprise)?*