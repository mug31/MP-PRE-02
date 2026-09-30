# Peta Sumber Data Variabel Dataset PRE-02
## Panduan Rujukan Cepat untuk Presentasi & Tanya-Jawab Dosen

> **Berkas dataset:** `dataset_pre02_fne_v3.csv` (26 baris × 11 kolom)  
> **Proyek:** Super ERP Farm Nation Enterprise (FNE) 2026  
> **Folder dokumen mentah:** `MP-datasetRaw/` (18 dokumen `.docx`)

---

## BAGIAN A — Daftar 18 Dokumen Sumber

| No | Kode Singkat | Nama File di `MP-datasetRaw/` | Isi Utama |
|:--:|:-------------|:-----------------------------|:----------|
| 1 | **KAK** | `2026 KAK Proyek Farm Nation Enterprise.docx` | Kerangka Acuan Kerja — ruang lingkup 12 fase, 15 *milestone gates* |
| 2 | **Pemetaan** | `2026 Pemetaan Proyek Pengembangan ERP Farm Nation Enterprise.docx` | Pemecahan ke 8 sub-proyek, kode `P-FNE-01`…`08`, matriks ketergantungan |
| 3 | **PMP-01** | `2026 PMP Super ERP Farm Nation Enterprise Foundation & Core Platform.docx` | PMP sub-proyek P-FNE-01 |
| 4 | **PMP-02** | `2026 PMP Super ERP Farm Nation Enterprise Core Agricultural Operatios.docx` | PMP sub-proyek P-FNE-02 |
| 5 | **PMP-03** | `2026 PMP Super ERP Farm Nation Enterprise Supply Chain & Procurement.docx` | PMP sub-proyek P-FNE-03 |
| 6 | **PMP-04** | `2026 PMP Super ERP Farm Nation Enterprise Production & Manufacturing.docx` | PMP sub-proyek P-FNE-04 |
| 7 | **PMP-05** | `2026 PMP Super ERP Farm Nation Enterprise Commerce Sales & Logistic.docx` | PMP sub-proyek P-FNE-05 |
| 8 | **PMP-06** | `2026 PMP Super ERP Farm Nation Enterprise Finance & HCM.docx` | PMP sub-proyek P-FNE-06 |
| 9 | **PMP-07** | `2026 PMP Super ERP Farm Nation Enterprise Intelligence & Decision Platform.docx` | PMP sub-proyek P-FNE-07 |
| 10 | **PMP-08** | `2026 PMP Super ERP Farm Nation Enterprise Advanced & Autonomous Enterprise.docx` | PMP sub-proyek P-FNE-08 |
| 11 | **SRS-01** | `2026 SRS Super ERP Farm Nation Enterprise FOUNDATION & CORE PLATFORM.docx` | SRS sub-proyek P-FNE-01 |
| 12 | **SRS-02** | `2026 SRS Super ERP Farm Nation Enterprise Core Agricultural Operations.docx` | SRS sub-proyek P-FNE-02 |
| 13 | **SRS-03** | `2026 SRS Super ERP Farm Nation Enterprise Supply Chain & Procurement.docx` | SRS sub-proyek P-FNE-03 |
| 14 | **SRS-04** | `2026 SRS Super ERP Farm Nation Enterprise PRODUCTION & MANUFACTURING.docx` | SRS sub-proyek P-FNE-04 |
| 15 | **SRS-05** | `2026 SRS Super ERP Farm Nation Enterprise Commerce Sales & Logistic.docx` | SRS sub-proyek P-FNE-05 |
| 16 | **SRS-06** | `2026 SRS Super ERP Farm Nation Enterprise Finance & HCM.docx` | SRS sub-proyek P-FNE-06 |
| 17 | **SRS-07** | `2026 SRS Super ERP Farm Nation Enterprise Intelligence & Decision Platform.docx` | SRS sub-proyek P-FNE-07 |
| 18 | **SRS-08** | `2026 SRS Super ERP Farm Nation Enterprise Advanced & Autonomous Enterprise.docx` | SRS sub-proyek P-FNE-08 |

---

## BAGIAN B — Peta Variabel → Dokumen & Bagian Spesifik

### Tabel Ringkasan: Setiap Kolom Dataset Berasal dari Mana

