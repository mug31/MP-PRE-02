# Hasil Simulasi Monte Carlo — P-FNE-07

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 77 aktivitas (sumber: `data/P-FNE-07_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**108**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**128**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**132**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-07 | dosen | FCFS | 77 | 128 | 92.5% | 13.3% | 0.0% | 2.76 | 4.36 | 5.46 | 10.3 |
| P-FNE-07 | dosen | SPT | 77 | 132 | 97.0% | 22.5% | 6.9% | 4.04 | 5.35 | 7.9 | 19.79 |
| P-FNE-07 | pmp | FCFS | 77 | 128 | 75.9% | 0.3% | 0.0% | 0.69 | 1.67 | 2.39 | 5.64 |
| P-FNE-07 | pmp | SPT | 77 | 132 | 97.1% | 8.5% | 1.0% | 2.05 | 2.37 | 4.08 | 16.21 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 17 aktivitas): 1.1, 1.2, 1.3, 1.5, 1.6, 2.1, 2.6, 2.11, 5.13, 6.7, 6.8, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8.
- Kadang kritis:

| ID | Aktivitas | Indeks kekritisan | Delay sendiri (CR) | Geser karena predecessor | Geser karena antrian resource |
|---|---|---|---|---|---|
| 2.2 | Data Lake Setup (MinIO/S3) | 100% | 0.06 | 0.77 | 0.00 |
| 2.4 | Database Schema Design | 100% | 0.10 | 0.83 | 0.00 |
| 7.1 | Pre-Deployment Checklist | 100% | 0.02 | 2.30 | 0.06 |
| 7.2 | Production Deployment | 100% | 0.04 | 2.38 | 0.00 |
| 5.11 | Optimization Engine (LP) | 96% | 0.12 | 0.28 | 1.56 |
| 6.4 | Integration with P-FNE-04 | 91% | 0.07 | 2.05 | 0.00 |
| 6.12 | Documentation Finalization | 90% | 0.06 | 2.24 | 0.00 |
| 5.9 | What-If Analysis Engine | 87% | 0.13 | 1.83 | -1.68 |
| 2.7 | Data Quality Rules Definition | 84% | 0.08 | 1.15 | 0.00 |
| 2.8 | Data Quality Monitoring | 84% | 0.07 | 1.23 | 0.00 |

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **3.26 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **62 hari** pada jadwal rencana, rata-rata **57.71 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 7.7 dari 77 aktivitas.
- Ada iterasi yang selesai **lebih cepat** dari rencana (dosen/FCFS 66 iterasi, dosen/SPT 19 iterasi, pmp/FCFS 233 iterasi, pmp/SPT 15 iterasi). Ini bukan galat: pada penjadwalan berbasis aturan antrian, memperpanjang satu aktivitas dapat mengubah urutan antrian sehingga orang terpakai lebih efisien (anomali penjadwalan Graham). Artinya jadwal rencana dengan aturan antrian ini belum optimal; ada ruang perbaikan lewat resource leveling.

