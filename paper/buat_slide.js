// PRE-02: slide presentasi hasil penelitian (Pertemuan 8).
// Jalankan: NODE_PATH=<folder node_modules berisi pptxgenjs> node buat_slide.js
// Semua angka diambil dari 04_implemen_desain_eksperimen/hasil_eksperimen dan hasil_analisis (lihat paper).
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.APPLY_THEME);

const HERE = __dirname;
const ROOT = path.join(HERE, "..");
const OUT = path.join(HERE, "Presentasi_Hasil_PRE02.pptx");

const THEME = {
  name: "PRE02 Teal Amber",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2A2F", lt1: "FFFFFF", dk2: "0F3D3E", lt2: "EAF2F1",
    accent1: "0F7173", accent2: "F2A541", accent3: "C8553D", accent4: "7A9E9F",
    accent5: "4F6D7A", accent6: "B8C5C6", hlink: "0F7173", folHlink: "4F6D7A",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.title = "Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas";
pres.author = "Muktibaskara Kusbianto, Muhammad Abdillah Kais Al Akmal, Muhammad Ainul Yaqin";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

pres.defineSlideMaster({
  title: "Judul Gelap",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.9, fontSize: 40, bold: true, color: C.background1, valign: "bottom" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.1, w: 11.7, h: 2.2, fontSize: 18, color: C.background2, valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Konten",
  background: { color: C.background1 },
  margin: [0.5, 0.6, 0.6, 0.6],
  slideNumber: { x: 12.4, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: C.accent5 },
  objects: [
    { text: { text: "PRE-02 · Jurnal Pustaka Data", options: { x: 0.6, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: C.accent5, isTextBox: true } } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 32, bold: true, color: C.text2, valign: "middle" }, text: "" } },
  ],
});

const T = (slide, text, opt) => slide.addText(text, Object.assign({ isTextBox: true, fontSize: 16, color: C.text1, margin: 0.05 }, opt));
const kartu = (slide, x, y, w, h, fill) =>
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill || C.background2 }, line: { color: fill || C.background2 }, rectRadius: 0.12 });
const lingkaran = (slide, x, y, teks, fill) => {
  slide.addShape(pres.shapes.OVAL, { x, y, w: 0.6, h: 0.6, fill: { color: fill || C.accent1 }, line: { color: fill || C.accent1 } });
  T(slide, teks, { x, y, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0 });
};
const angka = (slide, x, y, w, nilai, label, warna, ukuran) => {
  T(slide, nilai, { x, y, w, h: 0.9, fontSize: ukuran || 44, bold: true, color: warna || C.accent1, fontFace: "Cambria", margin: 0 });
  T(slide, label, { x, y: y + 0.9, w, h: 0.7, fontSize: 14, color: C.text1, margin: 0, valign: "top" });
};
const sumbuGaya = (extra) => Object.assign({
  catAxisLabelColor: HEX.dk1, valAxisLabelColor: HEX.dk1, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 11,
  valGridLine: { color: "D9E2E2", size: 0.75 }, catGridLine: { style: "none" }, titleFontFace: "+mn-lt",
}, extra);

// 1. Judul ----------------------------------------------------------------------------------------
pres.addSection({ title: "Pembuka" });
let s = pres.addSlide({ masterName: "Judul Gelap", sectionTitle: "Pembuka" });
s.addText("Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas", { placeholder: "title" });
s.addText([
  { text: "Muktibaskara Kusbianto, Muhammad Abdillah Kais Al Akmal, Muhammad Ainul Yaqin", options: { breakLine: true } },
  { text: "Fakultas Sains dan Teknologi, UIN Maulana Malik Ibrahim Malang", options: { breakLine: true, fontSize: 14 } },
  { text: "Studi kasus: 8 subproyek Super ERP Farm Nation Enterprise", options: { fontSize: 14 } },
], { placeholder: "body" });
s.addNotes("Presentasi hasil penelitian PRE-02 untuk naskah Jurnal Pustaka Data.");

