# Hasil Simulasi Iterasi Random — P-FNE-01

> Digenerate otomatis oleh `simulasi_iterasi.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 40 aktivitas (sumber: `data/P-FNE-01_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**131**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**131**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**131**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-01 | dosen | FCFS | 40 | 131 | 91.5% | 21.8% | 0.2% | 3.3 | 5.2 | 6.61 | 16.59 |
| P-FNE-01 | dosen | SPT | 40 | 131 | 91.5% | 21.8% | 0.2% | 3.3 | 5.2 | 6.61 | 16.59 |
| P-FNE-01 | pmp | FCFS | 40 | 131 | 91.5% | 2.5% | 0.0% | 1.26 | 2.13 | 3 | 9.15 |
| P-FNE-01 | pmp | SPT | 40 | 131 | 91.5% | 2.5% | 0.0% | 1.26 | 2.13 | 3 | 9.15 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 17 aktivitas): A01, A02, A04, A05, A06, A08, A09, A11, A12, A23, A27, A28, A34, A37, A38, A39, A40.
- Kadang kritis:

| ID | Aktivitas | Indeks kekritisan | Delay sendiri (CR) | Geser karena predecessor | Geser karena antrian resource |
|---|---|---|---|---|---|
| A30 | Task Management | 91% | 0.10 | 2.25 | 0.00 |
| A29 | Approval Matrix | 91% | 0.10 | 2.25 | 0.00 |
| A35 | Performance Testing | 91% | 0.14 | 2.69 | 0.00 |
| A36 | Security Testing | 89% | 0.11 | 2.69 | 0.00 |
| A13 | Import/Export | 83% | 0.12 | 1.69 | 0.00 |
| A14 | Duplicate Detection | 82% | 0.12 | 1.69 | 0.00 |
| A15 | Versioning | 81% | 0.10 | 1.69 | 0.00 |

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **3.3 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **0 hari** pada jadwal rencana, rata-rata **0.0 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 3.97 dari 40 aktivitas.
- Batasan resource tidak pernah membuat aktivitas di rantai penentu menunggu, sehingga hasil FCFS dan SPT sama; seluruh keterlambatan berasal dari CR beserta rambatannya.

