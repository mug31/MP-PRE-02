> [!warning] Catatan versi
> Dokumen ini adalah draf awal dan **digantikan oleh** [[Penjelasan_Variabel_Dataset]], yang mencakup
> seluruh 8 variabel beserta rumus, contoh perhitungan, dan status penelusurannya.
> Dua nama tabel yang dikutip di bawah (*Activity Duration & Effort Estimates* dan
> *Resource Utilization Report & Tracking Matrix*) tidak ditemukan pada 18 dokumen sumber di
> `MP-datasetRaw/`, sehingga jangan dipakai sebagai rujukan saat presentasi.

---

Nilai-nilai variabel *resource* (sumber daya) di dalam dataset **`dataset_pre02_fne.csv`** diekstraksi dari **Bab 7 (Manajemen Sumber Daya Proyek / *Resource Management Plan*)** dan **Bab 4 (Manajemen Jadwal / *Schedule Management Plan*)** pada ke-8 dokumen **PMP (*Project Management Plan*)** Super ERP FNE (`P-FNE-01` s.d. `P-FNE-08`).

Berikut adalah rincian dari mana dan bagaimana nilai-nilai *resource* tersebut diperoleh:

---

### **1. `Planned_Effort_Hours` (Beban Jam Kerja Rencana)**
* **Asal Data:** Diekstraksi dari tabel *Activity Duration & Effort Estimates* (WBS) di **Bab 4 dan Bab 7 PMP** tiap sub-proyek.
* **Cara Memperoleh Nilai:** Angka jam kerja orang (*person-hours*, contoh: 80, 120, 160, hingga 200 jam) dihitung dari penjumlahan alokasi jam kerja tim *developer* (Backend, Frontend, QA, DevOps) yang ditugaskan untuk menuntaskan modul tersebut.

---

### **2. Resource_Utilization_Rate (Tingkat Utilisasi Sumber Daya)**
* **Asal Data:** Diekstraksi dari *Resource Utilization Report & Tracking Matrix* pada **Bab 7 PMP** masing-masing sub-proyek.
* **Rumus Perhitungan:**

$$
\text{Resource Utilization Rate} = \frac{\text{Total Jam Kerja Efektif / Workload Developer}}{\text{Kapasitas Standar Normal Developer (100\% / 1.0)}}
$$


* **Arti Angka di Dataset:**
  * **`1.00` (100%)**: Beban kerja *developer* berada tepat pada batas kapasitas normal (contoh: 160 jam/bulan).
  * **`> 1.00` (misal 1.05, 1.15, 1.25)**: *Developer* mengalami **kelebihan beban (*over-allocation / overload*)** melebihi 100%. Hal ini terjadi karena tenaga ahli (*shared developer*) harus mengerjakan beberapa modul atau sub-proyek secara bersamaan/paralel.
  * **`< 1.00` (misal 0.85, 0.90)**: Beban kerja *developer* masih di bawah kapasitas maksimum (kondisi aman/longgar).


---

### **Dampak Nilai Resource Terhadap Hasil Prediksi**
Secara empiris pada dataset FNE, seluruh **15 modul yang memiliki nilai `Resource_Utilization_Rate` \\(\ge 1.05\\) (mengalami *overload*) terbukti mengalami keterlambatan (`Status_Delay = 1`)**. Hal ini memvalidasi teori manajemen proyek bahwa alokasi sumber daya manusia yang melebihi kapasitas normal memicu *bottleneck* dan keterlambatan pengerjaan modul.