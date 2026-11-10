# Revisi Dosen — Bimbingan 7 Oktober 2026

> Sumber: rekaman `Oct_7__2_30_PM_.mp3`. Segmen kelompok kita: **2:25–13:00** (presentasi + tanya jawab) dan
> **24:00–58:20** (bimbingan jadwal, resource, antrian, simulasi). Transkrip ulang segmen 23:30–58:20 ada di
> [[transkrip_bimbingan_7okt]].
>
> Koreksi terhadap `HANDOFF-revisi-dosen.md`: kebijakan antrian yang disebut dosen adalah **FCFS atau SPT
> (durasi paling pendek dulu)**, bukan "durasi terlama dulu". Segmen 24–47 sudah dipastikan bimbingan untuk
> kelompok kita.

---

## 1. Tabel Revisi

| No | Tahap | Revisi | Yang dikerjakan | Menit | Status |
|---|---|---|---|---|---|
| 1 | Paper | Perjelas tujuan ("mau ngapain?") | Jelaskan *kenapa* proyek bisa telat (CR, dependensi, keterbatasan resource) dan bagaimana delay merambat antaraktivitas | 4:51–6:18 | Pasti |
| 2 | Paper | Konfirmasi metode | Tanya dosen: simulasi iterasi random **menggantikan** supervised learning, atau hasilnya jadi **label/data** untuk ML | – | Perlu ditanyakan |
| 3 | Data | Ekstraksi bisa dilacak | Kolom sumber (dokumen + bab); data diambil apa adanya dari dokumen; boleh dibantu AI tapi dicek ke sumber; kalau antardokumen beda, diseragamkan | 30:33–32:38 | Pasti |
| 4 | Data | Jadwal aktivitas | Dari PMP: aktivitas/deliverable, durasi (angka + formula, bukan teks), predecessor, prioritas. *Arrival* = deadline predecessor + 1; *deadline* = arrival + durasi | 24:40–26:44, 37:01–38:05 | Pasti |
| 5 | Data | Kolom resource | Contoh dosen: PM, PO, BA, DevOps, Dev…; di PMP-01 §4.6.1 role-nya PM, DevOps, Backend, Frontend, Security, QA. Alokasi orang ke aktivitas ditentukan kelompok | 28:43–29:28, 33:02–33:51 | Pasti |
| 6 | Data | Jadwal per resource / antrian | Ubah sudut pandang dari aktivitas ke resource; kebijakan antrian FCFS atau SPT; dependensi wajib diikuti; opsional import ke aplikasi PM (MS Project dsb.) | 38:06–38:51, 46:12–47:30 | Pasti |
| 7 | Simulasi | CR disimulasikan, bukan dummy | `RAND()` < p → CR; tingkat kesulitan CR **juga di-random**, lalu durasi ditambah (contoh dosen 0,1–0,2 / 0,3 / 0,5); angka dijustifikasi sendiri | 50:01–53:44 | Pasti |
| 8 | Simulasi | Pisahkan jenis delay | Delay karena CR aktivitas sendiri vs delay merambat dari predecessor (rework) | 54:04–55:05 | Pasti |
| 9 | Simulasi | Iterasi | Ulangi N kali (contoh dosen 30; rencana 1000); random baru tiap putaran; data rencana tetap; hasil tiap putaran dicatat | 55:43–56:41 | Pasti |
| 10 | Hasil | Probabilitas keterlambatan | P(telat) = jumlah iterasi telat ÷ N | 55:37–56:05 | Pasti |
| 11 | Hasil | Sebaran | Rata-rata telat, persentil, histogram; penyebab (CR sendiri vs rambatan vs antrian resource); bandingkan antarsubproyek | 56:52–57:03 | Pasti |
| 12 | Diskusi | Pertanyaan terbuka dosen | "Kalau syarat dependensinya tidak diikuti, gimana?" — siapkan jawaban | 47:30 | Perlu dijawab |

**Urutan kerja dari dosen:** coba **satu subproyek dulu** sampai jalan (4 → 5 → 6 → 7–9 → 10–11), baru
diterapkan ke 8 subproyek ([35:48] "satu dulu… kalau tahu cara kerjanya baru nanti semuanya dimasukkan").

### Status pengerjaan (3 November 2026)

