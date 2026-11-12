# Bukti untuk Pembahasan (Pertemuan 7)

> Digenerate otomatis oleh `bukti_pembahasan.py`. Hasil utama Pertemuan 5–6 tidak berubah; E5 adalah analisis **post-hoc**.

## E1. Prediksi ekstrem (≤ 0,01 atau ≥ 0,99), keluaran mentah

| Model | Porsi prediksi ekstrem | Porsi ekstrem yang salah arah | Sumbangan ke Log Loss |
| :--- | ---: | ---: | ---: |
| Logistic Regression | 2,9% | 5,1% | 0,0081 |
| Random Forest | 0,0% | n/a | 0,0000 |
| Gradient Boosting | 0,0% | n/a | 0,0000 |
| MLP Neural Network | 27,2% | 31,6% | 1,0050 |

## E2. Transfer kalibrasi Platt (rata-rata 8 subproyek uji)

| Model | ECE Raw | ECE Platt dari 7 subproyek lain | ECE Platt oracle (subproyek sendiri) | Brier Raw | Brier Platt lain | Brier Platt oracle |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Gradient Boosting | 0,1615 | 0,2046 | 0,0271 | 0,1718 | 0,1907 | 0,1223 |
| Logistic Regression | 0,1780 | 0,2213 | 0,0284 | 0,1958 | 0,2058 | 0,1368 |
| MLP Neural Network | 0,3006 | 0,2924 | 0,0387 | 0,2859 | 0,2560 | 0,1343 |
| Random Forest | 0,1816 | 0,1908 | 0,0356 | 0,1761 | 0,1867 | 0,1265 |

Oracle = kalibrator dilatih dan diuji pada subproyek yang sama (batas atas, tidak mungkin dilakukan sebelum proyek berjalan).

## E3. Calibration slope Logistic Regression: data latih vs subproyek uji

| Subproyek uji | Slope latih | Slope uji | Intercept latih | Intercept uji |
| :--- | ---: | ---: | ---: | ---: |
| P-FNE-01 | 1,001 | 0,966 | -0,000 | 0,294 |
| P-FNE-02 | 1,001 | 1,769 | 0,000 | -2,676 |
| P-FNE-03 | 1,002 | 0,389 | -0,000 | 1,425 |
| P-FNE-04 | 1,000 | 1,106 | -0,000 | 3,361 |
| P-FNE-05 | 1,001 | 1,257 | -0,000 | -1,281 |
| P-FNE-06 | 1,001 | 0,921 | -0,000 | -0,256 |
| P-FNE-07 | 1,001 | 0,450 | 0,000 | -2,777 |
| P-FNE-08 | 1,001 | 1,602 | 0,000 | 1,956 |

## E4. Profil subproyek

| Subproyek | T (hari) | Ambang 5% (hari) | Rata-rata telat (hari) | Prevalensi | Rata-rata prediksi GB | Selisih | BSS GB | Utilisasi | Jarak profil fitur |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P-FNE-01 | 131 | 6,6 | 6,2 | 40,3% | 29,6% | -0,107 | 0,206 | 0,162 | 0,23 |
| P-FNE-02 | 232 | 11,6 | 5,9 | 0,4% | 13,0% | 0,126 | 0,918 | 0,179 | 0,96 |
| P-FNE-03 | 220 | 11,0 | 12,9 | 57,6% | 61,4% | 0,038 | 0,348 | 1,000 | 0,55 |
| P-FNE-04 | 120 | 6,0 | 18,6 | 98,9% | 80,3% | -0,186 | 0,806 | 1,000 | 0,86 |
| P-FNE-05 | 123 | 6,2 | 6,9 | 55,7% | 67,0% | 0,113 | 0,308 | 1,000 | 0,36 |
| P-FNE-06 | 120 | 6,0 | 5,9 | 38,1% | 38,9% | 0,008 | 0,318 | 0,618 | 0,30 |
| P-FNE-07 | 128 | 6,4 | 3,8 | 13,2% | 39,7% | 0,265 | 0,194 | 0,133 | 0,37 |
| P-FNE-08 | 62 | 3,1 | 3,4 | 54,0% | 14,7% | -0,393 | -0,414 | 0,048 | 0,56 |

