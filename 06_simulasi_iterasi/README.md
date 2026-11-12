# 06_simulasi_iterasi
## Simulasi Iterasi Random Keterlambatan — 8 Sub-Proyek Super ERP FNE

Implementasi revisi dosen bimbingan 7 Oktober 2026 ([[revisi_7okt]]): probabilitas keterlambatan dihitung dari
simulasi berulang berbasis jadwal aktivitas dan resource di PMP, dengan change request (CR) yang disimulasikan.
Metode dicoba dulu pada P-FNE-01, lalu diterapkan ke ke-8 subproyek.

### Alur

```
MP-datasetRaw/*.docx ──ekstraksi_pmp.py──▶ data/P-FNE-0X_aktivitas.csv + _resource.csv
                                                   │
                                     simulasi_iterasi.py (1000 iterasi × 2 skenario CR × 2 antrian)
                                                   │
                         hasil/ (ringkasan, iterasi, per aktivitas, histogram) + excel/P-FNE-0X.xlsx
```

### Isi folder

| Berkas | Isi | Revisi |
| :--- | :--- | :---: |
| `ekstraksi_pmp.py` | Membaca tabel asli di 8 berkas PMP `.docx` dan menulis jadwal + resource per subproyek. Semua tafsiran tertulis di kode dan di kolom `Catatan` | 3–5 |
| `data/P-FNE-0X_aktivitas.csv` | ID, durasi (hari kerja), predecessor, kebutuhan resource (`Role:jumlah`), durasi/dependensi/resource asli dokumen, sumber, catatan | 3, 4 |
| `data/P-FNE-0X_resource.csv` | Orang/tim, role, jendela ketersediaan, sumber | 5 |
| `simulasi_iterasi.py` | Penjadwalan dengan antrian resource (FCFS/SPT), simulasi CR, iterasi, ringkasan | 6–11 |
| `buat_excel.py` | Pembuat workbook Excel (dipanggil otomatis) | – |
| `ekstraksi_risiko.py` | Membaca register risiko di 8 PMP → `data/P-FNE-0X_risiko.csv` (peluang & dampak asli + hasil normalisasi) | Deskripsi Penelitian |
| `kalibrasi_risiko.py` | Mencari faktor mitigasi dampak risiko agar median keterlambatan P-FNE-08 sama dengan analisis kuantitatif PMP-08 §9.6.2 | Deskripsi Penelitian |
| `buat_dataset_ml.py` | Simulasi + kejadian risiko, dipantau di 25/50/75% jadwal → dataset untuk 4 model ML | Deskripsi Penelitian |
| `uji_dataset_ml.py` | 4 uji validasi dataset: kewajaran, kebocoran label, risiko vs teks PMP, kualitas data | – |
| `dataset_ml/` | `dataset_ml.csv` (24.000 baris, 7 fitur + label), `kalibrasi_risiko.csv`, dan `README.md` (kamus variabel, rujukan parameter, karakteristik) | Pertemuan 3 → 4 |
| `excel/P-FNE-0X.xlsx` | Untuk dosen: jadwal rencana & 1 iterasi CR dengan rumus hidup (`RAND()`/`IF`, tekan F9), jadwal per orang, 1000 iterasi | 4–10 |
| `hasil/00_RINGKASAN_SEMUA.md` | Ringkasan 8 subproyek (digenerate) | 10, 11 |
| `hasil/histogram_semua.png` | Sebaran keterlambatan 8 subproyek | 11 |
| `hasil/P-FNE-0X/` | Per subproyek: `00_RINGKASAN.md`, `iterasi.csv`, `per_aktivitas.csv`, `jadwal_rencana.csv`, histogram | 8–11 |

### Menjalankan

```bash
pip install openpyxl matplotlib
python ekstraksi_pmp.py          # hanya perlu jika dokumen PMP atau aturan ekstraksi berubah
python simulasi_iterasi.py   # semua subproyek; atau: python simulasi_iterasi.py 01 07
```

Parameter (peluang CR, kelas kesulitan, jumlah iterasi, kebijakan antrian) ada di bagian atas
`simulasi_iterasi.py`. Hasil dapat direplikasi (seed `42-<kode>`).

### Data yang dipakai per subproyek (pilihan A: tabel paling detail yang durasi DAN dependensinya tertulis)

