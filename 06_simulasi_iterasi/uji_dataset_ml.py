"""
PRE-02: Uji validasi dataset ML. Jalankan:  python uji_dataset_ml.py

1. Kewajaran   : tanpa CR dan tanpa risiko, proyek harus tepat rencana (SPI 1, telat 0, tidak ada CR/risiko).
2. Kebocoran   : fitur pada hari t harus identik jika semua kejadian risiko setelah t dibuang.
                 Uji pembanding yang sengaja bocor (memakai durasi akhir) harus TERDETEKSI.
3. Risiko vs PMP: ID, nama, peluang & dampak asli tiap baris data/P-FNE-0X_risiko.csv ada di teks PMP-nya.
4. Dataset     : tidak ada nilai kosong/duplikat, 3.000 baris per subproyek, label sama di ketiga titik
                 monitoring satu iterasi, dan fitur di rentang wajar.
"""

import csv
import random
import re
import zipfile
import xml.etree.ElementTree as ET

import buat_dataset_ml as ml
import simulasi_iterasi as sim
from ekstraksi_pmp import NAMA_PMP, RAW, W

N_KEBOCORAN = 100


def _siapkan(kode):
    akt, org = sim.baca_aktivitas(kode), sim.baca_resource(kode)
    dr = {a['ID']: a['Durasi_Hari'] for a in akt}
    ren = sim.jadwal_dengan_resource(akt, dr, org, ml.KEBIJAKAN)
    return akt, org, ren, max(j['selesai'] for j in ren.values())


def uji_kewajaran():
    p_cr = sim.P_CR
    sim.P_CR = 0.0
    try:
        for kode in sim.SUBPROYEK:
            akt, org, ren, sr = _siapkan(kode)
            cr, dcr, jad, terjadi = ml.iterasi(random.Random(1), akt, org, [], sim.SKENARIO_CR['dosen'], sr)
            assert abs(max(j['selesai'] for j in jad.values()) - sr) < 1e-9, kode
            for titik in ml.TITIK_MONITORING:
                f = ml.fitur(titik * sr, akt, ren, jad, dcr, org, cr, terjadi, sr)
                assert abs(f['SPI_Jadwal'] - 1) < 1e-9 and f['Frekuensi_CR'] == 0, (kode, titik, f)
                assert f['Risiko_Belum_Dimitigasi'] == 0 and abs(f['Pergeseran_Dependency_Hari']) < 1e-9, (kode, f)
                assert 0 <= f['Utilisasi_Resource'] <= 1 and 0 < f['Backlog_Sisa_Persen'] < 1, (kode, f)
    finally:
        sim.P_CR = p_cr
    return '8 subproyek tepat rencana tanpa gangguan'


def _jumlah_beda(sengaja_bocor):
    beda = total = 0
    for kode in sim.SUBPROYEK:
        akt, org, ren, sr = _siapkan(kode)
        risiko = ml.baca_risiko(kode)
        rng = random.Random(f'uji-kebocoran-{kode}')
        for _ in range(N_KEBOCORAN):
            cr, dcr, jad, terjadi = ml.iterasi(rng, akt, org, risiko, sim.SKENARIO_CR['dosen'], sr)
            for titik in ml.TITIK_MONITORING:
                t = round(titik * sr, 4)
                sebagian = [k for k in terjadi if k[0] <= t]
                d = dict(dcr)
                for _, i, tambah in sebagian:
                    d[i] = round(d[i] + tambah, 4)
                jad2 = sim.jadwal_dengan_resource(akt, d, org, ml.KEBIJAKAN)
                if sengaja_bocor:  # versi salah: progres memakai durasi akhir (termasuk risiko setelah t)
                    akhir = dict(dcr)
                    for _, i, tambah in terjadi:
                        akhir[i] += tambah
                    a = ml.fitur(t, akt, ren, jad, akhir, org, cr, [], sr)
                    b = ml.fitur(t, akt, ren, jad2, d, org, cr, [], sr)
                else:
                    a = ml.fitur(t, akt, ren, jad, dcr, org, cr, terjadi, sr)
                    b = ml.fitur(t, akt, ren, jad2, dcr, org, cr, sebagian, sr)
                total += 1
                beda += any(abs(a[k] - b[k]) > 1e-6 for k in ml.FITUR)
    return beda, total


def uji_kebocoran():
    beda, total = _jumlah_beda(False)
    assert beda == 0, f'ADA KEBOCORAN: {beda}/{total}'
    beda_salah, total_salah = _jumlah_beda(True)
    assert beda_salah > 0, 'Uji tidak mampu mendeteksi kebocoran'
    return f'0/{total} titik berbeda; versi sengaja bocor terdeteksi {beda_salah}/{total_salah}'


def uji_risiko_vs_pmp():
    norm = lambda s: re.sub(r'\s+', ' ', s).strip()
    total = 0
    for kode, nama in NAMA_PMP.items():
        f = next(RAW.glob(f'2026 PMP *{nama}.docx'))
        root = ET.fromstring(zipfile.ZipFile(f).read('word/document.xml'))
        sel = {norm(' '.join(''.join(t.text or '' for t in p.iter(W + 't')) for p in c.iter(W + 'p')))
               for c in root.iter(W + 'tc')}
        sel |= {norm(''.join(t.text or '' for t in c.iter(W + 't'))) for c in root.iter(W + 'tc')}
        paragraf = {norm(''.join(t.text or '' for t in p.iter(W + 't'))) for p in root.iter(W + 'p')}
        teks = ' '.join(sel | paragraf)
        with open(sim.DATA / f'P-FNE-{kode}_risiko.csv', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                total += 1
                assert r['ID'] in teks and norm(r['Risiko'])[:20] in teks, (kode, r['ID'], 'ID/nama')
                assert norm(r['Probabilitas_Dokumen']) in sel and norm(r['Dampak_Dokumen']) in sel, (kode, r['ID'])
    return f'{total}/{total} risiko cocok dengan teks PMP'


def uji_dataset():
    with open(ml.OUT / 'dataset_ml.csv', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    assert all(v != '' for r in rows for v in r.values()), 'ada nilai kosong'
    kunci = {(r['Subproyek'], r['Iterasi'], r['Titik_Monitoring']) for r in rows}
    assert len(kunci) == len(rows), 'ada baris duplikat'
    for kode in sim.SUBPROYEK:
        assert sum(r['Subproyek'] == f'P-FNE-{kode}' for r in rows) == ml.N_ITERASI * len(ml.TITIK_MONITORING)
    label = {}
    for r in rows:
        label.setdefault((r['Subproyek'], r['Iterasi']), set()).add(tuple(r[k] for k in ml.LABEL))
    assert all(len(v) == 1 for v in label.values()), 'label berbeda antartitik dalam satu iterasi'
    for r in rows:
        assert 0 < float(r['SPI_Jadwal']) <= 1.1 and 0 <= float(r['Utilisasi_Resource']) <= 1
        assert 0 <= float(r['Backlog_Sisa_Persen']) <= 1 and float(r['Sisa_Waktu_Hari']) > 0
        assert int(r['Risiko_Belum_Dimitigasi']) >= 0 and int(r['Frekuensi_CR']) >= 0
    return f'{len(rows)} baris, 0 kosong, 0 duplikat, label konsisten, rentang fitur wajar'


if __name__ == '__main__':
    for nama, fungsi in [('Kewajaran', uji_kewajaran), ('Kebocoran', uji_kebocoran),
                         ('Risiko vs PMP', uji_risiko_vs_pmp), ('Dataset', uji_dataset)]:
        print(f'[LULUS] {nama}: {fungsi()}')