| No | Status | Keterangan |
|---|---|---|
| 1 | ❌ Belum | Bahan dari hasil simulasi sudah ada (CR, rambatan, antrian, rantai kritis); belum ditulis ke paper |
| 2 | ❌ Belum | Ditanyakan pada bimbingan berikutnya |
| 3 | ✅ 8 subproyek | `06_simulasi_iterasi/ekstraksi_pmp.py` membaca tabel asli PMP; tiap baris punya kolom sumber & catatan. Dataset lama `dataset_pre02_fne*.csv` belum disentuh (menunggu no. 2) |
| 4–6 | ✅ 8 subproyek | Jadwal aktivitas, resource, antrian FCFS/SPT. Import ke MS Project belum dicoba |
| 7–11 | ✅ 8 subproyek | 1000 iterasi × 2 skenario CR × 2 antrian; ringkasan di `06_simulasi_iterasi/hasil/00_RINGKASAN_SEMUA.md` |
| 12 | ❌ Belum | Model saat ini: dependensi selalu dipatuhi |

---

## 2. Gambaran Besar: Apa yang Berubah

| | Sebelum revisi | Sesudah revisi |
|---|---|---|
| Unit analisis | 26 baris modul (`dataset_pre02_fne_v3.csv`), 1 baris = 1 modul | Jadwal aktivitas **di dalam** tiap subproyek (puluhan aktivitas + dependensi + resource) |
| `Change_Request_Count` | Angka dummy buatan sendiri | Hasil simulasi `RAND()` per aktivitas per iterasi |
| `Status_Delay` | Label turunan dari SPI estimasi | Hasil simulasi: selesai simulasi > selesai rencana |
| Probabilitas | Keluaran model ML (LR/RF/GB/MLP) | Proporsi iterasi yang telat (simulasi iterasi random) — atau tetap ML jika dosen memilih "pelengkap" (revisi 2) |
| Penjelasan "kenapa telat" | Feature importance | Jejak simulasi: CR sendiri, rambatan predecessor, menunggu resource |

Judul tetap cocok: "Prediksi Probabilitas Keterlambatan Proyek **Multi Sumber Daya Terbatas**". Justru
revisi 5–6 (antrian resource) yang membuat bagian "sumber daya terbatas" benar-benar dimodelkan.

---

## 3. Mulai dari Mana: Pilot P-FNE-01

> Status: langkah A–G sudah dibuat untuk P-FNE-01 lalu diterapkan ke 8 subproyek di `06_simulasi_iterasi/`
> (lihat README di folder tersebut). Rincian di bawah adalah rencana awal untuk pilot P-FNE-01.

Semua bahan pilot sudah ada di `MP-datasetRaw/2026 PMP Super ERP Farm Nation Enterprise Foundation & Core Platform.docx`.

| Langkah | Ambil dari (PMP-01) | Hasil yang dibuat | Tujuannya |
|---|---|---|---|
| **A. Jadwal aktivitas** (rev. 3–4) | §4.2.1 *High-Level Activities by Phase* — tabel Fase / Aktivitas / Durasi (minggu) / Dependensi. Validasi dengan §4.2.3 *Critical Path Analysis* (ES/EF/LS/LF) | Sheet `jadwal_aktivitas`: ID, aktivitas, fase, durasi (hari = minggu × 5 hari kerja), predecessor (ID), prioritas, **kolom sumber** (dokumen + §) | Jadwal **rencana** = patokan. "Telat" artinya selesai simulasi melewati selesai rencana ini |
| **B. Prioritas** (rev. 4) | §3.3.2 *Features by Priority (MoSCoW)*; backlog/sprint di §2.3.2 | Kolom `prioritas` di sheet jadwal | Penentu urutan kerja ketika beberapa aktivitas antre di resource yang sama |
| **C. Resource** (rev. 5) | §4.6.1 *Resource Requirements by Role* — jumlah orang per role per bulan (PM, DevOps, Backend, Frontend, Security, QA, …); §4.6.3 *Resource Leveling* | Sheet `resource`: daftar orang (PM, DevOps1–3, BE1–5, …) + kolom PIC per aktivitas. Aturan alokasi dicatat sebagai keputusan kelompok | Membuat beban kerja tiap orang terlihat; ini sumber delay karena **sumber daya terbatas** |
| **D. Jadwal per resource / antrian** (rev. 6) | Hasil A + C | Sheet `jadwal_resource`: per orang, urutan aktivitas yang dikerjakan; kebijakan FCFS atau SPT; aktivitas baru boleh mulai jika predecessor selesai **dan** orangnya kosong | Aktivitas bisa menunggu resource walau predecessor sudah selesai, sehingga delay antrian ikut terhitung |
| **E. Simulasi CR** (rev. 7–8) | §2.5 *Integrated Change Control*: klasifikasi perubahan **kecil ≤ 5%**, **sedang ≤ 20%**, **besar > 20%** impact | Kolom per aktivitas: `rand_CR`, `CR?`, `rand_kesulitan`, `tambahan_%`, `durasi_aktual`, `delay_sendiri`, `delay_rambatan` | Sumber ketidakpastian. Rentang tambahan durasi bisa dijustifikasi dari kelas di §2.5, bukan sekadar angka contoh dosen |
| **F. Iterasi** (rev. 9) | – | Sheet `iterasi`: 1 baris = 1 putaran (N = 1000): tanggal selesai subproyek, telat ya/tidak, berapa hari, jumlah CR | Mengubah satu skenario acak menjadi **sebaran** hasil |
| **G. Hasil** (rev. 10–11) | – | P(telat), rata-rata & persentil keterlambatan, histogram, porsi penyebab | Jawaban utama penelitian + bahan revisi 1 ("kenapa telat") |

