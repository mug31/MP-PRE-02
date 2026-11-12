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


TEMPLATE_DOC = HERE / 'Template_Pustaka_Data.doc'


def _template_docx(sementara):
    """Ubah template .doc asli ke .docx (LibreOffice) agar bisa diisi."""
    profil = sementara / 'lo-profil'
    subprocess.run(['soffice', f'-env:UserInstallation=file://{profil}', '--headless', '--convert-to', 'docx',
                    '--outdir', str(sementara), str(TEMPLATE_DOC)], check=True, capture_output=True)
    return sementara / (TEMPLATE_DOC.stem + '.docx')


def isi_template(polos, keluaran, gambar):
    """Pindahkan isi naskah (docx hasil pandoc) ke dalam template asli Jurnal Pustaka Data.

    Kop jurnal, logo, header, footer, dan pemisah kolom dari template dipertahankan; setiap paragraf naskah
    memakai gaya paragraf template (Heading1 tanpa nomor otomatis, Heading2, Normal, Caption, Rujukan)."""
    from copy import deepcopy
    from docx import Document
    from docx.oxml.ns import qn
    from docx.shared import Cm
    from docx.text.paragraph import Paragraph

    t = Document(TEMPLATE_DOCX_SEMENTARA[0])
    src = Document(polos)
    tb = list(t.element.body.iterchildren())

    def teks(el):
        return ''.join(x.text or '' for x in el.iter(qn('w:t')))

    def cari(awal, syarat):
        for i, el in enumerate(tb):
            if i >= awal and el.tag == qn('w:p') and syarat(teks(el)):
                return i
        raise SystemExit('Penanda template tidak ditemukan')

    i_judul = cari(0, lambda x: x.startswith('Judul Ditulis'))
    i_penulis, i_afil1, i_afil2, i_email = i_judul + 1, i_judul + 2, i_judul + 3, i_judul + 4
    i_abs = cari(i_judul, lambda x: x.startswith('The abstract is'))
    i_kw = cari(i_abs, lambda x: x.startswith('Keywords'))
    i_abk = cari(i_kw, lambda x: x.startswith('Isi abstrak'))
    i_kk = cari(i_abk, lambda x: x.startswith('Kata kunci'))
    i_cr = cari(i_kk, lambda x: x.startswith('©'))
    i_pend = cari(i_cr, lambda x: x.strip().startswith('Pendahuluan'))
    i_h1 = cari(i_pend, lambda x: x.startswith('3.') and 'Hasil' in x)       # Heading1 bernomor manual
    i_h2 = cari(i_pend, lambda x: x.startswith('2.1.'))
    i_par = i_pend + 1
    i_cap_tabel = next(i for i in range(i_pend, len(tb) - 1) if tb[i + 1].tag == qn('w:tbl'))
    i_tabel = i_cap_tabel + 1
    assert tb[i_tabel].tag == qn('w:tbl')
    i_cap_gambar = cari(i_tabel, lambda x: x.startswith('Gambar 1'))
    i_gambar = i_cap_gambar - 1
    i_rujukan = cari(i_cap_gambar, lambda x: x.startswith('Ikhsan'))
    i_sect2 = next(i for i in range(i_rujukan, len(tb)) if tb[i].tag == qn('w:p') and tb[i].find(qn('w:pPr')) is not None
                   and tb[i].find(qn('w:pPr')).find(qn('w:sectPr')) is not None)

    ppr = lambda i: deepcopy(tb[i].find(qn('w:pPr')))
    PPR = {'h1': ppr(i_h1), 'h2': ppr(i_h2), 'par': ppr(i_par), 'cap_tabel': ppr(i_cap_tabel),
           'cap_gambar': ppr(i_cap_gambar), 'gambar': ppr(i_gambar), 'rujukan': ppr(i_rujukan)}
    kn = PPR['cap_tabel'].makeelement(qn('w:keepNext'), {})
    PPR['cap_tabel'].insert(1, kn)
    tblpr_t = deepcopy(tb[i_tabel].find(qn('w:tblPr')))
    sel_t = tb[i_tabel].find('.//' + qn('w:tc'))
    ppr_sel = deepcopy(sel_t.find('.//' + qn('w:pPr'))) if sel_t.find('.//' + qn('w:pPr')) is not None else None

    def rpr_contoh(el):
        r = el.find(qn('w:r'))
        x = r.find(qn('w:rPr')) if r is not None else None
        return deepcopy(x) if x is not None else None

    def gabung_rpr(r, dasar):
        """rPr run = rPr contoh template + atribut khas dari naskah (miring, tebal, superskrip)."""
        if dasar is None or r.tag != qn('w:r'):
            return
        lama = r.find(qn('w:rPr'))
        baru = deepcopy(dasar)
        for tag in ('w:i', 'w:b', 'w:vertAlign'):
            for x in baru.findall(qn(tag)):
                baru.remove(x)
        if lama is not None:
            for tag in ('w:i', 'w:iCs', 'w:b', 'w:bCs', 'w:vertAlign'):
                for x in lama.findall(qn(tag)):
                    baru.append(deepcopy(x))
            r.remove(lama)
        r.insert(0, baru)

    def isi_runs(tujuan, asal, dasar='auto'):
        if dasar == 'auto':
            dasar = rpr_contoh(tujuan)
        for c in list(tujuan):
            if c.tag != qn('w:pPr'):
                tujuan.remove(c)
        for c in asal:
            if c.tag != qn('w:pPr'):
                salinan = deepcopy(c)
                gabung_rpr(salinan, dasar)
                tujuan.append(salinan)

    RPR = {'h1': rpr_contoh(tb[i_h1]), 'h2': rpr_contoh(tb[i_h2]), 'par': None, 'cap_tabel': None, 'cap_gambar': None,
           'rujukan': None}

    sp = [el for el in src.element.body.iterchildren()]
    def gaya(el):
        pp = el.find(qn('w:pPr'))
        st = pp.find(qn('w:pStyle')) if pp is not None else None
        return st.get(qn('w:val')) if st is not None else ''
    para = [el for el in sp if el.tag == qn('w:p')]
    cari_src = lambda f: next(el for el in para if f(el))
    isi_runs(tb[i_judul], cari_src(lambda e: gaya(e) == 'Title'))
    for r_ in tb[i_judul].iter(qn('w:r')):                 # template: judul 15 pt tidak cetak tebal
        rpr_ = r_.find(qn('w:rPr'))
        if rpr_ is None:
            rpr_ = r_.makeelement(qn('w:rPr'), {}); r_.insert(0, rpr_)
        for tag in ('w:b', 'w:bCs'):
            for x in rpr_.findall(qn(tag)):
                rpr_.remove(x)
            el_ = rpr_.makeelement(qn(tag), {qn('w:val'): '0'})
            rpr_.insert(0, el_)
    penulis = [el for el in para if gaya(el) == 'Penulis']
    afil = [el for el in para if gaya(el) == 'Afiliasi']
    isi_runs(tb[i_penulis], penulis[0])
    isi_runs(tb[i_afil1], afil[0])
    isi_runs(tb[i_email], afil[1])
    t.element.body.remove(tb[i_afil2])
    isi_runs(tb[i_abs], cari_src(lambda e: teks(e).startswith('Project managers')))
    isi_runs(tb[i_kw], cari_src(lambda e: teks(e).startswith('Keywords')))
    isi_runs(tb[i_abk], cari_src(lambda e: teks(e).startswith('Manajer proyek')))
    isi_runs(tb[i_kk], cari_src(lambda e: teks(e).startswith('Kata kunci')))
    for r in tb[i_cr].iter(qn('w:t')):
        r.text = r.text.replace('20xx', '2026')

    # buang isi contoh template (dari Pendahuluan sampai sebelum pemisah kolom) dan halaman petunjuk referensi
    for el in tb[i_pend:i_sect2] + [x for x in tb[i_sect2 + 1:] if x.tag != qn('w:sectPr')]:
        t.element.body.remove(el)
    jangkar = tb[i_sect2]

    mulai = next(i for i, el in enumerate(sp) if el.tag == qn('w:p') and teks(el).startswith('1. Pendahuluan'))
    antrian_gambar = list(gambar)
    nomor_rumus = [0]
    for el in sp[mulai:]:
        if el.tag == qn('w:sectPr'):
            continue
        if el.tag == qn('w:tbl'):
            baru = deepcopy(el)
            lama = baru.find(qn('w:tblPr'))
            baru.replace(lama, deepcopy(tblpr_t))
            tw = baru.find(qn('w:tblPr')).find(qn('w:tblW'))
            if tw is not None:
                tw.set(qn('w:type'), 'pct'); tw.set(qn('w:w'), '5000')
            for gc in baru.iter(qn('w:gridCol')):
                gc.attrib.pop(qn('w:w'), None)
            for tcw in baru.iter(qn('w:tcW')):
                tcw.set(qn('w:type'), 'auto'); tcw.set(qn('w:w'), '0')
            for pp in baru.iter(qn('w:p')):
                lama_ppr = pp.find(qn('w:pPr'))
                jc = lama_ppr.find(qn('w:jc')) if lama_ppr is not None else None
                if lama_ppr is not None:
                    pp.remove(lama_ppr)
                if ppr_sel is not None:
                    np_ = deepcopy(ppr_sel)
                    old = np_.find(qn('w:jc'))
                    if old is not None:
                        np_.remove(old)
                    if jc is not None:
                        np_.append(deepcopy(jc))
                    pp.insert(0, np_)
                for r in pp.iter(qn('w:r')):
                    rpr = r.find(qn('w:rPr'))
                    if rpr is None:
                        rpr = r.makeelement(qn('w:rPr'), {}); r.insert(0, rpr)
                    for tag in ('w:sz', 'w:szCs'):
                        x = rpr.find(qn(tag))
                        if x is None:
                            x = rpr.makeelement(qn(tag), {}); rpr.append(x)
                        x.set(qn('w:val'), '16')
            baris = baru.findall(qn('w:tr'))
            for tr in baris:                                   # baris tabel tidak dipecah antarkolom
                trpr = tr.find(qn('w:trPr'))
                if trpr is None:
                    trpr = tr.makeelement(qn('w:trPr'), {}); tr.insert(0, trpr)
                trpr.append(trpr.makeelement(qn('w:cantSplit'), {}))
            for tr in baris[:-1]:                              # seluruh tabel tetap satu blok
                for pp in tr.iter(qn('w:pPr')):
                    pp.insert(1 if pp.find(qn('w:pStyle')) is not None else 0, pp.makeelement(qn('w:keepNext'), {}))
            jangkar.addprevious(baru)
            continue
        g = gaya(el)
        if list(el.iter(qn('w:drawing'))):
            baru = el.makeelement(qn('w:p'), {})
            baru.append(deepcopy(PPR['gambar']))
            jangkar.addprevious(baru)
            Paragraph(baru, t._body).add_run().add_picture(str(antrian_gambar.pop(0)), width=Cm(7.6))
            continue
        kunci = {'Heading1': 'h1', 'Heading2': 'h2', 'JudulTabel': 'cap_tabel', 'ImageCaption': 'cap_gambar',
                 'Rujukan': 'rujukan'}.get(g, 'par')
        baru = el.makeelement(qn('w:p'), {})
        baru.append(deepcopy(PPR[kunci]))
        isi_runs(baru, el, RPR.get(kunci))
        if kunci == 'rujukan':                       # nomor [n] dibuat otomatis oleh gaya Rujukan template
            for x in baru.iter(qn('w:t')):
                x.text = re.sub(r'^\[\d+\]\s*', '', x.text or '')
                break
        M = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
        mpara = baru.find('.//' + M + 'oMathPara')
        if kunci == 'par' and mpara is not None and teks(el).strip() == '' :
            nomor_rumus[0] += 1
            pp = baru.find(qn('w:pPr'))
            for tag in ('w:ind', 'w:jc', 'w:tabs'):
                for x in pp.findall(qn(tag)):
                    pp.remove(x)
            tabs = pp.makeelement(qn('w:tabs'), {})
            for jenis, pos in (('center', '2160'), ('right', '4320')):
                tab = tabs.makeelement(qn('w:tab'), {qn('w:val'): jenis, qn('w:pos'): pos})
                tabs.append(tab)
            pp.append(tabs)
            omath = deepcopy(mpara.find(M + 'oMath'))
            for c in list(baru):
                if c.tag != qn('w:pPr'):
                    baru.remove(c)
            def run_tab(teks_=None):
                r = baru.makeelement(qn('w:r'), {})
                if teks_ is None:
                    r.append(r.makeelement(qn('w:tab'), {}))
                else:
                    x = r.makeelement(qn('w:t'), {}); x.text = teks_; r.append(x)
                return r
            baru.append(run_tab()); baru.append(omath); baru.append(run_tab()); baru.append(run_tab(f'({nomor_rumus[0]})'))
        jangkar.addprevious(baru)
    assert not antrian_gambar, 'Jumlah gambar tidak sesuai'

    for s in t.sections:
        for h in (s.header, s.first_page_header, s.even_page_header):
            for p in h.paragraphs:
                if 'Penulis' in p.text and p.runs:
                    p.runs[0].text = 'Kusbianto, Al Akmal, Ainul Yaqin'
                    p.runs[0].font.superscript = False
                    for r in p.runs[1:]:
                        r.text = ''
    t.save(keluaran)


TEMPLATE_DOCX_SEMENTARA = []


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
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        buat_gaya()
        polos = tmp / 'polos.docx'
        subprocess.run(['pandoc', str(KELUARAN_MD.name), '-o', str(polos), f'--reference-doc={REFERENSI_DOCX.name}',
                        '--resource-path=.'], cwd=HERE, check=True)
        REFERENSI_DOCX.unlink()
        TEMPLATE_DOCX_SEMENTARA[:] = [_template_docx(tmp)]
        gambar = [HERE / g for g in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', teks)]
        isi_template(polos, KELUARAN_DOCX, gambar)
    print(f'{len(urutan)} rujukan dikutip; luaran: {KELUARAN_MD.name}, {KELUARAN_DOCX.name} (diisi ke template asli)')


if __name__ == '__main__':
    main()
