"""
PRE-02: Ekstraksi jadwal aktivitas & resource dari 8 dokumen PMP (revisi dosen no. 3–5).

Membaca tabel ASLI di berkas .docx pada MP-datasetRaw/ (bukan salin manual), lalu menulis
untuk tiap subproyek:
  data/P-FNE-0X_aktivitas.csv : ID, durasi (hari kerja), predecessor, kebutuhan resource, sumber
  data/P-FNE-0X_resource.csv  : daftar orang/tim, role, jendela ketersediaan, sumber

Aturan umum (pilihan A, "ambil apa adanya"):
  - Dipakai tabel PALING DETAIL di tiap PMP yang menyebut durasi DAN dependensi secara tertulis.
    Jika dependensi aktivitas tidak lengkap, dipakai level sprint/milestone yang lengkap.
  - Satuan waktu hari kerja: 1 minggu = 5 hari, 1 sprint = 10 hari (sprint 2 minggu di semua PMP).
  - Setiap tafsiran (singkatan role, nama fase sebagai dependensi, dll.) dicatat di kolom Catatan
    dan di kamus pemetaan di bawah, sehingga dapat diperiksa ulang.

Jalankan:  python ekstraksi_pmp.py
"""

import csv
import datetime as dt
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / 'MP-datasetRaw'
DATA = HERE / 'data'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

NAMA_PMP = {
    '01': 'Foundation & Core Platform', '02': 'Core Agricultural Operatios', '03': 'Supply Chain & Procurement',
    '04': 'Production & Manufacturing', '05': 'Commerce Sales & Logistic', '06': 'Finance & HCM',
    '07': 'Intelligence & Decision Platform', '08': 'Advanced & Autonomous Enterprise',
}
TAK_TERBATAS = math.inf
HARI_PER_BULAN = 22  # 5 bulan PMP-01 = 22 minggu (§4.2.3) = 110 hari kerja


# ============================================================
# Pembaca docx
# ============================================================

def _teks(el):
    return ' '.join(''.join(t.text or '' for t in p.iter(W + 't')) for p in el.iter(W + 'p')).strip()


def tabel_pmp(kode):
    """Semua tabel di PMP: daftar (heading terdekat, baris-baris sel)."""
    f = next(RAW.glob(f'2026 PMP *{NAMA_PMP[kode]}.docx'))
    body = ET.fromstring(zipfile.ZipFile(f).read('word/document.xml')).find(W + 'body')
    heading, out = '', []
    for el in body:
        if el.tag == W + 'p':
            t = _teks(el)
            if t and len(t) < 90 and re.match(r'^\d+(\.\d+)*\.?\s', t):
                heading = t
        elif el.tag == W + 'tbl':
            rows = [[_teks(c) for c in r.findall(W + 'tc')] for r in el.findall(W + 'tr')]
            out.append((heading, rows))
    return out


def cari(tabel, heading_awal, *header):
    """Tabel pertama yang heading-nya diawali heading_awal dan baris header memuat semua kata."""
    for h, rows in tabel:
        if h.startswith(heading_awal) and all(any(k in c for c in rows[0]) for k in header):
            return rows
    raise LookupError(f'Tabel {heading_awal} {header} tidak ditemukan')


def semua(tabel, *header):
    return [(h, rows) for h, rows in tabel if all(any(k in c for c in rows[0]) for k in header)]


# ============================================================
# Utilitas
# ============================================================

def aktivitas(id_, fase, nama, durasi, pred, kebutuhan, durasi_dok, dep_dok, res_dok, sumber,
              prioritas='-', catatan=''):
    return {
        'ID': id_, 'Fase': fase, 'Aktivitas': nama, 'Durasi_Hari': int(durasi),
        'Predecessor': ';'.join(pred), 'Kebutuhan_Resource': ';'.join(f'{r}:{n}' for r, n in kebutuhan.items()),
        'Prioritas': prioritas, 'Durasi_Dokumen': durasi_dok, 'Dependensi_Dokumen': dep_dok,
        'Resource_Dokumen': res_dok, 'Sumber': sumber, 'Catatan': catatan,
    }