### Keputusan yang harus ditetapkan kelompok (dan ditulis justifikasinya di Bab III)

| Parameter | Usulan awal | Dasar justifikasi |
|---|---|---|
| Peluang CR per aktivitas (p) | 0,1 (contoh dosen) atau dibedakan per aktivitas memakai `Risk_Score` | Asumsi/literatur; sebutkan sebagai asumsi |
| Peluang tiap kelas kesulitan CR | misal kecil 60% / sedang 30% / besar 10% | Asumsi; uji sensitivitas |
| Tambahan durasi per kelas | kecil 0–5%, sedang 5–20%, besar 20–50% | Kelas *impact* di PMP-01 §2.5 (batas atas "besar" ditetapkan sendiri) |
| Kebijakan antrian | FCFS (utama), SPT (pembanding) | Disebut dosen [46:44–47:04] |
| Jumlah iterasi N | 1000 | Estimasi probabilitas stabil (galat baku maksimum ±1,6% vs ±9% pada N = 30) |
| Satuan waktu | hari kerja (1 minggu = 5 hari) | Durasi PMP dalam minggu |

### Alat

- **Excel/Sheets untuk pilot P-FNE-01.** Ini yang dicontohkan dosen (`RAND()`, `IF`, rumus *arrival/deadline*
  ditarik ke bawah). Iterasi 1000 kali memakai *Data Table* (What-If Analysis) dengan sel input kosong.
- **Python** setelah logika pilot disepakati, untuk 8 subproyek × 1000 iterasi dan grafik. Hasil Python harus
  dicocokkan dulu dengan Excel pada P-FNE-01.

---

## 4. Dampak ke Berkas yang Sudah Ada

| Berkas | Tindakan |
|---|---|
| `dataset_pre02_fne_v3.csv` | Jangan dihapus. Statusnya menunggu revisi 2; kemungkinan menjadi data level modul/pelengkap |
| `04_implemen_desain_eksperimen/experiment_pipeline.py` | Ditahan sampai revisi 2 dijawab. Jika ML jadi pelengkap, label `Status_Delay` diganti hasil simulasi |
| `04_implemen_desain_eksperimen/02_Draft_Metodologi_Eksperimen_Bab3.md` | §3.1 alur penelitian, §3.2 sumber data (tambah jadwal aktivitas & resource), §3.3 variabel (CR jadi variabel simulasi), §3.4 desain eksperimen (tambah simulasi iterasi random) |
| `catatan_dosen/Penjelasan_Variabel_Dataset.md`, `sumber_data_variabel.md` | Tambahkan sumber untuk jadwal aktivitas, resource, dan parameter simulasi |
| Bab I / pendahuluan | Revisi 1: kenapa proyek telat + mekanisme rambatan |

---

## 5. Untuk Ditanyakan di Bimbingan Berikutnya

1. Simulasi iterasi random menggantikan ML, atau hasil simulasi dipakai sebagai data/label ML?
2. Unit probabilitas: per subproyek saja, atau juga per aktivitas?
3. Apakah boleh memakai kelas *impact* di PMP §2.5 sebagai dasar tambahan durasi CR?
4. Jawaban kelompok untuk pertanyaan dosen [47:30]: jika syarat dependensi tidak diikuti (aktivitas mulai sebelum predecessor selesai), bagaimana memodelkannya — dilarang, atau diizinkan dengan penalti *rework*?
