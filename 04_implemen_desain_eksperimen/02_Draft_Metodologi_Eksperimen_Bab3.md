# BAB III: METODOLOGI PENELITIAN
## PRE-02: Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas
**Studi Kasus:** Portofolio Modul Pengembangan Super ERP Farm Nation Enterprise (FNE) 2026

---

### 3.1 Kerangka Konseptual dan Alur Penelitian

Penelitian ini mengadopsi pendekatan kuantitatif berbasis *supervised machine learning* dengan fokus pada peramalan probabilitas (*probabilistic forecasting*). Berbeda dengan penelitian konvensional yang memperlakukan prediksi risiko proyek semata-mata sebagai klasifikasi biner diskrit (*Delay vs No-Delay*), penelitian ini memformulasikan permasalahan ke dalam estimasi probabilitas numerik kontinu $P(Y = 1 | \mathbf{x}) \in [0, 1]$ yang terkalibrasi secara statistik.

Alur penelitian dirancang secara bertahap dan sistematis melalui enam tahapan utama:
1. **Identifikasi dan Ekstraksi Data:** Penggalian variabel operasional dan metrik pemantauan dari 8 dokumen *Project Management Plan* (PMP) dan *Software Requirements Specification* (SRS) Super ERP FNE 2026.
2. **Prapemrosesan Data (Preprocessing):** Pemeriksaan integritas data, penanganan nilai hilang, penyeragaman tipe data, dan standarisasi fitur numerik melalui *z-score scaling*.
3. **Penyekatan Data dan Validasi Silang:** Penerapan skema *Stratified 5-Fold Cross-Validation* untuk mengoptimalkan keandalan evaluasi statistik pada dataset berskala terbatas ($N = 26$).
4. **Pelatihan Model Machine Learning:** Pembangunan empat arsitektur model klasifikasi probabilistik: *Logistic Regression* (baseline), *Random Forest*, *Gradient Tree Boosting*, dan *Multi-Layer Perceptron* (MLP).
5. **Kalibrasi Probabilitas:** Penerapan teknik *Platt Scaling* dan *Isotonic Regression* guna mengoreksi deviasi probabilitas keluaran model agar mencerminkan frekuensi empiris sesungguhnya.
6. **Evaluasi dan Optimasi Ambang Batas (Early Warning Thresholding):** Pengujian kinerja melalui metrik diskriminasi (ROC-AUC) dan metrik kalibrasi (*Brier Score*, *Expected Calibration Error*), dilanjutkan dengan penetapan ambang batas peringatan dini multi-tingkat bagi *Project Manager*.

---

### 3.2 Objek Penelitian dan Sumber Data

Objek penelitian ini adalah ekosistem pengembangan perangkat lunak berskala besar (*enterprise software engineering*) bernama **Super ERP Farm Nation Enterprise (FNE)** tahun anggaran 2026. Sistem ini mengintegrasikan seluruh rantai nilai agroindustri sirkular dari hulu ke hilir yang didekomposisi ke dalam delapan sub-proyek independen yang saling terhubung:
1. `P-FNE-01`: Foundation & Core Platform
2. `P-FNE-02`: Core Agricultural Operations
3. `P-FNE-03`: Supply Chain & Procurement
4. `P-FNE-04`: Production & Manufacturing
5. `P-FNE-05`: Commerce, Sales & Logistics
6. `P-FNE-06`: Finance & Human Capital Management
7. `P-FNE-07`: Intelligence & Decision Platform
8. `P-FNE-08`: Advanced & Autonomous Enterprise

Data historis dan rencana pelaksanaan diekstraksi secara langsung dari repositori resmi proyek (`dataset_pre02_fne.csv`) yang mencakup 26 aktivitas/fitur modul tingkat operasional ($N = 26$). Setiap unit data merepresentasikan entitas modul perangkat lunak yang memiliki jadwal, alokasi jam kerja, dependensi arsitektural, dan catatan keterlambatan aktual pada fase monitoring & evaluasi.

---

### 3.3 Operasionalisasi Variabel Penelitian

Variabel dalam penelitian ini diklasifikasikan menjadi variabel bebas (fitur masukan $\mathbf{x}$) dan satu variabel terikat (target luaran $Y$).

#### 3.3.1 Variabel Bebas (Independent Variables)
Variabel bebas merepresentasikan kondisi faktual proyek pada fase pemantauan yang mencakup dimensi waktu, beban kerja, keterkaitan struktural, utilisasi sumber daya manusia, risiko inheren, dan fluktuasi lingkup pekerjaan:

1. **Durasi Rencana ($X_1$ — `Planned_Duration_Days`):**
   Estimasi rentang waktu pengerjaan modul dalam satuan hari kalender kerja sesuai jadwal *baseline* PMP.
