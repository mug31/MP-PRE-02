"""
PRE-02: Susun naskah paper Jurnal Pustaka Data dari naskah_sumber.md.

  python susun_paper.py

1. Sitasi [@kunci] diganti nomor [1], [2, 3] sesuai urutan kemunculan pertama (aturan template).
2. Daftar Rujukan disusun berurutan dari kamus RUJUKAN (metadata dari 02_Studi Literatur/Verifikasi_Literatur.md),
   hanya untuk rujukan yang dikutip. Kunci yang tidak dikenal atau rujukan yang tidak dikutip menghentikan skrip.
3. Gambar dan tabel diberi nomor (Gambar n. / Tabel n.).
4. Luaran: Paper_PRE02_Pustaka_Data.md dan Paper_PRE02_Pustaka_Data.docx (gaya template: Times New Roman 10 pt,
   judul 15 pt, A4 margin 25 mm, abstrak satu kolom lalu isi dua kolom, keterangan tabel/gambar 8 pt).
Kebutuhan: pandoc, python-docx
"""

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUMBER = HERE / 'naskah_sumber.md'
KELUARAN_MD = HERE / 'Paper_PRE02_Pustaka_Data.md'
KELUARAN_DOCX = HERE / 'Paper_PRE02_Pustaka_Data.docx'
REFERENSI_DOCX = HERE / 'gaya_pustaka_data.docx'

