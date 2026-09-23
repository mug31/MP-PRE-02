"""Generator slide presentasi gabungan Progres Pertemuan 1-5 PRE-02.

Seluruh angka pada slide P3 dan P5 dibaca langsung dari berkas sumber
(`dataset_pre02_fne.csv` dan folder `hasil_eksperimen/`) agar tidak pernah
menyimpang dari hasil eksperimen yang sebenarnya.

Jalankan:  uv run --with python-pptx python generate_presentasi_p1_p5.py
"""

import csv
import os
import statistics

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

# ============================================================
# DESIGN TOKENS — SWISS ACADEMIC / FOREST GREEN STYLE
# ============================================================
DARK_GREEN = RGBColor(0x1E, 0x42, 0x20)  # #1E4220 (Cover bg, Section headers)
MID_GREEN  = RGBColor(0x2C, 0x5F, 0x2D)  # #2C5F2D (Pill badges, accents)
SAGE_GREEN = RGBColor(0x97, 0xBC, 0x62)  # #97BC62 (Accents, rings)
MINT_LIGHT = RGBColor(0xE4, 0xEF, 0xD8)  # #E4EFD8 (Light green bg)
AMBER_GOLD = RGBColor(0xE8, 0xA3, 0x3D)  # #E8A33D (Gold badges & highlights)
CARD_BG    = RGBColor(0xF4, 0xF7, 0xF1)  # #F4F7F1 (Card background)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)  # #FFFFFF
DARK_TEXT  = RGBColor(0x23, 0x33, 0x24)  # #233324 (Body text)
MUTED_TEXT = RGBColor(0x5B, 0x6B, 0x5C)  # #5B6B5C (Footers & captions)
BORDER_COL = RGBColor(0xD0, 0xDE, 0xCC)  # Border color for cards
RED_ALERT  = RGBColor(0xB3, 0x3A, 0x2F)  # Zona merah EWS

FONT_TITLE = "Cambria"
FONT_BODY  = "Calibri"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
HASIL_DIR = os.path.join(REPO_DIR, "04_implemen_desain_eksperimen", "hasil_eksperimen")
REPO_URL = "https://github.com/mug31/MP-PRE-02"

# ============================================================
# PEMBACAAN DATA SUMBER
# ============================================================