| Kolom Dataset | Dokumen Sumber | Bab / Bagian yang Dirujuk | Nomor Tabel Spesifik di PMP | Cara Memperoleh Nilai | Status Data |
|:---|:---|:---|:---|:---|:---:|
| `Task_ID` | — | — | — | Penomoran urut peneliti (ACT-001 s.d. ACT-026) | Metadata |
| `Sub_Project` | **Pemetaan** | Tabel *Usulan Pemecahan Proyek* | Pemetaan: Tabel 0 (ID Proyek, Nama Proyek, Modul Utama) | Diambil langsung: kode sub-proyek P-FNE-01…08 | ✅ Terdokumentasi |
| `Task_Name` | **PMP-01…08** + **SRS-01…08** | **Bab 3 PMP** — Sub-bab 3.3 *Create WBS*; **Bab 4** — Sub-bab 4.4 *Define Activities* | PMP-01: Tabel 35, 48; PMP-05: Tabel 109; PMP-08: Tabel 88 | Nama modul dari WBS level 2/3 | ✅ Terdokumentasi |
| `Planned_Duration_Days` | **PMP-01…08** | **Bab 4 PMP** — Sub-bab 4.6 *Estimate Activity Durations* & 4.7 *Develop Schedule* | PMP-01: **Tabel 51** (*Sprint Schedule*); PMP-02: **Tabel 60**; PMP-03: **Tabel 76**; PMP-05: **Tabel 117** (122 baris); PMP-07: **Tabel 11**, 57–59; PMP-08: **Tabel 95**, 97 | Konversi sesuai satuan PMP *(lihat Bagian C)* | ⚠️ 18 terdokumentasi; 8 estimasi ahli |
| `Planned_Effort_Hours` | **PMP-01…08** | **Bab 7 PMP** — Sub-bab 7.4 *Staffing Management Plan*; **Bab 5** — *Activity-Based Costing* | PMP-01: Tabel 63 (tarif 8 jam/hari); PMP-02: Tabel 76 (8 jam/hari) | **Rumus:** `Effort = Durasi × 8 jam × 1.0 FTE` | 🔧 Turunan |
| `Predecessor_Count` | **Pemetaan** + **PMP-01…08** | **Pemetaan:** Kolom *Ketergantungan*; **Bab 4 PMP** — Sub-bab 4.5 *Sequence Activities* | Pemetaan: kolom Dependency; PMP-01: **Tabel 48** (kolom *Dependensi*); PMP-02: **Tabel 60** (kolom *Predecessor*); PMP-05: **Tabel 113**; PMP-07: Tabel 57–59 | Hitung jumlah dependensi *finish-to-start* | ⚠️ Level sub-proyek terdokumentasi; internal estimasi ahli |
| `Resource_Utilization_Rate` | **PMP-08** (rumus acuan) + semua PMP | **Bab 7 PMP** — Sub-bab 7.4.3 *Resource Utilization Plan* | PMP-08: **Tabel 153** (alokasi M1–M5, basis 160 jam/bulan); PMP-06: **Tabel 167** (target utilisasi 85%); PMP-02: Tabel 138; PMP-01: Tabel 55–56 | **Rumus:** `U = Jam Kerja / 160` | ⚠️ Rumus terdokumentasi; nilai estimasi ahli |
| `Risk_Score` | **PMP-01…08** | **Bab 9 PMP** — Sub-bab 9.3–9.4 *Risk Analysis & Prioritization*; **Lampiran E** | PMP-08: **Tabel 189** (R-001 IoT=0.48, R-003 Sim=0.50, R-005 ERP=0.36); PMP-02: Tabel 165 (R-010 Mobile Sync); PMP-01: Lampiran E Tabel 185/200+ | **Rumus:** `R = (P/5) × (I/5)` → [0, 1] | ⚠️ Rumus terdokumentasi; nilai estimasi ahli |
| `SPI_Value` | **PMP-01…08** | **Bab 4 PMP** — Sub-bab 4.8 *Schedule Control Thresholds*; **Bab 5** — *EVM Metrics* | PMP-08: **Tabel 103** (SPI Range & Tindakan), **Tabel 128** (formula SPI=EV/PV); PMP-01: **Tabel 57** (EVM Target), **Tabel 96** (PV vs AC vs EV); PMP-05: Tabel 43 | **Rumus:** `SPI = EV / PV` | ⚠️ Rumus terdokumentasi; nilai estimasi ahli |
| `Change_Request_Count` | **PMP-01…08** | **Bab 13 PMP** (atau Bab 2) — *Change Control Process & CCB*; **Lampiran J/D** | PMP-01: **Tabel 22** (CRF Template), **Tabel 23** (Komposisi CCB), **Tabel 25** (Change Log); PMP-05: Tabel 47–48; PMP-07: Tabel 29–30; PMP-08: Tabel 42, 46 | Jumlah CR yang disetujui CCB | ⚠️ Proses terdokumentasi; jumlah estimasi ahli |
| `Status_Delay` | Diturunkan dari `SPI_Value` | **Bab 4 PMP** — Sub-bab 4.8 *Schedule Control & Thresholds* | Sama dengan SPI_Value di atas | **Aturan:** `1` jika `SPI ≤ 0.90`; `0` jika `SPI > 0.90` | 🔧 Turunan |

**Legenda Status:**
- ✅ **Terdokumentasi** — nilainya dapat ditunjuk langsung pada halaman/tabel dokumen sumber
- 🔧 **Turunan** — dihitung dengan rumus standar dari nilai terdokumentasi
- ⚠️ **Estimasi Ahli** — rumus/prosedur dari dokumen, nilai per aktivitas ditetapkan peneliti (*expert judgment* — metode yang diakui PMBOK dan dipakai oleh PMP FNE sendiri)

