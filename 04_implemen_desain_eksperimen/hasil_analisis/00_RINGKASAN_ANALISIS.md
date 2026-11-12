# Ringkasan Analisis Data Eksperimen PRE-02 (Pertemuan 6)

> Digenerate otomatis oleh `analisis_data.py` dari `hasil_eksperimen/tabel_prediksi_oof.csv`. Jangan diedit manual.

- Sumber: `hasil_eksperimen/tabel_prediksi_oof.csv` (MD5 `c5f77b9699736fe3a8aeb92147626af2`), 24000 baris, 8000 iterasi; model rekomendasi Pertemuan 5: Gradient Boosting + Raw, θ* = 0,485. Dijalankan 2026-11-12 18:51, 204 detik.
- Selang kepercayaan (CI) 95%: bootstrap persentil, 2000 replikasi, resampling per iterasi simulasi (ketiga titik monitoring satu iterasi ikut bersama). CI menggambarkan variasi antar-iterasi untuk 8 subproyek yang sama; generalisasi ke subproyek lain dinilai dengan kolom konsistensi antarsubproyek.
- Uji hipotesis: selisih berpasangan satu arah, koreksi Holm atas 17 uji, α = 0,05.

## Keputusan hipotesis

| Hipotesis | Sumber | Pernyataan | Keputusan | Rincian |
| :--- | :--- | :--- | :--- | :--- |
| H1 | Eksperimen 1: LR sebagai baseline yang terkalibrasi dengan baik | Logistic Regression memberi probabilitas lebih akurat daripada pembanding naif dan terkalibrasi baik | **Diterima sebagian** | H1a signifikan; intercept 0,155 [0,089; 0,220], slope 0,586 [0,562; 0,610] |
| H2 | Eksperimen 2: RF untuk meningkatkan akurasi prediksi probabilitas | Random Forest lebih akurat (Brier lebih kecil) daripada Logistic Regression | **Diterima** | H2 signifikan |
| H3 | Eksperimen 3: GB untuk mencapai kalibrasi probabilitas terbaik | Gradient Boosting memiliki Brier dan ECE terkecil dibanding LR, RF, dan NN | **Diterima** | H3a signifikan; H3b signifikan; H3c signifikan; H3d signifikan; H3e signifikan; H3f signifikan |
| H4 | Eksperimen 4: NN untuk menangkap pola non-linear | Neural Network (sigmoid) lebih akurat (Brier lebih kecil) daripada Logistic Regression yang linear | **Ditolak** | H4 berlawanan |
| H5 | Eksperimen 5: analisis kalibrasi dan rekomendasi model dengan kalibrasi terbaik | Kalibrasi pasca-latih (Platt/Isotonic) menurunkan ECE dibanding probabilitas mentah (Raw) | **Ditolak** | 2 dari 8 signifikan membaik (H5g, H5h); 4 justru memburuk signifikan. Kalibrasi terbaik: ECE terendah Gradient Boosting + Raw (0,0560), Brier terendah Gradient Boosting + Raw (0,1718) |

| Hipotesis | Konsistensi antarsubproyek (8 selisih per subproyek) |
| :--- | :--- |
| H1 | H1a: 6/8 subproyek searah (Wilcoxon p = 0,098) |
| H2 | H2: 4/8 subproyek searah (Wilcoxon p = 0,273) |
| H3 | H3a: 4/8 subproyek searah (Wilcoxon p = 0,156); H3b: 5/8 subproyek searah (Wilcoxon p = 0,273); H3c: 5/8 subproyek searah (Wilcoxon p = 0,074); H3d: 4/8 subproyek searah (Wilcoxon p = 0,422); H3e: 5/8 subproyek searah (Wilcoxon p = 0,371); H3f: 6/8 subproyek searah (Wilcoxon p = 0,039) |
| H4 | H4: 3/8 subproyek searah (Wilcoxon p = 0,727) |
| H5 | H5a: 2/8 subproyek searah (Wilcoxon p = 0,945); H5b: 3/8 subproyek searah (Wilcoxon p = 0,809); H5c: 4/8 subproyek searah (Wilcoxon p = 0,473); H5d: 4/8 subproyek searah (Wilcoxon p = 0,527); H5e: 1/8 subproyek searah (Wilcoxon p = 0,988); H5f: 3/8 subproyek searah (Wilcoxon p = 0,844); H5g: 5/8 subproyek searah (Wilcoxon p = 0,230); H5h: 4/8 subproyek searah (Wilcoxon p = 0,320) |

