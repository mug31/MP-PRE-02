# Hasil Simulasi Iterasi Random — P-FNE-02

> Digenerate otomatis oleh `simulasi_iterasi.py`. Jangan diedit manual; jalankan ulang script.

## Jadwal Rencana

- 153 aktivitas (sumber: `data/P-FNE-02_aktivitas.csv`).
- Tanpa batasan resource: selesai hari kerja ke-**231**.
- Dengan batasan resource, antrian FCFS: selesai hari kerja ke-**232**.
- Dengan batasan resource, antrian SPT: selesai hari kerja ke-**232**.

## Hasil

| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P-FNE-02 | dosen | FCFS | 153 | 232 | 100.0% | 55.7% | 0.0% | 5.46 | 7 | 8.01 | 12.51 |
| P-FNE-02 | dosen | SPT | 153 | 232 | 100.0% | 55.8% | 0.0% | 5.47 | 7 | 8.01 | 12.51 |
| P-FNE-02 | pmp | FCFS | 153 | 232 | 100.0% | 1.7% | 0.0% | 2.09 | 2.86 | 3.46 | 7.23 |
| P-FNE-02 | pmp | SPT | 153 | 232 | 100.0% | 1.7% | 0.0% | 2.09 | 2.86 | 3.46 | 7.23 |

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 116 aktivitas): 1.1.1, 1.1.2, 1.1.4, 1.1.5, 2.2.1, 2.2.2, 2.2.3, 2.3.1, 2.3.2, 2.3.3, 2.4.1, 2.4.2, 3.1.1.1, 3.1.1.2, 3.1.1.3, 3.1.1.4, 3.1.2.1, 3.1.2.2, 3.1.2.3, 3.1.2.4, 3.1.5.3, 3.1.6.1, 3.1.6.2, 3.2.1.1, 3.2.1.2, 3.2.1.3, 3.2.2.1, 3.2.2.2, 3.2.2.3, 3.2.2.4, 3.2.3.1, 3.2.3.2, 3.2.4.1, 3.2.4.2, 3.2.5.1, 3.2.5.2, 3.2.6.3, 3.2.7.1, 3.2.7.2, 3.3.1.1, 3.3.1.2, 3.3.2.1, 3.3.2.2, 3.3.5.2, 3.3.6.1, 3.3.6.2, 3.4.1.1, 3.4.2.1, 3.4.2.2, 3.4.2.3, 3.4.3.1, 3.4.4.1, 3.4.4.2, 3.4.4.3, 3.4.8.2, 3.4.9.1, 3.4.9.2, 3.5.1.1, 3.5.1.2, 3.5.1.3, 3.5.3.2, 3.5.4.1, 3.5.4.2, 3.6.1.1, 3.6.1.2, 3.6.1.3, 3.6.1.4, 3.6.2.1, 3.6.3.1, 3.6.3.2, 5.1.1, 5.1.2, 5.1.3, 5.2.1, 5.2.2, 5.2.3, 5.2.4, 5.3.1, 5.3.2, 5.3.3, 5.4.1, 5.4.2, 5.4.3, 6.1.1, 6.2.1, 6.2.2, 6.3.1, 6.3.2, 6.3.3, 6.4.1, 6.4.2, 6.4.3, 6.5.1, 6.5.2, 6.5.3, 6.6.1, 7.1.1, 7.1.2, 7.2.1, 7.2.2, 7.2.3, 7.3.1, 7.3.2, 7.3.3, 7.4.1, 7.4.2, 7.4.3, 7.5.1, 7.5.2, 8.1.1, 8.1.2, 8.1.3, 8.2.1, 8.2.2, 8.3.1, 8.3.2.
- Kadang kritis:

| ID | Aktivitas | Indeks kekritisan | Delay sendiri (CR) | Geser karena predecessor | Geser karena antrian resource |
|---|---|---|---|---|---|
| 3.5.2.1 | Schedule Activity Reminder | 91% | 0.05 | 2.65 | 0.00 |
| 3.1.3.3 | View Analysis History | 90% | 0.02 | 1.03 | 0.09 |
| 3.1.3.1 | Record Soil Analysis | 90% | 0.05 | 0.95 | 0.00 |
| 3.1.3.2 | Generate Recommendations | 89% | 0.03 | 1.00 | 0.00 |
| 3.1.5.2 | Land Parcel UI | 77% | 0.07 | 0.95 | 0.00 |
| 3.1.4.2 | Manage Facilities | 76% | 0.02 | 0.98 | 0.04 |
| 3.5.3.1 | Activity Recording UI | 9% | 0.04 | 2.65 | 0.00 |

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR di rantai penentu: **5.46 hari** per iterasi.
- Waktu menunggu resource di rantai penentu: **3 hari** pada jadwal rencana, rata-rata **2.72 hari** per iterasi simulasi (antrean karena orang yang sama mengerjakan beberapa aktivitas).
- Rata-rata jumlah CR per iterasi: 15.32 dari 153 aktivitas.

