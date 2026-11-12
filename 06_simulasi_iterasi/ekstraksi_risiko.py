"""
PRE-02: Ekstraksi register risiko dari 8 dokumen PMP (variabel "jumlah risiko yang belum dimitigasi",
Deskripsi Penelitian §2).

Membaca tabel ASLI di MP-datasetRaw/ dan menulis data/P-FNE-0X_risiko.csv berisi:
  ID, Risiko, Kategori, Probabilitas_Dokumen, Dampak_Dokumen  : apa adanya dari PMP
  Peluang (0–1), Level_Dampak (1–5)                           : hasil normalisasi (aturan di bawah)
  Dipakai_Simulasi (1/0), Alasan                              : risiko yang ikut disimulasikan
  Sumber                                                      : bagian PMP

Aturan pemilihan tabel:
  - Register = tabel ber-ID risiko yang punya kolom peluang DAN dampak. Jika satu PMP punya beberapa
    tabel register, dipakai kelompok tabel (header identik) dengan baris terbanyak; tabel lain hanya
    dipakai untuk melengkapi kategori. Tabel tanpa ID (risiko biaya, komunikasi, vendor) tidak dipakai.
  - PMP-07 menulis tiap risiko sebagai tabel "Aspek | Detail" sendiri; tabel tersebut dibaca satu per satu.

Aturan normalisasi (urutan prioritas: persen > desimal > skala 1–5 > kata). Konversi skala peluang 1–5 memakai
nilai tengah rentang di PMP-01 §9.3.1 Probability-Impact Matrix (Very Low < 20%, Low 20–40%, Medium 40–60%,
High 60–80%, Very High > 80%):
  Peluang : "60%" -> 0,6 ; "(0.6)" -> 0,6 ; skala 1..5 -> 0,1/0,3/0,5/0,7/0,9 ;
            Very Low/Low/Medium/High/Very High -> 0,1/0,3/0,5/0,7/0,9
  Dampak  : skala 1..5 apa adanya ; desimal 0–1 -> level (<=0,1:1, <=0,3:2, <=0,5:3, <=0,8:4, >0,8:5) ;
            kata: Very Low/Negligible 1, Low/Minor 2, Medium/Moderate 3, High/Major 4, Very High/Severe/Critical 5

Risiko yang TIDAK disimulasikan (Dipakai_Simulasi = 0):
  - Perubahan scope/requirement: sudah dimodelkan sebagai change request (CR); jika ikut, terhitung dua kali.
  - Risiko biaya murni (budget, kurs, tarif): tidak menggeser jadwal.

Jalankan:  python ekstraksi_risiko.py
"""

import csv
import re
from pathlib import Path

from ekstraksi_pmp import NAMA_PMP, tabel_pmp

HERE = Path(__file__).resolve().parent
DATA = HERE / 'data'

SKALA_PELUANG = {1: 0.1, 2: 0.3, 3: 0.5, 4: 0.7, 5: 0.9}
KATA_PELUANG = [('very low', 0.1), ('very high', 0.9), ('low', 0.3), ('medium', 0.5), ('high', 0.7)]
KATA_DAMPAK = [('very low', 1), ('negligible', 1), ('very high', 5), ('severe', 5), ('critical', 5),
               ('catastrophic', 5), ('minor', 2), ('low', 2), ('moderate', 3), ('medium', 3),
               ('major', 4), ('high', 4)]

POLA_CR = re.compile(r'scope|requirement|perubahan (kebutuhan|persyaratan|ruang lingkup)|change request', re.I)
POLA_BIAYA = re.compile(r'budget|anggaran|biaya|cost|kurs|currency|tarif|harga|over ?run', re.I)
KATEGORI_BIAYA = re.compile(r'^(cost|biaya|finansial|keuangan|financial)', re.I)
POLA_ID = re.compile(r'^([A-Z]{1,5}(?:-[A-Z]{2,5})?-\d{1,3})\b')