## Rincian uji

| Uji | A | B | Metrik | A | B | Selisih [CI 95%] | p Holm | Subproyek searah | p Wilcoxon |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| H1a | Logistic Regression + Raw | Pembanding Naif + Raw | Brier | 0,1958 | 0,2715 | -0,0757 [-0,0813; -0,0703] | 0,0085 ✓ | 6/8 | 0,0977 |
| H2 | Random Forest + Raw | Logistic Regression + Raw | Brier | 0,1761 | 0,1958 | -0,0197 [-0,0232; -0,0163] | 0,0085 ✓ | 4/8 | 0,2734 |
| H3a | Gradient Boosting + Raw | Logistic Regression + Raw | Brier | 0,1718 | 0,1958 | -0,0240 [-0,0266; -0,0214] | 0,0085 ✓ | 4/8 | 0,1562 |
| H3b | Gradient Boosting + Raw | Random Forest + Raw | Brier | 0,1718 | 0,1761 | -0,0043 [-0,0066; -0,0020] | 0,0085 ✓ | 5/8 | 0,2734 |
| H3c | Gradient Boosting + Raw | MLP Neural Network + Raw | Brier | 0,1718 | 0,2859 | -0,1141 [-0,1220; -0,1066] | 0,0085 ✓ | 5/8 | 0,0742 |
| H3d | Gradient Boosting + Raw | Logistic Regression + Raw | ECE | 0,0560 | 0,0939 | -0,0379 [-0,0425; -0,0310] | 0,0085 ✓ | 4/8 | 0,4219 |
| H3e | Gradient Boosting + Raw | Random Forest + Raw | ECE | 0,0560 | 0,0762 | -0,0202 [-0,0306; -0,0078] | 0,0085 ✓ | 5/8 | 0,3711 |
| H3f | Gradient Boosting + Raw | MLP Neural Network + Raw | ECE | 0,0560 | 0,2188 | -0,1628 [-0,1733; -0,1530] | 0,0085 ✓ | 6/8 | 0,0391 |
| H4 | MLP Neural Network + Raw | Logistic Regression + Raw | Brier | 0,2859 | 0,1958 | 0,0901 [0,0832; 0,0977] | 1,0000 ✗ (berlawanan) | 3/8 | 0,7266 |
| H5a | Logistic Regression + Platt | Logistic Regression + Raw | ECE | 0,1026 | 0,0939 | 0,0087 [-0,0004; 0,0203] | 1,0000 | 2/8 | 0,9453 |
| H5b | Logistic Regression + Isotonic | Logistic Regression + Raw | ECE | 0,1058 | 0,0939 | 0,0119 [0,0016; 0,0232] | 1,0000 ✗ (berlawanan) | 3/8 | 0,8086 |
| H5c | Random Forest + Platt | Random Forest + Raw | ECE | 0,0765 | 0,0762 | 0,0003 [-0,0065; 0,0090] | 1,0000 | 4/8 | 0,4727 |
| H5d | Random Forest + Isotonic | Random Forest + Raw | ECE | 0,1101 | 0,0762 | 0,0339 [0,0247; 0,0428] | 1,0000 ✗ (berlawanan) | 4/8 | 0,5273 |
| H5e | Gradient Boosting + Platt | Gradient Boosting + Raw | ECE | 0,0857 | 0,0560 | 0,0297 [0,0210; 0,0358] | 1,0000 ✗ (berlawanan) | 1/8 | 0,9883 |
| H5f | Gradient Boosting + Isotonic | Gradient Boosting + Raw | ECE | 0,0701 | 0,0560 | 0,0141 [0,0045; 0,0236] | 1,0000 ✗ (berlawanan) | 3/8 | 0,8438 |
| H5g | MLP Neural Network + Platt | MLP Neural Network + Raw | ECE | 0,1417 | 0,2188 | -0,0771 [-0,0857; -0,0675] | 0,0085 ✓ | 5/8 | 0,2305 |
| H5h | MLP Neural Network + Isotonic | MLP Neural Network + Raw | ECE | 0,1840 | 0,2188 | -0,0348 [-0,0416; -0,0294] | 0,0085 ✓ | 4/8 | 0,3203 |

