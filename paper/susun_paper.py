"""
PRE-02: Susun naskah paper Jurnal Pustaka Data dari naskah_sumber.md (template 2026).

  python susun_paper.py

1. Sitasi [@kunci] diganti nomor [1], [2, 3] sesuai urutan kemunculan pertama (gaya IEEE).
2. References disusun berurutan dari kamus RUJUKAN (gaya IEEE, DOI berupa hyperlink aktif ke https://doi.org/),
   hanya untuk rujukan yang dikutip. Kunci yang tidak dikenal atau rujukan yang tidak dikutip menghentikan skrip.
3. Gambar dan tabel diberi nomor (Gambar n. / Tabel n.).
4. Isi naskah dipindahkan ke Template_Pustaka_Data_2026.docx (satu kolom, A4, margin 2 cm): kotak tanggal dan
   lisensi, judul, penulis, afiliasi, abstrak dalam kotak, bagian bernomor, empat pernyataan, dan References.
5. Luaran:
   - Paper_PRE02_Pustaka_Data.md                 naskah bernomor (publik)
   - Paper_PRE02_Pustaka_Data.docx               tanpa nomor WA (publik, untuk repositori)
   - Paper_PRE02_Pustaka_Data_GDocs.docx         tanpa nomor WA, tabel dibungkus agar tidak terbelah di Google Docs
   - Paper_PRE02_Pustaka_Data_submit.docx        DENGAN nomor WA dari kontak_wa.txt, untuk dikirim ke jurnal.
     kontak_wa.txt dan berkas *_submit.docx ada di .gitignore karena repositori ini publik.
Kebutuhan: pandoc, python-docx, pillow (+ font Liberation Serif)
"""

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUMBER = HERE / 'naskah_sumber.md'
KELUARAN_MD = HERE / 'Paper_PRE02_Pustaka_Data.md'
KELUARAN_DOCX = HERE / 'Paper_PRE02_Pustaka_Data.docx'
KELUARAN_GDOCS = HERE / 'Paper_PRE02_Pustaka_Data_GDocs.docx'   # versi untuk diunggah ke Google Docs
KELUARAN_SUBMIT = HERE / 'Paper_PRE02_Pustaka_Data_submit.docx' # dengan nomor WA (tidak di-commit)
REFERENSI_DOCX = HERE / 'gaya_pustaka_data.docx'
TEMPLATE_DOCX = HERE / 'Template_Pustaka_Data_2026.docx'
KONTAK_WA = HERE / 'kontak_wa.txt'                               # "Nama: nomor" per baris (tidak di-commit)

PENULIS = ['Muktibaskara Kusbianto', 'Muhammad Nailul Ghufron Majid', 'Rafiq Alhariri Andriansyah',
           'Muhammad Ainul Yaqin']
AFILIASI = 'Program Studi Teknik Informatika, Universitas Islam Negeri Maulana Malik Ibrahim Malang, Malang, Indonesia'
EMAIL_KORESPONDENSI = 'muktibaskrakusbianto@gmail.com'          # penulis pertama = penulis korespondensi
LEBAR_TEKS = 9638                                                # twip: 21 cm − 2 × 2 cm (template 2026)
LEBAR_GAMBAR_CM = 14                                             # batas template: lebar gambar ≤ 14 cm

