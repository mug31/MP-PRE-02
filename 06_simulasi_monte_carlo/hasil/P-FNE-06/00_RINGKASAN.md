# Hasil Simulasi Monte Carlo — P-FNE-06

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 12 aktivitas (sumber: `data/P-FNE-06_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**120**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**120**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**120**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-06 | dosen | FCFS | 12 | 120 | 66.6% | 20.0% | 1.3% | 2.7 | 5.01 | 6.95 | 17.5 |
| P-FNE-06 | dosen | SPT | 12 | 120 | 66.6% | 20.0% | 1.3% | 2.7 | 5.01 | 6.95 | 17.5 |
| P-FNE-06 | pmp | FCFS | 12 | 120 | 66.6% | 3.4% | 0.0% | 1.03 | 1.75 | 3.2 | 11.13 |
| P-FNE-06 | pmp | SPT | 12 | 120 | 66.6% | 3.4% | 0.0% | 1.03 | 1.75 | 3.2 | 11.13 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 11 aktivitas): M0, M1, M2, M3, M4, M5, M7, M8, M9, M10, M11.

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **2.7 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **0 hari** pada jadwal rencana, rata-rata **0.0 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 1.17 dari 12 aktivitas.
- Batasan resource tidak pernah membuat aktivitas di rantai penentu menunggu, sehingga hasil FCFS dan SPT sama; seluruh keterlambatan berasal dari CR beserta rambatannya.