> **Mengapa ada estimasi ahli?** Proyek FNE 2026 masih pada tahap **perencanaan (pra-eksekusi)**. Buktinya: tabel *Velocity Planning* di PMP P-FNE-01 menunjukkan kolom *Planned Velocity* terisi, tetapi kolom *Actual Velocity* masih kosong. Dokumen PMP menetapkan *bagaimana* SPI, utilisasi, dan CR akan dipantau (lengkap rumus, ambang, periodisasi), tetapi **belum memuat hasil pemantauannya**.

---

## BAGIAN C — Peta Durasi: Setiap Aktivitas Ditelusuri ke Sprint/Fase PMP

### Konvensi Konversi Satuan Waktu (dari PMP P-FNE-06)

```
1 sprint  = 2 minggu  = 10 hari kerja
1 minggu  = 5 hari kerja
1 hari    = 8 jam kerja (1.0 FTE)
```

### Tiga Jalur Konversi Durasi

| Jalur | Satuan di PMP | Sub-Proyek yang Memakai | Rumus Konversi |
|:-----:|:--------------|:------------------------|:---------------|
| **A** | Sprint | P-FNE-01, P-FNE-03, P-FNE-04 | `D = jumlah_sprint × 10 hari` |
| **B** | Fase / Minggu | P-FNE-02, P-FNE-06, P-FNE-07 | `D = jumlah_minggu × 5 hari` |
| **C** | Hari (langsung) | P-FNE-05 | `D = Σ durasi aktivitas dalam blok modul` |

> **Catatan P-FNE-08:** PMP hanya memuat estimasi *effort* per aktivitas dalam jam (PERT tiga titik), tanpa durasi kalender → durasi 3 modulnya ditetapkan lewat estimasi ahli.

### Tabel Penelusuran Per Aktivitas