2. **Beban Usaha Rencana ($X_2$ — `Planned_Effort_Hours`):**
   Akumulasi estimasi jam kerja personil (*person-hours*) yang dialokasikan untuk menuntaskan modul.
3. **Jumlah Ketergantungan Tugas Pendahulu ($X_3$ — `Predecessor_Count`):**
   Banyaknya aktivitas prasyarat langsung (*immediate predecessors*) yang harus diselesaikan modul lain sebelum modul terkait dapat dieksekusi. Variabel ini mengukur kerentanan modul terhadap perambatan keterlambatan lintas modul (*delay propagation*).
4. **Tingkat Utilisasi Sumber Daya ($X_4$ — `Resource_Utilization_Rate`):**
   Rasio pemanfaatan tim pengembang bersama (*shared developers*) terhadap batas kapasitas normal kerja (100% / 1.0). Diformulasikan sebagai:
   $$\text{Utilization} = \frac{\text{Alokasi Jam Kerja Efektif}}{\text{Kapasitas Standar Pengembang}}$$
   Nilai $> 1.0$ mencerminkan kondisi kelebihan beban (*over-allocation*) yang memicu *bottleneck*.
5. **Skor Risiko Inheren ($X_5$ — `Risk_Score`):**
   Indeks probabilitas-dampak ($P \times I$) dari register risiko modul yang bernilai kontinu antara $0.0$ hingga $1.0$.
6. **Schedule Performance Index ($X_6$ — `SPI_Value`):**
   Metrik kendali jadwal berbasis metode *Earned Value Management* (EVM) PMBOK pada titik kontrol evaluasi:
   $$\text{SPI} = \frac{\text{Earned Value (EV)}}{\text{Planned Value (PV)}}$$
   Nilai $\text{SPI} < 1.0$ menandakan progres aktual berada di belakang rencana jadwal.
7. **Frekuensi Usulan Perubahan ($X_7$ — `Change_Request_Count`):**
   Jumlah permohonan modifikasi spesifikasi kebutuhan atau arsitektur (*scope changes*) yang disetujui selama siklus pengembangan.

#### 3.3.2 Variabel Terikat (Dependent Variable)
Variabel terikat adalah status keterlambatan akhir dari modul proyek:
$$Y = \begin{cases} 1, & \text{jika modul mengalami keterlambatan jadwal penyelesaian} \\ 0, & \text{jika modul selesai tepat waktu atau lebih awal} \end{cases}$$

Model *machine learning* diinstruksikan untuk mempelajari fungsi pemetaan $f: \mathbf{x} \to [0, 1]$ yang menghasilkan taksiran peluang:
$$\hat{p} = P(Y = 1 | \mathbf{x})$$

---

### 3.4 Desain Eksperimen dan Protokol Pemodelan

Eksperimen dirancang secara komparatif melalui empat algoritma terkemuka dengan karakteristik matematis yang berbeda untuk menilai performa diskriminasi dan kualitas probabilitas:

#### 3.4.1 Skenario 1: Logistic Regression (Model Baseline)
*Logistic Regression* bertindak sebagai model acuan dasar (*baseline*). Model ini memodelkan probabilitas kejadian sebagai transformasi linear melalui fungsi sigmoid standar:
$$\hat{p}_{\text{LR}} = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
Bobot diestimasi dengan meminimalkan *log-loss* ditambah penalti $L_2$ (*Ridge regularization*, $C = 1.0$). Karena fungsi objektif ini konveks dan memiliki optimum tunggal, penelitian ini menyelesaikannya hingga konvergen dengan metode Newton-Raphson; solusi yang diperoleh setara dengan solver quasi-Newton L-BFGS (*Limited-memory Broyden–Fletcher–Goldfarb–Shanno*) pada pustaka scikit-learn.

#### 3.4.2 Skenario 2: Random Forest
*Random Forest* merupakan algoritma ensemble berbasis *bagging* (Bootstrap Aggregating) dari sekumpulan pohon keputusan acak (*de-correlated decision trees*). Estimasi probabilitas kelas diperoleh dari rata-rata proporsi kelas delay pada simpul daun (*leaf*) di seluruh $B$ pohon:
$$\hat{p}_{\text{RF}} = \frac{1}{B} \sum_{b=1}^{B} P_b(Y=1|\mathbf{x})$$
Dalam konfigurasi ini digunakan $B = 100$ pohon dengan kedalaman maksimum (*max_depth*) 3 dan $\lfloor\sqrt{7}\rfloor = 2$ fitur acak per percabangan, guna memitigasi risiko penghafalan varians pada dataset berukuran kecil.