def read_csv_dicts(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hitung_statistik_dataset():
    rows = read_csv_dicts(os.path.join(REPO_DIR, "dataset_pre02_fne.csv"))
    fitur = [
        "Planned_Duration_Days",
        "Planned_Effort_Hours",
        "Predecessor_Count",
        "Resource_Utilization_Rate",
        "Risk_Score",
        "SPI_Value",
        "Change_Request_Count",
    ]
    stats = {}
    for kol in fitur:
        nilai = [float(r[kol]) for r in rows]
        stats[kol] = {
            "mean": statistics.fmean(nilai),
            "std": statistics.stdev(nilai),
            "min": min(nilai),
            "max": max(nilai),
        }
    label = [int(r["Status_Delay"]) for r in rows]
    stats["_n"] = len(rows)
    stats["_delay"] = sum(label)
    stats["_ontime"] = len(label) - sum(label)
    return stats


def baca_metrik():
    rows = read_csv_dicts(os.path.join(HASIL_DIR, "tabel_metrik_evaluasi.csv"))
    for r in rows:
        for k in ("ROC_AUC", "Brier_Score", "Log_Loss", "ECE", "Accuracy", "F1_Score"):
            r[k] = float(r[k])
    return rows


def baca_feature_importance():
    rows = read_csv_dicts(os.path.join(HASIL_DIR, "tabel_feature_importance.csv"))
    return [(r["Feature"], float(r["Importance_MDI"])) for r in rows]


def baca_prediksi():
    return read_csv_dicts(os.path.join(HASIL_DIR, "tabel_prediksi_probabilitas_task.csv"))


STAT = hitung_statistik_dataset()
METRIK = baca_metrik()
FEATURE_IMP = baca_feature_importance()
PREDIKSI = baca_prediksi()

REKOMENDASI = min(METRIK, key=lambda r: r["Brier_Score"])
RAW = [r for r in METRIK if r["Kalibrasi"] == "Raw"]


def zona(nama):
    return [p for p in PREDIKSI if p["EWS_Risk_Zone"].startswith(nama)]


MERAH, KUNING, HIJAU = zona("MERAH"), zona("KUNING"), zona("HIJAU")
MERAH_BENAR = [p for p in MERAH if p["Status_Delay_Aktual"] == "1"]
TOTAL_DELAY = [p for p in PREDIKSI if p["Status_Delay_Aktual"] == "1"]

# ============================================================
# KERANGKA PRESENTASI
# ============================================================
prs = Presentation()
prs.slide_width = Inches(13.333333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

_page = {"n": 0}


def textbox(slide, left, top, width, height, text, size, color=DARK_TEXT,
            bold=False, font=FONT_BODY, align=PP_ALIGN.LEFT, spacing=1.0):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    for i, baris in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = baris
        p.alignment = align
        p.line_spacing = spacing
        p.font.name = font
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
    return tb


def add_header(slide, tag_text, title_text, subtitle_text=""):
    textbox(slide, 0.80, 0.45, 11.0, 0.35, tag_text.upper(), 10.0, AMBER_GOLD, bold=True)
    textbox(slide, 0.80, 0.75, 11.5, 0.65, title_text, 22.0, DARK_GREEN, bold=True, font=FONT_TITLE)
    if subtitle_text:
        textbox(slide, 0.80, 1.38, 11.5, 0.40, subtitle_text, 11.5, MUTED_TEXT)


def add_footer(slide):
    _page["n"] += 1
    textbox(slide, 0.80, 7.10, 8.0, 0.30,
            "PRE-02 — Prediksi Probabilitas Keterlambatan Proyek Multi Sumber Daya Terbatas",
            9.0, MUTED_TEXT)
    textbox(slide, 12.00, 7.10, 0.50, 0.30, str(_page["n"]), 9.0, MUTED_TEXT)


def new_slide(tag, title, subtitle=""):
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, tag, title, subtitle)
    add_footer(slide)
    return slide


def card(slide, left, top, width, height, fill=CARD_BG, border=BORDER_COL):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = border
    shp.line.width = Pt(1.0)
    shp.shadow.inherit = False
    shp.text_frame.text = ""
    return shp


def stat_card(slide, left, top, width, height, label, value, note, accent=MID_GREEN):
    card(slide, left, top, width, height)
    textbox(slide, left + 0.25, top + 0.22, width - 0.5, 0.30, label.upper(), 9.5, accent, bold=True)
    textbox(slide, left + 0.25, top + 0.58, width - 0.5, 0.55, value, 20.0, DARK_GREEN,
            bold=True, font=FONT_TITLE)
    textbox(slide, left + 0.25, top + 1.18, width - 0.5, height - 1.35, note, 10.0, MUTED_TEXT, spacing=1.15)


def bullets(slide, left, top, width, height, items, size=11.5, spacing=1.35, color=DARK_TEXT):
    teks = "\n".join(f"•  {i}" for i in items)
    return textbox(slide, left, top, width, height, teks, size, color, spacing=spacing)


def table(slide, data, left, top, width, height, col_widths, font_size=10.0,
          align=None, highlight_rows=(), row_height=0.30, links=None):
    shape = slide.shapes.add_table(len(data), len(data[0]), Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    tbl = shape.table
    tbl.first_row = True
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = Inches(w)
    for r, row in enumerate(data):
        tbl.rows[r].height = Inches(row_height if r else row_height + 0.04)
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = DARK_GREEN
            elif r in highlight_rows:
                cell.fill.fore_color.rgb = MINT_LIGHT
            else:
                cell.fill.fore_color.rgb = WHITE if r % 2 else CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(font_size)
            p.font.bold = r == 0 or r in highlight_rows
            p.font.color.rgb = WHITE if r == 0 else DARK_TEXT
            if align and c < len(align):
                p.alignment = align[c]
            if links and (r, c) in links and p.runs:
                p.runs[0].hyperlink.address = links[(r, c)]
                p.runs[0].font.color.rgb = MID_GREEN
                p.runs[0].font.underline = True
    return tbl


def link_text(slide, left, top, width, height, label, url, size=10.5, color=MID_GREEN):
    tb = textbox(slide, left, top, width, height, label, size, color, bold=True)
    run = tb.text_frame.paragraphs[0].runs[0]
    run.hyperlink.address = url
    run.font.underline = True
    return tb


CENTER = PP_ALIGN.CENTER
LEFT = PP_ALIGN.LEFT

# ============================================================
# SLIDE 1 — COVER
# ============================================================
s = prs.slides.add_slide(blank_layout)
s.background.fill.solid()
s.background.fill.fore_color.rgb = DARK_GREEN

for left, top, size, col in ((10.50, 4.50, 5.00, MID_GREEN), (11.30, 5.30, 3.40, SAGE_GREEN)):
    e = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(size), Inches(size))
    e.fill.solid()
    e.fill.fore_color.rgb = col
    e.line.fill.background()
    e.shadow.inherit = False

textbox(s, 0.80, 1.20, 9.0, 0.40, "PROGRES PENELITIAN PERTEMUAN 1–5", 14.0, AMBER_GOLD, bold=True)
textbox(s, 0.80, 1.75, 10.5, 2.20,
        "Prediksi Probabilitas Keterlambatan\nProyek Multi Sumber Daya Terbatas",
        34.0, WHITE, bold=True, font=FONT_TITLE, spacing=1.1)
textbox(s, 0.80, 3.85, 10.0, 1.00,
        "Studi Kasus: Portofolio 8 Modul Super ERP Farm Nation Enterprise (FNE) 2026\n"
        "Dari pemahaman masalah hingga pelaksanaan eksperimen dan hasil awal",
        13.0, MINT_LIGHT, spacing=1.3)
textbox(s, 0.80, 5.55, 8.0, 1.10,
        "Mukti Baskara  ·  Muhammad Nailul  ·  Rafiq\nManajemen Proyek — PRE-02  ·  September 2026",
        12.0, SAGE_GREEN, spacing=1.3)
add_footer(s)

# ============================================================
# SLIDE 2 — PETA PROGRES & PEMENUHAN OUTPUT
# ============================================================
s = new_slide("Ringkasan Capaian", "Peta Progres Pertemuan 1–5 dan Pemenuhan Output",
              "Setiap pertemuan diverifikasi terhadap daftar output pada dokumen Rencana Progress Penelitian")
table(s, [
    ["Pertemuan", "Output yang diminta", "Luaran yang dihasilkan", "Status"],
    ["P1 — Pemahaman umum", "Slide rencana penelitian", "Slide P1 (9 slide) + rekap di dek ini", "Selesai"],
    ["P2 — Studi literatur", "Matriks literatur 5–10 referensi; draft tinjauan pustaka",
     "Matriks 8 paper inti + tabel 28 referensi; draft Bab II + research gap", "Selesai"],
    ["P3 — Persiapan data", "Dataset siap pakai; dokumentasi preprocessing; deskripsi karakteristik data",
     "dataset_pre02_fne.csv (N = 26 × 7 fitur); dokumen P3 lengkap", "Selesai"],
    ["P4 — Implementasi desain", "Flow eksperimen; script/tools; draft metodologi",
     "Flow + 5 skenario; experiment_pipeline.py; draft Bab III", "Selesai"],
    ["P5 — Pelaksanaan", "Dataset hasil eksperimen; log pelaksanaan",
     "4 tabel + 3 grafik + ringkasan temuan otomatis; log pelaksanaan dan verifikasi replikasi", "Selesai"],
], 0.80, 2.05, 11.75, 3.80, [2.35, 3.30, 4.60, 1.50], font_size=10.5,
    align=[LEFT, LEFT, LEFT, CENTER], row_height=0.62)

textbox(s, 0.80, 6.15, 11.75, 0.70,
        "Alur naratif:  P1 apa masalahnya  →  P2 apa celah penelitiannya  →  P3 datanya apa  →  "
        "P4 bagaimana mengujinya  →  P5 apa hasilnya.",
        11.5, MID_GREEN, bold=True)

# ============================================================
# SLIDE 3 — P1: LATAR BELAKANG & MASALAH
# ============================================================
s = new_slide("Pertemuan 1 — Pemahaman Umum", "Latar Belakang dan Rumusan Masalah",
              "Klasifikasi risiko kualitatif tidak memberi ambang tindakan yang terukur bagi Project Manager")
card(s, 0.80, 2.00, 5.70, 4.55)
textbox(s, 1.10, 2.25, 5.10, 0.35, "KONTEKS PROYEK", 10.0, MID_GREEN, bold=True)
bullets(s, 1.10, 2.70, 5.10, 3.60, [
    "FNE menjalankan 8 sub-proyek ERP terintegrasi (P-FNE-01 s.d. P-FNE-08) secara paralel.",
    "Seluruh sub-proyek berbagi sumber daya developer yang terbatas.",
    "Antar-modul terdapat ketergantungan teknis, sehingga keterlambatan satu modul merambat ke modul turunannya.",
    "Monitoring berjalan pada dokumen PMP dan laporan progres berkala.",
], size=11.0)

card(s, 6.85, 2.00, 5.70, 4.55, fill=MINT_LIGHT)
textbox(s, 7.15, 2.25, 5.10, 0.35, "MASALAH YANG DIANGKAT", 10.0, MID_GREEN, bold=True)
bullets(s, 7.15, 2.70, 5.10, 2.60, [
    "Status risiko hanya berupa label kualitatif Low / Medium / High.",
    "Label tersebut tidak menyatakan seberapa besar peluang terlambat, sehingga sulit diubah menjadi ambang tindakan.",
    "Tindakan korektif cenderung diambil setelah keterlambatan terjadi, bukan sebelumnya.",
], size=11.0)
textbox(s, 7.15, 5.55, 5.10, 0.85,
        "Kebutuhan: angka peluang 0–1 yang dapat dipercaya\nsebagai pemicu peringatan dini.",
        12.0, DARK_GREEN, bold=True, font=FONT_TITLE, spacing=1.2)

# ============================================================
# SLIDE 4 — P1: TUJUAN, MANFAAT, BATASAN
# ============================================================
s = new_slide("Pertemuan 1 — Pemahaman Umum", "Tujuan, Manfaat, serta Batasan dan Ruang Lingkup")
kolom = [
    ("Tujuan Penelitian", [
        "Membangun model supervised learning yang memprediksi probabilitas keterlambatan pada fase monitoring & evaluation.",
        "Merancang early warning system berbasis ambang probabilitas untuk mendukung tindakan korektif dini.",
    ], MID_GREEN),
    ("Manfaat dan Kontribusi Ilmiah", [
        "Praktis: PM dapat memprioritaskan task berisiko tinggi dan memulihkan jadwal lebih cepat.",
        "Akademis: kerangka predictive monitoring probabilistik yang diuji kalibrasinya, bukan sekadar akurasi.",
        "Kontribusi 1: early warning system dengan probabilitas keterlambatan yang kuantitatif dan terkalibrasi.",
        "Kontribusi 2: informasi probabilitas sebagai dasar pengambilan keputusan berbasis risiko.",
        "Kontribusi 3: kerangka monitoring prediktif yang dapat diintegrasikan ke sistem manajemen proyek.",
    ], MID_GREEN),
    ("Batasan dan Ruang Lingkup", [
        "Hanya fase monitoring & evaluation, bukan perencanaan awal.",
        "Data bersumber dari dokumen KAK, PMP, dan SRS proyek FNE 2026.",
        "Empat algoritma probabilistik: LR, RF, Gradient Boosting, dan Neural Network.",
        "Unit analisis: task/modul, bukan keseluruhan proyek.",
    ], AMBER_GOLD),
]
for i, (judul, isi, warna) in enumerate(kolom):
    left = 0.80 + i * 4.00
    card(s, left, 2.00, 3.70, 4.55)
    textbox(s, left + 0.28, 2.25, 3.15, 0.35, judul.upper(), 10.0, warna, bold=True)
    bullets(s, left + 0.28, 2.72, 3.15, 3.60, isi, size=10.5, spacing=1.25)

# ============================================================
# SLIDE 5 — P1: VARIABEL PENELITIAN
# ============================================================
s = new_slide("Pertemuan 1 — Pemahaman Umum", "Identifikasi Variabel Penelitian",
              "Variabel konseptual pada P1 diterjemahkan menjadi kolom dataset yang tersedia pada P3")
table(s, [
    ["Variabel bebas (konseptual, P1)", "Operasionalisasi pada dataset (P3)", "Catatan"],
    ["Progres aktual dibanding rencana", "SPI_Value", "Schedule Performance Index = EV / PV"],
    ["Tingkat utilisasi sumber daya", "Resource_Utilization_Rate", "Nilai > 1.0 menandakan developer overload"],
    ["Jumlah risiko belum dimitigasi", "Risk_Score", "Indeks probabilitas × dampak, skala 0–1"],
    ["Frekuensi perubahan", "Change_Request_Count", "Jumlah change request yang disetujui"],
    ["Kinerja dependency antar-proyek", "Predecessor_Count", "Jumlah modul pendahulu (bukan status keterlambatannya)"],
    ["Sisa waktu hingga deadline", "Planned_Duration_Days", "Proksi; sisa waktu tidak tercatat pada PMP"],
    ["Backlog yang tersisa", "Planned_Effort_Hours", "Proksi; backlog tidak tercatat pada PMP"],
], 0.80, 2.05, 11.75, 3.55, [4.00, 3.55, 4.20], font_size=10.5, align=[LEFT, LEFT, LEFT])

card(s, 0.80, 5.85, 11.75, 0.95, fill=MINT_LIGHT)
textbox(s, 1.10, 6.05, 11.20, 0.60,
        "Variabel terikat (Y):  probabilitas keterlambatan P(Delay) bernilai kontinu 0–1 — 0 berarti aman, "
        "1 berarti kritis. Label pelatihan Status_Delay bersifat biner (0/1).",
        12.0, DARK_GREEN, bold=True, spacing=1.2)

# ============================================================
# SLIDE 6 — P2: MATRIKS LITERATUR
# ============================================================
s = new_slide("Pertemuan 2 — Studi Literatur", "Matriks Literatur: Delapan Paper Inti dan Posisinya",
              "28 referensi tertelaah; 8 paper inti berikut menjadi rujukan utama metodologi PRE-02")

SCHOLAR = "https://scholar.google.com/scholar?q="
matriks = [
    ("Batselier & Vanhoucke (2015)", "Earned Value / Earned Schedule", "Estimasi durasi deterministik",
     "Tidak menghasilkan probabilitas", "DOI", "https://doi.org/10.1016/j.ijproman.2015.04.003"),
    ("Wauters & Vanhoucke (2016)", "Decision tree, RF, boosting, SVM", "Prediksi durasi proyek",
     "Luaran durasi, bukan peluang terlambat", "DOI", "https://doi.org/10.1016/j.eswa.2015.10.008"),
    ("Choetkiertikul et al. (2017)", "Random Forest + dependency link", "Klasifikasi delay issue software",
     "Luaran biner, kalibrasi tidak diuji", "DOI", "https://doi.org/10.1007/s10664-016-9496-7"),
    ("Gondia et al. (2020)", "Naive Bayes, Decision Tree", "Kelas risiko Low / Medium / High",
     "Kelas diskret; tanpa sumber daya bersama", "DOI",
     "https://doi.org/10.1061/(ASCE)CO.1943-7862.0001736"),
    ("Browning & Yassine (2010)", "20 priority rule RCMPSP", "Prioritas alokasi sumber daya",
     "Heuristik statis, tidak prediktif", "Cari",
     SCHOLAR + "Resource-constrained+multi-project+scheduling+priority+rule+performance+revisited"),
    ("Niculescu-Mizil & Caruana (2005)", "Platt Scaling, Isotonic Regression", "Probabilitas terkalibrasi",
     "Bukan konteks proyek ERP", "DOI", "https://doi.org/10.1145/1102351.1102430"),
    ("Guo et al. (2017)", "Temperature Scaling, ECE", "Diagnosis overconfidence",
     "Domain computer vision dan NLP", "arXiv", "https://arxiv.org/abs/1706.04599"),
    ("Cabanillas et al. (2014)", "Predictive task monitoring", "Probabilitas pelanggaran deadline",
     "Bergantung log proses sekuensial", "Cari",
     SCHOLAR + "Predictive+Task+Monitoring+for+Business+Processes+Cabanillas"),
]
baris = [["Penulis (Tahun)", "Metode", "Luaran", "Celah terhadap PRE-02", "Sumber"]]
tautan = {}
for i, (penulis, metode, luaran, celah, label, url) in enumerate(matriks, start=1):
    baris.append([penulis, metode, luaran, celah, f"{label} ↗"])
    tautan[(i, 4)] = url
table(s, baris, 0.80, 2.00, 11.75, 4.00, [2.75, 2.55, 2.45, 2.85, 1.15], font_size=9.5,
      align=[LEFT, LEFT, LEFT, LEFT, CENTER], row_height=0.44, links=tautan)

textbox(s, 0.80, 6.30, 3.10, 0.35, "Dokumen lengkap:", 10.5, MUTED_TEXT)
link_text(s, 2.55, 6.30, 3.30, 0.35, "Matriks Literatur P2 (8 paper) ↗",
          REPO_URL + "/blob/main/Pertemuan2_Matriks_Literatur.md")
link_text(s, 6.00, 6.30, 3.10, 0.35, "Tinjauan Pustaka (28 referensi) ↗",
          REPO_URL + "/blob/main/02_Studi%20Literatur/Tinjauan%20Pustaka.md")
link_text(s, 9.40, 6.30, 3.15, 0.35, "Research Gap ↗",
          REPO_URL + "/blob/main/02_Studi%20Literatur/Research%20gap.md")
textbox(s, 0.80, 6.72, 11.75, 0.30,
        "Catatan: DOI Gondia et al. (2020) dan kedua entri bertanda “Cari” belum diverifikasi ke penerbit; "
        "gunakan tautan pencarian sebelum dikutip pada naskah akhir.",
        9.0, MUTED_TEXT)

# ============================================================
# SLIDE 7 — P2: RESEARCH GAP
# ============================================================
s = new_slide("Pertemuan 2 — Studi Literatur", "Empat Lapis Research Gap dan Posisi PRE-02")
gaps = [
    ("GAP 1", "Joint Resource–Dependency",
     "Sumber daya bersama dan dependensi antar-modul dimodelkan terpisah, belum simultan."),
    ("GAP 2", "Module-Level Probability",
     "Prediksi berhenti di level proyek atau epic, belum sampai level modul ERP."),
    ("GAP 3", "Delay Propagation",
     "Perambatan keterlambatan antar-modul belum dimodelkan eksplisit."),
    ("GAP 4", "Calibration",
     "Evaluasi berhenti pada akurasi dan AUC; kalibrasi probabilitas jarang diuji."),
]
for i, (tag, judul, isi) in enumerate(gaps):
    left = 0.80 + i * 3.00
    card(s, left, 2.00, 2.75, 3.10)
    textbox(s, left + 0.22, 2.22, 2.30, 0.30, tag, 10.0, AMBER_GOLD, bold=True)
    textbox(s, left + 0.22, 2.58, 2.35, 0.70, judul, 13.0, DARK_GREEN, bold=True,
            font=FONT_TITLE, spacing=1.1)
    textbox(s, left + 0.22, 3.42, 2.35, 1.50, isi, 10.5, MUTED_TEXT, spacing=1.2)

card(s, 0.80, 5.35, 11.75, 1.45, fill=DARK_GREEN, border=DARK_GREEN)
textbox(s, 1.10, 5.55, 11.20, 0.35, "POSISI PENELITIAN PRE-02", 10.0, AMBER_GOLD, bold=True)
textbox(s, 1.10, 5.92, 11.20, 0.75,
        "Memprediksi probabilitas keterlambatan terkalibrasi (0–1) pada level modul ERP, dengan fitur utilisasi "
        "sumber daya bersama dan jumlah dependensi pendahulu, lalu menerjemahkannya menjadi zona peringatan dini "
        "bagi Project Manager.",
        11.5, WHITE, spacing=1.25)

# ============================================================
# SLIDE 8 — P3: SUMBER DATA & PREPROCESSING
# ============================================================
s = new_slide("Pertemuan 3 — Persiapan Data", "Sumber Data, Pengumpulan, dan Preprocessing",
              "Luaran: dataset siap pakai `dataset_pre02_fne.csv` beserta dokumentasi tahapannya")
langkah = [
    ("01", "Identifikasi sumber", "KAK proyek FNE 2026, 8 dokumen PMP, dan 8 dokumen SRS. Sifat data: empiris-simulatif."),
    ("02", "Pengumpulan", "Ekstraksi task inti tiap sub-proyek yang memiliki durasi, effort, developer bersama, dan dependensi."),
    ("03", "Cleaning", "Verifikasi rentang nilai, tanpa missing value, dan pemisahan kolom metadata (ID, nama task)."),
    ("04", "Transformasi", "Standardisasi z-score dilatih hanya pada data latih di setiap fold untuk mencegah kebocoran data."),
]
for i, (no, judul, isi) in enumerate(langkah):
    left = 0.80 + i * 3.00
    card(s, left, 2.05, 2.75, 2.25)
    textbox(s, left + 0.22, 2.25, 1.0, 0.35, no, 16.0, SAGE_GREEN, bold=True, font=FONT_TITLE)
    textbox(s, left + 0.22, 2.68, 2.35, 0.35, judul, 12.0, DARK_GREEN, bold=True, font=FONT_TITLE)
    textbox(s, left + 0.22, 3.08, 2.35, 1.10, isi, 10.0, MUTED_TEXT, spacing=1.2)

stat_card(s, 0.80, 4.55, 2.75, 2.00, "Ukuran dataset", f"{STAT['_n']} × 7",
          "task inti dari 8 sub-proyek, 7 fitur numerik")
stat_card(s, 3.80, 4.55, 2.75, 2.00, "Distribusi kelas",
          f"{STAT['_delay']} : {STAT['_ontime']}",
          f"terlambat {STAT['_delay'] / STAT['_n'] * 100:.1f}% vs tepat waktu "
          f"{STAT['_ontime'] / STAT['_n'] * 100:.1f}%")
stat_card(s, 6.80, 4.55, 2.75, 2.00, "Missing value", "0",
          "tidak diperlukan imputasi maupun SMOTE")
stat_card(s, 9.80, 4.55, 2.75, 2.00, "Penyeimbangan", "Stratifikasi",
          "rasio kelas dijaga pada tiap fold cross-validation", accent=AMBER_GOLD)

# ============================================================
# SLIDE 9 — P3: KARAKTERISTIK DATA
# ============================================================
s = new_slide("Pertemuan 3 — Persiapan Data", "Deskripsi Karakteristik Data",
              f"Statistik deskriptif dihitung ulang langsung dari berkas CSV (N = {STAT['_n']}, standar deviasi sampel)")
baris = [["Variabel", "Rata-rata", "Std. Deviasi", "Min", "Maks"]]
fmt = {
    "Planned_Duration_Days": "{:.2f}", "Planned_Effort_Hours": "{:.2f}",
    "Predecessor_Count": "{:.2f}", "Resource_Utilization_Rate": "{:.3f}",
    "Risk_Score": "{:.3f}", "SPI_Value": "{:.3f}", "Change_Request_Count": "{:.2f}",
}
for kol, f in fmt.items():
    v = STAT[kol]
    baris.append([kol, f.format(v["mean"]), f.format(v["std"]), f.format(v["min"]), f.format(v["max"])])
table(s, baris, 0.80, 2.05, 6.85, 3.00, [2.85, 1.05, 1.15, 0.90, 0.90], font_size=10.0,
      align=[LEFT, CENTER, CENTER, CENTER, CENTER])

card(s, 8.00, 2.05, 4.55, 4.55)
textbox(s, 8.30, 2.28, 3.95, 0.35, "POLA YANG TERVERIFIKASI", 10.0, MID_GREEN, bold=True)
bullets(s, 8.30, 2.72, 3.95, 3.70, [
    "Seluruh 15 task dengan utilisasi ≥ 1.05 berstatus terlambat; dari 11 task sisanya hanya 1 yang terlambat.",
    "Seluruh 14 task dengan SPI ≤ 0.88 berstatus terlambat.",
    "5 dari 6 task dengan predecessor ≥ 3 mengalami keterlambatan.",
], size=10.5, spacing=1.25)
textbox(s, 8.30, 5.50, 3.95, 1.00,
        "Catatan kritis: SPI nyaris memisahkan kelas sendirian (terlambat 0.79–0.90; tepat waktu 0.91–0.98). "
        "Ini alasan utama metrik pada P5 mendekati sempurna.",
        10.0, RED_ALERT, spacing=1.2)

textbox(s, 0.80, 5.30, 6.85, 1.30,
        "Implikasi bagi desain eksperimen: dengan N = 26, pengujian tidak memakai satu kali split acak, "
        "melainkan Stratified 5-Fold Cross-Validation; model berkapasitas besar dihindari dan diganti model "
        "beregularisasi ketat.",
        11.0, DARK_TEXT, spacing=1.25)

# ============================================================
# SLIDE 10 — P4: FLOW EKSPERIMEN
# ============================================================
s = new_slide("Pertemuan 4 — Implementasi Desain Eksperimen", "Flow Eksperimen",
              "Diimplementasikan pada `experiment_pipeline.py`; seed 42 dikunci pada seluruh komponen acak")
flow = [
    ("01", "Muat data", "26 task × 7 fitur, pisahkan metadata dari matriks fitur X dan target Y."),
    ("02", "Stratified 5-Fold", "Bagi data menjadi 5 lipatan dengan rasio kelas tetap."),
    ("03", "Standardisasi", "Scaler dilatih hanya pada data latih tiap lipatan."),
    ("04", "Latih 4 model", "Logistic Regression, Random Forest, Gradient Boosting, dan MLP."),
    ("05", "Kalibrasi", "Platt dan Isotonic dilatih pada inner 3-fold di dalam data latih."),
    ("06", "Evaluasi & luaran", "Metrik, kurva, feature importance, prediksi per task, dan zona EWS."),
]
for i, (no, judul, isi) in enumerate(flow):
    left = 0.80 + (i % 3) * 4.00
    top = 2.10 + (i // 3) * 2.35
    card(s, left, top, 3.70, 2.05)
    textbox(s, left + 0.25, top + 0.20, 1.0, 0.30, no, 15.0, SAGE_GREEN, bold=True, font=FONT_TITLE)
    textbox(s, left + 0.25, top + 0.60, 3.20, 0.35, judul, 13.0, DARK_GREEN, bold=True, font=FONT_TITLE)
    textbox(s, left + 0.25, top + 1.02, 3.20, 0.90, isi, 10.5, MUTED_TEXT, spacing=1.2)

# ============================================================
# SLIDE 11 — P4: SKENARIO & PARAMETER
# ============================================================
s = new_slide("Pertemuan 4 — Implementasi Desain Eksperimen", "Lima Skenario Eksperimen dan Parameter Kontrol",
              "Skenario disusun mengikuti desain eksperimen pada dokumen Deskripsi Penelitian")
skenario = [
    ("SKENARIO 1", "Logistic Regression", "L2, C = 1.0", "Baseline; probabilitas alami dari fungsi sigmoid."),
    ("SKENARIO 2", "Random Forest", "100 pohon, depth 3", "Pola non-linear; menyediakan feature importance."),
    ("SKENARIO 3", "Gradient Boosting", "100 pohon, lr 0.05, depth 2", "Boosting pada log-loss."),
    ("SKENARIO 4", "MLP Neural Network", "16-8 neuron, ReLU, Adam", "Output sigmoid untuk pola non-linear."),
    ("SKENARIO 5", "Analisis Kalibrasi", "Raw vs Platt vs Isotonic", "Menguji keandalan angka probabilitas."),
]
for i, (tag, nama, param, isi) in enumerate(skenario):
    left = 0.80 + i * 2.40
    card(s, left, 2.05, 2.25, 3.05)
    textbox(s, left + 0.18, 2.25, 1.90, 0.30, tag, 9.0, AMBER_GOLD, bold=True)
    textbox(s, left + 0.18, 2.60, 1.95, 0.75, nama, 12.5, DARK_GREEN, bold=True, font=FONT_TITLE, spacing=1.1)
    textbox(s, left + 0.18, 3.42, 1.95, 0.45, param, 9.5, MID_GREEN, bold=True)
    textbox(s, left + 0.18, 3.95, 1.95, 1.00, isi, 9.5, MUTED_TEXT, spacing=1.2)

card(s, 0.80, 5.35, 11.75, 1.45, fill=MINT_LIGHT)
textbox(s, 1.10, 5.55, 11.20, 0.35, "VARIABEL KONTROL", 10.0, MID_GREEN, bold=True)
textbox(s, 1.10, 5.92, 11.20, 0.75,
        "Partisi data, seed acak (42), urutan fitur, dan prosedur standardisasi dibuat identik untuk seluruh "
        "skenario, sehingga perbedaan hasil hanya berasal dari algoritma dan teknik kalibrasinya. "
        "Eksperimen dijalankan ulang dan menghasilkan angka yang identik.",
        11.0, DARK_TEXT, spacing=1.25)

# ============================================================
# SLIDE 12 — P4: PROTOKOL VALIDASI & METRIK
# ============================================================
s = new_slide("Pertemuan 4 — Implementasi Desain Eksperimen", "Protokol Validasi dan Metrik Evaluasi")
card(s, 0.80, 2.05, 5.70, 4.50)
textbox(s, 1.10, 2.28, 5.10, 0.35, "PROTOKOL PENGENDALIAN BIAS", 10.0, MID_GREEN, bold=True)
bullets(s, 1.10, 2.75, 5.10, 3.60, [
    "Stratified 5-Fold Cross-Validation; ±5 task uji per lipatan.",
    "Standardisasi dan kalibrator hanya dilatih dari data latih (tanpa data leakage).",
    "Kalibrator memakai inner 3-fold di dalam data latih.",
    "Hold-out stratified 80:20 dijalankan sebagai pembanding indikatif.",
    "Seed 42 dikunci; hasil dapat direplikasi.",
], size=11.0, spacing=1.3)

card(s, 6.85, 2.05, 5.70, 4.50, fill=MINT_LIGHT)
textbox(s, 7.15, 2.28, 5.10, 0.35, "METRIK EVALUASI DUA DIMENSI", 10.0, MID_GREEN, bold=True)
textbox(s, 7.15, 2.72, 5.10, 0.30, "Kualitas probabilitas", 11.0, DARK_GREEN, bold=True)
bullets(s, 7.15, 3.05, 5.10, 1.35, [
    "Brier Score — rata-rata kuadrat selisih peluang dan kenyataan.",
    "Log Loss — hukuman berat untuk prediksi yakin yang keliru.",
    "Calibration curve dan Expected Calibration Error (5 bin).",
], size=10.5, spacing=1.2)
textbox(s, 7.15, 4.55, 5.10, 0.30, "Kemampuan diskriminasi", 11.0, DARK_GREEN, bold=True)
bullets(s, 7.15, 4.88, 5.10, 1.00, [
    "ROC-AUC, recall, specificity, dan F1-score.",
], size=10.5, spacing=1.2)
textbox(s, 7.15, 5.55, 5.10, 0.85,
        "Analisis tambahan: threshold analysis (Youden J) untuk ambang peringatan dini optimal, "
        "di samping ambang operasional EWS 0.35 dan 0.65.",
        10.5, MUTED_TEXT, spacing=1.2)

# ============================================================
# SLIDE 13 — P5: HASIL EVALUASI
# ============================================================
s = new_slide("Pertemuan 5 — Pelaksanaan Eksperimen", "Hasil Evaluasi Stratified 5-Fold Cross-Validation",
              "Angka dibaca langsung dari `tabel_metrik_evaluasi.csv`; Brier Score makin kecil makin baik")
baris = [["Model", "Kalibrasi", "ROC-AUC", "Brier Score", "Log Loss", "ECE", "Akurasi", "F1"]]
sorot = []
for r in METRIK:
    if r is REKOMENDASI:
        sorot.append(len(baris))
    baris.append([
        r["Model"].replace(" (Baseline)", ""), r["Kalibrasi"],
        f"{r['ROC_AUC']:.4f}", f"{r['Brier_Score']:.4f}", f"{r['Log_Loss']:.4f}",
        f"{r['ECE']:.4f}", f"{r['Accuracy'] * 100:.1f}%", f"{r['F1_Score']:.4f}",
    ])
table(s, baris, 0.80, 2.05, 11.75, 4.15, [2.65, 1.30, 1.30, 1.50, 1.30, 1.20, 1.30, 1.20],
      font_size=9.5, align=[LEFT, CENTER, CENTER, CENTER, CENTER, CENTER, CENTER, CENTER],
      highlight_rows=tuple(sorot), row_height=0.30)

textbox(s, 0.80, 6.45, 11.75, 0.55,
        f"Model rekomendasi (Brier Score terendah): {REKOMENDASI['Model']} — kalibrasi "
        f"{REKOMENDASI['Kalibrasi']}  ·  Brier {REKOMENDASI['Brier_Score']:.4f}  ·  "
        f"ECE {REKOMENDASI['ECE']:.4f}  ·  ROC-AUC {REKOMENDASI['ROC_AUC']:.4f}",
        11.5, DARK_GREEN, bold=True)

# ============================================================
# SLIDE 14 — P5: KURVA ROC & KALIBRASI
# ============================================================
s = new_slide("Pertemuan 5 — Pelaksanaan Eksperimen", "Kurva ROC dan Diagram Reliabilitas Kalibrasi",
              "Luaran grafik dari pipeline eksperimen (folder `hasil_eksperimen/`)")
s.shapes.add_picture(os.path.join(HASIL_DIR, "kurva_roc_perbandingan.png"),
                     Inches(1.30), Inches(2.00), height=Inches(3.85))
s.shapes.add_picture(os.path.join(HASIL_DIR, "kurva_kalibrasi_probabilitas.png"),
                     Inches(6.95), Inches(2.55), width=Inches(5.60))
textbox(s, 0.85, 6.05, 5.60, 0.85,
        "Diskriminasi: Logistic Regression dan MLP mencapai ROC-AUC 1.000; Gradient Boosting terendah "
        f"({min(r['ROC_AUC'] for r in RAW):.3f}).",
        10.5, MUTED_TEXT, spacing=1.2)
textbox(s, 6.95, 6.05, 5.60, 0.85,
        "Kalibrasi: titik yang mendekati garis diagonal menandakan probabilitas dapat dipercaya. "
        "Kalibrasi sekunder hanya memperbaiki Gradient Boosting.",
        10.5, MUTED_TEXT, spacing=1.2)

# ============================================================
# SLIDE 15 — P5: TEMUAN KUNCI & FEATURE IMPORTANCE
# ============================================================
s = new_slide("Pertemuan 5 — Pelaksanaan Eksperimen", "Temuan Kunci dan Prediktor Dominan")
s.shapes.add_picture(os.path.join(HASIL_DIR, "feature_importance_comparison.png"),
                     Inches(0.80), Inches(2.70), width=Inches(6.05))

card(s, 7.10, 2.05, 5.45, 4.55)
textbox(s, 7.40, 2.28, 4.85, 0.35, "TEMUAN", 10.0, MID_GREEN, bold=True)
top_fitur = FEATURE_IMP[:3]
bullets(s, 7.40, 2.72, 4.85, 3.80, [
    f"Model rekomendasi: {REKOMENDASI['Model'].replace(' (Baseline)', '')} "
    f"({REKOMENDASI['Kalibrasi']}) dengan Brier {REKOMENDASI['Brier_Score']:.4f}.",
    "Kalibrasi sekunder tidak selalu membantu: pada model yang probabilitasnya sudah baik, "
    "kalibrator yang dilatih dari ±20 sampel justru menambah noise.",
    "Prediktor dominan (MDI Random Forest): "
    + ", ".join(f"{n} ({v:.3f})" for n, v in top_fitur) + ".",
    "Hipotesis kendala sumber daya belum terdukung kuat: utilisasi berada di peringkat ketiga dan "
    f"{FEATURE_IMP[-2][0]} hanya {FEATURE_IMP[-2][1]:.3f}.",
    "Interpretasi manajerial: utilisasi berlebih adalah penyebab, penurunan SPI adalah manifestasinya, "
    "sehingga keduanya perlu dibaca sebagai satu kaskade.",
], size=10.5, spacing=1.25)

# ============================================================
# SLIDE 16 — P5: EARLY WARNING SYSTEM
# ============================================================
s = new_slide("Pertemuan 5 — Pelaksanaan Eksperimen", "Penerapan Early Warning System dan Threshold Analysis",
              "Zonasi operasional: Hijau P < 0.35  ·  Kuning 0.35 ≤ P < 0.65  ·  Merah P ≥ 0.65")
stat_card(s, 0.80, 2.05, 2.75, 1.95, "Zona Merah", f"{len(MERAH)} task",
          f"{len(MERAH_BENAR)} dari {len(TOTAL_DELAY)} task terlambat tertangkap", accent=RED_ALERT)
stat_card(s, 3.80, 2.05, 2.75, 1.95, "Zona Kuning", f"{len(KUNING)} task",
          "perlu peninjauan ulang sumber daya", accent=AMBER_GOLD)
stat_card(s, 6.80, 2.05, 2.75, 1.95, "Zona Hijau", f"{len(HIJAU)} task",
          "tidak ada task terlambat yang lolos ke zona ini")
stat_card(s, 9.80, 2.05, 2.75, 1.95, "Ambang Youden J", "θ* = 0.779",
          "ambang optimal statistik, dilaporkan terpisah dari ambang operasional")

contoh = ["ACT-026", "ACT-002", "ACT-018", "ACT-019", "ACT-001"]
baris = [["Task", "Sub-proyek", "Aktivitas", "Aktual", "P(Delay)", "Zona EWS"]]
for tid in contoh:
    p = next(x for x in PREDIKSI if x["Task_ID"] == tid)
    nama = p["Task_Name"] if len(p["Task_Name"]) <= 42 else p["Task_Name"][:41] + "…"
    baris.append([
        p["Task_ID"], p["Sub_Project"], nama,
        "Terlambat" if p["Status_Delay_Aktual"] == "1" else "Tepat waktu",
        f"{float(p['P_Delay_Rekomendasi']):.4f}", p["EWS_Risk_Zone"].split(" (")[0],
    ])
table(s, baris, 0.80, 4.25, 11.75, 1.90, [1.15, 1.35, 4.70, 1.55, 1.35, 1.65], font_size=10.0,
      align=[LEFT, LEFT, LEFT, CENTER, CENTER, CENTER])

textbox(s, 0.80, 6.35, 11.75, 0.60,
        "Tindakan yang dipicu: Hijau — pantau rutin  ·  Kuning — tinjau ulang alokasi developer  ·  "
        "Merah — eskalasi (crashing, fast-tracking, atau penyesuaian backlog).",
        11.0, DARK_TEXT)

# ============================================================
# SLIDE 17 — KETERBATASAN & RENCANA LANJUTAN
# ============================================================
s = new_slide("Penutup", "Keterbatasan yang Diakui dan Rencana Pertemuan 6–8")
card(s, 0.80, 2.05, 5.70, 4.50, fill=MINT_LIGHT)
textbox(s, 1.10, 2.28, 5.10, 0.35, "KETERBATASAN PENELITIAN", 10.0, RED_ALERT, bold=True)
bullets(s, 1.10, 2.75, 5.10, 3.60, [
    "N = 26 dengan ±5 task uji per lipatan; selisih kecil antar-model belum tentu signifikan.",
    "ROC-AUC ≈ 1.000 terjadi karena data empiris-simulatif hampir terpisah sempurna oleh SPI, "
    "bukan jaminan kinerja pada proyek riil.",
    "Isotonic Regression rawan overfitting pada ukuran sampel ini (Niculescu-Mizil & Caruana, 2005).",
    "Pemilihan model dan ambang dilakukan pada prediksi out-of-fold yang sama, sehingga estimasinya "
    "sedikit optimistis.",
], size=10.5, spacing=1.3)

card(s, 6.85, 2.05, 5.70, 4.50)
textbox(s, 7.15, 2.28, 5.10, 0.35, "RENCANA LANJUTAN", 10.0, MID_GREEN, bold=True)
rencana = [
    ("P6", "Analisis data eksperimen: uji signifikansi antar-model dan analisis kesalahan prediksi."),
    ("P7", "Pembahasan dan interpretasi: konfrontasi temuan dengan Browning & Yassine (2010) serta "
           "Batselier & Vanhoucke (2015)."),
    ("P8", "Finalisasi paper IMRAD, abstrak, sitasi, dan slide presentasi akhir."),
    ("Validasi", "Pengujian pada data proyek riil berukuran N > 100 sebagai agenda future work."),
]
for i, (tag, isi) in enumerate(rencana):
    top = 2.78 + i * 0.95
    textbox(s, 7.15, top, 0.90, 0.30, tag, 11.0, AMBER_GOLD, bold=True)
    textbox(s, 8.10, top, 4.15, 0.85, isi, 10.5, DARK_TEXT, spacing=1.2)

# ============================================================
# EKSPOR
# ============================================================
out_path = os.path.join(BASE_DIR, "PRE02_Presentasi_Progres_Pertemuan1-5.pptx")
prs.save(out_path)
print(f"[OK] {len(prs.slides.__iter__.__self__._sldIdLst)} slide tersimpan: {out_path}")