| Task_ID | Task_Name | Sub-Proyek | Durasi (hari) | Jalur | WBS & Sumber Spesifik di PMP (Bab, Tabel) | Status |
|:--------|:----------|:----------:|:---:|:---:|:---|:---:|
| ACT-001 | Infrastructure & K8s Cluster Setup | P-FNE-01 | 5 | A | **WBS 1.1**; PMP-01, **Bab 4 Tabel 51**: Sprint 0 = 1 minggu (5 hari) | ✅ |
| ACT-002 | IAM & SSO Implementation | P-FNE-01 | 20 | A | **WBS 1.2**; PMP-01, **Bab 4 Tabel 51**: Sprint 1 (*Auth & MFA*) + Sprint 2 (*RBAC & SSO*) = 2 sprint × 10 | ✅ |
| ACT-003 | Master Data Management (MDM) 24 Entities | P-FNE-01 | 20 | A | **WBS 1.3**; PMP-01, **Bab 4 Tabel 51**: Sprint 3 (*Schema & Core*) + Sprint 4 (*Advanced & Import/Export*) = 2 sprint × 10 | ✅ |
| ACT-004 | API Gateway & Kafka Event Bus Setup | P-FNE-01 | 10 | A | **WBS 1.5 + 1.6**; PMP-01, **Bab 4 Tabel 51**: Sprint 6 (*API Gateway & Event Bus*) = 1 sprint × 10 | ✅ |
| ACT-005 | Farm & Land Parcel Registration API | P-FNE-02 | 15 | B | **WBS 3.1**; PMP-02, **Bab 3 WBS 3.1** & **Bab 4**: Durasi fase makro; modul individual → estimasi ahli (3 minggu) | ⚠️ |
| ACT-006 | Crop Cycle Planning & Tracking Service | P-FNE-02 | 20 | B | **WBS 3.2.2**; PMP-02, **Bab 3 WBS 3.2.2**: Durasi fase makro; modul individual → estimasi ahli (4 minggu) | ⚠️ |
| ACT-007 | Harvest & Batch Quality Management | P-FNE-02 | 15 | B | **WBS 3.3**; PMP-02, **Bab 3 WBS 3.3**: Durasi fase makro; modul individual → estimasi ahli (3 minggu) | ⚠️ |
| ACT-008 | Mobile Offline Sync Engine | P-FNE-02 | 10 | B | **WBS 4.1–4.3**; PMP-02, **Bab 4 Tabel 60**: Fase *Mobile Development (Parallel)* = 10 hari | ✅ |
| ACT-009 | Supplier Portal & Performance Scorecard | P-FNE-03 | 10 | A | **Modul Supplier Mgmt**; PMP-03, **Bab 4 Tabel 76**: Sprint 3 = 1 sprint × 10 | ✅ |
| ACT-010 | Procurement & Purchase Order Workflow | P-FNE-03 | 30 | A | **Modul Procurement**; PMP-03, **Bab 4 Tabel 76**: Sprint 4–6 (*Procurement I + II + PO*) = 3 sprint × 10 | ✅ |
| ACT-011 | Inventory & Warehouse Multi-Location API | P-FNE-03 | 60 | A | **Modul Inventory+WH**; PMP-03, **Bab 4 Tabel 76**: Sprint 7–12 (*Inv I/II + WH I/II + Stock + Integration*) = 6 sprint × 10 | ✅ |
| ACT-012 | Production Planning & Multi-Level BOM Engine | P-FNE-04 | 20 | A | **WBS 2.1–2.2** (BOM & Prod Planning); PMP-04, **Bab 3 Sub-bab 3.4.1–3.4.2** & **Bab 4**: Sprint S1–S2 = 2 sprint × 10 | ✅ |
| ACT-013 | MRP Computation Engine | P-FNE-04 | 15 | A | **WBS 2.2.2** (MRP); PMP-04, **Bab 3**: Durasi tingkat WBS; modul individual → estimasi ahli (1.5 sprint ≈ 15 hari) | ⚠️ |
| ACT-014 | Production Costing & Asset Maintenance | P-FNE-04 | 30 | A | **WBS 2.5 + 2.6**; PMP-04, **Bab 3 Sub-bab 3.4.4–3.4.5** & **Bab 4**: Sprint S3–S5 = 3 sprint × 10 | ✅ |
| ACT-015 | Sales Order CRUD & Validation API | P-FNE-05 | 14 | C | **Blok Sales Order**; PMP-05, **Bab 4 Tabel 117**: ACT-019…024 internal = 3+2+2+2+3+2 = **14** | ✅ |
| ACT-016 | Customer 360 View & CRM Integration | P-FNE-05 | 32 | C | **Blok CRM**; PMP-05, **Bab 4 Tabel 117**: ACT-035…047 internal = 3+2+2+2+2+2+2+3+2+2+5+2+3 = **32** | ✅ |
| ACT-017 | Real-time Shipment & Logistics Tracking | P-FNE-05 | 36 | C | **Blok Logistics**; PMP-05, **Bab 4 Tabel 117**: ACT-065…077 internal = 3+2+3+3+3+2+2+2+3+5+2+3+3 = **36** | ✅ |
| ACT-018 | General Ledger & Auto Journal Ingestion | P-FNE-06 | 20 | B | **WBS 1.0 GL** (Sub-bab 3.2.2); PMP-06, **Bab 4 Tabel 28**: Sprint 3 Backend; Fase GL = 4 minggu × 5 | ✅ |
| ACT-019 | Accounts Payable Three-Way Matching | P-FNE-06 | 15 | B | **WBS 2.0 AP** (Sub-bab 3.3.2); PMP-06, **Bab 4 Tabel 28 & 57**: Sprint 4; modul AP → estimasi ahli (3 minggu) | ⚠️ |
| ACT-020 | Payroll Engine & HCM Attendance Sync | P-FNE-06 | 20 | B | **WBS 3.8.6 Payroll**; PMP-06, **Bab 4 Tabel 29**: Sprint 7–8 HCM = 4 minggu × 5 | ✅ |
| ACT-021 | Data Lake & Warehouse CDC Ingestion Pipeline | P-FNE-07 | 20 | B | **Fase 2: Data Platform**; PMP-07, **Bab 4 Tabel 11 & 57**: Fase 2 = 4 minggu × 5 | ✅ |
| ACT-022 | Executive BI Dashboard & KPI Alerting | P-FNE-07 | 20 | B | **Fase 3: BI & KPI**; PMP-07, **Bab 4 Tabel 11 & 58**: Fase 3 = 4 minggu × 5 | ✅ |
| ACT-023 | AI Demand & Crop Yield Forecasting Service | P-FNE-07 | 20 | B | **Fase 4: AI/ML**; PMP-07, **Bab 4 Tabel 11 & 59**: Fase 4 = 4 minggu × 5 | ✅ |
| ACT-024 | IoT Telemetry Streaming & Threshold Alerting | P-FNE-08 | 20 | — | **WBS 2.0 IoT**; PMP-08, **Bab 4 Tabel 95 & 115**: Sprint 3–4; hanya effort PERT → estimasi ahli durasi | ⚠️ |
| ACT-025 | Digital Twin Farm & Machine State Sync | P-FNE-08 | 20 | — | **WBS 3.0 Digital Twin**; PMP-08, **Bab 4 Tabel 95 & 116**: Sprint 5–6; hanya effort PERT → estimasi ahli durasi | ⚠️ |
| ACT-026 | What-If Simulation Engine & Autonomous Recommendation | P-FNE-08 | 25 | — | **WBS 4.0 + 5.0 Simulation**; PMP-08, **Bab 4 Tabel 95, 117–118**: Sprint 7–9; hanya effort PERT → estimasi ahli durasi | ⚠️ |

**Ringkasan:** 18 dari 26 aktivitas durasinya ✅ terdokumentasi langsung; 8 aktivitas ⚠️ estimasi ahli.

> **⚠️ Peringatan Penamaan:** PMP P-FNE-05 dan P-FNE-08 memakai kode `ACT-xxx` untuk aktivitas internal mereka sendiri. Kode tersebut **TIDAK SAMA** dengan `Task_ID` pada dataset ini. Contoh: `ACT-015` pada PMP P-FNE-05 adalah *Security Architecture*, sedangkan `ACT-015` pada dataset adalah *Sales Order CRUD & Validation API*.

---

## BAGIAN D — Peta Variabel Monitoring: Rumus & Lokasi di PMP

### D1. `Resource_Utilization_Rate` — Tingkat Utilisasi Sumber Daya