def orang_dari_jumlah(jumlah, sumber):
    """{role: n} -> daftar orang tersedia sepanjang proyek."""
    out = []
    for role, n in jumlah.items():
        for k in range(1, n + 1):
            out.append({'Orang': f'{role} {k}' if n > 1 else role, 'Role': role, 'Hari_Mulai': 1,
                        'Hari_Selesai': '', 'Sumber': sumber})
    return out


def parse_kebutuhan(teks, peta, catatan):
    """'BE:2, FE:1' / 'PM + BA' -> {role: n} memakai kamus peta (token -> role atau None)."""
    keb = {}
    for tok in re.split(r'\s*(?:,|\+|/)\s*', teks.strip()):
        if not tok:
            continue
        m = re.match(r'^(.+?):(\d+)$', tok)
        nama, n = (m.group(1).strip(), int(m.group(2))) if m else (tok.strip(), 1)
        if nama not in peta:
            raise KeyError(f'Token resource tidak dikenal: {nama!r} (dari {teks!r})')
        role = peta[nama]
        if role is None:
            catatan.add(f'"{nama}" tidak ada di tabel tim/kapasitas, tidak dibatasi')
            continue
        keb[role] = keb.get(role, 0) + n
    return keb


def batasi_kapasitas(akt, kapasitas):
    """Kebutuhan melebihi jumlah orang dibatasi ke kapasitas tim (dicatat)."""
    for a in akt:
        keb, ubah = {}, []
        for item in filter(None, a['Kebutuhan_Resource'].split(';')):
            r, n = item.split(':')
            n = int(n)
            if n > kapasitas[r]:
                ubah.append(f'{r} {n}→{kapasitas[r]}')
                n = kapasitas[r]
            keb[r] = n
        if ubah:
            a['Kebutuhan_Resource'] = ';'.join(f'{r}:{n}' for r, n in keb.items())
            a['Catatan'] = '; '.join(filter(None, [a['Catatan'], 'kebutuhan dibatasi kapasitas tim: ' + ', '.join(ubah)]))


def rentang_kode(teks, semua_kode):
    """'1.1-1.7' -> semua kode di antara keduanya (urutan tabel); '1.5, 2.2' -> [..]; '-' -> []."""
    out = []
    for bagian in re.split(r'\s*,\s*', teks.strip()):
        if bagian in ('', '-'):
            continue
        if '-' in bagian:
            a, b = bagian.split('-')
            i, j = semua_kode.index(a), semua_kode.index(b)
            out += semua_kode[i:j + 1]
        else:
            if bagian not in semua_kode:
                raise KeyError(f'Kode dependensi tidak dikenal: {bagian}')
            out.append(bagian)
    return out


BULAN = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Mei': 5, 'Jun': 6, 'Jul': 7, 'Agu': 8, 'Sep': 9,
         'Okt': 10, 'Nov': 11, 'Des': 12}


def tanggal(teks):
    d, b, y = teks.split()
    return dt.date(int(y), BULAN[b], int(d))


def hari_kerja_antara(d1, d2):
    """Jumlah hari Senin–Jumat setelah d1 sampai dengan d2."""
    n, d = 0, d1
    while d < d2:
        d += dt.timedelta(days=1)
        n += d.weekday() < 5
    return n


# ============================================================
# P-FNE-01 — §4.2.1 (40 aktivitas, minggu) + §4.6.1 (orang per bulan)
# ============================================================

