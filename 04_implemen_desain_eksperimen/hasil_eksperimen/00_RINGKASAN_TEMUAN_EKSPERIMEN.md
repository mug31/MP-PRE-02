# Ringkasan Temuan Eksperimen PRE-02 (versi 2)

> Digenerate otomatis oleh `experiment_pipeline.py`. Semua angka berasal dari prediksi out-of-fold *leave-one-subproject-out* (8 lipatan) pada `dataset_ml.csv`. Jangan diedit manual.

- Data: 24000 baris, 8 subproyek, label `Telat_Lebih_5_Persen` = 1 pada 44,8% baris
- Pembanding naif: Brier 0,2715, AUC 0,191
- **Model rekomendasi: Gradient Boosting + Raw** — Brier 0,1718, Brier Skill Score 0,367, ROC-AUC 0,815, ECE 0,0560, Log Loss 0,5158

## Skenario 0–5: perbandingan model

| Model | Kalibrasi | Brier | BSS | Log Loss | ECE | ROC-AUC | Ambang Youden | Recall | Specificity | F1 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pembanding Naif | Raw | 0,2715 | 0,000 | 0,7371 | 0,1546 | 0,191 | 1,000 | 0,0% | 100,0% | 0,000 |
| Logistic Regression | Raw | 0,1958 | 0,279 | 0,5888 | 0,0939 | 0,786 | 0,388 | 68,8% | 73,8% | 0,684 |
| Logistic Regression | Platt | 0,2145 | 0,210 | 0,6264 | 0,1026 | 0,716 | 0,499 | 62,6% | 77,0% | 0,655 |
| Logistic Regression | Isotonic | 0,2148 | 0,209 | 0,6268 | 0,1058 | 0,706 | 0,468 | 66,5% | 74,6% | 0,672 |
| Random Forest | Raw | 0,1761 | 0,351 | 0,5313 | 0,0762 | 0,818 | 0,474 | 72,6% | 79,6% | 0,734 |
| Random Forest | Platt | 0,1776 | 0,346 | 0,5410 | 0,0765 | 0,808 | 0,471 | 72,9% | 78,0% | 0,729 |
| Random Forest | Isotonic | 0,1860 | 0,315 | 0,5861 | 0,1101 | 0,797 | 0,464 | 75,7% | 72,4% | 0,722 |
| **Gradient Boosting** | Raw | 0,1718 | 0,367 | 0,5158 | 0,0560 | 0,815 | 0,485 | 65,7% | 81,9% | 0,699 |
| Gradient Boosting | Platt | 0,1860 | 0,315 | 0,5659 | 0,0857 | 0,777 | 0,497 | 64,6% | 83,1% | 0,696 |
| Gradient Boosting | Isotonic | 0,1880 | 0,307 | 0,5616 | 0,0701 | 0,771 | 0,459 | 61,6% | 86,7% | 0,692 |
| MLP Neural Network | Raw | 0,2859 | -0,053 | 1,6389 | 0,2188 | 0,696 | 0,491 | 73,2% | 57,0% | 0,647 |
| MLP Neural Network | Platt | 0,2616 | 0,036 | 0,7258 | 0,1417 | 0,583 | 0,426 | 73,6% | 49,7% | 0,625 |
| MLP Neural Network | Isotonic | 0,2633 | 0,030 | 1,4236 | 0,1840 | 0,650 | 0,812 | 39,5% | 86,3% | 0,506 |

- Ada kombinasi dengan BSS ≤ 0 (tidak lebih baik dari pembanding naif): MLP Neural Network/Raw.
- ROC-AUC tertinggi tanpa kalibrasi: Random Forest (0,818).
- Logistic Regression: Platt maupun Isotonic tidak memperbaiki Brier (Raw 0,1958 tetap terbaik).
- Random Forest: Platt maupun Isotonic tidak memperbaiki Brier (Raw 0,1761 tetap terbaik).
- Gradient Boosting: Platt maupun Isotonic tidak memperbaiki Brier (Raw 0,1718 tetap terbaik).
- MLP Neural Network: kalibrasi terbaik menurut Brier = Platt (Brier Raw 0,2859 → 0,2616; ROC-AUC Raw 0,696 → 0,583).
- ROC-AUC gabungan dapat berubah setelah kalibrasi walaupun kalibrasi bersifat monoton: setiap lipatan memakai pemetaan kalibrasi sendiri (dilatih pada subproyek lain), sehingga urutan prediksi antarsubproyek berubah, dan isotonic menghasilkan nilai seri.

## Skenario 6: per titik monitoring (model rekomendasi)

