# Hasil Simulasi Monte Carlo — P-FNE-08

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 19 aktivitas (sumber: `data/P-FNE-08_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**62**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**62**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**62**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-08 | dosen | FCFS | 19 | 62 | 86.3% | 0.6% | 0.1% | 1.38 | 2.25 | 2.89 | 7.33 |
| P-FNE-08 | dosen | SPT | 19 | 62 | 86.3% | 0.6% | 0.1% | 1.38 | 2.25 | 2.89 | 7.33 |
| P-FNE-08 | pmp | FCFS | 19 | 62 | 86.3% | 0.0% | 0.0% | 0.51 | 0.84 | 1.37 | 4.84 |
| P-FNE-08 | pmp | SPT | 19 | 62 | 86.3% | 0.0% | 0.0% | 0.51 | 0.84 | 1.37 | 4.84 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 19 aktivitas): ACT-004, ACT-005, ACT-008, ACT-012, ACT-019, ACT-023, ACT-024, ACT-030, ACT-035, ACT-047, ACT-066, ACT-070, ACT-075, ACT-086, ACT-107, ACT-109, ACT-114, ACT-116, ACT-117.

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **1.38 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **0 hari** pada jadwal rencana, rata-rata **0.0 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 1.9 dari 19 aktivitas.
- Batasan resource tidak pernah membuat aktivitas di rantai penentu menunggu, sehingga hasil FCFS dan SPT sama; seluruh keterlambatan berasal dari CR beserta rambatannya.