def peluang(teks):
    t = teks.strip()
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*%', t)
    if m:
        return float(m.group(1).replace(',', '.')) / 100
    m = re.search(r'\b0[.,]\d+\b', t)
    if m:
        return float(m.group(0).replace(',', '.'))
    m = re.search(r'\b([1-5])\b', t)
    if m:
        return SKALA_PELUANG[int(m.group(1))]
    low = t.lower()
    for kata, nilai in KATA_PELUANG:
        if kata in low:
            return nilai
    return None


def level_dampak(teks):
    t = teks.strip()
    m = re.search(r'\b0[.,]\d+\b', t)
    if m:
        v = float(m.group(0).replace(',', '.'))
        # ambang mengikuti label PMP-08 sendiri: Medium (0.6), High (0.7–0.8), Very High (0.9)
        return 1 if v <= 0.1 else 2 if v <= 0.3 else 3 if v <= 0.6 else 4 if v <= 0.8 else 5
    m = re.search(r'\b([1-5])\b', t)
    if m:
        return int(m.group(1))
    low = t.lower()
    for kata, nilai in KATA_DAMPAK:
        if kata in low:
            return nilai
    return None


def _kolom(header, *pola, kecuali=None):
    for i, h in enumerate(header):
        hs = h.strip()
        if any(re.search(p, hs, re.I) for p in pola) and not (kecuali and re.search(kecuali, hs, re.I)):
            return i
    return None


def baca_tabel_register(heading, rows):
    """Satu tabel register biasa -> daftar risiko (atau None jika bukan register)."""
    h = rows[0]
    k_id = _kolom(h, r'^(risk )?id$')
    k_nama = _kolom(h, r'^(risiko|risk|risk description)$')
    k_prob = _kolom(h, r'^prob')
    # Urutan: kolom dampak berupa nilai dulu ("Dampak Nilai", "Impact"), baru "Dampak" (bisa berupa teks uraian)
    k_damp = next((k for k in (_kolom(h, r'^dampak nilai$'), _kolom(h, r'^impact( \(i\))?$'),
                               _kolom(h, r'^dampak$')) if k is not None), None)
    k_kat = _kolom(h, r'kategori|category')
    k_desk = _kolom(h, r'^(deskripsi|penyebab)$')
    if k_nama is None or k_prob is None or k_damp is None:
        return None
    out = []
    for r in rows[1:]:
        if len(r) < len(h):
            continue
        nama = r[k_nama]
        rid = r[k_id].strip() if k_id is not None else ''
        if not rid:
            m = POLA_ID.match(nama)
            if not m:
                continue
            rid, nama = m.group(1), nama[m.end():].strip()
        if not POLA_ID.match(rid) or 'Rp' in r[k_damp]:
            continue
        out.append({'ID': rid, 'Risiko': nama, 'Kategori': r[k_kat] if k_kat is not None else '',
                    'Deskripsi': r[k_desk] if k_desk is not None else '',
                    'Probabilitas_Dokumen': r[k_prob], 'Dampak_Dokumen': r[k_damp], 'Sumber': heading})
    return out


def baca_aspek_detail(heading, rows):
    """Format PMP-07: satu tabel 'Aspek | Detail' per risiko."""
    if [c.strip() for c in rows[0][:2]] != ['Aspek', 'Detail']:
        return None
    d = {r[0].strip(): r[1].strip() for r in rows[1:] if len(r) >= 2}
    if 'Probability' not in d or 'Impact' not in d or 'Risk ID' not in d:
        return None
    nama = re.sub(r'^[A-Z-]+\d+:\s*', '', heading)
    return [{'ID': d['Risk ID'], 'Risiko': nama, 'Kategori': d.get('Kategori', ''),
             'Deskripsi': d.get('Deskripsi', ''), 'Probabilitas_Dokumen': d['Probability'],
             'Dampak_Dokumen': d['Impact'], 'Sumber': heading}]