Tambahan (dua arah): Gradient Boosting + Raw vs Random Forest + Raw, selisih Brier -0,0043 [-0,0066; -0,0020], p = 0,0010.

## Metrik dengan CI 95%

| Model | Kalibrasi | Brier | BSS | ROC-AUC | ECE | Intercept kalibrasi | Slope kalibrasi |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pembanding Naif | Raw | 0,2715 [0,2700; 0,2729] | 0,000 [0,000; 0,000] | – | 0,1546 [0,1437; 0,1662] | – | – |
| Logistic Regression | Raw | 0,1958 [0,1904; 0,2008] | 0,279 [0,259; 0,299] | 0,786 [0,778; 0,795] | 0,0939 [0,0863; 0,1017] | 0,155 [0,089; 0,220] | 0,586 [0,562; 0,610] |
| Logistic Regression | Platt | 0,2145 [0,2107; 0,2184] | 0,210 [0,195; 0,225] | 0,716 [0,705; 0,728] | 0,1026 [0,0973; 0,1103] | -0,094 [-0,143; -0,047] | 0,804 [0,748; 0,861] |
| Logistic Regression | Isotonic | 0,2148 [0,2110; 0,2186] | 0,209 [0,194; 0,224] | 0,706 [0,695; 0,717] | 0,1058 [0,0991; 0,1131] | -0,138 [-0,187; -0,091] | 0,741 [0,690; 0,793] |
| Random Forest | Raw | 0,1761 [0,1734; 0,1787] | 0,351 [0,341; 0,362] | 0,818 [0,811; 0,825] | 0,0762 [0,0703; 0,0826] | -0,074 [-0,120; -0,032] | 1,555 [1,499; 1,614] |
| Random Forest | Platt | 0,1776 [0,1741; 0,1811] | 0,346 [0,333; 0,359] | 0,808 [0,800; 0,816] | 0,0765 [0,0720; 0,0829] | -0,033 [-0,083; 0,013] | 1,007 [0,967; 1,051] |
| Random Forest | Isotonic | 0,1860 [0,1824; 0,1896] | 0,315 [0,301; 0,329] | 0,797 [0,789; 0,805] | 0,1101 [0,1035; 0,1167] | -0,109 [-0,163; -0,059] | 0,730 [0,695; 0,769] |
| Gradient Boosting | Raw | 0,1718 [0,1672; 0,1762] | 0,367 [0,351; 0,384] | 0,815 [0,806; 0,824] | 0,0560 [0,0504; 0,0636] | 0,112 [0,054; 0,168] | 0,850 [0,820; 0,882] |
| Gradient Boosting | Platt | 0,1860 [0,1817; 0,1901] | 0,315 [0,300; 0,331] | 0,777 [0,768; 0,788] | 0,0857 [0,0789; 0,0923] | 0,034 [-0,018; 0,082] | 0,913 [0,866; 0,964] |
| Gradient Boosting | Isotonic | 0,1880 [0,1839; 0,1919] | 0,307 [0,293; 0,323] | 0,771 [0,761; 0,781] | 0,0701 [0,0644; 0,0775] | -0,042 [-0,097; 0,008] | 0,724 [0,683; 0,770] |
| MLP Neural Network | Raw | 0,2859 [0,2795; 0,2925] | -0,053 [-0,080; -0,028] | 0,696 [0,687; 0,704] | 0,2188 [0,2113; 0,2277] | -1,585 [-1,722; -1,463] | 0,142 [0,134; 0,151] |
| MLP Neural Network | Platt | 0,2616 [0,2582; 0,2651] | 0,036 [0,022; 0,050] | 0,583 [0,573; 0,593] | 0,1417 [0,1354; 0,1514] | -0,360 [-0,413; -0,310] | 0,344 [0,304; 0,386] |
| MLP Neural Network | Isotonic | 0,2633 [0,2592; 0,2674] | 0,030 [0,013; 0,048] | 0,650 [0,641; 0,658] | 0,1840 [0,1752; 0,1920] | -0,760 [-0,829; -0,697] | 0,148 [0,139; 0,158] |

