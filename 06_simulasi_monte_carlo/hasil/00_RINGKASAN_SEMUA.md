# Ringkasan Hasil Simulasi Monte Carlo — 8 Subproyek Super ERP FNE

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Parameter

- Iterasi: **1000** per subproyek per skenario; seed `42-<kode>`; peluang CR per aktivitas: **0.1**
- Skenario CR `dosen`: rendah 60% (+10%–20%), sedang 30% (+30%), tinggi 10% (+50%)
- Skenario CR `pmp`: kecil 60% (+0%–5%), sedang 30% (+5%–20%), besar 10% (+20%–50%)
- Kebijakan antrian: FCFS (siap duluan dikerjakan duluan) dan SPT (durasi terpendek duluan)

## Hasil Utama (skenario `dosen`, FCFS)

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-01 | dosen | FCFS | 40 | 131 | 91.5% | 21.8% | 0.2% | 3.3 | 5.2 | 6.61 | 16.59 |
| P-FNE-02 | dosen | FCFS | 153 | 232 | 100.0% | 55.7% | 0.0% | 5.46 | 7 | 8.01 | 12.51 |
| P-FNE-03 | dosen | FCFS | 16 | 220 | 81.4% | 43.9% | 0.4% | 5.12 | 9 | 11 | 25.47 |
| P-FNE-04 | dosen | FCFS | 6 | 120 | 47.1% | 20.0% | 4.7% | 2.89 | 5.02 | 9 | 31.8 |
| P-FNE-05 | dosen | FCFS | 14 | 123 | 78.5% | 16.2% | 0.6% | 2.8 | 4.97 | 6.33 | 13.96 |
| P-FNE-06 | dosen | FCFS | 12 | 120 | 66.6% | 20.0% | 1.3% | 2.7 | 5.01 | 6.95 | 17.5 |
| P-FNE-07 | dosen | FCFS | 77 | 128 | 92.5% | 13.3% | 0.0% | 2.76 | 4.36 | 5.46 | 10.3 |
| P-FNE-08 | dosen | FCFS | 19 | 62 | 86.3% | 0.6% | 0.1% | 1.38 | 2.25 | 2.89 | 7.33 |

**Perhatian:** jumlah aktivitas tiap subproyek berbeda (mengikuti tingkat detail tiap PMP), sehingga P(telat) antarsubproyek tidak bisa dibandingkan mentah-mentah: subproyek dengan lebih banyak aktivitas di rantai kritis lebih sering terkena CR. Untuk perbandingan, gunakan P(telat > 10%) dan sebaran keterlambatannya.