def ekstrak(kode):
    tabel = tabel_pmp(kode)
    kelompok = {}  # header -> daftar risiko
    detail = []
    for i, (h, rows) in enumerate(tabel):
        if not rows:
            continue
        ad = baca_aspek_detail(_judul_risiko(kode, i) or h, rows)
        if ad:
            detail += ad
            continue
        reg = baca_tabel_register(h, rows)
        if reg:
            kelompok.setdefault(tuple(c.strip() for c in rows[0]), []).extend(reg)
    if detail:
        utama, lain = detail, [r for g in kelompok.values() for r in g]
    else:
        kunci = max(kelompok, key=lambda k: len(kelompok[k]))
        utama, lain = kelompok[kunci], [r for k, g in kelompok.items() if k != kunci for r in g]
    kategori_lain = {r['ID']: r['Kategori'] for r in lain if r['Kategori']}

    hasil, dilihat = [], set()
    for r in utama:
        if r['ID'] in dilihat:
            continue
        dilihat.add(r['ID'])
        r['Kategori'] = r['Kategori'] or kategori_lain.get(r['ID'], '')
        r['Peluang'] = peluang(r['Probabilitas_Dokumen'])
        r['Level_Dampak'] = level_dampak(r['Dampak_Dokumen'])
        teks = f"{r['Risiko']} {r['Deskripsi']}"
        if r['Peluang'] is None or r['Level_Dampak'] is None:
            r['Dipakai_Simulasi'], r['Alasan'] = 0, 'Peluang/dampak tidak terbaca'
        elif KATEGORI_BIAYA.match(r['Kategori']) or (POLA_BIAYA.search(r['Risiko']) and not re.search(
                r'delay|terlambat|keterlambatan|schedule|jadwal', r['Risiko'], re.I)):
            # dicek lebih dulu dari CR: uraian risiko biaya sering menyebut "scope" sebagai penyebab
            r['Dipakai_Simulasi'], r['Alasan'] = 0, 'Risiko biaya: tidak menggeser jadwal'
        elif POLA_CR.search(teks):
            r['Dipakai_Simulasi'], r['Alasan'] = 0, 'Perubahan scope/requirement: sudah dimodelkan sebagai CR'
        else:
            r['Dipakai_Simulasi'], r['Alasan'] = 1, ''
        r['Sumber'] = f"PMP-{kode} {r['Sumber']}".strip()
        hasil.append(r)
    return hasil


_JUDUL = {}


def _judul_risiko(kode, indeks):
    """Judul tepat di atas tabel ke-indeks (untuk PMP-07: 'R-TECH-001: Kegagalan ...')."""
    if kode not in _JUDUL:
        import zipfile
        import xml.etree.ElementTree as ET
        from ekstraksi_pmp import RAW, W, _teks
        f = next(RAW.glob(f'2026 PMP *{NAMA_PMP[kode]}.docx'))
        body = ET.fromstring(zipfile.ZipFile(f).read('word/document.xml')).find(W + 'body')
        judul, daftar = '', []
        for el in body:
            if el.tag == W + 'p':
                t = _teks(el)
                if t and len(t) < 120:
                    judul = t
            elif el.tag == W + 'tbl':
                daftar.append(judul)
        _JUDUL[kode] = daftar
    j = _JUDUL[kode][indeks]
    return j if POLA_ID.match(j) else ''


KOLOM = ['ID', 'Risiko', 'Kategori', 'Probabilitas_Dokumen', 'Dampak_Dokumen', 'Peluang', 'Level_Dampak',
         'Dipakai_Simulasi', 'Alasan', 'Sumber']


def main():
    print(f'{"Sub":<9}{"risiko":>7}{"dipakai":>9}{"rata2 peluang":>15}{"rata2 dampak":>14}')
    for kode in NAMA_PMP:
        rows = ekstrak(kode)
        with open(DATA / f'P-FNE-{kode}_risiko.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=KOLOM, extrasaction='ignore')
            w.writeheader()
            w.writerows(rows)
        pakai = [r for r in rows if r['Dipakai_Simulasi']]
        rp = sum(r['Peluang'] for r in pakai) / len(pakai) if pakai else 0
        rd = sum(r['Level_Dampak'] for r in pakai) / len(pakai) if pakai else 0
        print(f'P-FNE-{kode}{len(rows):>7}{len(pakai):>9}{rp:>15.2f}{rd:>14.2f}')


if __name__ == '__main__':
    main()