def p01():
    t = tabel_pmp('01')
    rows = cari(t, '4.2.1', 'Aktivitas', 'Dependensi')[1:]
    fase, akt = '', []
    for i, r in enumerate(rows, 1):
        fase = r[0] or fase
        akt.append({'ID': f'A{i:02d}', 'Fase': fase, 'Nama': r[1], 'Minggu': r[2], 'Dep': r[3]})
    per_fase = {}
    for a in akt:
        per_fase.setdefault(a['Fase'], []).append(a['ID'])
    fase_ke = list(per_fase)

    def fase_id(n):
        return per_fase[fase_ke[n - 1]]

    # Tafsiran teks dependensi -> ID (nama aktivitas atau nama fase = seluruh aktivitas fase itu)
    token = {
        'Environment': ['A01'], 'Kubernetes': ['A02'], 'Monitoring': ['A04'], 'Infrastructure': fase_id(1),
        'Auth': ['A06'], 'RBAC': ['A08'], 'IAM': fase_id(2), 'Schema': ['A11'], 'CRUD': ['A12'], 'MDM': fase_id(3),
        'Audit Trail': ['A16'], 'Gateway': ['A20'], 'Kafka': ['A24'], 'Publisher': ['A25'], 'Definition': ['A27'],
        'Execution': ['A28'], 'Notification': ['A31'], 'Integration': ['A34'], 'Testing': ['A35', 'A36'],
        'UAT': ['A37'], 'Deployment': ['A38'], 'DR Drill': ['A39'],
    }
    layanan = [i for n in range(2, 9) for i in fase_id(n)]  # "All Services" = Fase 2–8
    # Role per aktivitas: PMP-01 tidak menyebut PIC per aktivitas -> USULAN kelompok
    role = {**{i: 'DevOps' for i in ['A01', 'A02', 'A03', 'A04', 'A05', 'A20', 'A24', 'A26', 'A38', 'A39']},
            **{i: 'Security' for i in ['A07', 'A18', 'A22', 'A36']},
            **{i: 'Frontend' for i in ['A13', 'A17', 'A30', 'A32', 'A33']},
            **{i: 'QA' for i in ['A34', 'A35', 'A37']}, 'A40': 'PM'}
    should = {'A09', 'A14', 'A15', 'A19', 'A33'}  # §3.3.2 MoSCoW kolom Should Have
    catatan_khusus = {
        'A11': 'prioritas tersirat dari "24 Entity CRUD"', 'A17': 'Query = Must, Export = Should; diambil Must',
        'A18': 'prioritas tidak tercantum di §3.3.2 (diasumsikan Must)', 'A20': 'prioritas tersirat dari Routing',
        'A24': 'prioritas tersirat dari Pub/Sub', 'A29': 'prioritas tidak tercantum di §3.3.2 (diasumsikan Must)',
        'A38': '0,5 minggu = 2,5 hari, dibulatkan ke atas', 'A39': '0,5 minggu = 2,5 hari, dibulatkan ke atas',
    }
    out = []
    for a in akt:
        pred = []
        for tok in [x.strip() for x in a['Dep'].split(',')]:
            if tok == '-':
                continue
            ids = [x for x in layanan if x != a['ID']] if tok == 'All Services' else token[tok]
            pred += [x for x in ids if x not in pred]
        cat = [catatan_khusus.get(a['ID'], ''), 'role = usulan kelompok (PMP tidak menyebut PIC per aktivitas)']
        out.append(aktivitas(a['ID'], a['Fase'], a['Nama'], math.ceil(float(a['Minggu']) * 5), pred,
                             {role.get(a['ID'], 'Backend'): 1}, f"{a['Minggu']} minggu", a['Dep'], '-',
                             'PMP-01 §4.2.1; prioritas §3.3.2', 'Should' if a['ID'] in should else 'Must',
                             '; '.join(filter(None, cat))))

    res = cari(t, '4.6.1', 'Role', 'Month 1')[1:]
    nama_role = {'Project Manager': 'PM', 'DevOps Engineer': 'DevOps', 'Backend Developer': 'Backend',
                 'Frontend Developer': 'Frontend', 'Security Engineer': 'Security', 'QA Engineer': 'QA'}
    singkat = {'PM': 'PM', 'DevOps': 'DevOps', 'Backend': 'BE', 'Frontend': 'FE', 'Security': 'Sec', 'QA': 'QA'}
    orang = []
    for r in res:
        if r[0] not in nama_role:
            continue  # baris Total
        rl, bulanan = nama_role[r[0]], [int(x) for x in r[1:6]]
        for k in range(1, max(bulanan) + 1):
            aktif = [m for m, n in enumerate(bulanan, 1) if n >= k]
            assert aktif == list(range(aktif[0], aktif[-1] + 1)), f'jendela {rl}{k} tidak berurutan'
            orang.append({'Orang': f'{singkat[rl]}{k}', 'Role': rl,
                          'Hari_Mulai': (aktif[0] - 1) * HARI_PER_BULAN + 1,
                          'Hari_Selesai': '' if aktif[-1] == 5 else aktif[-1] * HARI_PER_BULAN,
                          'Sumber': f"PMP-01 §4.6.1 ({r[0]} {'-'.join(r[1:6])}); bulan {aktif[0]}–{aktif[-1]}"})
    return out, orang