## Dekomposisi Brier (Murphy)

| Model | Kalibrasi | Brier | Reliability | Resolution | Uncertainty | Sisa dalam bin |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| Pembanding Naif | Raw | 0,2715 | 0,0802 | 0,0614 | 0,2473 | 0,0054 |
| Logistic Regression | Raw | 0,1958 | 0,0108 | 0,0614 | 0,2473 | -0,0008 |
| Logistic Regression | Platt | 0,2145 | 0,0207 | 0,0532 | 0,2473 | -0,0002 |
| Logistic Regression | Isotonic | 0,2148 | 0,0188 | 0,0495 | 0,2473 | -0,0018 |
| Random Forest | Raw | 0,1761 | 0,0074 | 0,0791 | 0,2473 | 0,0005 |
| Random Forest | Platt | 0,1776 | 0,0108 | 0,0791 | 0,2473 | -0,0014 |
| Random Forest | Isotonic | 0,1860 | 0,0186 | 0,0831 | 0,2473 | 0,0032 |
| Gradient Boosting | Raw | 0,1718 | 0,0051 | 0,0811 | 0,2473 | 0,0005 |
| Gradient Boosting | Platt | 0,1860 | 0,0106 | 0,0717 | 0,2473 | -0,0002 |
| Gradient Boosting | Isotonic | 0,1880 | 0,0108 | 0,0696 | 0,2473 | -0,0004 |
| MLP Neural Network | Raw | 0,2859 | 0,0678 | 0,0276 | 0,2473 | -0,0015 |
| MLP Neural Network | Platt | 0,2616 | 0,0402 | 0,0269 | 0,2473 | 0,0011 |
| MLP Neural Network | Isotonic | 0,2633 | 0,0455 | 0,0271 | 0,2473 | -0,0024 |

## Per titik monitoring (CI 95%)

| Titik | Model | ROC-AUC | Brier |
| ---: | :--- | ---: | ---: |
| 25% | Logistic Regression + Raw | 0,734 [0,723; 0,745] | 0,2229 [0,2165; 0,2292] |
| 25% | Random Forest + Raw | 0,721 [0,709; 0,732] | 0,2098 [0,2065; 0,2132] |
| 25% | Gradient Boosting + Raw | 0,725 [0,714; 0,737] | 0,2089 [0,2038; 0,2142] |
| 25% | MLP Neural Network + Raw | 0,558 [0,546; 0,570] | 0,3700 [0,3618; 0,3788] |
| 50% | Logistic Regression + Raw | 0,762 [0,751; 0,773] | 0,2141 [0,2080; 0,2203] |
| 50% | Random Forest + Raw | 0,762 [0,751; 0,772] | 0,2005 [0,1973; 0,2038] |
| 50% | Gradient Boosting + Raw | 0,782 [0,771; 0,792] | 0,1911 [0,1857; 0,1964] |
| 50% | MLP Neural Network + Raw | 0,616 [0,604; 0,628] | 0,3509 [0,3422; 0,3602] |
| 75% | Logistic Regression + Raw | 0,865 [0,857; 0,873] | 0,1504 [0,1450; 0,1556] |
| 75% | Random Forest + Raw | 0,933 [0,927; 0,939] | 0,1180 [0,1147; 0,1211] |
| 75% | Gradient Boosting + Raw | 0,915 [0,909; 0,921] | 0,1154 [0,1103; 0,1201] |
| 75% | MLP Neural Network + Raw | 0,895 [0,888; 0,902] | 0,1368 [0,1313; 0,1423] |