# Gaya IEEE: inisial nama + nama belakang, "judul," *wadah*, vol., no., pp., tahun, doi.
RUJUKAN = {
    'ananta': 'D. Ananta, R. Z. T. Pamungkas, and M. Ainul Yaqin, "Analisis domain kinerja stakeholder pada proyek ERP menggunakan social network analysis," *Jurnal Pustaka Data (Pusat Akses Kajian Database, Analisa Teknologi, dan Arsitektur Komputer)*, vol. 6, no. 5, pp. 833–847, 2026, doi: 10.55382/jurnalpustakadata.v6i5.2152',
    'browning': 'T. R. Browning and A. A. Yassine, "Resource-constrained multi-project scheduling: priority rule performance revisited," *International Journal of Production Economics*, vol. 126, no. 2, pp. 212–228, 2010, doi: 10.1016/j.ijpe.2010.03.009',
    'batselier': 'J. Batselier and M. Vanhoucke, "Evaluation of deterministic state-of-the-art forecasting approaches for project duration based on earned value management," *International Journal of Project Management*, vol. 33, no. 7, pp. 1588–1596, 2015, doi: 10.1016/j.ijproman.2015.04.003',
    'wauters': 'M. Wauters and M. Vanhoucke, "A comparative study of artificial intelligence methods for project duration forecasting," *Expert Systems with Applications*, vol. 46, pp. 249–261, 2016, doi: 10.1016/j.eswa.2015.10.008',
    'choetkiertikul': 'M. Choetkiertikul, H. K. Dam, T. Tran, and A. Ghose, "Predicting the delay of issues with due dates in software projects," *Empirical Software Engineering*, vol. 22, no. 3, pp. 1223–1263, 2017, doi: 10.1007/s10664-016-9496-7',
    'kula': 'E. Kula, E. Greuter, A. van Deursen, and G. Gousios, "Dynamic prediction of delays in software projects using delay patterns and Bayesian modeling," in *Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2023)*, San Francisco, 2023, pp. 1012–1023, doi: 10.1145/3611643.3616328',
    'haekal': 'J. Haekal et al., "A random-forest-based framework for predicting schedule achievement in cloud enterprise resource planning projects using the critical path method and the programme evaluation and review technique," *South African Journal of Industrial Engineering*, vol. 37, no. 2, pp. 74–94, 2026',
    'gondia': 'A. Gondia, A. Siam, W. El-Dakhakhni, and A. H. Nassar, "Machine learning algorithms for construction projects delay risk prediction," *Journal of Construction Engineering and Management*, vol. 146, no. 1, Art. no. 04019085, 2020, doi: 10.1061/(ASCE)CO.1943-7862.0001736',
    'mandapatti': 'J. K. Mandapatti, "Machine learning models for predicting software project delays in large development teams," *Journal of Scalable Data Engineering and Intelligent Computing*, vol. 3, no. 2, pp. 65–69, 2026',
    'impivaara': 'V. Impivaara, "Machine learning for predicting delivery delays in manufacturing," Master\'s thesis, LUT University, Lappeenranta, 2025, urn:nbn:fi-fe20251215119518',
    'niculescu': 'A. Niculescu-Mizil and R. Caruana, "Predicting good probabilities with supervised learning," in *Proceedings of the 22nd International Conference on Machine Learning (ICML 2005)*, Bonn, 2005, pp. 625–632, doi: 10.1145/1102351.1102430',
    'guo': 'C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On calibration of modern neural networks," in *Proceedings of the 34th International Conference on Machine Learning (ICML 2017)*, PMLR, vol. 70, 2017, pp. 1321–1330',
    'cabanillas': 'C. Cabanillas, C. Di Ciccio, J. Mendling, and A. Baumgrass, "Predictive task monitoring for business processes," in *Business Process Management (BPM 2014)*, Lecture Notes in Computer Science, vol. 8659, 2014, pp. 424–432, doi: 10.1007/978-3-319-10172-9_31',
    'fitzsimmons': 'J. P. Fitzsimmons, R. Lu, Y. Hong, and I. Brilakis, "Construction schedule risk analysis – a hybrid machine learning approach," *Journal of Information Technology in Construction*, vol. 27, pp. 70–93, 2022, doi: 10.36680/j.itcon.2022.004',
    'friedman': 'J. H. Friedman, "Greedy function approximation: a gradient boosting machine," *The Annals of Statistics*, vol. 29, no. 5, pp. 1189–1232, 2001, doi: 10.1214/aos/1013203451',
    'pedregosa': 'F. Pedregosa et al., "Scikit-learn: machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011',
    'platt': 'J. Platt, "Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods," in *Advances in Large Margin Classifiers*, A. J. Smola, P. Bartlett, B. Schölkopf, and D. Schuurmans, Eds. Cambridge: MIT Press, 1999',
    'zadrozny': 'B. Zadrozny and C. Elkan, "Transforming classifier scores into accurate multiclass probability estimates," in *Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, Edmonton, 2002, pp. 694–699, doi: 10.1145/775047.775151',
    'brier': 'G. W. Brier, "Verification of forecasts expressed in terms of probability," *Monthly Weather Review*, vol. 78, no. 1, pp. 1–3, 1950, doi: 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2',
    'vancalster': 'B. Van Calster, D. Nieboer, Y. Vergouwe, B. De Cock, M. J. Pencina, and E. W. Steyerberg, "A calibration hierarchy for risk models was defined: from utopia to empirical data," *Journal of Clinical Epidemiology*, vol. 74, pp. 167–176, 2016, doi: 10.1016/j.jclinepi.2015.12.005',
    'murphy': 'A. H. Murphy, "A new vector partition of the probability score," *Journal of Applied Meteorology*, vol. 12, no. 4, pp. 595–600, 1973, doi: 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2',
    'youden': 'W. J. Youden, "Index for rating diagnostic tests," *Cancer*, vol. 3, no. 1, pp. 32–35, 1950, doi: 10.1002/1097-0142(1950)3:1<32::AID-CNCR2820030106>3.0.CO;2-3',
    'efron': 'B. Efron and R. J. Tibshirani, *An Introduction to the Bootstrap*. New York: Chapman & Hall, 1993, doi: 10.1201/9780429246593',
    'holm': 'S. Holm, "A simple sequentially rejective multiple test procedure," *Scandinavian Journal of Statistics*, vol. 6, no. 2, pp. 65–70, 1979',
    'wilcoxon': 'F. Wilcoxon, "Individual comparisons by ranking methods," *Biometrics Bulletin*, vol. 1, no. 6, pp. 80–83, 1945, doi: 10.2307/3001968',
    'grzelak': 'M. Grzelak, D. Voicu, R.-M. Stoica, and R. Vilau, "Predictive maintenance in logistics fleets: a comparative evaluation of random forest, XGBoost and logistic regression," *Logistics*, vol. 10, no. 8, Art. no. 183, 2026, doi: 10.3390/logistics10080183',
    'kannan': 'R. Kannan, H. A. Abdul Halim, K. Ramakrishnan, S. Ismail, and D. R. Wijaya, "Machine learning approach for predicting production delays: a quarry company case study," *Journal of Big Data*, vol. 9, no. 1, Art. no. 94, 2022, doi: 10.1186/s40537-022-00644-w',
    'sivakumar': 'V. Sivakumar and R. Sobika, "AI-driven predictive analytics for improving project planning: a task-level analysis of interdependencies and decision making," *International Journal of Scientific Research in Engineering and Management*, vol. 10, no. 7, 2026, doi: 10.55041/IJSREM65902',
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


_FONT_UKUR = None


def lebar_teks(teks_, pt=9):
    """Lebar teks Times New Roman dalam twip, diukur dengan Liberation Serif (metriknya sama)."""
    global _FONT_UKUR
    if _FONT_UKUR is None:
        from PIL import ImageFont
        _FONT_UKUR = ImageFont.truetype('LiberationSerif-Regular.ttf', 160)
    return _FONT_UKUR.getlength(teks_) / 160 * pt * 20 * 1.06   # +6% cadangan untuk huruf miring/tebal


def nomori_gambar_tabel(teks):
    n = iter(range(1, 100))
    teks = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: f'![Gambar {next(n)}. {m.group(1)}]({m.group(2)}){{width={LEBAR_GAMBAR_CM}cm}}', teks)
    # judul tabel: paragraf "Tabel n. ..." diberi gaya khusus (di atas tabel)
    teks = re.sub(r'^(Tabel \d+\. .+)$', r'::: {custom-style="Judul Tabel"}\n\1\n:::', teks, flags=re.M)
    return teks