# ============================================================
# P-FNE-02 — §4.3.1 Activity List (hari, predecessor, resource) + §7.3.1 Team Structure
# ============================================================

def p02():
    t = tabel_pmp('02')
    nama_fase = {'1': 'Fase 1: Persiapan & Inisiasi', '2': 'Fase 2: Foundation & Platform Setup',
                 '3': 'Fase 3: Module Development', '4': 'Fase 4: Mobile Development (paralel)',
                 '5': 'Fase 5: Integration & Event-Driven', '6': 'Fase 6: Testing & QA',
                 '7': 'Fase 7: Deployment & Go-Live', '8': 'Fase 8: Closure & Handover'}  # §4.6.2
    # §7.3.1 (diagram Team Structure): PM 1, PO 1, Tech Lead 1, QA Lead 1, BA 1, Backend 4, Frontend 2,
    # Mobile 1, DevOps 1, QA Engineers 2. Diagram menulis "Total: 14 Personil" padahal jumlahnya 15.
    kapasitas = {'PM': 1, 'PO': 1, 'Tech Lead': 1, 'QA Lead': 1, 'BA': 1, 'Backend': 4, 'Frontend': 2,
                 'Mobile': 1, 'DevOps': 1, 'QA': 2}
    peta = {'PM': 'PM', 'PO': 'PO', 'BA': 'BA', 'DevOps': 'DevOps', 'QA': 'QA', 'BE': 'Backend',
            'FE': 'Frontend', 'Mobile': 'Mobile', 'BE Lead': 'Backend', 'FE Lead': 'Frontend',
            'Tech Lead': 'Tech Lead', 'Dev': 'Backend', 'All Team': 'PM', 'Farm Mgr': None}
    out = []
    for _, rows in semua(t, 'ID', 'Durasi (Hari)', 'Predecessor', 'Resource'):
        for r in rows[1:]:
            cat = set()
            keb = parse_kebutuhan(r[4], peta, cat)
            if 'All Team' in r[4]:
                cat.add('"All Team" dimodelkan sebagai PM (pertemuan/dukungan seluruh tim dipimpin PM)')
            if 'Lead' in r[4] and 'Tech Lead' not in r[4]:
                cat.add('"BE/FE Lead" = satu developer senior di tim Backend/Frontend')
            pred = [] if r[3].strip() == '-' else [p.strip() for p in r[3].split(',')]
            out.append(aktivitas(r[0], nama_fase[r[0].split('.')[0]], r[1], int(r[2]), pred, keb,
                                 f'{r[2]} hari', r[3], r[4], 'PMP-02 §4.3.1 Activity List; resource §7.3.1',
                                 catatan='; '.join(sorted(cat))))
    ids = {a['ID'] for a in out}
    for a in out:
        for p in filter(None, a['Predecessor'].split(';')):
            assert p in ids, f'PMP-02 predecessor {p} tidak ada'
    batasi_kapasitas(out, kapasitas)
    return out, orang_dari_jumlah(kapasitas, 'PMP-02 §7.3.1 Team Structure')