| Model | Perubahan | Metrik | Nilai | CI 95% |
| :--- | :--- | :--- | ---: | ---: |
| Logistic Regression | 25% → 50% | ROC_AUC | 0,0283 | [0,0208; 0,0360] |
| Logistic Regression | 25% → 50% | Brier | -0,0088 | [-0,0141; -0,0034] |
| Logistic Regression | 50% → 75% | ROC_AUC | 0,1031 | [0,0950; 0,1116] |
| Logistic Regression | 50% → 75% | Brier | -0,0637 | [-0,0688; -0,0585] |
| Logistic Regression | 25% → 75% | ROC_AUC | 0,1314 | [0,1219; 0,1412] |
| Logistic Regression | 25% → 75% | Brier | -0,0725 | [-0,0777; -0,0670] |
| Random Forest | 25% → 50% | ROC_AUC | 0,0404 | [0,0296; 0,0516] |
| Random Forest | 25% → 50% | Brier | -0,0093 | [-0,0126; -0,0060] |
| Random Forest | 50% → 75% | ROC_AUC | 0,1717 | [0,1617; 0,1823] |
| Random Forest | 50% → 75% | Brier | -0,0825 | [-0,0860; -0,0792] |
| Random Forest | 25% → 75% | ROC_AUC | 0,2121 | [0,2011; 0,2237] |
| Random Forest | 25% → 75% | Brier | -0,0918 | [-0,0951; -0,0885] |
| Gradient Boosting | 25% → 50% | ROC_AUC | 0,0562 | [0,0481; 0,0647] |
| Gradient Boosting | 25% → 50% | Brier | -0,0178 | [-0,0222; -0,0134] |
| Gradient Boosting | 50% → 75% | ROC_AUC | 0,1333 | [0,1253; 0,1415] |
| Gradient Boosting | 50% → 75% | Brier | -0,0757 | [-0,0800; -0,0715] |
| Gradient Boosting | 25% → 75% | ROC_AUC | 0,1895 | [0,1805; 0,1993] |
| Gradient Boosting | 25% → 75% | Brier | -0,0936 | [-0,0979; -0,0897] |
| MLP Neural Network | 25% → 50% | ROC_AUC | 0,0579 | [0,0503; 0,0656] |
| MLP Neural Network | 25% → 50% | Brier | -0,0191 | [-0,0242; -0,0138] |
| MLP Neural Network | 50% → 75% | ROC_AUC | 0,2792 | [0,2683; 0,2913] |
| MLP Neural Network | 50% → 75% | Brier | -0,2141 | [-0,2224; -0,2063] |
| MLP Neural Network | 25% → 75% | ROC_AUC | 0,3370 | [0,3243; 0,3499] |
| MLP Neural Network | 25% → 75% | Brier | -0,2332 | [-0,2415; -0,2251] |

## Analisis ambang — Gradient Boosting + Raw

| Ambang | Keterangan | Titik | % diberi peringatan | Recall | Specificity | Precision | F1 |
| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0,485 | θ* Youden | Semua | 39,4% | 65,7% | 81,9% | 74,6% | 0,699 |
| 0,485 | θ* Youden | 25% | 37,8% | 56,7% | 77,5% | 67,2% | 0,615 |
| 0,485 | θ* Youden | 50% | 43,4% | 67,0% | 75,8% | 69,2% | 0,681 |
| 0,485 | θ* Youden | 75% | 37,1% | 73,5% | 92,4% | 88,7% | 0,804 |
| 0,350 | Batas Kuning | Semua | 48,7% | 73,6% | 71,5% | 67,7% | 0,705 |
| 0,350 | Batas Kuning | 25% | 49,3% | 67,7% | 65,6% | 61,4% | 0,644 |
| 0,350 | Batas Kuning | 50% | 53,9% | 75,0% | 63,2% | 62,3% | 0,680 |
| 0,350 | Batas Kuning | 75% | 42,8% | 78,1% | 85,9% | 81,8% | 0,799 |
| 0,650 | Batas Merah | Semua | 29,7% | 54,9% | 90,8% | 82,9% | 0,661 |
| 0,650 | Batas Merah | 25% | 22,4% | 40,0% | 91,8% | 79,9% | 0,533 |
| 0,650 | Batas Merah | 50% | 34,8% | 56,9% | 83,2% | 73,3% | 0,641 |
| 0,650 | Batas Merah | 75% | 31,8% | 67,9% | 97,4% | 95,4% | 0,793 |