## E5. Post-hoc: GB dengan fitur relatif terhadap T

Sisa_Waktu_Hari → Sisa_Waktu_Hari / T; Pergeseran_Dependency_Hari → Pergeseran_Dependency_Hari / T; fitur lain tetap.

| Subproyek | Varian | Prevalensi | Rata-rata prediksi | Brier | BSS | ECE | ROC-AUC |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Semua | Fitur asli (hasil utama) | 44,8% | 43,1% | 0,1718 | 0,367 | 0,0560 | 0,815 |
| Semua | Fitur relatif (post-hoc) | 44,8% | 43,3% | 0,1746 | 0,357 | 0,0478 | 0,809 |
| P-FNE-01 | Fitur asli (hasil utama) | 40,3% | 29,6% | 0,1930 | 0,206 | 0,1100 | 0,790 |
| P-FNE-01 | Fitur relatif (post-hoc) | 40,3% | 31,6% | 0,1903 | 0,218 | 0,0879 | 0,789 |
| P-FNE-02 | Fitur asli (hasil utama) | 0,4% | 13,0% | 0,0214 | 0,918 | 0,1263 | 0,683 |
| P-FNE-02 | Fitur relatif (post-hoc) | 0,4% | 12,8% | 0,0210 | 0,919 | 0,1240 | 0,656 |
| P-FNE-03 | Fitur asli (hasil utama) | 57,6% | 61,4% | 0,1733 | 0,348 | 0,0559 | 0,819 |
| P-FNE-03 | Fitur relatif (post-hoc) | 57,6% | 64,0% | 0,1758 | 0,338 | 0,0817 | 0,824 |
| P-FNE-04 | Fitur asli (hasil utama) | 98,9% | 80,3% | 0,0764 | 0,806 | 0,1864 | 0,925 |
| P-FNE-04 | Fitur relatif (post-hoc) | 98,9% | 78,1% | 0,0809 | 0,794 | 0,2078 | 0,915 |
| P-FNE-05 | Fitur asli (hasil utama) | 55,7% | 67,0% | 0,1816 | 0,308 | 0,1255 | 0,836 |
| P-FNE-05 | Fitur relatif (post-hoc) | 55,7% | 64,0% | 0,1736 | 0,338 | 0,0945 | 0,835 |
| P-FNE-06 | Fitur asli (hasil utama) | 38,1% | 38,9% | 0,1647 | 0,318 | 0,0294 | 0,795 |
| P-FNE-06 | Fitur relatif (post-hoc) | 38,1% | 36,7% | 0,1683 | 0,304 | 0,0407 | 0,793 |
| P-FNE-07 | Fitur asli (hasil utama) | 13,2% | 39,7% | 0,1972 | 0,194 | 0,2653 | 0,761 |
| P-FNE-07 | Fitur relatif (post-hoc) | 13,2% | 43,8% | 0,2296 | 0,062 | 0,3060 | 0,766 |
| P-FNE-08 | Fitur asli (hasil utama) | 54,0% | 14,7% | 0,3668 | -0,414 | 0,3935 | 0,796 |
| P-FNE-08 | Fitur relatif (post-hoc) | 54,0% | 15,2% | 0,3573 | -0,377 | 0,3877 | 0,796 |

## E6. Korelasi Spearman