# ============================================================
# P-FNE-03 — §4.2.2.2 Aktivitas Tingkat Tinggi (sprint) + §4.2.3.2 Dependency Matrix + §4.3.1
# ============================================================

def p03():
    t = tabel_pmp('03')
    akt = cari(t, '4.2.2.2', 'ID Aktivitas', 'Nama Aktivitas')[1:]
    dep = cari(t, '4.2.3.2', 'Aktivitas', 'Dependency')[1:]
    rentang = {}
    for r in akt:
        m = re.match(r'Sprint (\d+)(?:-(\d+))?', r[1])
        rentang[r[0]] = (int(m.group(1)), int(m.group(2) or m.group(1)))

    def dari_label(label):
        """'Sprint 1-2' / 'Sprint 9' / 'Sprint 1-16' -> ID aktivitas yang rentang sprint-nya tercakup."""
        m = re.match(r'Sprint (\d+)(?:-(\d+))?', label)
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        ids = [i for i, (x, y) in rentang.items() if a <= x and y <= b]
        assert ids, label
        return ids

    out = []
    for r, d in zip(akt, dep):
        assert d[0].split(':')[0] == r[1].split(':')[0], (r[1], d[0])
        pred = []
        for lbl in re.split(r'\s*,\s*', d[1]):
            if lbl != '-':
                pred += [x for x in dari_label(lbl.replace('(paralel)', '').strip()) if x not in pred]
        a, b = rentang[r[0]]
        cat = 'jenis "Overlap" dimodelkan Finish-to-Start (tim yang sama mengerjakan sprint berurutan)' \
            if d[2] == 'Overlap' else ''
        out.append(aktivitas(r[0], 'Sprint', r[1], (b - a + 1) * 10, pred, {'Tim Scrum': 1},
                             f'{b - a + 1} sprint × 10 hari (§4.2.1.3 Sprint Calendar)', d[1],
                             'tim sprint §4.3.1', 'PMP-03 §4.2.2.2; dependensi §4.2.3.2', catatan=cat))
    orang = [{'Orang': 'Tim Scrum', 'Role': 'Tim Scrum', 'Hari_Mulai': 1, 'Hari_Selesai': '',
              'Sumber': 'PMP-03 §4.3.1 Resource per Sprint: satu tim mengerjakan satu sprint dalam satu waktu'}]
    return out, orang


# ============================================================
# P-FNE-04 — §4.5.1 Milestone Schedule (milestone per sprint)
# ============================================================

def p04():
    t = tabel_pmp('04')
    rows = cari(t, '4.5.1', 'Milestone', 'Sprint')[1:]
    out, sprint_lalu = [], 0
    for r in rows:
        s = int(r[3].lstrip('S'))
        if r[0] == 'M1':
            sprint_lalu = 0  # kickoff = titik awal, bukan durasi
            continue
        if s == sprint_lalu:  # M8 berada di sprint yang sama dengan M7
            out[-1]['Aktivitas'] += f' + {r[1]}'
            out[-1]['Catatan'] = (f'{r[0]} ({r[2]}) tercatat di sprint S{s} yang sama dengan milestone sebelumnya; '
                                  'digabung (tanggal 31 Mar berselisih 2 minggu dari akhir S12)')
            continue
        n = s - sprint_lalu
        pred = [out[-1]['ID']] if out else []
        out.append(aktivitas(r[0], 'Milestone', f'S{sprint_lalu + 1}–S{s}: {r[1]}' if n > 1 else f'S{s}: {r[1]}',
                             n * 10, pred, {'Tim Scrum': 1}, f'{n} sprint ({r[3]}, {r[2]})', 'urutan milestone',
                             'tim sprint §4.7.1', 'PMP-04 §4.5.1 Milestone Schedule'))
        sprint_lalu = s
    orang = [{'Orang': 'Tim Scrum', 'Role': 'Tim Scrum', 'Hari_Mulai': 1, 'Hari_Selesai': '',
              'Sumber': 'PMP-04 §4.7.1 Team Capacity per Sprint (satu tim scrum)'}]
    return out, orang