| Aspek | Detail |
|:------|:-------|
| **Rumus** | `U = Jam Kerja Efektif / Kapasitas Standar (160 jam/bulan)` |
| **Lokasi rumus** | **Bab 7 PMP-08** — Tabel *Resource Utilization Plan* (1 FTE = 160 jam/bulan) |
| **Arti nilai** | `U = 1.00` → beban 100% normal; `U > 1.00` → *over-allocation/overload*; `U < 1.00` → beban longgar |
| **Mengapa bisa > 1.0?** | Setiap PMP hanya mencatat alokasi di dalam sub-proyeknya sendiri. Developer yang sama menangani beberapa sub-proyek paralel (*shared developer*) → utilisasi gabungan lintas sub-proyek tidak tercatat di dokumen mana pun. Nilai > 1.0 merepresentasikan fenomena ini. |
| **Contoh** | ACT-002 (IAM): developer dialokasikan 176 jam/bulan → `U = 176/160 = 1.10` |

**📍 Buka:** PMP masing-masing sub-proyek → **Bab 7** → cari tabel *Resource Utilization Plan* atau *Staffing Management Plan*

---

### D2. `Risk_Score` — Skor Risiko Inheren

| Aspek | Detail |
|:------|:-------|
| **Rumus** | `R = (P/5) × (I/5)` — P = Probability, I = Impact; skala Likert 1–5 |
| **Lokasi rumus** | **Bab 9 PMP** atau **Lampiran E** — *Risk Register* dan *Probability–Impact Matrix* |
| **Rentang** | [0.04, 1.00] secara teori; dataset: [0.18, 0.50] |
| **Contoh** | ACT-002 (IAM): P = 3, I = 3 → `R = (3/5) × (3/5) = 0.6 × 0.6 = 0.36` |

**📍 Buka:** PMP masing-masing sub-proyek → **Bab 9 / Lampiran E** → cari tabel *Risk Register* (kolom Probability, Impact, Score)

---

### D3. `SPI_Value` — Schedule Performance Index

| Aspek | Detail |
|:------|:-------|
| **Rumus** | `SPI = EV / PV` (Earned Value / Planned Value) |
| **Lokasi rumus** | **Bab 4 PMP** — Standar EVM (*Earned Value Management*); **Bab 7 PMP** — ambang peringatan SPI ≥ 0.8 |
| **Arti** | SPI < 1.0 = progres di belakang jadwal; SPI = 1.0 = tepat rencana |
| **Ambang delay** | `SPI ≤ 0.90` → Status_Delay = 1 (terlambat) |
| **Contoh** | ACT-002 (IAM): EV = 88, PV = 100 → `SPI = 88/100 = 0.88` → terlambat |

**📍 Buka:** PMP masing-masing sub-proyek → **Bab 4** → cari bagian *Earned Value Management*, *Performance Measurement Baseline*, atau *Schedule Control*

---

### D4. `Change_Request_Count` — Jumlah Usulan Perubahan

| Aspek | Detail |
|:------|:-------|
| **Definisi** | Jumlah *change request* lingkup yang disetujui oleh CCB (*Change Control Board*) |
| **Lokasi prosedur** | **Bab 3 & Bab 4 PMP** — Prosedur *Change Management*, Formulir CR, Alur Persetujuan CCB |
| **Rentang dataset** | 0 s.d. 4 usulan per modul |
| **Contoh** | ACT-004 (API Gateway & Kafka): 3 CR disetujui CCB — mencerminkan penyesuaian spesifikasi integrasi |

**📍 Buka:** PMP masing-masing sub-proyek → **Bab 3** (*Scope Management*) dan **Bab 4** (*Schedule Management*) → cari bagian *Change Control Process* atau *Change Request Procedure*

---

### D5. `Predecessor_Count` — Jumlah Dependensi Pendahulu

| Aspek | Detail |
|:------|:-------|
| **Definisi** | Jumlah modul/sub-proyek prasyarat langsung (*finish-to-start*) |
| **Lokasi** | **Pemetaan:** Kolom *Ketergantungan* antar sub-proyek; **Bab 4 PMP:** *Activity Sequencing* |
| **Contoh** | ACT-021 (Data Lake, P-FNE-07): Pemetaan mencatat P-FNE-07 bergantung pada P-FNE-02, 03, 04, 05, dan 06 → `Predecessor_Count = 5` |

**📍 Buka:** Dokumen *Pemetaan Proyek* → Tabel *Usulan Pemecahan* → kolom *Ketergantungan*; lalu PMP terkait → **Bab 4** → *Activity Sequencing* / *Network Diagram*

---

## BAGIAN E — Peta Sub-Proyek → Dokumen → Aktivitas

Tabel ini memudahkan mencari **aktivitas mana dibaca dari dokumen mana**.

### P-FNE-01: Foundation & Core Platform
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-01** `2026 PMP...Foundation & Core Platform.docx` | **SRS-01** `2026 SRS...FOUNDATION & CORE PLATFORM.docx` | ACT-001 Infrastructure & K8s Cluster Setup |
| | | ACT-002 IAM & SSO Implementation |
| | | ACT-003 Master Data Management (MDM) 24 Entities |
| | | ACT-004 API Gateway & Kafka Event Bus Setup |

