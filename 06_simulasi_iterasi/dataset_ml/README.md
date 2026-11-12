# Dataset ML PRE-02 — dari Simulasi Iterasi Random

Luaran **Pertemuan 3 (Persiapan Data)** untuk dipakai di **Pertemuan 4 (Implementasi Desain Eksperimen)**:
4 model probabilistik (Logistic Regression, Random Forest, Gradient Boosting, Neural Network) sesuai
`judul_dan_progres_penelitian/Deskripsi_Penelitian.md`.

| Luaran Pertemuan 3 (`progres_penelitian_MP.md`) | Di mana |
| :--- | :--- |
| Dataset siap pakai | `dataset_ml.csv` (24.000 baris, 0 nilai kosong, 0 duplikat) |
| Dokumentasi preprocessing | Bagian *Alur* dan *Asumsi* di bawah; kode `../ekstraksi_risiko.py`, `../buat_dataset_ml.py` |
| Deskripsi karakteristik data | Bagian *Karakteristik* di bawah |

## Alur

```
MP-datasetRaw/*.docx (8 PMP)
 ├─ ekstraksi_pmp.py     → data/P-FNE-0X_aktivitas.csv, _resource.csv   (jadwal & tim, sudah ada)
 └─ ekstraksi_risiko.py  → data/P-FNE-0X_risiko.csv                     (register risiko, BARU)
                                   │
buat_dataset_ml.py: 8 subproyek × 1000 iterasi (FCFS, CR skenario dosen + kejadian risiko)
   tiap iterasi dipantau di 25%, 50%, 75% jadwal rencana → 1 baris per titik
                                   │
                         dataset_ml/dataset_ml.csv
```

Satu iterasi = satu "proyek" yang dijalankan sampai selesai. **Fitur** = kondisi proyek pada hari monitoring;
**label** = keterlambatan di akhir proyek. Fitur hanya memakai kejadian sampai hari monitoring.

## Kamus variabel

| Kolom | Peran | Variabel Deskripsi Penelitian §2 | Cara hitung |
| :--- | :--- | :--- | :--- |
| `Subproyek` | Kelompok (untuk validasi) | – | P-FNE-01…08 |
| `Iterasi` | ID | – | 1…1000 |
| `Titik_Monitoring` | Metadata | – | 0,25 / 0,50 / 0,75 dari hari selesai rencana |
| `Hari_Monitoring` | Metadata | – | Titik × selesai rencana (hari kerja) |
| `SPI_Jadwal` | Fitur | Progres aktual vs rencana | EV/PV; nilai pekerjaan = durasi rencana; progres aktivitas berjalan memakai durasi yang sudah diketahui pada hari itu |
| `Sisa_Waktu_Hari` | Fitur | Sisa waktu hingga deadline | Selesai rencana − hari monitoring |
| `Backlog_Sisa_Persen` | Fitur | Backlog yang tersisa | 1 − EV/total durasi rencana |
| `Utilisasi_Resource` | Fitur | Tingkat utilisasi sumber daya | Hari-orang terpakai ÷ hari-orang tersedia (jendela ketersediaan tiap orang), hari 1 s.d. monitoring |
| `Risiko_Belum_Dimitigasi` | Fitur | Jumlah risiko yang belum dimitigasi | Kejadian risiko yang sudah terjadi dan aktivitas yang terkena belum selesai |
| `Frekuensi_CR` | Fitur | Frekuensi perubahan | Jumlah CR pada aktivitas yang sudah dimulai |
| `Pergeseran_Dependency_Hari` | Fitur | Kinerja dependency | Rata-rata pergeseran hari "siap" (menunggu predecessor) aktivitas yang sudah dimulai vs rencana |
| `Keterlambatan_Akhir_Hari` | Label (regresi) | Probabilitas keterlambatan | Selesai simulasi − selesai rencana |
| `Telat` | Label | 〃 | 1 jika > 0 hari |
| **`Telat_Lebih_5_Hari`** | **Label utama (disarankan)** | 〃 | 1 jika > 5 hari |
| `Telat_Lebih_10_Persen` | Label | 〃 | 1 jika > 10% durasi rencana (ambang eskalasi PMP-01) |

## Karakteristik

**Label per subproyek** (sama untuk ketiga titik monitoring; 1000 iterasi):

| Subproyek | Selesai rencana | Risiko disimulasikan | Rata-rata telat (hari) | P(telat) | P(> 5 hari) | P(> 10%) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| P-FNE-01 | 131 | 17 | 5,26 | 99,9% | 49,6% | 1,1% |
| P-FNE-02 | 232 | 9 | 5,74 | 100,0% | 60,9% | 0,0% |
| P-FNE-03 | 220 | 22 | 10,39 | 99,9% | 85,0% | 3,7% |
| P-FNE-04 | 120 | 18 | 12,57 | 99,0% | 89,7% | 46,9% |
| P-FNE-05 | 123 | 29 | 5,61 | 99,9% | 52,1% | 2,9% |
| P-FNE-06 | 120 | 13 | 4,96 | 98,7% | 40,8% | 4,8% |
| P-FNE-07 | 128 | 12 | 3,53 | 96,2% | 23,8% | 0,2% |
| P-FNE-08 | 62 | 28 | 2,78 | 99,9% | 5,7% | 1,1% |
| **Semua** | | | | **99,2%** | **50,9%** | **7,6%** |

Pilihan label: `Telat` hampir selalu 1 dan `Telat_Lebih_10_Persen` hanya 7,6%, sehingga
**`Telat_Lebih_5_Hari` (50,9%) paling seimbang** dan disarankan sebagai label utama. Ambang 5 hari sama dengan
`BATAS_TELAT_HARI` di simulasi.