#### 3.4.3 Skenario 3: Gradient Tree Boosting
*Gradient Boosting* membangun pohon keputusan secara aditif dan sekuensial dengan meminimalkan gradien residual dari fungsi deviance log-likelihood:
$$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \gamma_m h_m(\mathbf{x})$$
Setiap pohon regresi $h_m$ (kedalaman maksimum 2) dilatih pada pseudo-residual $r_i = y_i - \hat{p}_i$, dan nilai daunnya dihitung dengan langkah Newton $\gamma = \sum r_i / \sum \hat{p}_i(1 - \hat{p}_i)$ (Friedman, 2001). Sebanyak $M = 100$ iterasi dengan *learning rate (shrinkage)* kecil sebesar $\eta = 0.05$ dipadukan dengan *subsampling* baris (0.8) guna memastikan pemodelan tetap berada dalam batas kestabilan non-overfitting.

#### 3.4.4 Skenario 4: Multi-Layer Perceptron (MLP Neural Network)
Model jaringan saraf tiruan lapis-banyak dirancang dengan arsitektur kompak dua lapis tersembunyi ($16 \to 8$). Transformasi non-linear dihitung menggunakan fungsi aktivasi ReLU pada lapis tersembunyi, dan diproyeksikan ke lapis luaran bersel tunggal menggunakan aktivasi sigmoid:
$$\mathbf{h}_1 = \text{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)$$
$$\mathbf{h}_2 = \text{ReLU}(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2)$$
$$\hat{p}_{\text{MLP}} = \sigma(\mathbf{w}_3^T \mathbf{h}_2 + b_3)$$
Optimasi bobot menggunakan algoritma Adam (*Adaptive Moment Estimation*; laju belajar 0.01, 1000 iterasi *full-batch*) dengan koefisien regularisasi bobot $\alpha = 0.01$.

---

### 3.5 Protokol Validasi dan Isolasi Data

Untuk mencegah fenomena kebocoran data (*data leakage*) dan bias optimasi:
1. **Stratified 5-Fold Cross-Validation:** Dataset disekat ke dalam 5 lipatan (*folds*) dengan mempertahankan proporsi kelas asli pada tiap lipatan (rasio $\approx 61.5\%$ kelas delay : $38.5\%$ kelas tepat waktu).
2. **Transformasi Fitur Terisolasi:** Estimasi rata-rata ($\mu$) dan simpangan baku ($\sigma$) untuk standardisasi fitur dihitung murni pada lipatan data latih (*training fold*), lalu diterapkan pada lipatan data uji (*test fold*).
3. **Replikasi Eksperimen:** Seluruh generator bilangan acak dikunci menggunakan *seed* bernilai 42 (`random_state=42`).
4. **Validasi Pembanding (Hold-out 80:20):** Sebagai pembanding operasional, dilakukan satu kali pemisahan *stratified train-test* 80:20 (21 task latih : 5 task uji). Mengingat data uji hanya berisi 5 task, hasil ini diperlakukan sebagai indikasi dan tidak digunakan untuk pemilihan model.

---

### 3.6 Metode Kalibrasi Probabilitas (Skenario 5)

Mengingat model ensemble seperti Random Forest cenderung menghasilkan probabilitas yang terdistorsi ke arah nilai tengah ($0.3 - 0.7$), kalibrasi probabilitas pasca-pelatihan (*post-hoc calibration*) diterapkan menggunakan dua pendekatan:
1. **Platt Scaling (Sigmoid Model):** Melatih model regresi logistik univariat terhadap keluaran tak terkalibrasi $f(\mathbf{x})$:
   $$\hat{p}_{\text{cal}} = \frac{1}{1 + \exp(A f(\mathbf{x}) + B)}$$
2. **Isotonic Regression:** Metode non-parametrik yang memasang fungsi tangga monotonik naik (*piecewise constant non-decreasing function*) guna meminimalkan kuadrat selisih antara probabilitas terkalibrasi dan label empiris:
   $$\min \sum (y_i - m(f_i))^2 \quad \text{dengan syarat } m(f_i) \le m(f_j) \text{ untuk } f_i \le f_j$$

Agar tidak terjadi kebocoran data, kalibrator tidak pernah dilatih pada data uji. Di dalam setiap fold training, prediksi *out-of-fold* terlebih dahulu dihasilkan melalui *inner stratified 3-fold cross-validation*; kalibrator dilatih pada prediksi tersebut, kemudian model dasar dilatih ulang pada seluruh fold training dan kalibrator diterapkan pada keluaran model untuk fold uji. Kombinasi model × metode kalibrasi (Raw, Platt, Isotonic) dengan *Brier Score* terendah ditetapkan sebagai **model rekomendasi**; jika terdapat nilai yang sama, digunakan ECE lalu *Log Loss* sebagai penentu.

---

### 3.7 Metrik Evaluasi Kinerja Eksperimen