- **Durasi:** Bab 4 PMP-01 → tabel Sprint Schedule (Sprint 0–5)
- **WBS/Nama:** Bab 3 PMP-01 → Struktur WBS; SRS-01 → Daftar Modul
- **Risk:** Bab 9 PMP-01 → Risk Register
- **Resource:** Bab 7 PMP-01 → Resource Utilization Plan
- **Bukti pra-eksekusi:** Tabel *Velocity Planning* → *Actual Velocity* kosong

---

### P-FNE-02: Core Agricultural Operations
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-02** `2026 PMP...Core Agricultural Operatios.docx` | **SRS-02** `2026 SRS...Core Agricultural Operations.docx` | ACT-005 Farm & Land Parcel Registration API |
| | | ACT-006 Crop Cycle Planning & Tracking Service |
| | | ACT-007 Harvest & Batch Quality Management |
| | | ACT-008 Mobile Offline Sync Engine |

- **Durasi:** Bab 4 PMP-02 → fase/milestone dalam minggu (Jalur B); ACT-008 = 10 hari (Fase *Mobile Development Parallel*)
- **WBS/Nama:** Bab 3 PMP-02; SRS-02

---

### P-FNE-03: Supply Chain & Procurement
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-03** `2026 PMP...Supply Chain & Procurement.docx` | **SRS-03** `2026 SRS...Supply Chain & Procurement.docx` | ACT-009 Supplier Portal & Performance Scorecard |
| | | ACT-010 Procurement & Purchase Order Workflow |
| | | ACT-011 Inventory & Warehouse Multi-Location API |

- **Durasi:** Bab 4 PMP-03 → Sprint Schedule (Jalur A): Sprint 3 (Supplier), Sprint 4–6 (Procurement), Sprint 7–12 (Inventory+Warehouse)
- **WBS/Nama:** Bab 3 PMP-03; SRS-03

---

### P-FNE-04: Production & Manufacturing
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-04** `2026 PMP...Production & Manufacturing.docx` | **SRS-04** `2026 SRS...PRODUCTION & MANUFACTURING.docx` | ACT-012 Production Planning & Multi-Level BOM Engine |
| | | ACT-013 MRP Computation Engine |
| | | ACT-014 Production Costing & Asset Maintenance |

- **Durasi:** Bab 3–4 PMP-04 → WBS 2.1–2.2 (Sprint S1–S2 = 20 hari), WBS 2.5+2.6 (Sprint S3–S5 = 30 hari)
- **WBS/Nama:** Bab 3 PMP-04; SRS-04

---

### P-FNE-05: Commerce, Sales & Logistics
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-05** `2026 PMP...Commerce Sales & Logistic.docx` | **SRS-05** `2026 SRS...Commerce Sales & Logistic.docx` | ACT-015 Sales Order CRUD & Validation API |
| | | ACT-016 Customer 360 View & CRM Integration |
| | | ACT-017 Real-time Shipment & Logistics Tracking |

- **Durasi:** Bab 4 PMP-05 → Tabel *Activity Duration Estimates* (122 aktivitas internal, Jalur C)
  - ACT-015 = blok Sales Order (ACT-019…024 internal PMP) → Σ = 14 hari
  - ACT-016 = blok CRM (ACT-035…047 internal PMP) → Σ = 32 hari
  - ACT-017 = blok Logistics (ACT-065…077 internal PMP) → Σ = 36 hari

---

### P-FNE-06: Finance & HCM
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-06** `2026 PMP...Finance & HCM.docx` | **SRS-06** `2026 SRS...Finance & HCM.docx` | ACT-018 General Ledger & Auto Journal Ingestion |
| | | ACT-019 Accounts Payable Three-Way Matching |
| | | ACT-020 Payroll Engine & HCM Attendance Sync |

- **Durasi:** Bab 4 PMP-06 → fase dalam minggu (Jalur B); GL = 4 minggu, Payroll = 4 minggu
- **Konvensi waktu:** PMP-06 menetapkan **1 sprint = 2 minggu = 10 hari kerja** (menjadi acuan seluruh dataset)

---

### P-FNE-07: Intelligence & Decision Platform
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-07** `2026 PMP...Intelligence & Decision Platform.docx` | **SRS-07** `2026 SRS...Intelligence & Decision Platform.docx` | ACT-021 Data Lake & Warehouse CDC Ingestion Pipeline |
| | | ACT-022 Executive BI Dashboard & KPI Alerting |
| | | ACT-023 AI Demand & Crop Yield Forecasting Service |

- **Durasi:** Bab 4 PMP-07 → fase dalam minggu (Jalur B): Fase 2 (CDC) = 4 minggu, Fase 3 (BI) = 4 minggu, Fase 4 (AI) = 4 minggu → masing-masing 20 hari
- **Predecessor_Count = 5:** Pemetaan mencatat P-FNE-07 bergantung pada 5 sub-proyek lain (P-FNE-02, 03, 04, 05, 06)

