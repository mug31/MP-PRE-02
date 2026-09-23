# BAB II: TINJAUAN PUSTAKA DAN LANDASAN TEORI

## 2.1. Manajemen Multiproyek dengan Sumber Daya Terbatas (*Resource-Constrained Multi-Project Management*)

Dalam lingkungan industri modern, implementasi sistem teknologi informasi berskala masif umumnya dipecah menjadi beberapa sub-proyek independen yang dieksekusi secara simultan di bawah satu portofolio terpadu (*mega-enterprise system*). Kondisi ini secara teoritis dikenal sebagai *Resource-Constrained Multi-Project Scheduling Problem* (RCMPSP) (Browning & Yassine, 2010). Karakteristik utama dari lingkungan ini adalah keberadaan sumber daya kritis (*shared resources*)—seperti arsitek sistem, tim *DevOps*, atau infrastruktur bersama—yang dialokasikan ke berbagai sub-proyek sekaligus.

Ketika suatu aktivitas mengalami peningkatan beban kerja (*effort overrun*) atau terjadi perubahan kebutuhan (*change request*), alokasi sumber daya bersama tersebut dapat melampaui kapasitas normal (*resource overallocation* / utilisasi > 1.0). Browning & Yassine (2010) menggarisbawahi bahwa hambatan pada sumber daya bersama (*resource bottlenecks*) tidak hanya berdampak lokal pada aktivitas yang bersangkutan, melainkan memicu efek domino keterlambatan (*cascading delays*) ke aktivitas hilir maupun sub-proyek lain yang saling terhubung melalui dependensi tugas (*predecessor-successor relationships*).

---

## 2.2. Pendekatan Tradisional Pengawasan Kinerja: *Earned Value Management* (EVM) dan Batasannya

Secara konvensional, pengendalian dan pemantauan kinerja proyek bersandar pada metodologi *Earned Value Management* (EVM) yang mengintegrasikan aspek lingkup (*scope*), waktu (*time*), dan biaya (*cost*) (Project Management Institute, 2021). Salah satu indikator fundamental EVM dalam menilai kesehatan jadwal adalah *Schedule Performance Index* ($SPI$), yang dirumuskan sebagai:

$$SPI = \frac{EV}{PV}$$

Di mana $EV$ (*Earned Value*) mencerminkan nilai pekerjaan yang telah terselesaikan secara riil, dan $PV$ (*Planned Value*) merepresentasikan rencana nilai pekerjaan yang seharusnya diselesaikan pada titik waktu evaluasi. Nilai $SPI < 1.0$ mengindikasikan bahwa laju pengerjaan proyek berada di belakang jadwal yang direncanakan.

Meskipun $SPI$ dan ekstensinya—seperti *Earned Schedule* ($ES$) dan *Earned Duration* ($ED$)—terbukti berguna dalam evaluasi deterministik (Batselier & Vanhoucke, 2015), pendekatan ini memiliki keterbatasan intrinsik yang signifikan:
1. **Asumsi Linieritas:** EVM mengasumsikan tren kinerja masa lalu akan berlanjut secara linier ke masa depan, mengabaikan kompleksitas interdependensi jaringan kerja (*network topology*).
2. **Ketiadaan Informasi Ketidakpastian:** EVM hanya menghasilkan estimasi titik deterministik tunggal (misal estimasi waktu penyelesaian akhir / $EAC_t$) tanpa menyajikan derajat keyakinan atau distribusi probabilitas kegagalan.
3. **Sifat Reaktif:** Metrik EVM merupakan indikator tertinggal (*lagging indicator*) yang baru mendeteksi anomali setelah defiasi fisik terjadi, sehingga membatasi ruang tindakan preventif.

---

## 2.3. Pendekatan *Machine Learning* dalam Prediksi Keterlambatan Proyek

Untuk mengatasi kelemahan model deterministik, penelitian manajemen proyek dekade terakhir mulai mengadopsi algoritma kecerdasan buatan dan *Machine Learning* (Wauters & Vanhoucke, 2016; Choetkiertikul et al., 2017). Berbagai algoritma pembelajaran terarah (*supervised learning*) diterapkan untuk memetakan pola non-linear antara kondisi operasional proyek dengan hasil keterlambatan:

