# Ringkasan Hasil Simulasi Monte Carlo — Pilot P-FNE-01

> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.

## Parameter

- Iterasi: **1000**, seed 42; peluang CR per aktivitas: **0.1**
- Skenario CR `dosen`: rendah 60% (+10%–20%), sedang 30% (+30%), tinggi 10% (+50%)
- Skenario CR `pmp`: kecil 60% (+0%–5%), sedang 30% (+5%–20%), besar 10% (+20%–50%)
- Kebijakan antrian: FCFS (siap duluan dikerjakan duluan) dan SPT (durasi terpendek duluan)

## Jadwal Rencana

- Tanpa batasan resource (rumus dependensi dosen): selesai hari ke-**131** (≈ 26.2 minggu).
- Dengan batasan resource PMP §4.6.1, antrian FCFS: selesai hari ke-**131** (≈ 26.2 minggu).
- Dengan batasan resource PMP §4.6.1, antrian SPT: selesai hari ke-**131** (≈ 26.2 minggu).
- PMP-01 §4.2.3 (Critical Path Analysis) menyebut 22 minggu (110 hari kerja). Selisihnya berasal dari tabel aktivitas §4.2.1 yang durasinya lebih panjang daripada ringkasan per fase di §4.2.3 (contoh: Fase 1 = 6 minggu kerja dengan rantai 5 minggu di §4.2.1, tetapi 4 minggu di §4.2.3). Patokan "telat" pada simulasi ini adalah jadwal rencana hasil §4.2.1 + resource, bukan angka 22 minggu.

## Hasil per Skenario

| Skenario CR | Antrian | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |
|---|---|---|---|---|---|---|---|---|---|
| dosen | FCFS | 131 | 92.2% | 26.7% | 0.6% | 4.17 | 6 | 8 | 19 |
| dosen | SPT | 131 | 92.2% | 26.7% | 0.6% | 4.17 | 6 | 8 | 19 |
| pmp | FCFS | 131 | 92.2% | 11.1% | 0.0% | 2.9 | 4 | 6 | 12 |
| pmp | SPT | 131 | 92.2% | 11.1% | 0.0% | 2.9 | 4 | 6 | 12 |

Satuan keterlambatan: hari kerja. P80 = 80% iterasi selesai dengan keterlambatan tidak lebih dari nilai ini.

## Aktivitas Paling Menentukan (skenario `dosen`, FCFS)

Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).

- Selalu kritis (100% iterasi, 17 aktivitas): A01, A02, A04, A05, A06, A08, A09, A11, A12, A23, A27, A28, A34, A37, A38, A39, A40. CR di aktivitas ini pasti memundurkan tanggal selesai proyek.
- Kadang kritis (menjadi penentu hanya jika terkena CR yang cukup besar):

| ID | Aktivitas | Role | Indeks kekritisan | Delay sendiri (CR) | Geser karena predecessor | Geser karena antrian resource |
|---|---|---|---|---|---|---|
| A30 | Task Management | Frontend | 92% | 0.17 | 2.74 | 0.00 |
| A35 | Performance Testing | QA | 91% | 0.17 | 3.30 | 0.00 |
| A29 | Approval Matrix | Backend | 90% | 0.12 | 2.74 | 0.00 |
| A36 | Security Testing | Security | 90% | 0.15 | 3.30 | 0.00 |
| A13 | Import/Export | Frontend | 82% | 0.15 | 2.07 | 0.00 |
| A14 | Duplicate Detection | Backend | 81% | 0.15 | 2.07 | 0.00 |
| A15 | Versioning | Backend | 81% | 0.14 | 2.07 | 0.00 |

Nilai delay/geser adalah rata-rata hari per iterasi. "Delay sendiri" = tambahan durasi karena CR di aktivitas itu; "geser" = mundurnya tanggal mulai dibanding rencana (rambatan).

## Penyebab Keterlambatan (skenario `dosen`, FCFS)

- Rata-rata tambahan durasi CR yang berada di rantai penentu: **4.17 hari** per iterasi.
- Rata-rata waktu menunggu resource di rantai penentu: **0.0 hari** per iterasi.
- Rata-rata jumlah CR per iterasi: 3.92 dari 40 aktivitas.
- **Batasan resource tidak pernah mengikat** pada pilot ini: dengan jumlah orang di PMP-01 §4.6.1 dan asumsi 1 aktivitas dikerjakan 1 orang, tidak ada aktivitas di rantai penentu yang menunggu orang. Karena itu hasil FCFS dan SPT identik, dan seluruh keterlambatan berasal dari CR beserta rambatannya. Antrian resource baru berpengaruh jika orang dibagi antarsubproyek (portofolio 8 subproyek) atau jika satu aktivitas membutuhkan lebih dari satu orang.
- P(telat) sama pada kedua skenario CR karena tambahan sekecil apa pun dibulatkan ke atas menjadi minimal 1 hari, sehingga "telat" (> 0 hari) hanya bergantung pada ada/tidaknya CR di rantai penentu. Perbedaan skenario terlihat pada P(telat > 5 hari) dan sebarannya.

## Berkas

- `iterasi.csv` — satu baris per iterasi × skenario × kebijakan
- `ringkasan.csv` — tabel hasil per skenario
- `per_aktivitas.csv` — delay sendiri vs rambatan per aktivitas
- `jadwal_rencana.csv` — jadwal rencana per aktivitas (tanpa resource, FCFS, SPT)
- `histogram_keterlambatan.png` — sebaran keterlambatan