# Format: nama penulis. tahun. judul. *wadah*. volume(nomor): halaman. DOI (sesuai petunjuk template)
RUJUKAN = {
    'ananta': 'Ananta, D., Pamungkas, R. Z. T., & Ainul Yaqin, M. 2026. Analisis domain kinerja stakeholder pada proyek ERP menggunakan social network analysis. *Jurnal Pustaka Data (Pusat Akses Kajian Database, Analisa Teknologi, dan Arsitektur Komputer)*. 6(5): 833–847. doi:10.55382/jurnalpustakadata.v6i5.2152',
    'browning': 'Browning, T. R. & Yassine, A. A. 2010. Resource-constrained multi-project scheduling: priority rule performance revisited. *International Journal of Production Economics*. 126(2): 212–228. doi:10.1016/j.ijpe.2010.03.009',
    'batselier': 'Batselier, J. & Vanhoucke, M. 2015. Evaluation of deterministic state-of-the-art forecasting approaches for project duration based on earned value management. *International Journal of Project Management*. 33(7): 1588–1596. doi:10.1016/j.ijproman.2015.04.003',
    'wauters': 'Wauters, M. & Vanhoucke, M. 2016. A comparative study of artificial intelligence methods for project duration forecasting. *Expert Systems with Applications*. 46: 249–261. doi:10.1016/j.eswa.2015.10.008',
    'choetkiertikul': 'Choetkiertikul, M., Dam, H. K., Tran, T., & Ghose, A. 2017. Predicting the delay of issues with due dates in software projects. *Empirical Software Engineering*. 22(3): 1223–1263. doi:10.1007/s10664-016-9496-7',
    'kula': 'Kula, E., Greuter, E., van Deursen, A., & Gousios, G. 2023. Dynamic prediction of delays in software projects using delay patterns and Bayesian modeling. *Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2023)*. San Francisco. 1012–1023. doi:10.1145/3611643.3616328',
    'haekal': 'Haekal, J., Mu’min, R., Lesmana, S. A., Triana, N. E., Suwandari, Y. D., Rukmayadi, D., & Prihanto, I. G. 2026. A random-forest-based framework for predicting schedule achievement in cloud enterprise resource planning projects using the critical path method and the programme evaluation and review technique. *South African Journal of Industrial Engineering*. 37(2): 74–94',
    'gondia': 'Gondia, A., Siam, A., El-Dakhakhni, W., & Nassar, A. H. 2020. Machine learning algorithms for construction projects delay risk prediction. *Journal of Construction Engineering and Management*. 146(1): 04019085. doi:10.1061/(ASCE)CO.1943-7862.0001736',
    'mandapatti': 'Mandapatti, J. K. 2026. Machine learning models for predicting software project delays in large development teams. *Journal of Scalable Data Engineering and Intelligent Computing*. 3(2): 65–69',
    'impivaara': 'Impivaara, V. 2025. *Machine learning for predicting delivery delays in manufacturing*. Tesis Magister. Lappeenranta: LUT University. urn:nbn:fi-fe20251215119518',
    'niculescu': 'Niculescu-Mizil, A. & Caruana, R. 2005. Predicting good probabilities with supervised learning. *Proceedings of the 22nd International Conference on Machine Learning (ICML 2005)*. Bonn. 625–632. doi:10.1145/1102351.1102430',
    'guo': 'Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. 2017. On calibration of modern neural networks. *Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR*. 70: 1321–1330',
    'cabanillas': 'Cabanillas, C., Di Ciccio, C., Mendling, J., & Baumgrass, A. 2014. Predictive task monitoring for business processes. *Business Process Management (BPM 2014), Lecture Notes in Computer Science*. 8659: 424–432. doi:10.1007/978-3-319-10172-9_31',
    'fitzsimmons': 'Fitzsimmons, J. P., Lu, R., Hong, Y., & Brilakis, I. 2022. Construction schedule risk analysis – a hybrid machine learning approach. *Journal of Information Technology in Construction*. 27: 70–93. doi:10.36680/j.itcon.2022.004',
    'friedman': 'Friedman, J. H. 2001. Greedy function approximation: a gradient boosting machine. *The Annals of Statistics*. 29(5): 1189–1232. doi:10.1214/aos/1013203451',
    'pedregosa': 'Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. 2011. Scikit-learn: machine learning in Python. *Journal of Machine Learning Research*. 12: 2825–2830',
    'platt': 'Platt, J. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. dalam: Smola, A. J., Bartlett, P., Schölkopf, B., & Schuurmans, D. (Eds). 1999. *Advances in Large Margin Classifiers*. Cambridge: MIT Press',
    'zadrozny': 'Zadrozny, B. & Elkan, C. 2002. Transforming classifier scores into accurate multiclass probability estimates. *Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. Edmonton. 694–699. doi:10.1145/775047.775151',
    'brier': 'Brier, G. W. 1950. Verification of forecasts expressed in terms of probability. *Monthly Weather Review*. 78(1): 1–3. doi:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2',
    'vancalster': 'Van Calster, B., Nieboer, D., Vergouwe, Y., De Cock, B., Pencina, M. J., & Steyerberg, E. W. 2016. A calibration hierarchy for risk models was defined: from utopia to empirical data. *Journal of Clinical Epidemiology*. 74: 167–176. doi:10.1016/j.jclinepi.2015.12.005',
    'murphy': 'Murphy, A. H. 1973. A new vector partition of the probability score. *Journal of Applied Meteorology*. 12(4): 595–600. doi:10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2',
    'youden': 'Youden, W. J. 1950. Index for rating diagnostic tests. *Cancer*. 3(1): 32–35. doi:10.1002/1097-0142(1950)3:1<32::AID-CNCR2820030106>3.0.CO;2-3',
    'efron': 'Efron, B. & Tibshirani, R. J. 1993. *An Introduction to the Bootstrap*. New York: Chapman & Hall. doi:10.1201/9780429246593',
    'holm': 'Holm, S. 1979. A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*. 6(2): 65–70',
    'wilcoxon': 'Wilcoxon, F. 1945. Individual comparisons by ranking methods. *Biometrics Bulletin*. 1(6): 80–83. doi:10.2307/3001968',
    'grzelak': 'Grzelak, M., Voicu, D., Stoica, R.-M., & Vilau, R. 2026. Predictive maintenance in logistics fleets: a comparative evaluation of random forest, XGBoost and logistic regression. *Logistics*. 10(8): 183. doi:10.3390/logistics10080183',
    'kannan': 'Kannan, R., Abdul Halim, H. A., Ramakrishnan, K., Ismail, S., & Wijaya, D. R. 2022. Machine learning approach for predicting production delays: a quarry company case study. *Journal of Big Data*. 9(1): 94. doi:10.1186/s40537-022-00644-w',
    'sivakumar': 'Sivakumar, V. & Sobika, R. 2026. AI-driven predictive analytics for improving project planning: a task-level analysis of interdependencies and decision making. *International Journal of Scientific Research in Engineering and Management*. 10(7). doi:10.55041/IJSREM65902',
}


