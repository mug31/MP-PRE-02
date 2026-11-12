# Dataset ML PRE-02 — dari Simulasi Iterasi Random

Luaran **Pertemuan 3 (Persiapan Data)** untuk dipakai di **Pertemuan 4 (Implementasi Desain Eksperimen)**:
4 model probabilistik (Logistic Regression, Random Forest, Gradient Boosting, Neural Network) sesuai
`judul_dan_progres_penelitian/Deskripsi_Penelitian.md`.

| Luaran Pertemuan 3 (`progres_penelitian_MP.md`) | Di mana |
| :--- | :--- |
| Dataset siap pakai | `dataset_ml.csv` (24.000 baris, 0 nilai kosong, 0 duplikat) |
| Dokumentasi preprocessing | Bagian *Alur*, *Parameter & rujukan*; kode `../ekstraksi_risiko.py`, `../buat_dataset_ml.py` |
| Deskripsi karakteristik data | Bagian *Karakteristik* |

## Alur

```
MP-datasetRaw/*.docx (8 PMP)
 ├─ ekstraksi_pmp.py     → data/P-FNE-0X_aktivitas.csv, _resource.csv   (jadwal & tim)
 └─ ekstraksi_risiko.py  → data/P-FNE-0X_risiko.csv                     (register risiko)
                                   │
kalibrasi_risiko.py  → dataset_ml/kalibrasi_risiko.csv   (faktor mitigasi, dicocokkan ke PMP-08 §9.6.2)
                                   │
buat_dataset_ml.py: 8 subproyek × 1000 iterasi (FCFS, CR skenario dosen + kejadian risiko)
   tiap iterasi dipantau di 25%, 50%, 75% jadwal rencana → 1 baris per titik
                                   │
dataset_ml/dataset_ml.csv   →   uji_dataset_ml.py (4 uji validasi)
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
| **`Telat_Lebih_5_Persen`** | **Label utama** | 〃 | 1 jika > 5% durasi rencana — **PMP-01 §4.7.3 Schedule Change Control**: perubahan > 5% baseline schedule harus disetujui Sponsor (≤ 5% cukup PM) |
| `Telat_Lebih_10_Persen` | Label | 〃 | 1 jika > 10% durasi rencana — **PMP-01 §8.4.3 Escalation Triggers**: "Schedule Delay > 10%" → eskalasi ke Sponsor |

## Parameter & rujukan

Setiap angka di simulasi punya rujukan:

| Komponen | Nilai | Rujukan |
| :--- | :--- | :--- |
| Daftar risiko, peluang, level dampak | Apa adanya dari register risiko tiap PMP | Bagian register di tiap PMP (kolom `Sumber` di `data/P-FNE-0X_risiko.csv`) |
| Konversi peluang 1–5 → persen | 10% / 30% / 50% / 70% / 90% | **PMP-01 §9.3.1** Probability-Impact Matrix: Very Low < 20%, Low 20–40%, Medium 40–60%, High 60–80%, Very High > 80% (nilai tengah) |
| Skala dampak ke jadwal | 0,5% / 3% / 7,5% / 15% / 25% durasi rencana aktivitas yang terkena | **PMP-01 §9.3.1**, "Dampak (Biaya, Jadwal, Kualitas)": Very Low < 1%, Low 1–5%, Medium 5–10%, High 10–20%, Very High > 20% (nilai tengah; > 20% diambil 25%) |
| Faktor mitigasi dampak | **0,4** | **Kalibrasi ke PMP-08 §9.6.2** (Monte Carlo: target 20 minggu, P50 21 minggu → median +5%). Hasil simulasi P-FNE-08 dengan faktor 0,4: median **+5,3%** (lihat `kalibrasi_risiko.csv`) |
| Change request | 10%; rendah 60% (+10–20%), sedang 30% (+30%), tinggi 10% (+50%) | Contoh dosen, bimbingan 7 Okt 2026 [50:35], [52:04–53:21]; pembagian 60/30/10 = asumsi kelompok |
| Risiko yang tidak disimulasikan | Perubahan scope/requirement dan risiko biaya murni (23 dari 171) | Scope = sudah dimodelkan sebagai CR (hindari hitung dua kali); biaya tidak menggeser jadwal |
| Label utama | > 5% durasi rencana | PMP-01 §4.7.3 |

Kalibrasi hanya menyamakan **median**. Simulasi hanya menambah durasi (CR, risiko), sehingga tidak bisa
menghasilkan penyelesaian lebih cepat dari rencana dan sebarannya lebih sempit dari PMP-08:

| P-FNE-08 | P20 | P50 | P80 | Peluang tepat waktu |
| :--- | ---: | ---: | ---: | ---: |
| PMP-08 §9.6.2 | −2,5% | +5,0% | +12,5% | 55% |
| Simulasi (faktor 0,4) | +3,8% | **+5,3%** | +7,1% | 0% |

## Karakteristik

**Label per subproyek** (sama untuk ketiga titik monitoring; 1000 iterasi):

| Subproyek | Selesai rencana | Risiko disimulasikan | Rata-rata telat (hari) | Median telat | P(telat) | **P(> 5%)** | P(> 10%) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P-FNE-01 | 131 | 17 | 6,16 | +4,4% | 100,0% | 40,3% | 2,2% |
| P-FNE-02 | 232 | 9 | 5,89 | +2,5% | 100,0% | 0,4% | 0,0% |
| P-FNE-03 | 220 | 22 | 12,85 | +5,4% | 100,0% | 57,6% | 6,3% |
| P-FNE-04 | 120 | 18 | 18,61 | +14,9% | 100,0% | 98,9% | 82,4% |
| P-FNE-05 | 123 | 29 | 6,91 | +5,3% | 100,0% | 55,7% | 4,6% |
| P-FNE-06 | 120 | 13 | 5,85 | +4,2% | 100,0% | 38,1% | 6,7% |
| P-FNE-07 | 128 | 12 | 3,85 | +2,8% | 97,6% | 13,2% | 0,1% |
| P-FNE-08 | 62 | 28 | 3,41 | +5,2% | 100,0% | 54,0% | 2,4% |
| **Semua** | | | | | **99,7%** | **44,8%** | **13,1%** |

`Telat` hampir selalu 1 sehingga tidak informatif; **`Telat_Lebih_5_Persen` (44,8%) dipakai sebagai label utama**.
P-FNE-02 hampir selalu 0 dan P-FNE-04 hampir selalu 1 pada label ini: P-FNE-02 terdiri dari 153 aktivitas kecil
sehingga gangguan saling meredam, sedangkan P-FNE-04 hanya 6 milestone besar sehingga setiap gangguan langsung
mengenai milestone panjang (akibat tingkat detail PMP yang berbeda, lihat `../README.md`).

**Statistik fitur** (24.000 baris):

| Fitur | Rata-rata | Simpangan baku | Min | Maks | Korelasi dengan label utama, semua subproyek (titik 0,25 / 0,50 / 0,75) | Korelasi dengan keterlambatan **di dalam** subproyek (titik 0,50, rentang 8 subproyek) |
| :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| SPI_Jadwal | 0,940 | 0,054 | 0,552 | 1,013 | −0,42 / −0,45 / −0,65 | −0,61 … −0,73 |
| Sisa_Waktu_Hari | 71,0 | 40,6 | 15,5 | 174,0 | −0,21 / −0,21 / −0,21 | – (konstan) |
| Backlog_Sisa_Persen | 0,518 | 0,219 | 0,157 | 0,898 | 0,15 / 0,21 / 0,65 | 0,61 … 0,73 |
| Utilisasi_Resource | 0,517 | 0,407 | 0,048 | 1,000 | 0,38 / 0,38 / 0,38 | – (hampir konstan) |
| Risiko_Belum_Dimitigasi | 0,46 | 0,89 | 0 | 11 | 0,20 / 0,35 / 0,30 | −0,08 … 0,43 |
| Frekuensi_CR | 2,11 | 3,30 | 0 | 26 | −0,25 / −0,30 / −0,33 | 0,29 … 0,57 |
| Pergeseran_Dependency_Hari | 1,47 | 1,52 | −0,36 | 17,18 | 0,25 / 0,26 / 0,50 | 0,15 … 0,69 |

Catatan membaca korelasi:

- **`Frekuensi_CR` negatif jika semua subproyek dicampur, tetapi positif di dalam setiap subproyek** (0,29–0,57).
  Penyebabnya perbedaan antarsubproyek: P-FNE-02 rata-rata 9 CR (153 aktivitas) tetapi hampir tidak pernah
  telat > 5%. Ini contoh paradoks Simpson dan alasan validasi harus per subproyek.
- `Sisa_Waktu_Hari` dan `Utilisasi_Resource` hampir tidak bervariasi di dalam satu subproyek (simpangan baku
  0 dan 0,003); keduanya terutama membedakan subproyek.
- `Risiko_Belum_Dimitigasi` hanya berkorelasi jelas di P-FNE-04 (0,43). Risiko dihitung "terbuka" hanya selama
  aktivitas yang terkena masih berjalan, sehingga jarang tertangkap pada titik monitoring. Ini temuan, bukan
  kesalahan, dan layak dibahas di keterbatasan.

## Validasi (`python uji_dataset_ml.py`)

| Uji | Hasil |
| :--- | :--- |
| Kewajaran: tanpa CR & risiko | 8 subproyek tepat rencana (SPI 1, telat 0, tidak ada CR/risiko tercatat) |
| Kebocoran label | 0 dari 2.400 titik berubah jika semua kejadian risiko setelah hari monitoring dibuang. Versi yang sengaja bocor terdeteksi (651/2.400), jadi uji ini mampu menangkap kebocoran |
| Risiko vs PMP | 171/171 risiko: ID, nama, peluang, dan dampak asli ditemukan di teks PMP-nya |
| Dataset | 24.000 baris, 0 kosong, 0 duplikat, label sama di ketiga titik satu iterasi, rentang fitur wajar |
| Reproduksi | Dataset identik byte per byte saat dibuat ulang (seed `42-ml-<kode>`) |
| Hasil simulasi lama | `simulasi_iterasi.py` dan seluruh `hasil/` tidak diubah |

## Untuk Pertemuan 4 (kontrak data pipeline)

| Hal | Isi |
| :--- | :--- |
| Fitur (X) | 7 kolom: `SPI_Jadwal` … `Pergeseran_Dependency_Hari` |
| Label (y) | `Telat_Lebih_5_Persen` |
| Kelompok validasi | `Subproyek`: latih di 7 subproyek, uji di 1, bergantian 8 kali (*leave-one-subproject-out*). Baris dari iterasi yang sama (3 titik) tidak boleh terpisah ke latih dan uji. Karena P-FNE-02 dan P-FNE-04 hampir satu kelas, metrik (AUC, Brier) dihitung dari gabungan prediksi semua lipatan, bukan rata-rata per lipatan |
| Analisis per titik | `Titik_Monitoring` untuk melihat kapan peringatan dini mulai akurat |
| Analisis sensitivitas (disarankan) | Ulangi dengan `FAKTOR_DAMPAK` 0,2 dan 1,0 di `buat_dataset_ml.py` |

## Menjalankan ulang

```bash
cd 06_simulasi_iterasi
python ekstraksi_risiko.py     # hanya jika PMP/aturan ekstraksi risiko berubah
python kalibrasi_risiko.py     # ±20 detik; memastikan FAKTOR_DAMPAK sesuai PMP-08 §9.6.2
python buat_dataset_ml.py      # ±1,5 menit; hasil identik setiap dijalankan
python uji_dataset_ml.py       # ±15 detik; 4 uji validasi
```