## Semua Skenario

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-01 | dosen | FCFS | 40 | 131 | 91.5% | 21.8% | 0.2% | 3.3 | 5.2 | 6.61 | 16.59 |
| P-FNE-01 | dosen | SPT | 40 | 131 | 91.5% | 21.8% | 0.2% | 3.3 | 5.2 | 6.61 | 16.59 |
| P-FNE-01 | pmp | FCFS | 40 | 131 | 91.5% | 2.5% | 0.0% | 1.26 | 2.13 | 3 | 9.15 |
| P-FNE-01 | pmp | SPT | 40 | 131 | 91.5% | 2.5% | 0.0% | 1.26 | 2.13 | 3 | 9.15 |
| P-FNE-02 | dosen | FCFS | 153 | 232 | 100.0% | 55.7% | 0.0% | 5.46 | 7 | 8.01 | 12.51 |
| P-FNE-02 | dosen | SPT | 153 | 232 | 100.0% | 55.8% | 0.0% | 5.47 | 7 | 8.01 | 12.51 |
| P-FNE-02 | pmp | FCFS | 153 | 232 | 100.0% | 1.7% | 0.0% | 2.09 | 2.86 | 3.46 | 7.23 |
| P-FNE-02 | pmp | SPT | 153 | 232 | 100.0% | 1.7% | 0.0% | 2.09 | 2.86 | 3.46 | 7.23 |
| P-FNE-03 | dosen | FCFS | 16 | 220 | 81.4% | 43.9% | 0.4% | 5.12 | 9 | 11 | 25.47 |
| P-FNE-03 | dosen | SPT | 16 | 220 | 81.4% | 43.9% | 0.4% | 5.12 | 9 | 11 | 25.47 |
| P-FNE-03 | pmp | FCFS | 16 | 220 | 81.4% | 10.3% | 0.0% | 1.91 | 3.59 | 5.03 | 14.06 |
| P-FNE-03 | pmp | SPT | 16 | 220 | 81.4% | 10.3% | 0.0% | 1.91 | 3.59 | 5.03 | 14.06 |
| P-FNE-04 | dosen | FCFS | 6 | 120 | 47.1% | 20.0% | 4.7% | 2.89 | 5.02 | 9 | 31.8 |
| P-FNE-04 | dosen | SPT | 6 | 120 | 47.1% | 20.0% | 4.7% | 2.89 | 5.02 | 9 | 31.8 |
| P-FNE-04 | pmp | FCFS | 6 | 120 | 47.1% | 6.7% | 1.2% | 1.12 | 1.4 | 3.79 | 24.29 |
| P-FNE-04 | pmp | SPT | 6 | 120 | 47.1% | 6.7% | 1.2% | 1.12 | 1.4 | 3.79 | 24.29 |
| P-FNE-05 | dosen | FCFS | 14 | 123 | 78.5% | 16.2% | 0.6% | 2.8 | 4.97 | 6.33 | 13.96 |
| P-FNE-05 | dosen | SPT | 14 | 123 | 78.5% | 16.2% | 0.6% | 2.8 | 4.97 | 6.33 | 13.96 |
| P-FNE-05 | pmp | FCFS | 14 | 123 | 78.5% | 2.6% | 0.0% | 1.07 | 1.86 | 3.09 | 9.22 |
| P-FNE-05 | pmp | SPT | 14 | 123 | 78.5% | 2.6% | 0.0% | 1.07 | 1.86 | 3.09 | 9.22 |
| P-FNE-06 | dosen | FCFS | 12 | 120 | 66.6% | 20.0% | 1.3% | 2.7 | 5.01 | 6.95 | 17.5 |
| P-FNE-06 | dosen | SPT | 12 | 120 | 66.6% | 20.0% | 1.3% | 2.7 | 5.01 | 6.95 | 17.5 |
| P-FNE-06 | pmp | FCFS | 12 | 120 | 66.6% | 3.4% | 0.0% | 1.03 | 1.75 | 3.2 | 11.13 |
| P-FNE-06 | pmp | SPT | 12 | 120 | 66.6% | 3.4% | 0.0% | 1.03 | 1.75 | 3.2 | 11.13 |
| P-FNE-07 | dosen | FCFS | 77 | 128 | 92.5% | 13.3% | 0.0% | 2.76 | 4.36 | 5.46 | 10.3 |
| P-FNE-07 | dosen | SPT | 77 | 132 | 97.0% | 22.5% | 6.9% | 4.04 | 5.35 | 7.9 | 19.79 |
| P-FNE-07 | pmp | FCFS | 77 | 128 | 75.9% | 0.3% | 0.0% | 0.69 | 1.67 | 2.39 | 5.64 |
| P-FNE-07 | pmp | SPT | 77 | 132 | 97.1% | 8.5% | 1.0% | 2.05 | 2.37 | 4.08 | 16.21 |
| P-FNE-08 | dosen | FCFS | 19 | 62 | 86.3% | 0.6% | 0.1% | 1.38 | 2.25 | 2.89 | 7.33 |
| P-FNE-08 | dosen | SPT | 19 | 62 | 86.3% | 0.6% | 0.1% | 1.38 | 2.25 | 2.89 | 7.33 |
| P-FNE-08 | pmp | FCFS | 19 | 62 | 86.3% | 0.0% | 0.0% | 0.51 | 0.84 | 1.37 | 4.84 |
| P-FNE-08 | pmp | SPT | 19 | 62 | 86.3% | 0.0% | 0.0% | 0.51 | 0.84 | 1.37 | 4.84 |

## Berkas

- `ringkasan_semua.csv` — tabel di atas
- `histogram_semua.png` — sebaran keterlambatan 8 subproyek
- `P-FNE-0X/` — per subproyek: ringkasan, iterasi, per aktivitas, jadwal rencana, histogram