*   **Logistic Regression (LR):** Digunakan secara luas sebagai model *baseline* parametrik. Keunggulan utamanya terletak pada sifat interpretabilitas bobot koefisien dan fungsi logistik (sigmoid) yang secara alami memetakan kombinasi linier fitur ke interval probabilitas $[0, 1]$ (Niculescu-Mizil & Caruana, 2005).
*   **Random Forest (RF):** Merupakan metode *ensemble learning* berbasis *bagging* sejumlah pohon keputusan (*decision trees*). RF terbukti tangguh terhadap fenomena *overfitting* serta mampu menangkap interaksi non-linear tingkat tinggi antar-fitur seperti skor risiko dan frekuensi revisi (Choetkiertikul et al., 2017). Estimasi probabilitas kelas diperoleh melalui agregasi proporsi suara (*vote fraction*) dari seluruh pohon estimator via fungsi `predict_proba`.
*   **Gradient Boosting Machine (GBM):** Membangun pohon keputusan secara sekuensial dengan mengoptimalkan fungsi kerugian (*loss function*). GBM kerap kali menghasilkan daya diskriminasi (*discriminative power*) tertinggi dalam data tabular kompleks (Gondia et al., 2020).
*   **Artificial Neural Networks (ANN):** Mampu memodelkan fungsi aproksimasi non-linear yang sangat fleksibel melalui arsitektur multi-lapisan (*feedforward layers*). Dengan aktivasi output bertipe *sigmoid*, jaringan saraf menghasilkan nilai kontinu antara 0 dan 1 yang merepresentasikan estimasi peluang terjadinya keterlambatan (Wauters & Vanhoucke, 2016).

---

## 2.4. Teori Kalibrasi Probabilitas dan Evaluasi Model Probabilistik

Sebagian besar penelitian klasifikasi terfokus hanya pada metrik diskriminasi seperti *Accuracy*, *F1-score*, atau *Area Under the ROC Curve* ($AUC$). Namun, dalam konteks pengambilan keputusan manajerial, nilai luaran probabilitas tidak hanya dituntut mampu memisahkan kelas (diskriminasi), melainkan harus mencerminkan frekuensi empiris sesungguhnya—kondisi ini disebut **probabilitas yang terkalibrasi dengan baik (*well-calibrated probability*)** (Niculescu-Mizil & Caruana, 2005; Guo et al., 2017).

Sebagai contoh, jika sebuah model memprediksi 100 aktivitas proyek memiliki probabilitas keterlambatan sebesar $0.80$, maka secara aktual sekitar 80 dari 100 aktivitas tersebut harus benar-benar mengalami keterlambatan. Jika hanya 40 aktivitas yang terlambat, model tersebut mengalami *overconfidence* yang parah.

Untuk mengevaluasi dan membandingkan kualitas probabilitas yang dihasilkan oleh model, penelitian ini mengadopsi instrumen evaluasi probabilistic terstandar:

### 1. Brier Score
Dirumuskan oleh Glenn W. Brier (1950), *Brier Score* ($BS$) mengukur rata-rata kuadrat selisih antara probabilitas prediksi ($p_i$) dan label biner aktual ($y_i \in \{0, 1\}$):

$$BS = \frac{1}{N} \sum_{i=1}^{N} (p_i - y_i)^2$$

Nilai $BS$ berkisar antara $0$ (kalibrasi sempurna) hingga $1$ (prediksi selalu salah total). Metrik ini dapat didekomposisi menjadi komponen reliabilitas, resolusi, dan ketidakpastian (*uncertainty*).

### 2. Logarithmic Loss (*Log Loss* / *Cross-Entropy*)
*Log Loss* memberikan penalti eksponensial terhadap prediksi probabilitas yang sangat percaya diri tetapi keliru:

$$\text{Log Loss} = -\frac{1}{N} \sum_{i=1}^{N} \Big[ y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i) \Big]$$

### 3. Diagram Reliabilitas (*Calibration Curve*) dan *Expected Calibration Error* (ECE)
Diagram reliabilitas membagi rentang prediksi $[0, 1]$ ke dalam sejumlah $M$ interval (*bins*). Untuk setiap bin $B_m$, dihitung rata-rata probabilitas prediksi ($\text{conf}(B_m)$) dibandingkan dengan proporsi positif aktual ($\text{acc}(B_m)$). Besaran deviasi kalibrasi dirangkum ke dalam metrik *Expected Calibration Error* (ECE) (Guo et al., 2017):