| Subproyek | Sumber jadwal | Aktivitas | Resource | Catatan penting |
| :--- | :--- | :---: | :--- | :--- |
| P-FNE-01 | §4.2.1 High-Level Activities (minggu) | 40 | §4.6.1 orang per bulan (16 orang) | Role per aktivitas = **usulan kelompok** (PMP tidak menyebut PIC) |
| P-FNE-02 | §4.3.1 Activity List (hari, predecessor, resource) | 153 | §7.3.1 Team Structure (15 orang) | Kebutuhan orang per aktivitas tertulis (mis. `BE:2`) |
| P-FNE-03 | §4.2.2.2 aktivitas per sprint + §4.2.3.2 Dependency Matrix | 16 | §4.3.1: satu tim scrum | Satu tim mengerjakan satu sprint dalam satu waktu |
| P-FNE-04 | §4.5.1 Milestone Schedule (sprint) | 6 | §4.7.1: satu tim scrum | Dependensi aktivitas hanya 6 butir umum → level milestone |
| P-FNE-05 | Sprint Schedule (§4.7.3 B) + tanggal milestone §4.4.3 | 14 | satu tim scrum | Dependensi aktivitas hanya 20 dari ±120 → level sprint |
| P-FNE-06 | §4.2.1 Daftar Milestone + jaringan §4.4.1–4.4.2 | 12 | tim inti + tim frontend (§4.5) | Sebagian aktivitas hanya ber-story point → level milestone |
| P-FNE-07 | §4.3.1–4.3.7 Detail Aktivitas (hari, dependensi, sumber daya) | 77 | §4.6.3 Sprint Capacity (18 orang) | Satu-satunya subproyek dengan antrian resource yang terasa |
| P-FNE-08 | §4.10.2 Critical Path Analysis (ES/EF) | 19 | §7.4.2 per orang (21 orang) | Hanya aktivitas kritis yang punya durasi & urutan tertulis |

Akibat pilihan A, jumlah aktivitas berbeda antarsubproyek, sehingga P(telat) **tidak bisa dibandingkan mentah-mentah**.
Gunakan P(telat > 10%) dan sebarannya untuk perbandingan.

### Model

1. **Satuan waktu** hari kerja: 1 minggu = 5 hari, 1 sprint = 10 hari. Rumus dosen: arrival = selesai predecessor + 1;
   selesai = mulai + durasi − 1.
2. **Resource**: aktivitas mulai jika siap DAN semua orang yang dibutuhkan (per role) kosong. Antrian FCFS atau SPT;
   jika aktivitas terdepan belum bisa mulai, aktivitas berikutnya boleh mulai bila orangnya ada.
3. **CR**: tiap aktivitas `RAND() < 0,1` → kena CR; kelas kesulitan diacak; tambahan durasi = durasi rencana × persentase
   (pecahan hari, tidak dibulatkan agar aktivitas 1 hari tidak otomatis +100%).
4. **Iterasi**: 1000 kali; bilangan random yang sama dipakai untuk kedua skenario CR dan kedua kebijakan antrian.

### Keputusan & asumsi yang perlu disepakati kelompok

1. Role per aktivitas P-FNE-01 (usulan).
2. Singkatan role yang ditafsirkan: "BE/FE Lead" = developer senior, "All Team(s)" = PM, "Leads" = Tech Lead;
   pihak luar tim (Sponsor, Users, Farm Mgr, PO di P-FNE-07) tidak dibatasi.
3. Peluang CR 10% dan pembagian kelas kesulitan 60/30/10%.
4. P-FNE-01: orang hanya boleh *memulai* aktivitas di dalam jendela ketersediaannya (1 bulan = 22 hari kerja).
5. Batas "telat": hasil disajikan untuk > 0 hari, > 5 hari, dan > 10% durasi rencana.

### Temuan untuk dibahas dengan dosen

- **Dokumen PMP tidak konsisten antara tabel aktivitas dan ringkasannya**: P-FNE-01 (§4.2.1 ≈ 26 minggu vs §4.2.3
  22 minggu), P-FNE-02 (rangkaian aktivitas 231 hari vs ringkasan §4.6.2 155 hari), P-FNE-08 (§4.10.1 120 hari,
  §4.10.2 62 hari, §4.11 124 hari; nama ACT-019 dan ACT-114 berbeda antartabel), P-FNE-02 §7.3.1 menulis
  "14 personil" padahal rinciannya 15.
- **Antrian resource hanya terasa di P-FNE-03 dan P-FNE-07** (dan sedikit di P-FNE-02). P-FNE-03 tanpa batasan tim
  selesai hari ke-140, dengan satu tim scrum hari ke-220 (= 44 minggu di dokumen). P-FNE-07 tanpa batasan 108 hari,
  dengan FCFS 128, SPT 132.
- **Anomali penjadwalan di P-FNE-07**: sebagian iterasi selesai lebih cepat dari rencana karena CR mengubah urutan
  antrian. Jadwal rencana dengan aturan antrian belum optimal.