def buat_gaya():
    """Dokumen referensi pandoc (hanya menentukan nama gaya; tata letak akhir diambil dari template)."""
    from docx import Document
    from docx.enum.style import WD_STYLE_TYPE

    subprocess.run(['pandoc', '-o', str(REFERENSI_DOCX), '--print-default-data-file', 'reference.docx'], check=True)
    d = Document(REFERENSI_DOCX)
    for nama in ('Penulis', 'Afiliasi', 'Judul Tabel', 'Rujukan'):
        try:
            d.styles[nama]
        except KeyError:
            d.styles.add_style(nama, WD_STYLE_TYPE.PARAGRAPH)
    d.save(REFERENSI_DOCX)


def baca_wa():
    """Nomor WA per penulis dari kontak_wa.txt; kosong bila berkas tidak ada."""
    if not KONTAK_WA.exists():
        return {}
    wa = {}
    for baris in KONTAK_WA.read_text(encoding='utf-8').splitlines():
        if baris.strip() and not baris.startswith('#') and ':' in baris:
            nama, nomor = baris.split(':', 1)
            wa[nama.strip()] = nomor.strip()
    kurang = [p for p in PENULIS if p not in wa]
    if kurang:
        sys.exit(f'Nomor WA belum ada di {KONTAK_WA.name}: {kurang}')
    return wa


def bungkus_tabel(tbl, judul):
    """Bungkus judul tabel + tabel dalam tabel satu sel tanpa garis yang barisnya tidak boleh dipecah.

    Google Docs mengabaikan keepNext antarbaris tabel sehingga tabel terbelah antarhalaman, tetapi
    mematuhi cantSplit pada baris. Dengan satu baris pembungkus, judul dan tabel selalu pindah bersama."""
    from docx.oxml.ns import qn
    W = LEBAR_TEKS
    luar = tbl.makeelement(qn('w:tbl'), {})
    tblpr = luar.makeelement(qn('w:tblPr'), {})
    for tag, at in (('w:tblW', {'w:w': str(W), 'w:type': 'dxa'}), ('w:jc', {'w:val': 'center'}),
                    ('w:tblLayout', {'w:type': 'fixed'})):
        tblpr.append(tblpr.makeelement(qn(tag), {qn(k): v for k, v in at.items()}))
    mar = tblpr.makeelement(qn('w:tblCellMar'), {})
    for sisi in ('top', 'left', 'bottom', 'right'):
        mar.append(mar.makeelement(qn('w:' + sisi), {qn('w:w'): '0', qn('w:type'): 'dxa'}))
    tblpr.append(mar)
    luar.append(tblpr)
    grid = luar.makeelement(qn('w:tblGrid'), {})
    grid.append(grid.makeelement(qn('w:gridCol'), {qn('w:w'): str(W)}))
    luar.append(grid)
    tr = luar.makeelement(qn('w:tr'), {})
    trpr = tr.makeelement(qn('w:trPr'), {})
    trpr.append(trpr.makeelement(qn('w:cantSplit'), {}))
    tr.append(trpr)
    tc = tr.makeelement(qn('w:tc'), {})
    tcpr = tc.makeelement(qn('w:tcPr'), {})
    tcpr.append(tcpr.makeelement(qn('w:tcW'), {qn('w:w'): str(W), qn('w:type'): 'dxa'}))
    brd = tcpr.makeelement(qn('w:tcBorders'), {})
    for sisi in ('top', 'left', 'bottom', 'right'):
        brd.append(brd.makeelement(qn('w:' + sisi), {qn('w:val'): 'nil'}))
    tcpr.append(brd)
    tc.append(tcpr)
    isi_judul = ''.join(x.text or '' for x in judul.iter(qn('w:t'))) if judul is not None else ''
    if judul is not None and judul.tag == qn('w:p') and isi_judul.startswith('Tabel '):
        judul.getparent().remove(judul)
        tc.append(judul)
    tc.append(tbl)
    akhir = tc.makeelement(qn('w:p'), {})                      # sel wajib diakhiri paragraf; dibuat 1 pt
    ppr = akhir.makeelement(qn('w:pPr'), {})
    ppr.append(ppr.makeelement(qn('w:spacing'), {qn('w:before'): '0', qn('w:after'): '0',
                                                  qn('w:line'): '20', qn('w:lineRule'): 'exact'}))
    rpr = ppr.makeelement(qn('w:rPr'), {})
    rpr.append(rpr.makeelement(qn('w:sz'), {qn('w:val'): '2'}))
    ppr.append(rpr)
    akhir.append(ppr)
    tc.append(akhir)
    tr.append(tc)
    luar.append(tr)
    return luar


# urutan anak pPr menurut skema OOXML (elemen yang disisipkan harus di posisi yang benar)
URUTAN_PPR = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl', 'numPr',
              'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap',
              'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid',
              'spacing', 'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection',
              'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']