$$\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \Big| \text{acc}(B_m) - \text{conf}(B_m) \Big|$$

---

## 2.5. Sistem Peringatan Dini (*Early Warning System*) Berbasis *Threshold* Probabilitas

Penerapan luaran probabilitas terkalibrasi menjadi fondasi krusial bagi perancangan sistem peringatan dini (*early warning system* / EWS) (Cabanillas et al., 2014). Berbeda dengan sistem biner dengan batas tetap $0.5$, EWS adaptif memungkinkan *Project Manager* menetapkan ambang batas peringatan (*warning thresholds*) berdasarkan matriks dampak dan toleransi risiko organisasi:

*   **Zona Hijau ($P < \tau_{\text{low}}$):** Aktivitas berjalan stabil, tidak memerlukan intervensi.
*   **Zona Kuning / Waspada ($\tau_{\text{low}} \le P < \tau_{\text{high}}$):** Terdeteksi gejala penyimpangan (misal: utilisasi mulai melebihi kapasitas atau terjadi akumulasi *predecessor delay*); sistem menyarankan peninjauan ulang sumber daya.
*   **Zona Merah / Bahaya ($P \ge \tau_{\text{high}}$):** Peluang keterlambatan sangat tinggi; sistem memicu eskalasi darurat, seperti penambahan kapasitas (*crashing*), penataan ulang jadwal (*fast-tracking*), atau penyesuaian *backlog*.

Melalui analisis kurva presisi-sensitivitas (*Precision-Recall Tradeoff*), nilai ambang batas $\tau$ dapat dioptimasi guna meminimalkan *false alarm rate* (alarm palsu yang membebani tim) sekaligus memaksimalkan deteksi dini sebelum batas waktu terlampaui.

Pada penelitian PRE-02, ambang operasional tersebut ditetapkan secara konsisten di seluruh bab sebagai $\tau_{\text{low}} = 0.35$ dan $\tau_{\text{high}} = 0.65$, sehingga zonasi yang dipakai adalah **Hijau ($P < 0.35$)**, **Kuning ($0.35 \le P < 0.65$)**, dan **Merah ($P \ge 0.65$)**. Nilai ini merupakan ambang tindakan manajerial (*action threshold*) yang dirancang pada tahap desain eksperimen, dan dilaporkan terpisah dari ambang optimal statistik hasil analisis *Youden J* pada tahap evaluasi.

---

## 2.6. Perumusan *Research Gap* dan Posisi Penelitian PRE-02

Melalui sintesis kritis terhadap literatur yang telah dipaparkan pada Sub-bab 2.1 hingga 2.5, diidentifikasi tiga celah penelitian (*research gaps*) utama:

1.  **Kesenjangan Representasi Luaran (Label Diskret vs Probabilitas Kontinu Terkalibrasi):**
    Sebagian besar penelitian terdahulu (misal Choetkiertikul et al., 2017; Gondia et al., 2020) mengklasifikasikan keterlambatan ke dalam label kategorial kaku (*Delay* / *No Delay* atau *Low/Med/High*). Pendekatan ini menghilangkan informasi nuansa derajat kepastian. Penelitian **PRE-02** mengisi celah ini dengan merekayasa model yang menghasilkan probabilitas numerik kontinu $[0, 1]$ yang teruji kalibrasinya.
2.  **Kesenjangan Konteks Interdependensi Multiproyek:**
    Banyak model prediktif terdahulu dievaluasi pada proyek perangkat lunak tunggal (*isolated single projects*). PRE-02 menempatkan objek kajian pada ekosistem multiproyek berskala *enterprise* (**Super ERP Farm Nation Enterprise 2026**), di mana faktor *resource utilization rate*, jumlah *predecessor*, skor risiko, dan frekuensi *change request* saling berinteraksi lintas 8 sub-proyek.
3.  **Ketiadaan Pengujian Kalibrasi dan Metrik Brier Score pada EWS Proyek:**
    Evaluasi model ML pada literatur manajemen proyek hampir selalu terbatas pada akurasi dan AUC, tanpa memverifikasi apakah probabilitas tersebut mencerminkan probabilitas empiris riil. PRE-02 secara eksplisit menjadikan *Brier Score*, *Log Loss*, *ECE*, dan *Calibration Curves* sebagai tolok ukur utama dalam menyeleksi algoritma terbaik untuk operasionalisasi *early warning system*.
