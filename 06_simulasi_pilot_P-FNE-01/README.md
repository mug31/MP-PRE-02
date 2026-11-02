# 06_simulasi_pilot_P-FNE-01
## Pilot Simulasi Monte Carlo Keterlambatan — Sub-Proyek P-FNE-01

Implementasi revisi dosen bimbingan 7 Oktober 2026 ([[revisi_7okt]]) pada **satu subproyek dulu**
(P-FNE-01 Foundation & Core Platform), sebelum diterapkan ke 8 subproyek.

### Isi folder

| Berkas | Isi | Revisi |
| :--- | :--- | :---: |
| `data/jadwal_aktivitas_P-FNE-01.csv` | 40 aktivitas dari PMP-01 §4.2.1: durasi, predecessor, prioritas (§3.3.2), role usulan, kolom sumber + interpretasi dependensi | 3, 4 |
| `data/resource_P-FNE-01.csv` | 16 orang dari PMP-01 §4.6.1 (jumlah per role per bulan → jendela ketersediaan tiap orang; 1 bulan = 22 hari kerja) | 5 |
| `simulasi_monte_carlo.py` | Penjadwalan per resource (FCFS/SPT), simulasi CR, 1000 iterasi, ringkasan | 6–11 |
| `buat_excel.py` | Pembuat `pilot_P-FNE-01.xlsx` (dipanggil otomatis) | – |
| `pilot_P-FNE-01.xlsx` | Workbook untuk dosen: jadwal rencana & 1 iterasi CR dengan rumus hidup (`RAND()`/`IF`, tekan F9), jadwal per orang, hasil 1000 iterasi | 4–10 |
| `hasil/00_RINGKASAN_HASIL.md` | Ringkasan hasil (digenerate) | 10, 11 |
| `hasil/*.csv`, `hasil/histogram_keterlambatan.png` | Data iterasi, ringkasan, per aktivitas, jadwal rencana, grafik sebaran | 10, 11 |

### Menjalankan

```bash
pip install openpyxl matplotlib
python simulasi_monte_carlo.py
```

Parameter (peluang CR, kelas kesulitan, jumlah iterasi, kebijakan antrian) ada di bagian atas
`simulasi_monte_carlo.py`. Hasil dapat direplikasi (seed 42).

### Keputusan & asumsi yang perlu disepakati kelompok

1. **Role per aktivitas** di `jadwal_aktivitas_P-FNE-01.csv` adalah usulan; PMP tidak menyebut PIC per aktivitas
   (dosen [29:28]: alokasi diserahkan ke kelompok).
2. **Dependensi berupa nama fase** ("Infrastructure", "IAM", "All Services") ditafsirkan sebagai seluruh aktivitas
   fase tersebut selesai — lihat kolom `Interpretasi_Dependensi`.
3. **Durasi**: 1 minggu = 5 hari kerja; 0,5 minggu dibulatkan ke atas menjadi 3 hari.
4. **Peluang CR 10% dan kelas kesulitan** (60/30/10%) adalah asumsi; dua skenario besar tambahan dibandingkan:
   angka contoh dosen dan kelas *impact* Change Control PMP-01 §2.5.1.
5. **Satu aktivitas dikerjakan satu orang**; orang yang masih ada di bulan ke-5 dianggap tersedia sampai proyek selesai.
   Orang hanya boleh *memulai* aktivitas di dalam jendela ketersediaannya, tetapi boleh menyelesaikannya melewati jendela itu.
6. **Role di PMP** hanya PM, DevOps, Backend, Frontend, Security, dan QA (§4.6.1); PO/BA yang disebut dosen sebagai contoh
   tidak ada di tabel resource P-FNE-01.

### Temuan awal yang perlu dibahas dengan dosen

- Jadwal rencana dari tabel aktivitas §4.2.1 selesai di **hari ke-131 (≈ 26 minggu)**, sedangkan ringkasan
  *Critical Path* §4.2.3 di dokumen yang sama menyebut **22 minggu** — dokumen PMP tidak konsisten.
- Dengan jumlah orang di §4.6.1, **antrian resource tidak pernah mengikat** pada P-FNE-01, sehingga FCFS = SPT.
  Batasan sumber daya kemungkinan baru terasa di level portofolio (orang dibagi ke 8 subproyek).