// 2. Masalah ----------------------------------------------------------------------------------------
pres.addSection({ title: "Latar belakang" });
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Latar belakang" });
s.addText("Manajer proyek butuh peluang telat, bukan sekadar label", { placeholder: "title" });
const masalah = [
  ["1", "Sumber daya dipakai bersama", "Keterlambatan satu aktivitas menahan aktivitas lain yang menunggu orang yang sama"],
  ["2", "EVM memberi satu angka", "Ramalan durasi deterministik, tanpa tingkat keyakinan"],
  ["3", "Model ML jarang dicek kalibrasinya", "Probabilitas 0,8 hanya bermakna bila ±80% proyek dengan nilai itu benar-benar telat"],
];
masalah.forEach(([n, judul, isi], i) => {
  const y = 1.6 + i * 1.6;
  lingkaran(s, 0.8, y + 0.1, n);
  T(s, judul, { x: 1.7, y, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
  T(s, isi, { x: 1.7, y: y + 0.5, w: 5.6, h: 0.8, fontSize: 15 });
});
kartu(s, 7.8, 1.6, 4.9, 4.6, C.text2);
T(s, "Tujuan penelitian", { x: 8.1, y: 1.85, w: 4.3, h: 0.5, fontSize: 18, bold: true, color: C.accent2 });
T(s, "Membangun dan membandingkan model yang memprediksi probabilitas keterlambatan > 5% dari baseline, dari kondisi proyek saat monitoring, lalu menguji kalibrasinya dan menentukan ambang peringatan dini.",
  { x: 8.1, y: 2.45, w: 4.3, h: 3.4, fontSize: 17, color: C.background1, valign: "top" });

// 3. Data -------------------------------------------------------------------------------------------
pres.addSection({ title: "Metode" });
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Metode" });
s.addText("Data historis dibangkitkan dari dokumen PMP", { placeholder: "title" });
const alur = [
  ["8 PMP", "337 aktivitas, sumber daya per peran, 171 risiko"],
  ["Simulasi", "1.000 iterasi random per subproyek: CR 10%, risiko sesuai register, antrean FCFS"],
  ["Monitoring", "Kondisi dicatat di 25%, 50%, 75% jadwal; hanya info s.d. hari itu"],
  ["Dataset", "24.000 observasi, 7 variabel, label telat > 5% (44,8%)"],
];
alur.forEach(([judul, isi], i) => {
  const x = 0.6 + i * 3.15;
  kartu(s, x, 1.7, 2.85, 3.0);
  T(s, judul, { x: x + 0.2, y: 1.9, w: 2.45, h: 0.6, fontSize: 22, bold: true, color: C.accent1, fontFace: "Cambria" });
  T(s, isi, { x: x + 0.2, y: 2.6, w: 2.45, h: 1.9, fontSize: 15, valign: "top" });
  if (i < 3) T(s, "→", { x: x + 2.85, y: 2.85, w: 0.3, h: 0.5, fontSize: 22, color: C.accent2, align: "center", margin: 0 });
});
T(s, "Faktor dampak risiko f = 0,4 dipilih agar median keterlambatan P-FNE-08 (+5,3%) cocok dengan analisis risiko kuantitatif PMP-08 (P50: 21 dari 20 minggu).",
  { x: 0.6, y: 5.1, w: 12.1, h: 0.9, fontSize: 15, italic: true, color: C.accent5 });

// 4. Desain eksperimen ------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Metode" });
s.addText("Empat model, tiga cara kalibrasi, diuji per subproyek", { placeholder: "title" });
const model = [["LR", "Logistic Regression"], ["RF", "Random Forest"], ["GB", "Gradient Boosting"], ["NN", "Neural Network sigmoid"]];
model.forEach(([k, nama], i) => {
  const y = 1.6 + i * 1.05;
  lingkaran(s, 0.8, y, k.length > 1 ? k : k, i === 2 ? C.accent2 : C.accent1);
  T(s, nama, { x: 1.6, y, w: 4.2, h: 0.6, fontSize: 18, valign: "middle" });
});
kartu(s, 6.3, 1.6, 6.4, 1.5);
T(s, "Validasi leave-one-subproject-out", { x: 6.55, y: 1.7, w: 5.9, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
T(s, "Latih di 7 subproyek, uji di subproyek ke-8, ulang 8 kali", { x: 6.55, y: 2.25, w: 5.9, h: 0.7, fontSize: 15 });
kartu(s, 6.3, 3.3, 6.4, 1.5);
T(s, "Kalibrasi: Raw, Platt, Isotonic", { x: 6.55, y: 3.4, w: 5.9, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
T(s, "Kalibrator dilatih dari subproyek lain di data latih", { x: 6.55, y: 3.95, w: 5.9, h: 0.7, fontSize: 15 });
kartu(s, 6.3, 5.0, 6.4, 1.5);
T(s, "Metrik & uji", { x: 6.55, y: 5.1, w: 5.9, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
T(s, "Brier, BSS, ECE, ROC-AUC · bootstrap 2.000× · Holm · Wilcoxon", { x: 6.55, y: 5.65, w: 5.9, h: 0.7, fontSize: 15 });

// 5. Hasil: model terbaik -----------------------------------------------------------------------------
pres.addSection({ title: "Hasil" });
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Hasil" });
s.addText("Gradient Boosting paling akurat dan paling terkalibrasi", { placeholder: "title" });
s.addChart(pres.charts.BAR, [{ name: "Brier score", labels: ["Naif", "LR", "RF", "GB", "NN"], values: [0.2715, 0.1958, 0.1761, 0.1718, 0.2859] }],
  sumbuGaya({ x: 0.6, y: 1.5, w: 7.4, h: 5.2, barDir: "col", chartColors: [HEX.accent6, HEX.accent4, HEX.accent4, HEX.accent1, HEX.accent3],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.000", dataLabelColor: HEX.dk1, valAxisMinVal: 0, valAxisMaxVal: 0.32,
    valAxisLabelFormatCode: "0.00", showTitle: true, title: "Brier score (makin kecil makin baik)", titleColor: HEX.dk1, titleFontSize: 14, showLegend: false, varyColors: true }));
angka(s, 8.5, 1.6, 4.2, "0,367", "Brier skill score GB: 37% lebih akurat dari tebakan naif");
angka(s, 8.5, 3.3, 4.2, "0,056", "ECE GB: selisih rata-rata probabilitas vs kejadian aktual");
angka(s, 8.5, 5.0, 4.2, "0,815", "ROC-AUC GB (RF 0,818, setara)");
s.addNotes("Selisih Brier GB vs RF -0,0043 [-0,0066; -0,0020], signifikan. NN BSS negatif (-0,053).");

// 6. Kalibrasi -----------------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Hasil" });
s.addText("Kalibrasi tambahan malah memperburuk", { placeholder: "title" });
s.addImage({ path: path.join(ROOT, "04_implemen_desain_eksperimen/hasil_eksperimen/kurva_kalibrasi_probabilitas.png"), x: 0.6, y: 1.5, w: 7.7, h: 3.5, altText: "Reliability diagram empat model dan efek kalibrasi pada GB" });
T(s, "Kiri: kurva makin dekat garis diagonal = makin terkalibrasi. Kanan: Platt dan Isotonic menjauhkan GB dari diagonal.", { x: 0.6, y: 5.1, w: 7.7, h: 0.8, fontSize: 12, color: C.accent5 });
kartu(s, 8.7, 1.5, 4.0, 4.9);
T(s, "Kenapa?", { x: 8.95, y: 1.65, w: 3.5, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
T(s, [
  { text: "Kalibrasi tidak berpindah antarproyek", options: { bold: true, breakLine: true } },
  { text: "ECE GB 0,16 → 0,20 bila Platt dilatih dari proyek lain; 0,03 bila dari proyek sendiri", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 8 } },
  { text: "GB sudah terkalibrasi", options: { bold: true, breakLine: true } },
  { text: "Model yang sudah baik tidak butuh kalibrasi lagi (Niculescu-Mizil & Caruana, 2005)" },
], { x: 8.95, y: 2.2, w: 3.5, h: 4.0, fontSize: 15, valign: "top" });

// 7. Hipotesis -----------------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Hasil" });
s.addText("Hasil uji hipotesis", { placeholder: "title" });
const hdr = (t) => ({ text: t, options: { bold: true, color: HEX.lt1, fill: { color: HEX.dk2 } } });
const warnaKeputusan = { "Diterima": HEX.accent1, "Diterima sebagian": "B07A1E", "Ditolak": HEX.accent3 };
const baris = [
  ["H1", "LR lebih akurat dari naif dan terkalibrasi", "Diterima sebagian", "Lebih akurat, tetapi slope 0,586 (terlalu ekstrem)"],
  ["H2", "RF lebih akurat dari LR", "Diterima", "Brier −0,0197"],
  ["H3", "GB Brier & ECE terkecil", "Diterima", "Unggul di 6 dari 6 uji"],
  ["H4", "NN lebih akurat dari LR", "Ditolak", "NN terlalu yakin: 27% prediksi ekstrem"],
  ["H5", "Platt/Isotonic menurunkan ECE", "Ditolak", "Hanya membaik pada NN"],
];
s.addTable([[hdr("Kode"), hdr("Hipotesis"), hdr("Keputusan"), hdr("Bukti")]].concat(baris.map(([k, h, d, b]) => [
  { text: k, options: { bold: true } }, h, { text: d, options: { bold: true, color: warnaKeputusan[d] } }, b])),
  { x: 0.6, y: 1.5, w: 12.1, colW: [0.9, 4.4, 2.3, 4.5], fontSize: 15, fontFace: "Calibri", color: HEX.dk1, border: { type: "solid", pt: 0.75, color: "D9E2E2" }, rowH: 0.7, valign: "middle" });
T(s, "Keunggulan signifikan pada gabungan iterasi, tetapi tidak konsisten di setiap subproyek (uji Wilcoxon): GB > RF hanya di 5 dari 8 subproyek.",
  { x: 0.6, y: 5.9, w: 12.1, h: 0.8, fontSize: 15, italic: true, color: C.accent5 });

// 8. Per titik monitoring -------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Hasil" });
s.addText("Makin lama proyek berjalan, makin tepat prediksinya", { placeholder: "title" });
s.addChart(pres.charts.LINE, [
  { name: "GB", labels: ["25%", "50%", "75%"], values: [0.725, 0.782, 0.915] },
  { name: "RF", labels: ["25%", "50%", "75%"], values: [0.721, 0.762, 0.933] },
  { name: "LR", labels: ["25%", "50%", "75%"], values: [0.734, 0.762, 0.865] },
  { name: "NN", labels: ["25%", "50%", "75%"], values: [0.558, 0.616, 0.895] },
], sumbuGaya({ x: 0.6, y: 1.5, w: 7.6, h: 5.2, chartColors: [HEX.accent1, HEX.accent2, HEX.accent5, HEX.accent3], lineSize: 3, lineDataSymbolSize: 9,
  valAxisMinVal: 0.5, valAxisMaxVal: 1.0, valAxisLabelFormatCode: "0.00", showLegend: true, legendPos: "b", legendFontFace: "+mn-lt", legendFontSize: 12,
  showTitle: true, title: "ROC-AUC per titik monitoring (% jadwal rencana)", titleColor: HEX.dk1, titleFontSize: 14 }));
angka(s, 8.7, 1.7, 4.0, "0,725 → 0,915", "ROC-AUC GB dari seperempat ke tiga perempat jadwal", undefined, 30);
T(s, "Peringatan dini memberi waktu bertindak lebih panjang, tetapi lebih sering keliru. Sejalan dengan Kula dkk. (2023): prediksi makin akurat saat informasi bertambah.",
  { x: 8.7, y: 3.6, w: 4.0, h: 2.6, fontSize: 15, valign: "top" });

// 9. Peringatan dini -----------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Hasil" });
s.addText("Peringatan dini: separuh proyek telat terdeteksi di awal", { placeholder: "title" });
angka(s, 0.6, 1.6, 3.8, "56,7%", "proyek yang akhirnya telat sudah diperingatkan pada titik 25% (ambang 0,485)");
angka(s, 4.7, 1.6, 3.8, "81,0%", "sudah pernah diperingatkan sampai titik 75%");
angka(s, 8.8, 1.6, 3.8, "38,0%", "proyek tepat waktu pernah dapat peringatan palsu", C.accent3);
const zona = [["Hijau", "P < 0,35", "Pemantauan rutin", "7A9E9F"], ["Kuning", "0,35 – 0,65", "Pantau ketat, tindakan ringan", "D9A43B"], ["Merah", "P ≥ 0,65", "Tindakan mahal, eskalasi", "C8553D"]];
zona.forEach(([n, r, aksi, warna], i) => {
  const x = 0.6 + i * 4.1;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.0, w: 3.8, h: 1.7, fill: { color: warna }, line: { color: warna }, rectRadius: 0.12 });
  T(s, `${n} · ${r}`, { x: x + 0.2, y: 4.15, w: 3.4, h: 0.6, fontSize: 18, bold: true, color: C.background1 });
  T(s, aksi, { x: x + 0.2, y: 4.8, w: 3.4, h: 0.7, fontSize: 15, color: C.background1 });
});
T(s, "Peringatan palsu umumnya proyek yang nyaris telat: median keterlambatan 3,6% (ambang 5%).", { x: 0.6, y: 6.0, w: 12.1, h: 0.6, fontSize: 15, italic: true, color: C.accent5 });

// 10. Variabel berpengaruh ------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Hasil" });
s.addText("SPI jadwal adalah sinyal paling kuat", { placeholder: "title" });
s.addChart(pres.charts.BAR, [{ name: "Kenaikan Brier saat variabel diacak", labels: ["Frekuensi CR (−0,0010)", "Pergeseran dependency (−0,0003)", "Risiko belum dimitigasi (0,0000)", "Utilisasi sumber daya (0,0014)", "Sisa waktu (0,0063)", "Backlog sisa (0,0072)", "SPI jadwal (0,0782)"],
  values: [-0.0010, -0.0003, -0.0000, 0.0014, 0.0063, 0.0072, 0.0782] }],
  sumbuGaya({ x: 0.6, y: 1.5, w: 7.6, h: 5.2, barDir: "bar", chartColors: [HEX.accent1], showValue: false,
    valAxisLabelFormatCode: "0.00", showLegend: false, showTitle: true, title: "Permutation importance GB (kenaikan Brier)", titleColor: HEX.dk1, titleFontSize: 14 }));
kartu(s, 8.6, 1.5, 4.1, 4.9);
T(s, "Bukan berarti dependency tidak penting", { x: 8.85, y: 1.65, w: 3.6, h: 0.9, fontSize: 18, bold: true, color: C.text2 });
T(s, "Pergeseran dependency berkorelasi dengan telat (ρ 0,30), tetapi juga kuat dengan SPI (ρ −0,69). Begitu SPI diketahui, informasinya sudah tercakup. CR menunjukkan paradoks Simpson antarsubproyek.",
  { x: 8.85, y: 2.6, w: 3.6, h: 3.6, fontSize: 15, valign: "top" });

// 11. Keterbatasan --------------------------------------------------------------------------------------
pres.addSection({ title: "Penutup" });
s = pres.addSlide({ masterName: "Konten", sectionTitle: "Penutup" });
s.addText("Batas generalisasi: kasus P-FNE-08", { placeholder: "title" });
angka(s, 0.6, 1.6, 3.6, "14,7%", "rata-rata prediksi GB untuk P-FNE-08", C.accent3);
angka(s, 4.4, 1.6, 3.6, "54,0%", "proporsi telat aktual P-FNE-08", C.text2);
T(s, "Subproyek terpendek (62 hari, ambang 5% hanya 3,1 hari) dengan utilisasi terendah: berada di luar kondisi yang dilihat model dari 7 subproyek lain. Normalisasi fitur tidak memperbaikinya.",
  { x: 0.6, y: 3.6, w: 7.4, h: 1.6, fontSize: 16, valign: "top" });
kartu(s, 8.6, 1.5, 4.1, 4.9);
T(s, "Keterbatasan", { x: 8.85, y: 1.65, w: 3.6, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
T(s, [
  { text: "Data historis hasil simulasi dari PMP", options: { bullet: true, breakLine: true } },
  { text: "Hanya 8 subproyek", options: { bullet: true, breakLine: true } },
  { text: "Antrean sumber daya hanya FCFS", options: { bullet: true, breakLine: true } },
  { text: "Propagasi antarsubproyek belum dimodelkan", options: { bullet: true } },
], { x: 8.85, y: 2.25, w: 3.6, h: 3.8, fontSize: 15, valign: "top", paraSpaceAfter: 8 });

// 12. Kesimpulan ----------------------------------------------------------------------------------------
s = pres.addSlide({ masterName: "Judul Gelap", sectionTitle: "Penutup" });
s.addText("Kesimpulan", { placeholder: "title" });
s.addText([
  { text: "GB tanpa kalibrasi tambahan: probabilitas paling akurat dan terkalibrasi (Brier 0,172; ECE 0,056)", options: { bullet: true, breakLine: true } },
  { text: "Kalibrasi harus memakai data proyek yang sama, bukan proyek lain", options: { bullet: true, breakLine: true } },
  { text: "Zona Hijau/Kuning/Merah layak dipakai; tindakan mahal sebaiknya menunggu titik 50%", options: { bullet: true, breakLine: true } },
  { text: "Lanjutan: validasi dengan data realisasi, kalibrasi ulang bertahap, tambah proyek", options: { bullet: true } },
], { placeholder: "body", paraSpaceAfter: 6, fontSize: 18 });

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("Tersimpan:", OUT);
})();