# ============================================================
# P-FNE-05 — Sprint Schedule (§4.7.3 B) + Milestone (§4.4.3) untuk fase setelah sprint
# ============================================================

def p05():
    t = tabel_pmp('05')
    sprint = next(rows for h, rows in semua(t, 'Sprint', 'Date Range', 'Focus'))[1:]
    ms = next(rows for h, rows in semua(t, 'Milestone ID', 'Estimated Date'))[1:]
    out = []
    for r in sprint:
        id_ = 'S' + r[0].split()[-1]
        out.append(aktivitas(id_, 'Sprint', f'{r[0]}: {r[2]}', 10, [out[-1]['ID']] if out else [],
                             {'Tim Scrum': 1}, f'1 sprint ({r[1]})', 'urutan sprint', r[4],
                             'PMP-05 §4.7.3 B. Sprint Schedule'))
    akhir_sprint = tanggal('12 Feb 2027')  # akhir Sprint 9 (tabel Sprint Schedule)
    assert sprint[-1][1].endswith('12 Feb 2027')
    lalu = akhir_sprint
    for r in ms:
        d = tanggal(r[3])
        if d <= akhir_sprint:
            continue
        n = hari_kerja_antara(lalu, d)
        out.append(aktivitas(r[0], 'Pasca-sprint', f'{r[1]}', n, [out[-1]['ID']], {'Tim Scrum': 1},
                             f'{n} hari kerja ({lalu:%d %b} → {d:%d %b %Y})', 'urutan milestone', '-',
                             'PMP-05 §4.4.3 Milestone (tanggal)'))
        lalu = d
    out[0]['Catatan'] = 'libur 21 Des–1 Jan di antara Sprint 6 dan 7 tidak dihitung (jadwal dalam hari kerja)'
    orang = [{'Orang': 'Tim Scrum', 'Role': 'Tim Scrum', 'Hari_Mulai': 1, 'Hari_Selesai': '',
              'Sumber': 'PMP-05 sprint dikerjakan berurutan oleh satu tim'}]
    return out, orang


# ============================================================
# P-FNE-06 — §4.2.1 Daftar Milestone (durasi minggu) + §4.4.1 jaringan + §4.4.2 dependensi kunci
# ============================================================

def p06():
    t = tabel_pmp('06')
    rows = cari(t, '4.2.1', 'Milestone', 'Durasi')[1:]
    # §4.4.1: M0→M1→M2→M3→M4→M5→M7→M8→M9→M10→M11; M6 (Frontend, paralel) setelah desain (§4.4.2)
    # dan sebelum integrasi M7 ("All Services Complete").
    pred = {'M0': [], 'M6': ['M2'], 'M7': ['M5', 'M6']}
    urut = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M7', 'M8', 'M9', 'M10', 'M11']
    for a, b in zip(urut, urut[1:]):
        pred.setdefault(b, [a])
    out = []
    for r in rows:
        minggu = int(re.match(r'(\d+)', r[3]).group(1))
        tim = 'Tim Frontend' if r[0] == 'M6' else 'Tim Inti'
        out.append(aktivitas(r[0], 'Milestone', r[1], minggu * 5, pred[r[0]], {tim: 1}, r[3],
                             '§4.4.1 critical path' if r[0] != 'M6' else '§4.4.2: Frontend setelah UI/UX Design',
                             tim, 'PMP-06 §4.2.1 Daftar Milestone; dependensi §4.4.1–4.4.2',
                             catatan='paralel dengan M3–M5 (tim frontend terpisah, §4.5)' if r[0] == 'M6' else ''))
    orang = [{'Orang': 'Tim Inti', 'Role': 'Tim Inti', 'Hari_Mulai': 1, 'Hari_Selesai': '',
              'Sumber': 'PMP-06 §4.5 Resource Allocation per Sprint'},
             {'Orang': 'Tim Frontend', 'Role': 'Tim Frontend', 'Hari_Mulai': 1, 'Hari_Selesai': '',
              'Sumber': 'PMP-06 §4.5 (frontend developer terpisah dari backend)'}]
    return out, orang