---

### P-FNE-08: Advanced & Autonomous Enterprise
| Dokumen PMP | Dokumen SRS | Aktivitas Dataset |
|:---|:---|:---|
| **PMP-08** `2026 PMP...Advanced & Autonomous Enterprise.docx` | **SRS-08** `2026 SRS...Advanced & Autonomous Enterprise.docx` | ACT-024 IoT Telemetry Streaming & Threshold Alerting |
| | | ACT-025 Digital Twin Farm & Machine State Sync |
| | | ACT-026 What-If Simulation Engine & Autonomous Recommendation |

- **Durasi:** PMP-08 hanya memuat estimasi effort dalam jam (PERT), tanpa durasi kalender → **seluruh 3 modul = estimasi ahli**
- **Resource:** Bab 7 PMP-08 → Tabel *Resource Utilization Plan* menjadi referensi utama rumus utilisasi (1 FTE = 160 jam/bulan)

---

## BAGIAN F — Riwayat Revisi Dataset (v1 → v2 → v3)

| Versi | Status | Perubahan dari Versi Sebelumnya |
|:------|:------:|:-------------------------------|
| `dataset_pre02_fne_v1_arsip.csv` | Arsip | Rasio effort/durasi tidak konsisten (6.67–9.0 jam/hari) |
| `dataset_pre02_fne_v2.csv` | Arsip | Identik dengan v1; disimpan sebagai pembanding |
| **`dataset_pre02_fne_v3.csv`** | **✅ Aktif** | 11 durasi disinkronisasi ulang ke PMP; effort distandarisasi `D × 8 jam` |

### Detail 11 Baris yang Direvisi pada v3

| Task | Durasi Lama → Baru | Dasar Penelusuran ke PMP |
|:-----|:---:|:---|
| ACT-001 | 10 → **5** | PMP-01, Sprint 0 = 1 minggu |
| ACT-008 | 15 → **10** | PMP-02, fase Mobile Development (Parallel) = 10 hari |
| ACT-009 | 15 → **10** | PMP-03, Sprint 3 (Supplier Management) |
| ACT-010 | 25 → **30** | PMP-03, Sprint 4–6 (Procurement I + II) |
| ACT-011 | 25 → **60** | PMP-03, Sprint 7–12 (Inventory I/II + Warehouse I/II) |
| ACT-014 | 15 → **30** | PMP-04, WBS 2.5 + 2.6 (Sprint S3–S5) |
| ACT-015 | 15 → **14** | PMP-05, blok aktivitas ACT-019…024 internal |
| ACT-016 | 15 → **32** | PMP-05, blok aktivitas ACT-035…047 internal |
| ACT-017 | 20 → **36** | PMP-05, blok aktivitas ACT-065…077 internal |
| ACT-021 | 25 → **20** | PMP-07, Fase 2 = 4 minggu |
| ACT-023 | 25 → **20** | PMP-07, Fase 4 = 4 minggu |

---

## BAGIAN G — Struktur Bab Seluruh Dokumen PMP (Table of Contents)

Seluruh 8 PMP disusun **seragam** mengikuti 10 Knowledge Areas PMBOK. Berikut daftar bab beserta **variabel dataset yang terkait**:

| Bab | Judul Bab | Variabel Dataset yang Dirujuk |
|:---:|:----------|:------------------------------|
| 1 | **Pendahuluan** (*Introduction*) — Latar Belakang, Tujuan, Timeline, Asumsi & Kendala, Ketergantungan | `Sub_Project`, `Predecessor_Count` |
| 2 | **Manajemen Integrasi** (*Project Integration Management*) — Project Charter, Metodologi Hybrid Agile-Waterfall, Change Control | `Change_Request_Count` |
| 3 | **Manajemen Ruang Lingkup** (*Project Scope Management*) — **WBS, WBS Dictionary**, Scope Control | `Task_Name`, `Change_Request_Count` |
| 4 | **Manajemen Jadwal** (*Project Schedule Management*) — Activity Definition, **Sequencing**, **Duration Estimation**, **Sprint Schedule**, Milestone, Gantt, **Schedule Control & EVM Thresholds** | `Planned_Duration_Days`, `Predecessor_Count`, `SPI_Value`, `Status_Delay` |
| 5 | **Manajemen Biaya** (*Project Cost Management*) — Activity-Based Costing, Budget Baseline, **EVM Metrics** | `Planned_Effort_Hours` (basis tarif 8 jam/hari), `SPI_Value` |
| 6 | **Manajemen Mutu** (*Project Quality Management*) — Quality KPIs, QA/QC | — |
| 7 | **Manajemen Sumber Daya** (*Project Resource Management*) — RACI, **Staffing Plan**, **Resource Loading**, **Resource Utilization Plan** | `Planned_Effort_Hours`, `Resource_Utilization_Rate` |
| 8 | **Manajemen Komunikasi** (*Project Communication Management*) — Stakeholder Channels | — |
| 9 | **Manajemen Risiko** (*Project Risk Management*) — RBS, **Risk Register**, **P×I Matrix**, Risk Response | `Risk_Score` |
| 10 | **Manajemen Pengadaan** (*Project Procurement Management*) — Make-or-Buy | — |
| 11 | **Manajemen Pemangku Kepentingan** (*Project Stakeholder Management*) — Power/Interest Grid | — |
| 12 | **Lampiran** — A: Charter, B: Gantt, C: Budget, D: RACI, **E: Risk Register Lengkap**, F: RTM, G: Acceptance, H: Communication, **J/D: Change Request Form & Change Log** | `Risk_Score`, `Change_Request_Count` |
| 13* | **Proses Perubahan & Persetujuan** (*Change Control & Approval*) — CCB, CRF, Change Log | `Change_Request_Count` |
| 14* | **Penutupan Proyek** (*Project Closure*) — Handover, Lessons Learned | — |