def isi_template(polos, keluaran, gambar, wa=None, bungkus=False):
    """Pindahkan isi naskah (docx hasil pandoc) ke dalam Template_Pustaka_Data_2026.docx.

    Kotak tanggal/lisensi, header, dan footer template dipertahankan; judul, penulis, afiliasi, abstrak, dan
    kata kunci diisi di tempat contohnya; isi contoh dari "1. Pendahuluan" sampai daftar periksa diganti isi
    naskah dengan format paragraf contoh template (Heading1 bergaris, paragraf menjorok, tabel dan keterangan
    9 pt, rujukan [n] menggantung)."""
    from copy import deepcopy
    from urllib.parse import quote
    from docx import Document
    from docx.oxml.ns import qn
    from docx.shared import Cm
    from docx.text.paragraph import Paragraph
    from docx.opc.constants import RELATIONSHIP_TYPE as RT

    t = Document(TEMPLATE_DOCX)
    src = Document(polos)
    body = t.element.body
    tb = list(body.iterchildren())

    def teks(el):
        return ''.join(x.text or '' for x in el.iter(qn('w:t')))

    def cari(awal, syarat, tag='w:p'):
        for i, el in enumerate(tb):
            if i >= awal and el.tag == qn(tag) and syarat(teks(el)):
                return i
        raise SystemExit('Penanda template tidak ditemukan')

    def sisip_ppr(pp, el):
        """Sisipkan el ke pPr pp di posisi skema yang benar (menggantikan elemen bertag sama)."""
        nama = el.tag.split('}')[1]
        lama = pp.find(el.tag)
        if lama is not None:
            pp.replace(lama, el)
            return
        idx = URUTAN_PPR.index(nama)
        for c in pp:
            n_ = c.tag.split('}')[1]
            if n_ in URUTAN_PPR and URUTAN_PPR.index(n_) > idx:
                c.addprevious(el)
                return
        pp.append(el)

    i_judul = cari(0, lambda x: x.startswith('Judul Ditulis'))
    i_penulis = i_judul + 1
    i_afil = [i_judul + 2, i_judul + 3, i_judul + 4]
    i_email = cari(i_judul, lambda x: x.startswith('* Penulis Korespondensi'))
    i_abs = cari(i_email, lambda x: x.startswith('Abstract'), 'w:tbl')
    i_pend = cari(i_abs, lambda x: x.strip() == '1. Pendahuluan')
    i_par = i_pend + 1
    i_cap_tabel = cari(i_pend, lambda x: x.startswith('Tabel 1.'))
    i_tabel = i_cap_tabel + 1
    assert tb[i_tabel].tag == qn('w:tbl')
    i_gambar = next(i for i in range(i_tabel, len(tb)) if list(tb[i].iter(qn('w:drawing'))))
    i_cap_gambar = cari(i_gambar, lambda x: x.startswith('Figure 1'))
    i_ref = cari(i_cap_gambar, lambda x: x.strip() == 'References')
    i_rujukan = cari(i_ref, lambda x: x.startswith('[1]'))

    def ppr(i):
        return deepcopy(tb[i].find(qn('w:pPr')))

    def rpr_run(el, k=0):
        rs = el.findall(qn('w:r'))
        x = rs[k].find(qn('w:rPr')) if len(rs) > k else None
        return deepcopy(x) if x is not None else None

    PPR = {'h1': ppr(i_pend), 'par': ppr(i_par), 'cap_tabel': ppr(i_cap_tabel), 'cap_gambar': ppr(i_cap_gambar),
           'gambar': ppr(i_gambar), 'rujukan': ppr(i_rujukan)}
    RPR = {'h1': rpr_run(tb[i_pend]), 'par': rpr_run(tb[i_par]), 'cap_label': rpr_run(tb[i_cap_tabel]),
           'cap': rpr_run(tb[i_cap_gambar], 2), 'rujukan': rpr_run(tb[i_rujukan])}
    sisip_ppr(PPR['cap_tabel'], PPR['cap_tabel'].makeelement(qn('w:keepNext'), {}))
    sisip_ppr(PPR['gambar'], PPR['gambar'].makeelement(qn('w:keepNext'), {}))
    for x in PPR['gambar'].findall(qn('w:pBdr')):                # bingkai abu-abu hanya penanda contoh template
        PPR['gambar'].remove(x)
    # Heading2 tidak dicontohkan template: gaya Heading2 template + huruf Times New Roman 10 pt tebal hitam
    PPR['h2'] = PPR['h1'].makeelement(qn('w:pPr'), {})
    sisip_ppr(PPR['h2'], PPR['h2'].makeelement(qn('w:pStyle'), {qn('w:val'): 'Heading2'}))
    sisip_ppr(PPR['h2'], PPR['h2'].makeelement(qn('w:keepNext'), {}))
    sisip_ppr(PPR['h2'], PPR['h2'].makeelement(qn('w:spacing'), {qn('w:before'): '160', qn('w:after'): '80'}))
    RPR['h2'] = deepcopy(RPR['par'])
    for tag in ('w:b', 'w:bCs'):
        RPR['h2'].append(RPR['h2'].makeelement(qn(tag), {}))
    for tag in ('w:sz', 'w:szCs'):
        RPR['h2'].append(RPR['h2'].makeelement(qn(tag), {qn('w:val'): '20'}))
    sisip_ppr(PPR['h1'], PPR['h1'].makeelement(qn('w:keepNext'), {}))
    tblpr_t = deepcopy(tb[i_tabel].find(qn('w:tblPr')))

    def gabung_rpr(r, dasar):
        """rPr run = rPr contoh template + atribut khas dari naskah (miring, tebal, superskrip)."""
        if dasar is None or r.tag != qn('w:r'):
            return
        lama = r.find(qn('w:rPr'))
        baru = deepcopy(dasar)
        for tag in ('w:i', 'w:iCs', 'w:b', 'w:bCs', 'w:vertAlign'):
            for x in baru.findall(qn(tag)):
                baru.remove(x)
        if lama is not None:
            for tag in ('w:b', 'w:bCs', 'w:i', 'w:iCs', 'w:vertAlign'):
                for x in lama.findall(qn(tag)):
                    baru.append(deepcopy(x))
            r.remove(lama)
        r.insert(0, baru)

    def isi_runs(tujuan, asal, dasar='auto'):
        if dasar == 'auto':
            dasar = rpr_run(tujuan)
        for c in list(tujuan):
            if c.tag != qn('w:pPr'):
                tujuan.remove(c)
        for c in asal:
            if c.tag != qn('w:pPr'):
                salinan = deepcopy(c)
                gabung_rpr(salinan, dasar)
                for r in salinan.iter(qn('w:r')):          # run di dalam hyperlink dan sejenisnya
                    if r is not salinan:
                        gabung_rpr(r, dasar)
                tujuan.append(salinan)

    def run(p, teks_, rpr, atas=False):
        r = p.makeelement(qn('w:r'), {})
        if rpr is not None:
            rp = deepcopy(rpr)
            if atas:
                for x in rp.findall(qn('w:sz')) + rp.findall(qn('w:szCs')):
                    rp.remove(x)
                rp.append(rp.makeelement(qn('w:vertAlign'), {qn('w:val'): 'superscript'}))
            r.append(rp)
        if teks_ == '\t':
            r.append(r.makeelement(qn('w:tab'), {}))
        else:
            x = r.makeelement(qn('w:t'), {qn('xml:space'): 'preserve'})
            x.text = teks_
            r.append(x)
        p.append(r)
        return r

    def kosongkan(p):
        for c in list(p):
            if c.tag != qn('w:pPr'):
                p.remove(c)

    def label_tebal(p, rpr_label):
        """Pisahkan "Tabel n." / "Gambar n." di awal keterangan menjadi run tebal (gaya template)."""
        r0 = p.find(qn('w:r'))
        t0 = r0.find(qn('w:t')) if r0 is not None else None
        m = re.match(r'((?:Tabel|Gambar) \d+\.)(.*)', t0.text or '', re.S) if t0 is not None else None
        assert m, 'Keterangan tidak diawali "Tabel n." / "Gambar n."'
        t0.text = m.group(2)
        t0.set(qn('xml:space'), 'preserve')
        lbl = r0.makeelement(qn('w:r'), {})
        lbl.append(deepcopy(rpr_label))
        x = lbl.makeelement(qn('w:t'), {})
        x.text = m.group(1)
        lbl.append(x)
        r0.addprevious(lbl)

    sp = list(src.element.body.iterchildren())

    def gaya(el):
        pp = el.find(qn('w:pPr'))
        st = pp.find(qn('w:pStyle')) if pp is not None else None
        return st.get(qn('w:val')) if st is not None else ''

    para = [el for el in sp if el.tag == qn('w:p')]
    cari_src = lambda f: next(el for el in para if f(el))

    # --- judul, penulis, afiliasi, penulis korespondensi
    isi_runs(tb[i_judul], cari_src(lambda e: gaya(e) == 'Title'))
    p = tb[i_penulis]
    r_nama, r_sup = rpr_run(p, 0), rpr_run(p, 1)
    kosongkan(p)
    for k, nama in enumerate(PENULIS, 1):
        run(p, (', ' if k > 1 else '') + nama, r_nama)
        run(p, f'{k}' + ('*' if k == 1 else ''), r_sup, atas=True)
    contoh = tb[i_afil[0]]
    r_no, r_af = rpr_run(contoh, 0), rpr_run(contoh, 1)
    for k, nama in enumerate(PENULIS, 1):
        baru = deepcopy(contoh)
        kosongkan(baru)
        run(baru, f'{k}', r_no, atas=True)
        run(baru, ' ' + AFILIASI + (f', {wa[nama]}' if wa else ''), r_af)
        tb[i_afil[0]].addprevious(baru)
    for i in i_afil:
        body.remove(tb[i])
    p = tb[i_email]
    r_a, r_b = rpr_run(p, 0), rpr_run(p, len(p.findall(qn('w:r'))) - 1)
    kosongkan(p)
    run(p, '* Penulis Korespondensi: ', r_a)
    run(p, EMAIL_KORESPONDENSI, r_b)

    # --- abstrak dan kata kunci (dalam kotak abstrak template)
    kotak = tb[i_abs]
    kp = list(kotak.iter(qn('w:p')))
    cari_k = lambda f: next(x for x in kp if f(teks(x)))

    def isi_kata_kunci(p, nilai):
        rs = p.findall(qn('w:r'))
        j = next(i for i, r in enumerate(rs) if ''.join(x.text or '' for x in r.iter(qn('w:t'))).rstrip().endswith(':'))
        rpr_nilai = rpr_run(p, len(rs) - 1)
        for r in rs[j + 1:]:
            p.remove(r)
        label = ''.join(x.text or '' for r in rs[:j + 1] for x in r.iter(qn('w:t')))
        run(p, ('' if label.endswith(' ') else ' ') + nilai, rpr_nilai)

    isi_runs(cari_k(lambda x: x.startswith('Write your abstract')), cari_src(lambda e: teks(e).startswith('Project managers')))
    isi_runs(cari_k(lambda x: x.startswith('Tuliskan abstrak')), cari_src(lambda e: teks(e).startswith('Manajer proyek')))
    kw_en = teks(cari_src(lambda e: teks(e).startswith('Keywords:'))).split(':', 1)[1].strip()
    kw_id = teks(cari_src(lambda e: teks(e).startswith('Kata kunci:'))).split(':', 1)[1].strip()
    isi_kata_kunci(cari_k(lambda x: x.startswith('Keywords:')), kw_en)
    isi_kata_kunci(cari_k(lambda x: x.startswith('Kata Kunci:')), kw_id)

    # --- buang isi contoh template: dari "1. Pendahuluan" sampai akhir (termasuk daftar periksa), kecuali sectPr
    for el in tb[i_pend:]:
        if el.tag != qn('w:sectPr'):
            body.remove(el)
    jangkar = body.find(qn('w:sectPr'))

    mulai = next(i for i, el in enumerate(sp) if el.tag == qn('w:p') and teks(el).startswith('1. Pendahuluan'))
    antrian_gambar = list(gambar)
    nomor_rumus = [0]
    M = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
    for el in sp[mulai:]:
        if el.tag not in (qn('w:p'), qn('w:tbl')):         # sectPr dan penanda bookmark pandoc antarparagraf
            continue
        if el.tag == qn('w:tbl'):
            baru = deepcopy(el)
            baru.replace(baru.find(qn('w:tblPr')), deepcopy(tblpr_t))
            tblpr = baru.find(qn('w:tblPr'))
            # margin sel ditulis sebagai left/right (bukan start/end): Google Docs hanya membaca left/right
            mar = tblpr.makeelement(qn('w:tblCellMar'), {})
            for sisi, w_ in (('top', '0'), ('left', '72'), ('bottom', '0'), ('right', '72')):
                mar.append(mar.makeelement(qn('w:' + sisi), {qn('w:w'): w_, qn('w:type'): 'dxa'}))
            tblpr.append(mar)
            # lebar kolom dari isi: minimal selebar kata terpanjang, sisa lebar halaman dibagi menurut isi terpanjang
            margin_sel = 2 * 72
            isi = [[''.join(x.text or '' for x in tc.iter(qn('w:t'))) for tc in tr.findall(qn('w:tc'))]
                   for tr in baru.findall(qn('w:tr'))]
            nkol = max(len(r) for r in isi)
            kata = [max((lebar_teks(w) for r in isi if j < len(r) for w in r[j].split()), default=100)
                    for j in range(nkol)]
            panjang = [max((lebar_teks(r[j]) for r in isi if j < len(r)), default=100) for j in range(nkol)]
            minimum = [k + margin_sel for k in kata]
            if sum(minimum) >= LEBAR_TEKS:
                lebar_k = [m * LEBAR_TEKS / sum(minimum) for m in minimum]
            else:
                sisa = LEBAR_TEKS - sum(minimum)
                ingin = [max(p_ + margin_sel - m, 0) for p_, m in zip(panjang, minimum)]
                if sum(ingin) <= sisa:                          # semua muat satu baris: sisa dibagi rata
                    lebar_k = [m + i + (sisa - sum(ingin)) / nkol for m, i in zip(minimum, ingin)]
                else:
                    # kolom angka diusahakan satu baris lebih dulu (water-filling per kelompok)
                    def angka(j):
                        sel = [r[j].strip() for r in isi[1:] if j < len(r) and r[j].strip()]
                        return bool(sel) and sum(bool(re.match(r'[−\-\d\[]', s)) for s in sel) > len(sel) / 2
                    lebar_k = list(minimum)
                    for kelompok in ([j for j in range(nkol) if angka(j)], [j for j in range(nkol) if not angka(j)]):
                        urut = sorted(kelompok, key=lambda j: ingin[j])
                        for n_, j in enumerate(urut):
                            beri = min(ingin[j], sisa / (len(urut) - n_))
                            lebar_k[j] += beri
                            sisa -= beri
            lebar_k = [int(round(w)) for w in lebar_k]
            tw = tblpr.find(qn('w:tblW'))
            tw.set(qn('w:type'), 'dxa'); tw.set(qn('w:w'), str(sum(lebar_k)))
            grid = baru.find(qn('w:tblGrid'))
            for gc in list(grid):
                grid.remove(gc)
            for w in lebar_k:
                grid.append(grid.makeelement(qn('w:gridCol'), {qn('w:w'): str(w)}))
            baris = baru.findall(qn('w:tr'))
            for nb, tr in enumerate(baris):
                for tc, w in zip(tr.findall(qn('w:tc')), lebar_k):
                    tcpr = tc.find(qn('w:tcPr'))
                    if tcpr is None:
                        tcpr = tc.makeelement(qn('w:tcPr'), {}); tc.insert(0, tcpr)
                    for x in list(tcpr):
                        if x.tag in (qn('w:tcW'), qn('w:tcMar'), qn('w:tcBorders')):
                            tcpr.remove(x)
                    tcw = tcpr.makeelement(qn('w:tcW'), {qn('w:w'): str(w), qn('w:type'): 'dxa'})
                    tcpr.insert(0, tcw)
                    # garis gaya template: di atas dan di bawah judul kolom, dan di bawah baris terakhir
                    brd = tcpr.makeelement(qn('w:tcBorders'), {})
                    for sisi, ada in (('top', nb == 0), ('bottom', nb == 0 or nb == len(baris) - 1)):
                        if ada:
                            brd.append(brd.makeelement(qn('w:' + sisi), {qn('w:val'): 'single', qn('w:sz'): '4',
                                                                          qn('w:space'): '0', qn('w:color'): '000000'}))
                    tcw.addnext(brd)
                    tcm = tcpr.makeelement(qn('w:tcMar'), {})       # margin juga per sel
                    for sisi in ('left', 'right'):
                        tcm.append(tcm.makeelement(qn('w:' + sisi), {qn('w:w'): '72', qn('w:type'): 'dxa'}))
                    brd.addnext(tcm)
                    for pp in tc.iter(qn('w:p')):
                        lama_ppr = pp.find(qn('w:pPr'))
                        jc = lama_ppr.find(qn('w:jc')) if lama_ppr is not None else None
                        if lama_ppr is not None:
                            pp.remove(lama_ppr)
                        np_ = pp.makeelement(qn('w:pPr'), {})
                        np_.append(np_.makeelement(qn('w:spacing'), {qn('w:before'): '20', qn('w:after'): '20'}))
                        np_.append(deepcopy(jc) if jc is not None else
                                   np_.makeelement(qn('w:jc'), {qn('w:val'): 'center' if nb == 0 else 'left'}))
                        pp.insert(0, np_)
                        # isi sel: Times New Roman 9 pt seperti contoh tabel template; judul kolom tebal
                        for r in list(pp.iter(qn('w:r'))) + list(pp.iter(M + 'r')):
                            rpr = r.find(qn('w:rPr'))
                            if rpr is None:
                                rpr = r.makeelement(qn('w:rPr'), {})
                                r.insert(1 if r.find(M + 'rPr') is not None else 0, rpr)
                            if r.tag == qn('w:r'):
                                fn = rpr.find(qn('w:rFonts'))
                                if fn is None:
                                    fn = rpr.makeelement(qn('w:rFonts'), {}); rpr.insert(0, fn)
                                for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
                                    fn.set(qn(a), 'Times New Roman')
                                if nb == 0 and rpr.find(qn('w:b')) is None:
                                    fn.addnext(rpr.makeelement(qn('w:b'), {}))
                            for tag in ('w:color',):
                                x = rpr.find(qn(tag))
                                if x is None:
                                    x = rpr.makeelement(qn(tag), {}); rpr.append(x)
                                x.set(qn('w:val'), '000000')
                            for tag in ('w:sz', 'w:szCs'):
                                x = rpr.find(qn(tag))
                                if x is None:
                                    x = rpr.makeelement(qn(tag), {}); rpr.append(x)
                                x.set(qn('w:val'), '18')
                trpr = tr.find(qn('w:trPr'))
                if trpr is None:
                    trpr = tr.makeelement(qn('w:trPr'), {}); tr.insert(0, trpr)
                trpr.append(trpr.makeelement(qn('w:cantSplit'), {}))      # baris tabel tidak dipecah
                if nb == 0:
                    trpr.append(trpr.makeelement(qn('w:tblHeader'), {}))
            for tr in baris[:-1]:                              # seluruh tabel tetap satu blok
                for pp in tr.iter(qn('w:pPr')):
                    sisip_ppr(pp, pp.makeelement(qn('w:keepNext'), {}))
            if bungkus:
                baru = bungkus_tabel(baru, jangkar.getprevious())
            jangkar.addprevious(baru)
            continue
        g = gaya(el)
        if list(el.iter(qn('w:drawing'))):
            baru = el.makeelement(qn('w:p'), {})
            baru.append(deepcopy(PPR['gambar']))
            jangkar.addprevious(baru)
            Paragraph(baru, t._body).add_run().add_picture(str(antrian_gambar.pop(0)), width=Cm(LEBAR_GAMBAR_CM))
            continue
        kunci = {'Heading1': 'h1', 'Heading2': 'h2', 'JudulTabel': 'cap_tabel', 'ImageCaption': 'cap_gambar',
                 'Rujukan': 'rujukan'}.get(g, 'par')
        baru = el.makeelement(qn('w:p'), {})
        baru.append(deepcopy(PPR[kunci]))
        isi_runs(baru, el, RPR.get({'cap_tabel': 'cap', 'cap_gambar': 'cap'}.get(kunci, kunci)))
        if kunci in ('cap_tabel', 'cap_gambar'):
            label_tebal(baru, RPR['cap_label'])
        if kunci == 'h1' and teks(baru).strip() == 'Daftar Rujukan':
            for x in baru.iter(qn('w:t')):
                x.text = ''
            next(baru.iter(qn('w:t'))).text = 'References'
        if kunci == 'rujukan':                        # "[n]" + tab + isi, seperti contoh rujukan template
            r0 = baru.find(qn('w:r'))
            t0 = r0.find(qn('w:t'))
            m = re.match(r'(\[\d+\])\s*(.*)', t0.text or '', re.S)
            t0.text = m.group(2)
            nomor = r0.makeelement(qn('w:r'), {}); nomor.append(deepcopy(RPR['rujukan']))
            x = nomor.makeelement(qn('w:t'), {}); x.text = m.group(1); nomor.append(x)
            tab = r0.makeelement(qn('w:r'), {}); tab.append(deepcopy(RPR['rujukan']))
            tab.append(tab.makeelement(qn('w:tab'), {}))
            r0.addprevious(nomor); r0.addprevious(tab)
        mpara = baru.find('.//' + M + 'oMathPara')
        if kunci == 'par' and mpara is not None and teks(el).strip() == '':
            nomor_rumus[0] += 1                        # rumus di tengah, nomor (n) rata kanan
            pp = baru.find(qn('w:pPr'))
            for tag in ('w:ind', 'w:jc', 'w:tabs'):
                for x in pp.findall(qn(tag)):
                    pp.remove(x)
            tabs = pp.makeelement(qn('w:tabs'), {})
            for jenis, pos in (('center', str(LEBAR_TEKS // 2)), ('right', str(LEBAR_TEKS))):
                tabs.append(tabs.makeelement(qn('w:tab'), {qn('w:val'): jenis, qn('w:pos'): pos}))
            sisip_ppr(pp, tabs)
            omath = deepcopy(mpara.find(M + 'oMath'))
            kosongkan(baru)
            run(baru, '\t', RPR['par']); baru.append(omath)
            run(baru, '\t', RPR['par']); run(baru, f'({nomor_rumus[0]})', RPR['par'])
        sebelum = jangkar.getprevious()
        if kunci in ('par', 'h1', 'h2') and sebelum is not None and sebelum.tag == qn('w:tbl'):
            pp = baru.find(qn('w:pPr'))                # jarak 6 pt agar teks tidak menempel garis bawah tabel
            sp_ = pp.find(qn('w:spacing'))
            if sp_ is None:
                sp_ = pp.makeelement(qn('w:spacing'), {})
                sisip_ppr(pp, sp_)
            sp_.set(qn('w:before'), '160')
        jangkar.addprevious(baru)
    assert not antrian_gambar, 'Jumlah gambar tidak sesuai'

    # URL dan DOI dijadikan hyperlink aktif (syarat template: DOI harus bisa diklik)
    pola = re.compile(r'https://\S+?(?=[.,;)]?(?:\s|$))|(?<=doi: )10\.\S+?(?=\.?(?:\s|$))')
    for wt in list(body.iter(qn('w:t'))):
        m = pola.search(wt.text or '')
        if not m:
            continue
        r_asal = wt.getparent()
        sebelum, isi_url, sesudah = wt.text[:m.start()], m.group(0), wt.text[m.end():]
        url = isi_url if isi_url.startswith('https://') else 'https://doi.org/' + quote(isi_url, safe="/:;()-._")
        wt.text = sebelum
        wt.set(qn('xml:space'), 'preserve')
        r_url, r_akhir = deepcopy(r_asal), deepcopy(r_asal)
        r_url.find(qn('w:t')).text = isi_url
        r_akhir.find(qn('w:t')).text = sesudah
        r_akhir.find(qn('w:t')).set(qn('xml:space'), 'preserve')
        rpr = r_url.find(qn('w:rPr'))
        if rpr is None:
            rpr = r_url.makeelement(qn('w:rPr'), {})
            r_url.insert(0, rpr)
        for tag in ('w:color', 'w:u'):
            for x in rpr.findall(qn(tag)):
                rpr.remove(x)
        rpr.append(rpr.makeelement(qn('w:color'), {qn('w:val'): '0563C1'}))
        rpr.append(rpr.makeelement(qn('w:u'), {qn('w:val'): 'single'}))
        tautan = r_asal.makeelement(qn('w:hyperlink'), {qn('r:id'): t.part.relate_to(url, RT.HYPERLINK, is_external=True)})
        tautan.append(r_url)
        r_asal.addnext(tautan)
        tautan.addnext(r_akhir)
    t.save(keluaran)


def main():
    teks = SUMBER.read_text(encoding='utf-8')
    teks = re.sub(r'<!--.*?-->\n?', '', teks, flags=re.S)
    teks, urutan = nomori_sitasi(teks)
    tidak_dikutip = sorted(set(RUJUKAN) - set(urutan))
    if tidak_dikutip:
        sys.exit(f'Rujukan di kamus tetapi tidak dikutip: {tidak_dikutip}')
    teks = nomori_gambar_tabel(teks)
    daftar = '\n\n'.join(f'::: {{custom-style="Rujukan"}}\n[{i}] {RUJUKAN[k]}.\n:::' for i, k in enumerate(urutan, 1))
    teks = teks.rstrip() + '\n\n# References {.unnumbered}\n\n' + daftar + '\n'
    teks = teks.replace('---\n\n', '---\n\n<!-- Dihasilkan otomatis oleh susun_paper.py dari naskah_sumber.md. Jangan disunting. -->\n\n', 1)
    KELUARAN_MD.write_text(teks, encoding='utf-8')
    wa = baca_wa()
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        buat_gaya()
        polos = tmp / 'polos.docx'
        subprocess.run(['pandoc', str(KELUARAN_MD.name), '-o', str(polos), f'--reference-doc={REFERENSI_DOCX.name}',
                        '--resource-path=.'], cwd=HERE, check=True)
        REFERENSI_DOCX.unlink()
        gambar = [HERE / g for g in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', teks)]
        isi_template(polos, KELUARAN_DOCX, gambar)
        isi_template(polos, KELUARAN_GDOCS, gambar, bungkus=True)
        if wa:
            isi_template(polos, KELUARAN_SUBMIT, gambar, wa=wa)
    print(f'{len(urutan)} rujukan dikutip; luaran: {KELUARAN_MD.name}, {KELUARAN_DOCX.name}, {KELUARAN_GDOCS.name}'
          + (f', {KELUARAN_SUBMIT.name} (dengan nomor WA)' if wa else f' ({KONTAK_WA.name} tidak ada: versi submit dilewati)'))


if __name__ == '__main__':
    main()