# ============================================================
# P-FNE-07 — §4.3.1–4.3.7 Detail Aktivitas (hari, dependensi, sumber daya) + §4.6.3 kapasitas
# ============================================================

def p07():
    t = tabel_pmp('07')
    kap_rows = cari(t, '4.6.3', 'Role', 'Sprint Capacity')[1:]
    nama_role = {'Project Manager': 'PM', 'Tech Lead': 'Tech Lead', 'Backend Developer': 'Backend',
                 'Frontend Developer': 'Frontend', 'Data Engineer': 'Data Engineer', 'Data Scientist': 'Data Scientist',
                 'ML Engineer': 'ML Engineer', 'Knowledge Engineer': 'Knowledge Engineer', 'QA Engineer': 'QA',
                 'DevOps Engineer': 'DevOps', 'Business Analyst': 'BA'}
    kapasitas = {}
    for r in kap_rows:
        m = re.match(r'(.+?)(?:\s*\((\d+)\))?$', r[0])
        if m.group(1) in nama_role:
            kapasitas[nama_role[m.group(1)]] = int(m.group(2) or 1)
    peta = {'PM': 'PM', 'Leads': 'Tech Lead', 'BA': 'BA', 'PO': None, 'Tech Lead': 'Tech Lead', 'DevOps': 'DevOps',
            'Sponsor': None, 'Data Engineer': 'Data Engineer', 'DE': 'Data Engineer', 'QA': 'QA', 'FE': 'Frontend',
            'BE': 'Backend', 'Backend': 'Backend', 'Frontend': 'Frontend', 'ML Engineer': 'ML Engineer',
            'Data Scientist': 'Data Scientist', 'Knowledge Engineer': 'Knowledge Engineer', 'Users': None,
            'All Teams': 'PM', 'All': 'PM'}
    tabel_fase = [(h, rows) for h, rows in semua(t, 'Kode', 'Durasi (Hari)', 'Dependensi') if h.startswith('4.3.')]
    baris = [(h, r) for h, rows in tabel_fase for r in rows[1:] if re.match(r'^\d+\.\d+$', r[0])]
    kode = [r[0] for _, r in baris]
    out = []
    for h, r in baris:
        cat = set()
        keb = parse_kebutuhan(r[4], peta, cat)
        if re.search(r'\bAll', r[4]):
            cat.add('"All Teams" dimodelkan sebagai PM (koordinasi seluruh tim)')
        if 'Leads' in r[4]:
            cat.add('"Leads" dimodelkan sebagai Tech Lead')
        out.append(aktivitas(r[0], re.sub(r'^4\.3\.\d+\.\s*', '', h), r[1], int(r[2]), rentang_kode(r[3], kode),
                             keb, f'{r[2]} hari', r[3], r[4], f'PMP-07 §{h.split()[0].rstrip(".")}; kapasitas §4.6.3',
                             catatan='; '.join(sorted(cat))))
    batasi_kapasitas(out, kapasitas)
    return out, orang_dari_jumlah(kapasitas, 'PMP-07 §4.6.3 Sprint Capacity Planning')


# ============================================================
# P-FNE-08 — §4.10.2 Critical Path Analysis (ES/EF) + resource §4.6.4 / §4.4.3 + §7.4.2
# ============================================================

