# Hasil Simulasi Monte Carlo — P-FNE-04

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 6 aktivitas (sumber: `data/P-FNE-04_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**120**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**120**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**120**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-04 | dosen | FCFS | 6 | 120 | 47.1% | 20.0% | 4.7% | 2.89 | 5.02 | 9 | 31.8 |
| P-FNE-04 | dosen | SPT | 6 | 120 | 47.1% | 20.0% | 4.7% | 2.89 | 5.02 | 9 | 31.8 |
| P-FNE-04 | pmp | FCFS | 6 | 120 | 47.1% | 6.7% | 1.2% | 1.12 | 1.4 | 3.79 | 24.29 |
| P-FNE-04 | pmp | SPT | 6 | 120 | 47.1% | 6.7% | 1.2% | 1.12 | 1.4 | 3.79 | 24.29 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 6 aktivitas): M2, M3, M4, M5, M6, M7.

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **2.89 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **0 hari** pada jadwal rencana, rata-rata **0.0 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 0.6 dari 6 aktivitas.
- Batasan resource tidak pernah membuat aktivitas di rantai penentu menunggu, sehingga hasil FCFS dan SPT sama; seluruh keterlambatan berasal dari CR beserta rambatannya.