def nomori_sitasi(teks):
    urutan = []
    pola = re.compile(r'\[(@[^\]]+)\]')

    def ganti(m):
        kunci = [k.strip().lstrip('@') for k in m.group(1).split(';')]
        for k in kunci:
            if k not in RUJUKAN:
                sys.exit(f'Kunci sitasi tidak dikenal: {k}')
            if k not in urutan:
                urutan.append(k)
        return '[' + ', '.join(str(urutan.index(k) + 1) for k in kunci) + ']'

    return pola.sub(ganti, teks), urutan


def nomori_gambar_tabel(teks):
    n = iter(range(1, 100))
    teks = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)', lambda m: f'![Gambar {next(n)}. {m.group(1)}]({m.group(2)}){{width=7.6cm}}', teks)
    # judul tabel: paragraf "Tabel n. ..." diberi gaya khusus (rata tengah, 8 pt, di atas tabel)
    teks = re.sub(r'^(Tabel \d+\. .+)$', r'::: {custom-style="Judul Tabel"}\n\1\n:::', teks, flags=re.M)
    return teks


def buat_gaya():
    """Dokumen referensi pandoc dengan gaya mengikuti template Jurnal Pustaka Data."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
    from docx.shared import Pt, Mm

    subprocess.run(['pandoc', '-o', str(REFERENSI_DOCX), '--print-default-data-file', 'reference.docx'], check=True)
    d = Document(REFERENSI_DOCX)
    sec = d.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    for sisi in ('top_margin', 'bottom_margin', 'left_margin', 'right_margin'):
        setattr(sec, sisi, Mm(25))

    def atur(nama, ukuran, tebal=False, miring=False, rata=WD_ALIGN_PARAGRAPH.JUSTIFY, sebelum=0, sesudah=4):
        try:
            st = d.styles[nama]
        except KeyError:
            st = d.styles.add_style(nama, WD_STYLE_TYPE.PARAGRAPH)
        f = st.font
        f.name, f.size, f.bold, f.italic = 'Times New Roman', Pt(ukuran), tebal, miring
        f.color.rgb = None
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
        if rfonts is not None:
            for a in list(rfonts.attrib):
                if 'Theme' in a:
                    del rfonts.attrib[a]
        pf = st.paragraph_format
        pf.alignment, pf.space_before, pf.space_after, pf.line_spacing = rata, Pt(sebelum), Pt(sesudah), 1.0

    C, L = WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT
    for nama in ('Normal', 'Body Text', 'First Paragraph', 'Compact'):
        atur(nama, 10)
    atur('Title', 15, rata=C, sesudah=8)
    atur('Penulis', 10, tebal=True, rata=C, sesudah=0)
    atur('Afiliasi', 9, rata=C, sesudah=8)
    atur('Heading 1', 10, tebal=True, rata=L, sebelum=8, sesudah=4)
    atur('Heading 2', 10, rata=L, sebelum=6, sesudah=3)
    atur('Heading 3', 10, miring=True, rata=L, sebelum=4, sesudah=2)
    atur('Judul Tabel', 8, rata=C, sebelum=6, sesudah=2)
    atur('Image Caption', 8, rata=C, sesudah=6)
    atur('Captioned Figure', 10, rata=C)
    atur('Rujukan', 8, rata=L, sesudah=2)
    d.save(REFERENSI_DOCX)


def rapikan_docx():
    """Abstrak satu kolom, isi dua kolom (pemisah setelah paragraf 'Kata kunci'); tabel 8 pt."""
    from copy import deepcopy
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Pt

    d = Document(KELUARAN_DOCX)
    for t in d.tables:
        tblpr = t._tbl.tblPr
        lebar = tblpr.find(qn('w:tblW'))
        if lebar is None:
            lebar = OxmlElement('w:tblW')
            tblpr.append(lebar)
        lebar.set(qn('w:type'), 'pct')
        lebar.set(qn('w:w'), '5000')
        tata = tblpr.find(qn('w:tblLayout'))
        if tata is None:
            tata = OxmlElement('w:tblLayout')
            tblpr.append(tata)
        tata.set(qn('w:type'), 'autofit')
        grid = t._tbl.find(qn('w:tblGrid'))
        if grid is not None:
            for gc in grid.findall(qn('w:gridCol')):
                gc.attrib.pop(qn('w:w'), None)
        for sel in t._tbl.iter(qn('w:tcW')):
            sel.set(qn('w:type'), 'auto')
            sel.set(qn('w:w'), '0')
        for baris in t.rows:
            for sel in baris.cells:
                for par in sel.paragraphs:
                    for run in par.runs:
                        run.font.size = Pt(8)
                        run.font.name = 'Times New Roman'
    kunci = [p for p in d.paragraphs if p.text.startswith('Kata kunci:')]
    assert kunci, 'Paragraf "Kata kunci" tidak ditemukan'
    body_sect = d.element.body.find(qn('w:sectPr'))
    sect_satu = deepcopy(body_sect)
    cols = sect_satu.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols')
        sect_satu.append(cols)
    cols.set(qn('w:num'), '1')
    ppr = kunci[0]._p.get_or_add_pPr()
    ppr.append(sect_satu)
    cols2 = body_sect.find(qn('w:cols'))
    if cols2 is None:
        cols2 = OxmlElement('w:cols')
        body_sect.append(cols2)
    cols2.set(qn('w:num'), '2')
    cols2.set(qn('w:space'), '425')
    jenis = OxmlElement('w:type')
    jenis.set(qn('w:val'), 'continuous')
    body_sect.insert(0, jenis)
    d.save(KELUARAN_DOCX)


def main():
    teks = SUMBER.read_text(encoding='utf-8')
    teks = re.sub(r'<!--.*?-->\n?', '', teks, flags=re.S)
    teks, urutan = nomori_sitasi(teks)
    tidak_dikutip = sorted(set(RUJUKAN) - set(urutan))
    if tidak_dikutip:
        sys.exit(f'Rujukan di kamus tetapi tidak dikutip: {tidak_dikutip}')
    teks = nomori_gambar_tabel(teks)
    daftar = '\n\n'.join(f'::: {{custom-style="Rujukan"}}\n[{i}] {RUJUKAN[k]}.\n:::' for i, k in enumerate(urutan, 1))
    teks = teks.rstrip() + '\n\n# Daftar Rujukan {.unnumbered}\n\n' + daftar + '\n'
    teks = teks.replace('---\n\n', '---\n\n<!-- Dihasilkan otomatis oleh susun_paper.py dari naskah_sumber.md. Jangan disunting. -->\n\n', 1)
    KELUARAN_MD.write_text(teks, encoding='utf-8')
    buat_gaya()
    subprocess.run(['pandoc', str(KELUARAN_MD.name), '-o', str(KELUARAN_DOCX.name),
                    f'--reference-doc={REFERENSI_DOCX.name}', '--resource-path=.'], cwd=HERE, check=True)
    rapikan_docx()
    print(f'{len(urutan)} rujukan dikutip; luaran: {KELUARAN_MD.name}, {KELUARAN_DOCX.name}')


if __name__ == '__main__':
    main()