> *Bab 13 dan 14 hanya ada secara eksplisit pada PMP P-FNE-01; pada PMP lainnya, isinya berada di Bab 2 (Integrasi) dan Bab 12 (Lampiran).

---

## BAGIAN H — Cheat Sheet: Jawaban Cepat untuk Pertanyaan Dosen

### "Data ini data apa? Dapat dari mana?"
> Data **empiris-simulatif** dari dokumen perencanaan proyek Super ERP Farm Nation Enterprise 2026. Tersimpan di folder `MP-datasetRaw/` berupa 1 KAK, 1 Pemetaan Proyek, 8 PMP, dan 8 SRS — total 18 dokumen `.docx`.

### "Mengapa data bukan dari proyek yang sudah berjalan?"
> Proyek FNE 2026 masih pada tahap perencanaan (pra-eksekusi). Buktinya: tabel *Velocity Planning* di PMP P-FNE-01 menunjukkan *Actual Velocity* masih kosong. Variabel rencana (durasi, effort, dependensi) diambil langsung dari dokumen; variabel monitoring (SPI, utilisasi, risk, CR) ditetapkan melalui *expert judgment* mengikuti rumus dan ambang yang tertulis pada PMP.

### "Variabel durasi diperoleh dari mana?"
> Dari **Bab 4 PMP** (*Schedule Management Plan*) tiap sub-proyek — tabel Sprint Schedule, Activity Duration Estimates, atau jadwal Fase/Milestone. Konversi: 1 sprint = 10 hari kerja, 1 minggu = 5 hari kerja (ketentuan PMP P-FNE-06).

### "Variabel effort diperoleh dari mana?"
> **Diturunkan** dari durasi: `Effort = Durasi × 8 jam × 1.0 FTE`. Basis 8 jam/hari dari **Bab 7 PMP** (*Resource Management Plan*), kapasitas 160 jam/bulan.

### "Variabel utilisasi diperoleh dari mana?"
> Rumusnya dari **Bab 7 PMP-08** — tabel *Resource Utilization Plan*: `U = Jam Kerja / 160`. Nilai > 1.0 karena *shared developer* lintas sub-proyek paralel yang tidak tercatat di satu PMP mana pun.

### "Variabel risiko diperoleh dari mana?"
> Rumusnya dari **Bab 9 / Lampiran E PMP** — *Risk Register*: `R = (P/5) × (I/5)`, skala Likert 1–5 dikonversi ke [0,1].

### "Variabel SPI diperoleh dari mana?"
> Rumus `SPI = EV/PV` dari **Bab 4 PMP** (standar EVM PMBOK). Ambang peringatan SPI ≥ 0.8 juga tercantum di **Bab 7 PMP**.

### "Label Status_Delay ditentukan bagaimana?"
> **Diturunkan dari SPI:** jika `SPI ≤ 0.90` → terlambat (1); jika `SPI > 0.90` → tepat waktu (0). Aturan ini konsisten dengan ambang kinerja jadwal pada PMP. Hasilnya: 16 modul terlambat (61.5%), 10 tepat waktu (38.5%).

### "Apa bedanya data terdokumentasi vs estimasi ahli?"
> **Terdokumentasi** = nilainya bisa ditunjuk langsung di halaman/tabel dokumen (contoh: durasi ACT-002 = Sprint 1–2 PMP-01). **Estimasi ahli** = rumus/prosedur dari PMP, tapi nilai per aktivitas ditetapkan peneliti karena proyek belum dieksekusi. *Expert judgment* adalah metode yang diakui PMBOK dan dipakai oleh PMP FNE sendiri.

### "Kenapa SPI bisa menjadi prediktor dominan?"
> Karena `Status_Delay` diturunkan langsung dari kondisi `SPI ≤ 0.90`, sehingga SPI memiliki daya pisah sangat tinggi. Oleh karena itu, eksperimen diulang **tanpa** `SPI_Value` sebagai fitur untuk menguji kemampuan prediksi dini yang sesungguhnya.

---

*Dokumen ini disusun sebagai panduan rujukan cepat. Untuk penjelasan lengkap beserta contoh perhitungan, lihat [`Penjelasan_Variabel_Dataset.md`](Penjelasan_Variabel_Dataset.md) di folder yang sama.*

tags: #paper #mp #academic #research #dataset #rujukan-dosen
