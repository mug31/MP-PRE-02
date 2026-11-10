# Hasil Simulasi Iterasi Random — P-FNE-03

> Digenerate otomatis oleh `simulasi_iterasi.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 16 aktivitas (sumber: `data/P-FNE-03_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**140**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**220**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**220**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-03 | dosen | FCFS | 16 | 220 | 81.4% | 43.9% | 0.4% | 5.12 | 9 | 11 | 25.47 |
| P-FNE-03 | dosen | SPT | 16 | 220 | 81.4% | 43.9% | 0.4% | 5.12 | 9 | 11 | 25.47 |
| P-FNE-03 | pmp | FCFS | 16 | 220 | 81.4% | 10.3% | 0.0% | 1.91 | 3.59 | 5.03 | 14.06 |
| P-FNE-03 | pmp | SPT | 16 | 220 | 81.4% | 10.3% | 0.0% | 1.91 | 3.59 | 5.03 | 14.06 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 16 aktivitas): A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12, A13, A14, A15, A16.

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **5.12 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **160 hari** pada jadwal rencana, rata-rata **164.01 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 1.64 dari 16 aktivitas.