| Titik | Prevalensi | Brier | BSS | ROC-AUC | ECE |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 25% | 44,8% | 0,2089 | 0,230 | 0,725 | 0,0697 |
| 50% | 44,8% | 0,1911 | 0,296 | 0,782 | 0,1081 |
| 75% | 44,8% | 0,1154 | 0,575 | 0,915 | 0,0637 |

## Brier per subproyek uji (model rekomendasi vs pembanding naif)

| Subproyek | Prevalensi | Brier model | Brier naif | BSS |
| :--- | ---: | ---: | ---: | ---: |
| P-FNE-01 | 40,3% | 0,1930 | 0,2432 | 0,206 |
| P-FNE-02 | 0,4% | 0,0214 | 0,2612 | 0,918 |
| P-FNE-03 | 57,6% | 0,1733 | 0,2657 | 0,348 |
| P-FNE-04 | 98,9% | 0,0764 | 0,3935 | 0,806 |
| P-FNE-05 | 55,7% | 0,1816 | 0,2623 | 0,308 |
| P-FNE-06 | 38,1% | 0,1647 | 0,2417 | 0,318 |
| P-FNE-07 | 13,2% | 0,1972 | 0,2448 | 0,194 |
| P-FNE-08 | 54,0% | 0,3668 | 0,2595 | -0,414 |

Model rekomendasi lebih buruk dari pembanding naif (BSS ≤ 0) pada: P-FNE-08.

## Peringatan dini (model rekomendasi)

Ambang Youden θ* = 0,485 (Recall 65,7%, Specificity 81,9%). Zona: Hijau < 0,35 ≤ Kuning < 0,65 ≤ Merah.

| Titik | Proyek yang akhirnya telat & sudah di zona Merah | Proyek tepat waktu yang masuk zona Merah | Telat terdeteksi ≥ θ* | Tepat waktu ≥ θ* |
| ---: | ---: | ---: | ---: | ---: |
| 25% | 40,0% | 8,2% | 56,7% | 22,5% |
| 50% | 56,9% | 16,8% | 67,0% | 24,2% |
| 75% | 67,9% | 2,6% | 73,5% | 7,6% |

## Kepentingan fitur

| Fitur | Koefisien LR | Odds ratio LR | MDI RF | Permutation RF (± SD) |
| :--- | ---: | ---: | ---: | ---: |
| SPI_Jadwal | -1,017 | 0,362 | 0,437 | 0,0493 (± 0,0302) |
| Pergeseran_Dependency_Hari | 0,598 | 1,819 | 0,108 | 0,0038 (± 0,0033) |
| Backlog_Sisa_Persen | 0,703 | 2,021 | 0,082 | 0,0036 (± 0,0035) |
| Sisa_Waktu_Hari | -0,785 | 0,456 | 0,035 | 0,0013 (± 0,0010) |
| Utilisasi_Resource | 0,716 | 2,046 | 0,203 | 0,0004 (± 0,0034) |
| Risiko_Belum_Dimitigasi | 0,307 | 1,359 | 0,032 | 0,0003 (± 0,0007) |
| Frekuensi_CR | -0,354 | 0,702 | 0,103 | -0,0009 (± 0,0013) |

## Skenario 7: sensitivitas faktor dampak risiko

Model Gradient Boosting + Raw dijalankan ulang pada dataset dengan faktor dampak berbeda.

| Faktor dampak | Prevalensi label | Brier | BSS | ROC-AUC | ECE |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0,4 (utama) | 44,8% | 0,1718 | 0,367 | 0,815 | 0,0560 |
| 0,2 | 26,9% | 0,1312 | 0,383 | 0,837 | 0,0293 |
| 1,0 | 75,1% | 0,1654 | 0,258 | 0,771 | 0,1137 |

## Catatan membaca

- BSS (Brier Skill Score) = 1 − Brier model / Brier pembanding naif; > 0 berarti lebih baik dari menebak proporsi telat.
- Ambang Youden dipilih pada prediksi out-of-fold yang sama dengan yang dievaluasi, sehingga Recall/Specificity pada ambang itu sedikit optimistis; metrik probabilitas (Brier, Log Loss, ECE, AUC) tidak bergantung ambang.
- ROC-AUC pembanding naif di bawah 0,5 adalah konsekuensi validasi per subproyek: prediksinya = proporsi telat di 7 subproyek latih, yang justru lebih rendah ketika subproyek uji banyak telat (dan sebaliknya). Pembanding naif dipakai untuk Brier/BSS, bukan untuk AUC.
- P-FNE-02 dan P-FNE-04 hampir satu kelas pada label ini; ROC-AUC per subproyek tidak dilaporkan.
