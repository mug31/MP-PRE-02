# Hasil Simulasi Monte Carlo — P-FNE-05

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 14 aktivitas (sumber: `data/P-FNE-05_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**123**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**123**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**123**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-05 | dosen | FCFS | 14 | 123 | 78.5% | 16.2% | 0.6% | 2.8 | 4.97 | 6.33 | 13.96 |
| P-FNE-05 | dosen | SPT | 14 | 123 | 78.5% | 16.2% | 0.6% | 2.8 | 4.97 | 6.33 | 13.96 |
| P-FNE-05 | pmp | FCFS | 14 | 123 | 78.5% | 2.6% | 0.0% | 1.07 | 1.86 | 3.09 | 9.22 |
| P-FNE-05 | pmp | SPT | 14 | 123 | 78.5% | 2.6% | 0.0% | 1.07 | 1.86 | 3.09 | 9.22 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 14 aktivitas): S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, M8, M9, M10, M11.

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **2.8 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **0 hari** pada jadwal rencana, rata-rata **0.0 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 1.4 dari 14 aktivitas.
- Batasan resource tidak pernah membuat aktivitas di rantai penentu menunggu, sehingga hasil FCFS dan SPT sama; seluruh keterlambatan berasal dari CR beserta rambatannya.