| Fitur | Titik | ρ dengan label (gabungan) | ρ dengan label (median dalam subproyek) | ρ dengan SPI (gabungan) | ρ dengan SPI (median dalam subproyek) |
| :--- | :--- | ---: | ---: | ---: | ---: |
| Risiko_Belum_Dimitigasi | Semua | 0,278 | 0,016 | -0,281 | -0,055 |
| Risiko_Belum_Dimitigasi | 25% | 0,206 | 0,035 | -0,207 | -0,018 |
| Risiko_Belum_Dimitigasi | 50% | 0,322 | 0,022 | -0,279 | 0,017 |
| Risiko_Belum_Dimitigasi | 75% | 0,309 | 0,004 | -0,356 | 0,013 |
| Frekuensi_CR | Semua | -0,159 | 0,324 | -0,037 | -0,542 |
| Frekuensi_CR | 25% | -0,135 | 0,264 | -0,174 | -0,631 |
| Frekuensi_CR | 50% | -0,173 | 0,372 | -0,118 | -0,654 |
| Frekuensi_CR | 75% | -0,204 | 0,449 | 0,262 | -0,639 |
| Pergeseran_Dependency_Hari | Semua | 0,243 | 0,303 | -0,564 | -0,687 |
| Pergeseran_Dependency_Hari | 25% | 0,175 | 0,218 | -0,698 | -0,813 |
| Pergeseran_Dependency_Hari | 50% | 0,203 | 0,401 | -0,510 | -0,825 |
| Pergeseran_Dependency_Hari | 75% | 0,493 | 0,505 | -0,663 | -0,801 |
| Utilisasi_Resource | Semua | 0,289 | -0,054 | -0,153 | 0,224 |
| Utilisasi_Resource | 25% | 0,293 | -0,121 | -0,132 | 0,786 |
| Utilisasi_Resource | 50% | 0,286 | -0,238 | -0,006 | 0,582 |
| Utilisasi_Resource | 75% | 0,294 | -0,146 | -0,352 | 0,389 |
| SPI_Jadwal | Semua | -0,554 | -0,457 | 1,000 | 1,000 |
| SPI_Jadwal | 25% | -0,435 | -0,311 | 1,000 | 1,000 |
| SPI_Jadwal | 50% | -0,492 | -0,498 | 1,000 | 1,000 |
| SPI_Jadwal | 75% | -0,786 | -0,714 | 1,000 | 1,000 |

## E7. Contoh kasus (GB + Raw)

| Jenis | Subproyek | Iterasi | Telat akhir | P 25% | P 50% | P 75% | Zona 25/50/75 | SPI 25/50/75 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- |
| Telat, terdeteksi dini | P-FNE-03 | 301 | 11,7 hari (5,3%) | 0,796 | 0,853 | 0,826 | Merah/Merah/Merah | 0,928/0,919/0,944 |
| Tepat waktu, peringatan palsu | P-FNE-03 | 216 | 10,6 hari (4,8%) | 0,630 | 0,694 | 0,635 | Kuning/Merah/Kuning | 0,956/0,937/0,949 |

## E8. Peringatan palsu: seberapa dekat proyek tepat waktu dengan ambang 5%

| Ambang | Kelompok | Jumlah iterasi | Median keterlambatan akhir (% T) | Porsi telat > 3% |
| :--- | :--- | ---: | ---: | ---: |
| θ* Youden (0,485) | Tepat waktu, pernah diperingatkan | 1681 | 3,6% | 67,3% |
| θ* Youden (0,485) | Tepat waktu, tidak pernah diperingatkan | 2737 | 2,8% | 44,8% |
| Batas Kuning (0,350) | Tepat waktu, pernah diperingatkan | 2231 | 3,5% | 64,5% |
| Batas Kuning (0,350) | Tepat waktu, tidak pernah diperingatkan | 2187 | 2,8% | 42,0% |
| Batas Merah (0,650) | Tepat waktu, pernah diperingatkan | 970 | 3,7% | 70,7% |
| Batas Merah (0,650) | Tepat waktu, tidak pernah diperingatkan | 3448 | 2,9% | 48,5% |
