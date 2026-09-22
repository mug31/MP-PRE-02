# 04_implemen_desain_eksperimen
## Capaian Pertemuan 4: Implementasi Desain Eksperimen
**Topik:** PRE-02 — Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas  
**Studi Kasus:** Portofolio Modul Super ERP Farm Nation Enterprise (FNE) 2026  

---

### 📂 Struktur Berkas pada Folder Ini:

| Berkas | Jenis Output | Deskripsi & Isi |
| :--- | :---: | :--- |
| [`01_Flow_dan_Skenario_Eksperimen.md`](01_Flow_dan_Skenario_Eksperimen.md) | **Flow Eksperimen & Skenario** | Flowchart pipeline ML (Mermaid), rincian 5 skenario eksperimen, penentuan parameter, dan protokol replikasi. |
| [`02_Draft_Metodologi_Eksperimen_Bab3.md`](02_Draft_Metodologi_Eksperimen_Bab3.md) | **Draft Bagian Metodologi** | Naskah ilmiah Bab III Metodologi Penelitian (standar paper IEEE/SINTA) mencakup operasionalisasi variabel, formulasi matematis Brier Score, ECE, dan zonasi EWS. |
| [`experiment_pipeline.py`](experiment_pipeline.py) | **Script/Tools Eksperimen** | Program Python untuk mengeksekusi pelatihan 4 model ML (LR, RF, GB, MLP), kalibrasi Platt Scaling & Isotonic Regression (nested, tanpa kebocoran data), evaluasi 5-fold CV + hold-out 80:20, threshold analysis Youden, dan ekspor grafik/tabel. |
| [`generate_pertemuan4_pptx.py`](generate_pertemuan4_pptx.py) | **Generator Presentasi** | Script otomasi pembuatan slide deck presentasi Pertemuan 4 berdesain *Swiss Academic Style*. |
| [`PRE02_Pertemuan4_Implementasi_Desain_Eksperimen.pptx`](PRE02_Pertemuan4_Implementasi_Desain_Eksperimen.pptx) | **Slide Deck Presentasi** | 8 slide siap presentasi ke dosen pembimbing mengenai implementasi desain eksperimen. |

---

### 🚀 Cara Menjalankan Script Eksperimen:

Pastikan dependensi telah terpasang:
```bash
pip install numpy matplotlib
```

Jalankan pipeline eksperimen:
```bash
python experiment_pipeline.py
```

Luaran yang akan otomatis digenerate ke sub-folder `hasil_eksperimen/`:
1. `tabel_metrik_evaluasi.csv` (ROC-AUC, Brier Score, Log Loss, ECE, Accuracy, Precision, Recall, Specificity, F1, confusion matrix per model × kalibrasi Raw/Platt/Isotonic).
2. `kurva_roc_perbandingan.png` (Plot kurva ROC 4 algoritma).
3. `kurva_kalibrasi_probabilitas.png` (Reliability Diagram: 4 model mentah & efek Platt/Isotonic pada model rekomendasi).
4. `feature_importance_comparison.png` (Diagram batang kontribusi fitur pemicu delay).
5. `tabel_prediksi_probabilitas_task.csv` (Prediksi probabilitas $P(\text{Delay})$ tiap model, probabilitas model rekomendasi, dan zona EWS per aktivitas modul FNE).
6. `tabel_metrik_holdout_80_20.csv` (Validasi pembanding hold-out stratified 80:20).
7. `00_RINGKASAN_TEMUAN_EKSPERIMEN.md` (Laporan ringkasan untuk Bab IV & V; seluruh kalimat temuan digenerate otomatis dari hasil).

---

### 📋 Checklist Pemenuhan Silabus Pertemuan 4:
- [x] **Implementasi metode sesuai instruksi:** 4 model probabilitas + kalibrasi Platt & Isotonic terimplementasi dalam script Python (diverifikasi terhadap scikit-learn).
- [x] **Penyusunan skenario eksperimen:** 5 skenario (LR, RF, GB, MLP, Kalibrasi) terdokumentasi lengkap.
- [x] **Penentuan parameter dan variabel kontrol:** Variabel $X_1 \dots X_7$ & $Y$, hyperparameter tuning, dan fixed seed 42 terkunci.
- [x] **Flow eksperimen:** Diagram pipeline flowchart visual tersedia di dokumen.
- [x] **Script/tools eksperimen:** `experiment_pipeline.py` siap pakai.
- [x] **Draft bagian metodologi:** Bab III lengkap tersedia di `02_Draft_Metodologi_Eksperimen_Bab3.md`.