**Statistik fitur** (24.000 baris):

| Fitur | Rata-rata | Simpangan baku | Min | Maks | Korelasi dengan label utama (titik 0,25 / 0,50 / 0,75) |
| :--- | ---: | ---: | ---: | ---: | :--- |
| SPI_Jadwal | 0,952 | 0,048 | 0,588 | 1,016 | −0,29 / −0,35 / −0,48 |
| Sisa_Waktu_Hari | 71,0 | 40,6 | 15,5 | 174,0 | 0,33 / 0,33 / 0,33 |
| Backlog_Sisa_Persen | 0,512 | 0,221 | 0,155 | 0,897 | −0,12 / −0,02 / 0,38 |
| Utilisasi_Resource | 0,517 | 0,407 | 0,048 | 1,000 | 0,40 / 0,38 / 0,38 |
| Risiko_Belum_Dimitigasi | 0,23 | 0,57 | 0 | 8 | 0,13 / 0,23 / 0,19 |
| Frekuensi_CR | 2,12 | 3,31 | 0 | 26 | 0,13 / 0,12 / 0,09 |
| Pergeseran_Dependency_Hari | 1,20 | 1,36 | −0,41 | 15,33 | 0,33 / 0,40 / 0,56 |

Arah korelasi sesuai logika: SPI rendah, dependency bergeser, dan risiko terbuka → lebih sering telat; makin dekat
akhir proyek, korelasinya makin kuat.

**Catatan penting untuk eksperimen:** `Sisa_Waktu_Hari` dan `Utilisasi_Resource` hampir tidak bervariasi
**di dalam** satu subproyek (simpangan baku di dalam subproyek 0 dan 0,003); keduanya terutama membedakan
subproyek. Karena itu validasi harus **per subproyek** (lihat di bawah), agar model tidak sekadar mengenali
subproyek.

## Asumsi (perlu disepakati / disampaikan ke dosen)

| No. | Asumsi | Nilai | Dasar |
| :--- | :--- | :--- | :--- |
| 1 | Peluang & besar CR | 10%; rendah 60% (+10–20%), sedang 30% (+30%), tinggi 10% (+50%) | Contoh dosen; pembagian kelas = asumsi kelompok |
| 2 | Konversi skala risiko | Peluang 1–5 → 0,1/0,3/0,5/0,7/0,9; dampak kata/desimal → level 1–5 | Aturan di `ekstraksi_risiko.py` |
| 3 | Risiko yang tidak disimulasikan | Perubahan scope/requirement (sudah = CR) dan risiko biaya murni | Hindari hitung dua kali; biaya tidak menggeser jadwal |
| 4 | **Peluang residual risiko** | 0,5 × peluang di PMP | Risiko di register sudah punya rencana respons. **Asumsi kelompok** |
| 5 | **Dampak risiko** | Level 1–5 → +1,25% / 2,5% / 5% / 7,5% / 12,5% durasi rencana aktivitas | Skala contoh dosen (5–50%) × 0,25. **Asumsi kelompok** |
| 6 | Sasaran & waktu risiko | Waktu acak seragam; mengenai 1 aktivitas yang sedang berjalan | PMP tidak memetakan risiko ke aktivitas |
| 7 | Mitigasi | Risiko "terbuka" sampai aktivitas yang terkena selesai | PMP tidak memuat jadwal mitigasi |
| 8 | Dependency antarproyek | Diwakili pergeseran predecessor di dalam subproyek | PMP tidak memodelkan antarproyek secara kuantitatif |

Asumsi 4 dan 5 adalah **kalibrasi**: tanpa keduanya (risiko apa adanya), 100% iterasi telat lebih dari 5 hari di
hampir semua subproyek sehingga label tidak bervariasi. Nilainya ada di bagian atas `buat_dataset_ml.py`
(`FAKTOR_PELUANG`, `FAKTOR_DAMPAK`) dan dapat diubah lalu dijalankan ulang.

## Validasi yang sudah dilakukan

| Pemeriksaan | Hasil |
| :--- | :--- |
| Nilai kosong / duplikat | 0 / 0 |
| Ekstraksi risiko | 171 risiko dari 8 PMP; 148 disimulasikan; setiap baris punya kolom `Sumber` dan nilai asli dokumen |
| Kebocoran label | Fitur pada hari t dihitung ulang dengan semua kejadian risiko setelah t dibuang → **identik** di 2.400 titik uji. Versi yang sengaja bocor terdeteksi (122/720 titik berbeda), jadi uji ini memang mampu menangkap kebocoran |
| Hasil simulasi lama | `simulasi_iterasi.py` dan seluruh `hasil/` tidak diubah |

## Untuk Pertemuan 4 (kontrak data pipeline)

| Hal | Isi |
| :--- | :--- |
| Fitur (X) | 7 kolom: `SPI_Jadwal` … `Pergeseran_Dependency_Hari` |
| Label (y) | `Telat_Lebih_5_Hari` (disarankan) |
| Kelompok validasi | `Subproyek`: latih di 7 subproyek, uji di 1, bergantian 8 kali (*leave-one-subproject-out*). Baris dari iterasi yang sama (3 titik) tidak boleh terpisah ke latih dan uji |
| Analisis per titik | `Titik_Monitoring` untuk melihat kapan peringatan dini mulai akurat |

## Menjalankan ulang

```bash
cd 06_simulasi_iterasi
python ekstraksi_risiko.py     # hanya jika PMP/aturan ekstraksi risiko berubah
python buat_dataset_ml.py      # ±1,5 menit; seed 42-ml-<kode>, hasil identik setiap dijalankan
```
