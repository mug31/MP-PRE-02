# 04_implemen_desain_eksperimen
## Capaian Pertemuan 4: Implementasi Desain Eksperimen
**Topik:** PRE-02 — Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas  
**Studi Kasus:** Portofolio Modul Super ERP Farm Nation Enterprise (FNE) 2026  

---

### 📂 Struktur Berkas pada Folder Ini:

| Berkas | Jenis Output | Deskripsi & Isi |
| :--- | :---: | :--- |
| [`01_Flow_dan_Skenario_Eksperimen.md`](file:///C:/Users/nailul/Documents/Files_Kuliah_Local/Workspace-MP-PRE-02/MP-PRE-02-github/04_implemen_desain_eksperimen/01_Flow_dan_Skenario_Eksperimen.md) | **Flow Eksperimen & Skenario** | Flowchart pipeline ML (Mermaid), rincian 5 skenario eksperimen, penentuan parameter, dan protokol replikasi. |
| [`02_Draft_Metodologi_Eksperimen_Bab3.md`](file:///C:/Users/nailul/Documents/Files_Kuliah_Local/Workspace-MP-PRE-02/MP-PRE-02-github/04_implemen_desain_eksperimen/02_Draft_Metodologi_Eksperimen_Bab3.md) | **Draft Bagian Metodologi** | Naskah ilmiah Bab III Metodologi Penelitian (standar paper IEEE/SINTA) mencakup operasionalisasi variabel, formulasi matematis Brier Score, ECE, dan zonasi EWS. |
| [`experiment_pipeline.py`](file:///C:/Users/nailul/Documents/Files_Kuliah_Local/Workspace-MP-PRE-02/MP-PRE-02-github/04_implemen_desain_eksperimen/experiment_pipeline.py) | **Script/Tools Eksperimen** | Program Python untuk mengeksekusi pelatihan 4 model ML (LR, RF, GB, MLP), kalibrasi Isotonic, evaluasi 5-fold CV, dan ekspor grafik/tabel. |
| [`generate_pertemuan4_pptx.py`](file:///C:/Users/nailul/Documents/Files_Kuliah_Local/Workspace-MP-PRE-02/MP-PRE-02-github/04_implemen_desain_eksperimen/generate_pertemuan4_pptx.py) | **Generator Presentasi** | Script otomasi pembuatan slide deck presentasi Pertemuan 4 berdesain *Swiss Academic Style*. |
| [`PRE02_Pertemuan4_Implementasi_Desain_Eksperimen.pptx`](file:///C:/Users/nailul/Documents/Files_Kuliah_Local/Workspace-MP-PRE-02/MP-PRE-02-github/04_implemen_desain_eksperimen/PRE02_Pertemuan4_Implementasi_Desain_Eksperimen.pptx) | **Slide Deck Presentasi** | 8 slide siap presentasi ke dosen pembimbing mengenai implementasi desain eksperimen. |

---

### 🚀 Cara Menjalankan Script Eksperimen:

Pastikan dependensi telah terpasang:
```bash
pip install scikit-learn pandas matplotlib
```

Jalankan pipeline eksperimen:
```bash
python experiment_pipeline.py
```

Luaran yang akan otomatis digenerate ke sub-folder `hasil_eksperimen/`:
1. `tabel_metrik_evaluasi.csv` (ROC-AUC, Brier Score, Log Loss, ECE, Accuracy, F1 per model).
2. `kurva_roc_perbandingan.png` (Plot kurva ROC 4 algoritma).
3. `kurva_kalibrasi_probabilitas.png` (Reliability Diagram perbandingan kalibrasi).
4. `feature_importance_comparison.png` (Diagram batang kontribusi fitur pemicu delay).
5. `tabel_prediksi_probabilitas_task.csv` (Prediksi probabilitas $P(\text{Delay})$ dan zona EWS per aktivitas modul FNE).
6. `00_RINGKASAN_TEMUAN_EKSPERIMEN.md` (Laporan ringkasan siap kutip untuk Bab IV & V).

---

### 📋 Checklist Pemenuhan Silabus Pertemuan 4:
- [x] **Implementasi metode sesuai instruksi:** 4 model probabilitas + kalibrasi terimplementasi dalam script Python.
- [x] **Penyusunan skenario eksperimen:** 5 skenario (LR, RF, GB, MLP, Kalibrasi) terdokumentasi lengkap.
- [x] **Penentuan parameter dan variabel kontrol:** Variabel $X_1 \dots X_7$ & $Y$, hyperparameter tuning, dan fixed seed 42 terkunci.
- [x] **Flow eksperimen:** Diagram pipeline flowchart visual tersedia di dokumen.
- [x] **Script/tools eksperimen:** `experiment_pipeline.py` siap pakai.
- [x] **Draft bagian metodologi:** Bab III lengkap tersedia di `02_Draft_Metodologi_Eksperimen_Bab3.md`.