Evaluasi performa dilakukan secara komprehensif mencakup dua dimensi:

#### 3.7.1 Dimensi Kualitas Probabilitas
1. **Brier Score (BS):**
   $$BS = \frac{1}{N} \sum_{i=1}^{N} (\hat{p}_i - y_i)^2$$
   Nilai $BS \in [0, 1]$, di mana nilai mendekati 0 mencerminkan akurasi estimasi probabilitas yang semakin presisi.
2. **Logarithmic Loss (Cross-Entropy):**
   $$\text{LogLoss} = -\frac{1}{N} \sum_{i=1}^{N} [y_i \ln(\hat{p}_i) + (1 - y_i) \ln(1 - \hat{p}_i)]$$
   Mengukur penalti eksponensial terhadap estimasi probabilitas yang sangat yakin tetapi tidak sesuai dengan hasil aktual.
3. **Expected Calibration Error (ECE):**
   $$ECE = \sum_{m=1}^{M} \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
   Dengan $M = 5$ bin interval probabilitas berlebar sama (jumlah bin dibatasi karena $N = 26$), mengukur deviasi absolut antara rata-rata akurasi faktual terhadap rata-rata estimasi keyakinan probabilitas model.

#### 3.7.2 Dimensi Diskriminasi Klasifikasi
1. **Area Under ROC Curve (ROC-AUC):**
   Menilai kapasitas pemisahan model terhadap pasangan instansi positif dan negatif di seluruh spektrum nilai ambang batas.
2. **Sensitivity (Recall) dan Specificity:**
   Mengukur daya deteksi keterlambatan riil versus ketahanan model dari alarm palsu (*false positive*).
3. **F1-Score:**
   Rata-rata harmonik antara *Precision* dan *Recall* pada ambang batas operasional.

---

### 3.8 Mekanisme Ambang Batas Peringatan Dini (Early Warning Decision Rule)

Untuk menerjemahkan keluaran probabilitas numerik menjadi kebijakan manajerial yang dapat ditindaklanjuti (*actionable insight*), dilakukan analisis ambang batas menggunakan indeks Youden ($J = \text{Sensitivity} + \text{Specificity} - 1$) pada model rekomendasi; ambang $\theta^* = \arg\max J$ dilaporkan sebagai titik potong biner optimal. Untuk keperluan operasional, luaran sistem dikelompokkan ke dalam tiga zona mitigasi dengan batas tetap:

| Zona Peringatan | Rentang Probabilitas $P(\text{Delay})$ | Implikasi Risiko | Rekomendasi Manajerial bagi Project Manager |
| :---: | :---: | :---: | :--- |
| **Zona Hijau**<br>*(Low Risk)* | $0.00 \le \hat{p} < 0.35$ | Terkendali | Pemantauan rutin tanpa intervensi alokasi sumber daya tambahan. |
| **Zona Kuning**<br>*(Moderate Risk / Watchlist)* | $0.35 \le \hat{p} < 0.65$ | Rawan Keterlambatan | Koordinasi intensif antar-pimpinan modul, pembekuan perubahan lingkup (*scope lock*), dan audit kesiapan dependensi pendahulu. |
| **Zona Merah**<br>*(Critical Alert)* | $0.65 \le \hat{p} \le 1.00$ | Keterlambatan Sangat Pasti | Intervensi aktif: perbanyakan alokasi developer (*crashing*), penataan ulang jadwal (*fast-tracking*), atau pemotongan lingkup non-esensial ke rilis berikutnya. |

---

### 3.9 Keterbatasan Desain Penelitian

1. **Ukuran sampel terbatas ($N = 26$).** Setiap fold uji pada *5-fold cross-validation* hanya memuat sekitar 5 task, sehingga estimasi metrik memiliki varians yang tinggi dan perbedaan kecil antar-model tidak dapat dianggap signifikan secara statistik.
2. **Sifat data empiris-simulatif.** Data disusun dari dokumen perencanaan proyek FNE, bukan dari rekaman historis multi-proyek. Nilai ROC-AUC yang mendekati 1.0 mengindikasikan kelas hampir terpisah sempurna pada data ini, sehingga temuan perlu divalidasi ulang pada data proyek riil sebelum digeneralisasi.
3. **Kalibrasi pada sampel kecil.** Kalibrator hanya dilatih pada sekitar 20 sampel per fold. *Isotonic Regression* rawan *overfitting* pada ukuran ini, sedangkan *Platt Scaling* lebih stabil karena hanya memiliki dua parameter (Niculescu-Mizil & Caruana, 2005).
4. **Estimasi sedikit optimistis.** Pemilihan model rekomendasi dan ambang $\theta^*$ dilakukan pada prediksi *out-of-fold* yang sama dengan yang dilaporkan, tanpa lapisan validasi terpisah.