def p08():
    t = tabel_pmp('08')
    cpm = cari(t, '4.10.2', 'Activity', 'ES', 'EF')[1:]
    pert = {r[0]: r for r in cari(t, '4.6.4', 'Activity ID', 'Optimistic')[1:]}
    daftar = {r[1]: r for r in cari(t, '4.4.3', 'Activity ID', 'Responsible')[1:]}
    # §7.4.2 Resource Requirements: jumlah per peran -> orang bernama seperti di §4.6.4 (mis. "IoT Eng 1")
    jumlah = {r[0]: int(r[1]) for r in cari(t, '7.4.2', 'Peran', 'Jumlah')[1:]}
    singkat = {'IoT Engineer': 'IoT Eng', 'Twin Engineer': 'Twin Eng', 'Simulation Engineer': 'Sim Eng',
               'Autonomous Engineer': 'Auto Eng', 'Frontend Engineer': 'Frontend', 'Simulation Lead': 'Sim Lead',
               'Autonomous Lead': 'Auto Lead', 'QA Engineer': 'QA', 'DevOps Engineer': 'DevOps'}
    orang = []
    for peran, n in jumlah.items():
        nama = singkat.get(peran, peran)
        for k in range(1, n + 1):
            orang.append({'Orang': f'{nama} {k}' if n > 1 else nama, 'Role': f'{nama} {k}' if n > 1 else nama,
                          'Hari_Mulai': 1, 'Hari_Selesai': '', 'Sumber': f'PMP-08 §7.4.2 ({peran} {n})'})
    # Penanggung jawab berupa singkatan peran di §4.4.3 -> orang di §7.4.2
    peta = {o['Orang']: o['Orang'] for o in orang}
    peta.update({'BA': 'Business Analyst', 'PM': 'Project Manager', 'User': None, 'All Engineer': None,
                 'Frontend Engineer': 'Frontend 1'})
    out = []
    for r in cpm:
        id_, label = r[0].split()[0], re.search(r'\((.+)\)', r[0]).group(1)
        es, ef = int(r[1]), int(r[2])
        if id_ in pert:
            res, src = pert[id_][6], '§4.6.4'
        else:
            res, src = daftar[id_][4], '§4.4.3'
        cat = set()
        keb = parse_kebutuhan(res, peta, cat)
        if res == 'Frontend Engineer':
            cat.add('"Frontend Engineer" (peran) dipetakan ke Frontend 1')
        if 'All Engineer' in res:
            cat.add('"All Engineer" (bug fixing oleh semua engineer) tidak dibatasi satu orang')
        nama_daftar = daftar[id_][2]
        if label.lower() not in nama_daftar.lower() and (id_ not in pert or label.lower() not in pert[id_][1].lower()):
            cat.add(f'§4.10.2 menyebut "{label}", daftar aktivitas §4.4.3 menyebut "{nama_daftar}"')
        nama = nama_daftar if label.lower() == nama_daftar.lower() else f'{label} — {nama_daftar}'
        out.append(aktivitas(id_, 'Critical path', nama, ef - es, [out[-1]['ID']] if out else [],
                             keb, f'ES {es} → EF {ef}', 'urutan critical path §4.10.1', res,
                             f'PMP-08 §4.10.2 (ES/EF); resource {src}; orang §7.4.2', catatan='; '.join(sorted(cat))))
    out[0]['Catatan'] = '; '.join(filter(None, [out[0]['Catatan'],
                                                'hanya aktivitas critical path yang memiliki durasi & urutan tertulis '
                                                '(§4.10.2); aktivitas non-kritis disebut ber-float 5–15 hari tanpa rincian']))
    return out, orang


# ============================================================

def tulis(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    DATA.mkdir(exist_ok=True)
    for kode, fungsi in [('01', p01), ('02', p02), ('03', p03), ('04', p04), ('05', p05), ('06', p06),
                         ('07', p07), ('08', p08)]:
        akt, orang = fungsi()
        roles = {o['Role'] for o in orang}
        for a in akt:
            for item in filter(None, a['Kebutuhan_Resource'].split(';')):
                assert item.split(':')[0] in roles, f"P-FNE-{kode} {a['ID']}: role {item} tidak ada di resource"
        tulis(DATA / f'P-FNE-{kode}_aktivitas.csv', akt)
        tulis(DATA / f'P-FNE-{kode}_resource.csv', orang)
        print(f'P-FNE-{kode}: {len(akt):3d} aktivitas, {len(orang):2d} orang/tim, '
              f'total durasi {sum(a["Durasi_Hari"] for a in akt)} hari-aktivitas')


if __name__ == '__main__':
    main()