## Deteksi dini (kumulatif per iterasi)

| Ambang | Telat diperingatkan s.d. 25% / 50% / 75% | Tepat waktu diperingatkan (palsu) s.d. 25% / 50% / 75% | Telat tak pernah diperingatkan | Sisa hari saat peringatan pertama (rata-rata / median) |
| :--- | ---: | ---: | ---: | ---: |
| θ* Youden (0,485) | 56,7% / 73,6% / 81,0% | 22,5% / 36,7% / 38,0% | 19,0% | 92,3 / 90,0 |
| Batas Kuning (0,350) | 67,7% / 80,8% / 84,5% | 34,4% / 49,3% / 50,5% | 15,5% | 97,7 / 90,0 |
| Batas Merah (0,650) | 40,0% / 60,4% / 74,4% | 8,2% / 20,7% / 22,0% | 25,6% | 82,7 / 90,0 |

## Per subproyek — Gradient Boosting + Raw

| Subproyek | Prevalensi | Rata-rata prediksi | Prediksi naif | Brier | BSS | ECE | Reliability | Resolution | ROC-AUC |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P-FNE-01 | 40,3% | 29,6% | 45,4% | 0,1930 | 0,206 | 0,1100 | 0,0174 | 0,0640 | 0,790 |
| P-FNE-02 | 0,4% | 13,0% | 51,1% | 0,0214 | 0,918 | 0,1263 | 0,0170 | 0,0001 | 0,683 |
| P-FNE-03 | 57,6% | 61,4% | 42,9% | 0,1733 | 0,348 | 0,0559 | 0,0042 | 0,0745 | 0,819 |
| P-FNE-04 | 98,9% | 80,3% | 37,0% | 0,0764 | 0,806 | 0,1864 | 0,0668 | 0,0017 | 0,925 |
| P-FNE-05 | 55,7% | 67,0% | 43,2% | 0,1816 | 0,308 | 0,1255 | 0,0202 | 0,0847 | 0,836 |
| P-FNE-06 | 38,1% | 38,9% | 45,7% | 0,1647 | 0,318 | 0,0294 | 0,0014 | 0,0720 | 0,795 |
| P-FNE-07 | 13,2% | 39,7% | 49,3% | 0,1972 | 0,194 | 0,2653 | 0,1005 | 0,0175 | 0,761 |
| P-FNE-08 | 54,0% | 14,7% | 43,5% | 0,3668 | -0,414 | 0,3935 | 0,1805 | 0,0592 | 0,796 |

## Kepentingan fitur — Gradient Boosting + Raw (permutation, kenaikan Brier di subproyek uji)

| Peringkat | Fitur | Rata-rata | SD antarlipatan | Lipatan positif |
| ---: | :--- | ---: | ---: | ---: |
| 1 | SPI_Jadwal | 0,07815 | 0,05411 | 8/8 |
| 2 | Backlog_Sisa_Persen | 0,00719 | 0,00957 | 7/8 |
| 3 | Sisa_Waktu_Hari | 0,00631 | 0,00955 | 6/8 |
| 4 | Utilisasi_Resource | 0,00144 | 0,01169 | 1/8 |
| 5 | Risiko_Belum_Dimitigasi | -0,00001 | 0,00017 | 4/8 |
| 6 | Pergeseran_Dependency_Hari | -0,00026 | 0,00092 | 3/8 |
| 7 | Frekuensi_CR | -0,00098 | 0,00239 | 1/8 |
