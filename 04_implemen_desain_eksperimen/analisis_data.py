"""
PRE-02: Analisis Data Eksperimen (Pertemuan 6)
Studi kasus: 8 subproyek Super ERP Farm Nation Enterprise (FNE) 2026

Menganalisis luaran Pertemuan 5 (hasil_eksperimen/tabel_prediksi_oof.csv) tanpa melatih ulang model, kecuali
permutation importance model rekomendasi (Bagian F).

  A. Selang kepercayaan 95% semua metrik (bootstrap klaster per iterasi simulasi, B = 2000)
  B. Uji hipotesis H1–H5, satu per eksperimen di Deskripsi_Penelitian.md §4:
       H1  Eksp. 1 LR "baseline ... terkalibrasi dengan baik"  : Brier LR < naif; intercept kalibrasi ≈ 0, slope ≈ 1
       H2  Eksp. 2 RF "meningkatkan akurasi"                   : Brier RF < Brier LR
       H3  Eksp. 3 GB "kalibrasi probabilitas terbaik"         : Brier dan ECE GB < tiap model lain
       H4  Eksp. 4 NN "menangkap pola non-linear"              : Brier NN < Brier LR
       H5  Eksp. 5 "rekomendasi model dengan kalibrasi terbaik": ECE Platt/Isotonic < ECE Raw (tiap model)
     Uji: selisih berpasangan bootstrap (satu arah), koreksi Holm atas seluruh uji; ketahanan antarsubproyek dengan
     uji peringkat bertanda Wilcoxon eksak pada 8 selisih per subproyek.
  C. Dekomposisi Brier (Murphy, 1973): reliability, resolution, uncertainty
  D. Analisis per titik monitoring dengan selang kepercayaan
  E. Analisis ambang & deteksi dini (Deskripsi §5 Analisis Tambahan; §6 early warning system)
  F. Analisis per subproyek & kepentingan fitur model rekomendasi

Jalankan (dari folder ini, setelah experiment_pipeline.py):
  python analisis_data.py
Kebutuhan: pandas, numpy, scikit-learn, matplotlib, joblib
"""

import argparse
import itertools
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from sklearn.inspection import permutation_importance

import experiment_pipeline as ep
from experiment_pipeline import (FITUR, GRUP, KALIBRASI, LABEL, MODEL, NAIF, SEED, TITIK, ZONA, N_BIN_ECE,
                                 WARNA, GARIS, TINTA, TINTA_2, PERMUKAAN, _gaya, f, pct)

HASIL_EKSP = ep.HERE / 'hasil_eksperimen'
N_BOOT = 2000
ALFA = 0.05
TITIK_LIST = [0.25, 0.5, 0.75]
SINGKAT = {'Logistic Regression': 'LR', 'Random Forest': 'RF', 'Gradient Boosting': 'GB',
           'MLP Neural Network': 'NN', NAIF: 'Naif'}

# ============================================================
# 0. DATA
# ============================================================


def kolom(model, kal):
    return f'P_{model.replace(" ", "_")}_{kal}'


def semua_kombinasi():
    return [(NAIF, 'Raw')] + [(m, k) for m in MODEL for k in KALIBRASI]


def muat_prediksi(path):
    p = pd.read_csv(path)
    for m, k in semua_kombinasi():
        assert kolom(m, k) in p.columns, f'Kolom prediksi tidak ada: {kolom(m, k)}'
    klaster = p.groupby([GRUP, 'Iterasi'], sort=False).ngroup().to_numpy()
    assert (np.bincount(klaster) == len(TITIK_LIST)).all(), 'Setiap iterasi harus punya 3 titik monitoring'
    return p, klaster


# ============================================================
# 1. METRIK BERBOBOT (bobot = berapa kali klaster terambil di bootstrap; bobot 1 = metrik biasa)
# ============================================================

def siapkan(y, p):
    """Prakomputasi agar metrik berbobot cepat dihitung berulang kali."""
    urut = np.argsort(p, kind='mergesort')
    ps = p[urut]
    gid = np.concatenate([[0], np.cumsum(ps[1:] != ps[:-1])])
    q = np.clip(p, 1e-6, 1 - 1e-6)
    return {'y': y.astype(float), 'p': p, 'bin': np.minimum((p * N_BIN_ECE).astype(int), N_BIN_ECE - 1),
            'urut': urut, 'ys': y[urut].astype(float), 'gid': gid, 'L': np.log(q / (1 - q)),
            'll': -(y * np.log(np.clip(p, 1e-15, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-15, 1)))}


def _sigmoid(x):
    return 0.5 * (1 + np.tanh(0.5 * x))


def intercept_slope(L, y, w):
    """Kalibrasi logistik: y ~ a + b·logit(p) (slope) dan y ~ a + offset(logit(p)) (intercept, calibration-in-the-large).
    Kalibrasi sempurna: intercept 0, slope 1 (Van Calster dkk., 2016)."""
    a = 0.0
    for _ in range(100):
        mu = _sigmoid(a + L)
        da = (w * (y - mu)).sum() / (w * mu * (1 - mu)).sum()
        a += da
        if abs(da) < 1e-10:
            break
    def ll(c, b):  # log-likelihood berbobot, stabil secara numerik
        eta = c + b * L
        return (w * (y * eta - np.logaddexp(0, eta))).sum()

    c, b = 0.0, 1.0
    sekarang = ll(c, b)
    for _ in range(200):
        mu = _sigmoid(c + b * L)
        r, v = w * (y - mu), w * mu * (1 - mu)
        g0, g1 = r.sum(), (r * L).sum()
        h00, h01, h11 = v.sum(), (v * L).sum(), (v * L * L).sum()
        det = h00 * h11 - h01 ** 2
        dc, db = (h11 * g0 - h01 * g1) / det, (h00 * g1 - h01 * g0) / det
        langkah = 1.0  # Newton teredam: langkah dipotong setengah sampai log-likelihood naik
        while langkah > 1e-8 and ll(c + langkah * dc, b + langkah * db) < sekarang:
            langkah /= 2
        c, b = c + langkah * dc, b + langkah * db
        sekarang = ll(c, b)
        if langkah * (abs(dc) + abs(db)) < 1e-10:
            break
    return a, b


METRIK = ['Brier', 'Log_Loss', 'ECE', 'ROC_AUC', 'Intercept_Kalibrasi', 'Slope_Kalibrasi']


def nilai(s, w, lengkap=True):
    W = w.sum()
    y, p = s['y'], s['p']
    brier = (w * (p - y) ** 2).sum() / W
    nb = np.bincount(s['bin'], w * y, N_BIN_ECE) - np.bincount(s['bin'], w * p, N_BIN_ECE)
    ece = np.abs(nb).sum() / W
    ws = w[s['urut']]
    pos = np.bincount(s['gid'], ws * s['ys'])
    neg = np.bincount(s['gid'], ws * (1 - s['ys']))
    auc = (pos * (np.cumsum(neg) - neg + 0.5 * neg)).sum() / (pos.sum() * neg.sum()) if pos.sum() and neg.sum() else np.nan
    hasil = [brier, (w * s['ll']).sum() / W, ece, auc]
    if lengkap:
        hasil += list(intercept_slope(s['L'], y, w))
    return hasil


# ============================================================
# A–D. BOOTSTRAP KLASTER
# ============================================================

def butir_bootstrap(p, klaster, rek):
    """Daftar (label, model, kalibrasi, mask baris) yang dihitung di setiap replikasi bootstrap."""
    butir = [('Semua', m, k, None) for m, k in semua_kombinasi()]
    model_titik = [(NAIF, 'Raw')] + [(m, 'Raw') for m in MODEL] + ([rek] if rek[1] != 'Raw' else [])
    for t in TITIK_LIST:
        mask = (p[TITIK] == t).to_numpy()
        butir += [(t, m, k, mask) for m, k in model_titik]
    return butir


def _hitung_chunk(prakom, klaster, counts):
    out = np.empty((len(counts), len(prakom), len(METRIK)))
    for i, c in enumerate(counts):
        w = c[klaster].astype(float)
        for j, (s, mask, lengkap) in enumerate(prakom):
            v = nilai(s, w if mask is None else w[mask], lengkap)
            out[i, j, :len(v)] = v
            out[i, j, len(v):] = np.nan
    return out


def bootstrap(p, klaster, butir, n_boot, n_jobs):
    y = p[LABEL].to_numpy()
    prakom = []
    for lbl, m, k, mask in butir:
        q = p[kolom(m, k)].to_numpy()
        lengkap = lbl == 'Semua' and m != NAIF
        prakom.append((siapkan(y if mask is None else y[mask], q if mask is None else q[mask]), mask, lengkap))
    n_k = klaster.max() + 1
    rng = np.random.default_rng(SEED)
    counts = rng.multinomial(n_k, np.full(n_k, 1 / n_k), size=n_boot)  # dibangkitkan sekali → hasil tidak bergantung n_jobs
    titik = _hitung_chunk(prakom, klaster, np.ones((1, n_k), int))[0]
    chunks = np.array_split(counts, max(1, min(n_boot, 64)))
    boot = np.concatenate(Parallel(n_jobs=n_jobs)(delayed(_hitung_chunk)(prakom, klaster, c) for c in chunks))
    return titik, boot


def tabel_ci(butir, titik, boot, label):
    idx = {(b[0], b[1], b[2]): i for i, b in enumerate(butir)}
    baris = []
    for lbl, m, k, _ in butir:
        if lbl != label:
            continue
        i, n = idx[(lbl, m, k)], idx[(lbl, NAIF, 'Raw')]
        r = {'Model': m, 'Kalibrasi': k} if label == 'Semua' else {TITIK: lbl, 'Model': m, 'Kalibrasi': k}
        bss_t = 1 - titik[i, 0] / titik[n, 0]
        bss_b = 1 - boot[:, i, 0] / boot[:, n, 0]
        nama_metrik = METRIK if label == 'Semua' else METRIK[:4]
        for j, nm in enumerate(nama_metrik):
            r[nm] = titik[i, j]
            v = boot[:, i, j]
            r[nm + '_CI_Bawah'], r[nm + '_CI_Atas'] = np.percentile(v, [2.5, 97.5]) if np.isfinite(v).all() else (np.nan, np.nan)
            if nm == 'Brier':
                r['BSS'] = bss_t
                r['BSS_CI_Bawah'], r['BSS_CI_Atas'] = np.percentile(bss_b, [2.5, 97.5])
        baris.append(r)
    t = pd.DataFrame(baris)
    if label == 'Semua':
        nf = t.Model == NAIF
        t.loc[nf, [c for c in t.columns if c.startswith(('Intercept', 'Slope', 'ROC_AUC'))]] = np.nan  # tak bermakna utk naif
    return t


# ============================================================
# B. UJI HIPOTESIS
# ============================================================

def daftar_uji():
    """(Hipotesis, kode, A, B, metrik). Arah yang diharapkan selalu: metrik A < metrik B."""
    LR, RF, GB, NN = [(m, 'Raw') for m in MODEL]
    u = [('H1', 'H1a', LR, (NAIF, 'Raw'), 'Brier'),
         ('H2', 'H2', RF, LR, 'Brier'),
         ('H3', 'H3a', GB, LR, 'Brier'), ('H3', 'H3b', GB, RF, 'Brier'), ('H3', 'H3c', GB, NN, 'Brier'),
         ('H3', 'H3d', GB, LR, 'ECE'), ('H3', 'H3e', GB, RF, 'ECE'), ('H3', 'H3f', GB, NN, 'ECE'),
         ('H4', 'H4', NN, LR, 'Brier')]
    huruf = iter('abcdefgh')
    for m in MODEL:
        for k in ('Platt', 'Isotonic'):
            u.append(('H5', f'H5{next(huruf)}', (m, k), (m, 'Raw'), 'ECE'))
    return u


def holm(pv):
    pv = np.asarray(pv, float)
    urut = np.argsort(pv)
    adj = np.empty_like(pv)
    berjalan = 0.0
    for r, i in enumerate(urut):
        berjalan = max(berjalan, min(1.0, (len(pv) - r) * pv[i]))
        adj[i] = berjalan
    return adj


def wilcoxon_eksak(d):
    """Uji peringkat bertanda Wilcoxon eksak, satu arah (H1: median selisih < 0). Mengembalikan p."""
    d = np.asarray(d, float)
    d = d[d != 0]
    if len(d) == 0:
        return 1.0
    r = pd.Series(np.abs(d)).rank().to_numpy()
    t_obs = r[d > 0].sum()
    semua = np.array([sum(ri for ri, s in zip(r, tanda) if s) for tanda in itertools.product([0, 1], repeat=len(d))])
    return float((semua <= t_obs + 1e-12).mean())


def metrik_subproyek(p, model, kal, nama):
    y = p[LABEL].to_numpy()
    q = p[kolom(model, kal)].to_numpy()
    g = p[GRUP].to_numpy()
    out = {}
    for sub in sorted(np.unique(g)):
        m = g == sub
        out[sub] = np.mean((q[m] - y[m]) ** 2) if nama == 'Brier' else ep.ece(y[m], q[m])
    return pd.Series(out)


def tabel_uji(p, butir, titik, boot):
    idx = {(b[0], b[1], b[2]): i for i, b in enumerate(butir)}
    j = {'Brier': 0, 'ECE': 2}
    baris = []
    for h, kode, A, B, nm in daftar_uji():
        ia, ib = idx[('Semua', *A)], idx[('Semua', *B)]
        sel = boot[:, ia, j[nm]] - boot[:, ib, j[nm]]
        dsub = metrik_subproyek(p, *A, nm) - metrik_subproyek(p, *B, nm)
        baris.append({'Hipotesis': h, 'Kode_Uji': kode, 'A': f'{A[0]} + {A[1]}', 'B': f'{B[0]} + {B[1]}',
                      'Metrik': nm, 'Nilai_A': titik[ia, j[nm]], 'Nilai_B': titik[ib, j[nm]],
                      'Selisih_A_minus_B': titik[ia, j[nm]] - titik[ib, j[nm]],
                      'CI_Bawah': np.percentile(sel, 2.5), 'CI_Atas': np.percentile(sel, 97.5),
                      'p_Bootstrap': (1 + (sel >= 0).sum()) / (len(sel) + 1),
                      'Subproyek_Searah': int((dsub < 0).sum()), 'p_Wilcoxon_Subproyek': wilcoxon_eksak(dsub.values)})
    t = pd.DataFrame(baris)
    t['p_Holm'] = holm(t.p_Bootstrap)
    t['Signifikan'] = (t.p_Holm < ALFA).astype(int)
    t['Arah_Berlawanan_Signifikan'] = (t.CI_Bawah > 0).astype(int)
    return t


def keputusan(uji, ci):
    """Ringkas keputusan tiap hipotesis dari hasil uji (aturan tertulis di kolom Kriteria)."""
    lr = ci[(ci.Model == 'Logistic Regression') & (ci.Kalibrasi == 'Raw')].iloc[0]
    kal_baik = (lr.Intercept_Kalibrasi_CI_Bawah <= 0 <= lr.Intercept_Kalibrasi_CI_Atas and
                lr.Slope_Kalibrasi_CI_Bawah <= 1 <= lr.Slope_Kalibrasi_CI_Atas)
    s = uji.set_index('Kode_Uji')

    def status(kode):
        r = s.loc[kode]
        return 'signifikan' if r.Signifikan else ('berlawanan' if r.Arah_Berlawanan_Signifikan else 'tidak')

    def rangkum(kodes):
        n = sum(status(k) == 'signifikan' for k in kodes)
        lawan = sum(status(k) == 'berlawanan' for k in kodes)
        if n == len(kodes):
            return 'Diterima'
        return 'Diterima sebagian' if n > lawan else 'Ditolak'

    def konsisten(kodes):
        return '; '.join(f'{k}: {s.loc[k].Subproyek_Searah}/8 subproyek searah (Wilcoxon p = '
                         f'{f(s.loc[k].p_Wilcoxon_Subproyek, 3)})' for k in kodes)

    h1_kode = 'Diterima' if (status('H1a') == 'signifikan' and kal_baik) else \
        ('Diterima sebagian' if (status('H1a') == 'signifikan' or kal_baik) else 'Ditolak')
    h5 = [k for k in s.index if k.startswith('H5')]
    kom = ci[ci.Model != NAIF]
    ece_min, brier_min = kom.loc[kom.ECE.idxmin()], kom.loc[kom.Brier.idxmin()]
    baris = [
        ('H1', 'Eksperimen 1: LR sebagai baseline yang terkalibrasi dengan baik',
         'Logistic Regression memberi probabilitas lebih akurat daripada pembanding naif dan terkalibrasi baik',
         'H1a signifikan (Brier LR < naif) DAN CI intercept kalibrasi memuat 0 serta CI slope memuat 1', h1_kode,
         f'H1a {status("H1a")}; intercept {f(lr.Intercept_Kalibrasi, 3)} [{f(lr.Intercept_Kalibrasi_CI_Bawah, 3)}; '
         f'{f(lr.Intercept_Kalibrasi_CI_Atas, 3)}], slope {f(lr.Slope_Kalibrasi, 3)} [{f(lr.Slope_Kalibrasi_CI_Bawah, 3)}; '
         f'{f(lr.Slope_Kalibrasi_CI_Atas, 3)}]'),
        ('H2', 'Eksperimen 2: RF untuk meningkatkan akurasi prediksi probabilitas',
         'Random Forest lebih akurat (Brier lebih kecil) daripada Logistic Regression', 'H2 signifikan',
         rangkum(['H2']), f'H2 {status("H2")}'),
        ('H3', 'Eksperimen 3: GB untuk mencapai kalibrasi probabilitas terbaik',
         'Gradient Boosting memiliki Brier dan ECE terkecil dibanding LR, RF, dan NN',
         'H3a–H3f semua signifikan; sebagian bila hanya sebagian', rangkum(['H3a', 'H3b', 'H3c', 'H3d', 'H3e', 'H3f']),
         '; '.join(f'{k} {status(k)}' for k in ['H3a', 'H3b', 'H3c', 'H3d', 'H3e', 'H3f'])),
        ('H4', 'Eksperimen 4: NN untuk menangkap pola non-linear',
         'Neural Network (sigmoid) lebih akurat (Brier lebih kecil) daripada Logistic Regression yang linear',
         'H4 signifikan', rangkum(['H4']), f'H4 {status("H4")}'),
        ('H5', 'Eksperimen 5: analisis kalibrasi dan rekomendasi model dengan kalibrasi terbaik',
         'Kalibrasi pasca-latih (Platt/Isotonic) menurunkan ECE dibanding probabilitas mentah (Raw)',
         'Per pasangan model × metode (8 uji); diterima bila semua signifikan, sebagian bila yang membaik lebih banyak '
         'daripada yang memburuk signifikan, selain itu ditolak', rangkum(h5),
         f'{sum(status(k) == "signifikan" for k in h5)} dari {len(h5)} signifikan membaik '
         f'({", ".join(k for k in h5 if status(k) == "signifikan")}); '
         f'{sum(status(k) == "berlawanan" for k in h5)} justru memburuk signifikan. Kalibrasi terbaik: ECE terendah '
         f'{ece_min.Model} + {ece_min.Kalibrasi} ({f(ece_min.ECE)}), Brier terendah {brier_min.Model} + '
         f'{brier_min.Kalibrasi} ({f(brier_min.Brier)})')]
    t = pd.DataFrame(baris, columns=['Hipotesis', 'Sumber_Deskripsi', 'Pernyataan', 'Kriteria', 'Keputusan', 'Rincian'])
    kode_h = {h: [k for k in s.index if k.startswith(h)] for h in t.Hipotesis}
    t['Konsistensi_Antarsubproyek'] = [konsisten(kode_h[h]) for h in t.Hipotesis]
    return t


def uji_rekomendasi(butir, titik, boot, tabel_eksp):
    """Tambahan (bukan hipotesis): apakah rekomendasi berbeda nyata dari kombinasi terbaik kedua (dua arah)."""
    idx = {(b[0], b[1], b[2]): i for i, b in enumerate(butir)}
    urut = tabel_eksp[tabel_eksp.Model != NAIF].sort_values(['Brier', 'ECE', 'Log_Loss'])
    a, b = tuple(urut.iloc[0][['Model', 'Kalibrasi']]), tuple(urut.iloc[1][['Model', 'Kalibrasi']])
    sel = boot[:, idx[('Semua', *a)], 0] - boot[:, idx[('Semua', *b)], 0]
    p2 = min(1.0, 2 * min((sel >= 0).mean(), (sel <= 0).mean()) + 2 / (len(sel) + 1))
    return {'A': f'{a[0]} + {a[1]}', 'B': f'{b[0]} + {b[1]}', 'Metrik': 'Brier',
            'Selisih_A_minus_B': titik[idx[('Semua', *a)], 0] - titik[idx[('Semua', *b)], 0],
            'CI_Bawah': np.percentile(sel, 2.5), 'CI_Atas': np.percentile(sel, 97.5), 'p_Dua_Arah': p2}


def uji_titik(butir, titik, boot, rek):
    """Perubahan ROC-AUC & Brier antartitik monitoring (berpasangan: titik-titik berasal dari iterasi yang sama)."""
    idx = {(b[0], b[1], b[2]): i for i, b in enumerate(butir)}
    baris = []
    for m, k in [(mm, 'Raw') for mm in MODEL] + ([rek] if rek[1] != 'Raw' else []):
        for t1, t2 in [(0.25, 0.5), (0.5, 0.75), (0.25, 0.75)]:
            for j, nm in [(3, 'ROC_AUC'), (0, 'Brier')]:
                i1, i2 = idx[(t1, m, k)], idx[(t2, m, k)]
                sel = boot[:, i2, j] - boot[:, i1, j]
                baris.append({'Model': m, 'Kalibrasi': k, 'Dari': t1, 'Ke': t2, 'Metrik': nm,
                              'Nilai_Dari': titik[i1, j], 'Nilai_Ke': titik[i2, j], 'Perubahan': titik[i2, j] - titik[i1, j],
                              'CI_Bawah': np.percentile(sel, 2.5), 'CI_Atas': np.percentile(sel, 97.5)})
    return pd.DataFrame(baris)


# ============================================================
# C. DEKOMPOSISI BRIER (Murphy, 1973)
# ============================================================

def murphy(y, q):
    b = np.minimum((q * N_BIN_ECE).astype(int), N_BIN_ECE - 1)
    n = np.bincount(b, minlength=N_BIN_ECE).astype(float)
    m = n > 0
    pk = np.bincount(b, q, N_BIN_ECE)[m] / n[m]
    ok = np.bincount(b, y, N_BIN_ECE)[m] / n[m]
    o = y.mean()
    rel = (n[m] * (pk - ok) ** 2).sum() / len(y)
    res = (n[m] * (ok - o) ** 2).sum() / len(y)
    unc = o * (1 - o)
    brier = np.mean((q - y) ** 2)
    return {'Brier': brier, 'Reliability': rel, 'Resolution': res, 'Uncertainty': unc,
            'Sisa_Dalam_Bin': brier - (rel - res + unc)}


def tabel_murphy(p):
    y = p[LABEL].to_numpy().astype(float)
    return pd.DataFrame([{'Model': m, 'Kalibrasi': k, **murphy(y, p[kolom(m, k)].to_numpy())}
                         for m, k in semua_kombinasi()])


# ============================================================
# E. AMBANG & DETEKSI DINI
# ============================================================

def _biner(y, q, a):
    pred = q >= a
    tp, fp = int((pred & (y == 1)).sum()), int((pred & (y == 0)).sum())
    tn, fn = int((~pred & (y == 0)).sum()), int((~pred & (y == 1)).sum())
    rec = tp / (tp + fn) if tp + fn else np.nan
    spe = tn / (tn + fp) if tn + fp else np.nan
    pre = tp / (tp + fp) if tp + fp else np.nan
    return {'Persen_Peringatan': pred.mean(), 'Recall': rec, 'Specificity': spe, 'Precision': pre,
            'F1': 2 * pre * rec / (pre + rec) if (tp and pre + rec) else 0.0, 'Youden_J': rec + spe - 1,
            'TP': tp, 'FP': fp, 'TN': tn, 'FN': fn}


def ambang_khusus(theta):
    return [(theta, 'θ* Youden'), (ZONA[0], 'Batas Kuning'), (ZONA[1], 'Batas Merah')]


def tabel_ambang(p, rek, theta):
    y = p[LABEL].to_numpy()
    q = p[kolom(*rek)].to_numpy()
    baris = [{'Ambang': a, 'Keterangan': '', 'Titik_Monitoring': 'Semua', **_biner(y, q, a)}
             for a in np.round(np.arange(0.05, 0.96, 0.05), 2)]
    for a, ket in ambang_khusus(theta):
        baris.append({'Ambang': a, 'Keterangan': ket, 'Titik_Monitoring': 'Semua', **_biner(y, q, a)})
        for t in TITIK_LIST:
            m = (p[TITIK] == t).to_numpy()
            baris.append({'Ambang': a, 'Keterangan': ket, 'Titik_Monitoring': t, **_biner(y[m], q[m], a)})
    return pd.DataFrame(baris)


def tabel_deteksi_dini(p, data, rek, theta):
    """Untuk tiap iterasi: titik monitoring pertama yang probabilitasnya ≥ ambang (peringatan pertama)."""
    q = p.pivot_table(index=[GRUP, 'Iterasi'], columns=TITIK, values=kolom(*rek))[TITIK_LIST]
    y = p.groupby([GRUP, 'Iterasi'])[LABEL].first().reindex(q.index)
    sisa = data.pivot_table(index=[GRUP, 'Iterasi'], columns=TITIK, values='Sisa_Waktu_Hari')[TITIK_LIST].reindex(q.index)
    baris = []
    for a, ket in ambang_khusus(theta):
        naik = (q.to_numpy() >= a)
        kum = np.maximum.accumulate(naik, axis=1)  # sudah pernah diperingatkan sampai titik t
        pertama = np.where(naik.any(1), naik.argmax(1), -1)
        r = {'Ambang': a, 'Keterangan': ket}
        for kelas, nama in [(1, 'Telat'), (0, 'Tepat')]:
            m = (y == kelas).to_numpy()
            for j, t in enumerate(TITIK_LIST):
                r[f'{nama}_Diperingatkan_sd_{int(t * 100)}'] = kum[m, j].mean()
        mt = (y == 1).to_numpy() & (pertama >= 0)
        s = sisa.to_numpy()[mt, pertama[mt]]
        r['Rata2_Sisa_Hari_Saat_Peringatan_Pertama'] = np.mean(s) if len(s) else np.nan
        r['Median_Sisa_Hari_Saat_Peringatan_Pertama'] = np.median(s) if len(s) else np.nan
        r['Telat_Tidak_Pernah_Diperingatkan'] = 1 - kum[(y == 1).to_numpy(), -1].mean()
        baris.append(r)
    return pd.DataFrame(baris)


# ============================================================
# F. PER SUBPROYEK & KEPENTINGAN FITUR
# ============================================================

def tabel_subproyek(p, data, rek):
    y_all = p[LABEL].to_numpy()
    baris = []
    for sub in sorted(p[GRUP].unique()):
        m = (p[GRUP] == sub).to_numpy()
        y = y_all[m].astype(float)
        q = p.loc[m, kolom(*rek)].to_numpy()
        n = p.loc[m, kolom(NAIF, 'Raw')].to_numpy()
        mu = murphy(y, q)
        r = {GRUP: sub, 'Prevalensi': y.mean(), 'Rata2_Prediksi_Model': q.mean(), 'Prediksi_Naif': n.mean(),
             'Brier': mu['Brier'], 'Brier_Naif': np.mean((n - y) ** 2), 'ECE': ep.ece(y, q),
             'Reliability': mu['Reliability'], 'Resolution': mu['Resolution'],
             'ROC_AUC': ep.roc_auc_score(y, q) if 0 < y.sum() < len(y) else np.nan}
        r['BSS'] = 1 - r['Brier'] / r['Brier_Naif']
        r['Selisih_Prediksi_Prevalensi'] = r['Rata2_Prediksi_Model'] - r['Prevalensi']
        baris.append(r)
    t = pd.DataFrame(baris)
    profil = data.groupby(GRUP)[FITUR + ['Keterlambatan_Akhir_Hari']].mean().reset_index()
    return t, profil


def _perm_lipatan(rek, X, y, g, latih, uji):
    est = ep.buat_estimator(rek[0], rek[1], g[latih]).fit(X[latih], y[latih])
    r = permutation_importance(est, X[uji], y[uji], scoring='neg_brier_score', n_repeats=10, random_state=SEED)
    return r.importances_mean


def tabel_kepentingan(data, rek, n_jobs):
    X, y, g = data[FITUR].to_numpy(), data[LABEL].to_numpy(), data[GRUP].to_numpy()
    lip = ep.pembagian_luar(g)
    imp = np.array(Parallel(n_jobs=n_jobs)(delayed(_perm_lipatan)(rek, X, y, g, tr, te) for tr, te in lip))
    t = pd.DataFrame({'Fitur': FITUR, 'Rata2_Kenaikan_Brier': imp.mean(0), 'SD_Antar_Lipatan': imp.std(0, ddof=1),
                      'Min': imp.min(0), 'Maks': imp.max(0), 'Lipatan_Positif': (imp > 0).sum(0)})
    for i, sub in enumerate(sorted(np.unique(g))):
        t[f'Lipatan_{sub}'] = imp[[j for j, (_, te) in enumerate(lip) if g[te][0] == sub][0]]
    t['Peringkat'] = t.Rata2_Kenaikan_Brier.rank(ascending=False).astype(int)
    return t.sort_values('Peringkat').reset_index(drop=True)


# ============================================================
# GRAFIK
# ============================================================

def label_uji(r):
    a, b = r.A.split(' + '), r.B.split(' + ')
    sa = SINGKAT[a[0]] + ('' if a[1] == 'Raw' else f' {a[1]}')
    sb = SINGKAT[b[0]] + ('' if b[1] == 'Raw' else f' {b[1]}')
    return f'{r.Kode_Uji}: {sa} − {sb}'


def grafik_uji(uji, path):
    bag = [('Brier', 'Selisih Brier Score (A − B)'), ('ECE', 'Selisih ECE (A − B)')]
    n = [len(uji[uji.Metrik == m]) for m, _ in bag]
    fig, axs = plt.subplots(1, 2, figsize=(12, 0.42 * max(n) + 1.6), facecolor=PERMUKAAN)
    for ax, (m, judul) in zip(axs, bag):
        s = uji[uji.Metrik == m].iloc[::-1]
        pos = np.arange(len(s))
        for yy, (_, r) in zip(pos, s.iterrows()):
            ax.plot([r.CI_Bawah, r.CI_Atas], [yy, yy], color=WARNA['Logistic Regression'], lw=2, solid_capstyle='round')
            biru = WARNA['Logistic Regression']
            if r.Signifikan:
                ax.plot(r.Selisih_A_minus_B, yy, 'o', ms=8, mec=biru, mew=2, mfc=biru)
            elif r.Arah_Berlawanan_Signifikan:
                ax.plot(r.Selisih_A_minus_B, yy, 'X', ms=10, mec=biru, mew=1, mfc=biru)
            else:
                ax.plot(r.Selisih_A_minus_B, yy, 'o', ms=8, mec=biru, mew=2, mfc=PERMUKAAN)
        ax.axvline(0, color=TINTA_2, lw=1)
        ax.set_yticks(pos, [label_uji(r) for _, r in s.iterrows()], fontsize=8)
        ax.set_ylim(-0.7, len(s) - 0.3)
        _gaya(ax, judul, '← A lebih baik    |    B lebih baik →', '')
    h = [plt.Line2D([], [], marker='o', ls='-', color=WARNA['Logistic Regression'], mfc=WARNA['Logistic Regression'],
                    label='Signifikan (Holm, α = 0,05)'),
         plt.Line2D([], [], marker='X', ms=9, ls='-', color=WARNA['Logistic Regression'],
                    label='Signifikan berlawanan arah (CI 95% seluruhnya > 0)'),
         plt.Line2D([], [], marker='o', ls='-', color=WARNA['Logistic Regression'], mfc=PERMUKAAN, label='Tidak signifikan')]
    fig.legend(handles=h, loc='lower center', ncol=3, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_murphy(mur, path):
    t = mur.iloc[::-1].reset_index(drop=True)
    pos = np.arange(len(t))
    fig, ax = plt.subplots(figsize=(7.5, 6), facecolor=PERMUKAAN)
    ax.barh(pos + 0.19, t.Reliability, height=0.36, color=WARNA['Logistic Regression'], label='Reliability (kecil = terkalibrasi)')
    ax.barh(pos - 0.19, t.Resolution, height=0.36, color=WARNA['Random Forest'], label='Resolution (besar = daya beda tinggi)')
    ax.set_yticks(pos, [f'{SINGKAT[m]} {k}' if m != NAIF else 'Naif' for m, k in zip(t.Model, t.Kalibrasi)], fontsize=8)
    _gaya(ax, 'Dekomposisi Brier Score (Murphy): Brier ≈ Reliability − Resolution + Uncertainty', 'Nilai komponen', '')
    ax.legend(fontsize=8, frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_ambang(p, rek, theta, path):
    y = p[LABEL].to_numpy()
    q = p[kolom(*rek)].to_numpy()
    a = np.linspace(0.01, 0.99, 99)
    r = pd.DataFrame([_biner(y, q, x) for x in a])
    fig, ax = plt.subplots(figsize=(7.5, 4.8), facecolor=PERMUKAAN)
    for nm, w, g in [('Recall', 'Logistic Regression', '-'), ('Specificity', 'Random Forest', '--'),
                     ('Precision', 'Gradient Boosting', '-.')]:
        ax.plot(a, r[nm], color=WARNA[w], ls=g, lw=2, label=nm)
    for x, ket in ambang_khusus(theta):
        ax.axvline(x, color=TINTA_2, lw=0.8, ls=':')
        ax.text(x + 0.008, 0.03, f'{ket} ({f(x, 2)})', rotation=90, fontsize=7, color=TINTA_2, va='bottom')
    _gaya(ax, f'Analisis ambang peringatan — {rek[0]} + {rek[1]}', 'Ambang probabilitas', 'Nilai')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=8, frameon=False, loc='center right')
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_deteksi(det, path):
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=PERMUKAAN, sharey=True)
    x = [25, 50, 75]
    warna = ['Logistic Regression', 'Random Forest', 'Gradient Boosting']
    for (_, r), w in zip(det.iterrows(), warna):
        lbl = f'{r.Keterangan} ({f(r.Ambang, 2)})'
        for ax, nama in zip(axs, ['Telat', 'Tepat']):
            ax.plot(x, [100 * r[f'{nama}_Diperingatkan_sd_{t}'] for t in x], color=WARNA[w], ls=GARIS[w], lw=2,
                    marker='o', ms=6, label=lbl)
    _gaya(axs[0], 'Proyek yang akhirnya TELAT: sudah diperingatkan', 'Sampai titik monitoring (% jadwal rencana)',
          '% iterasi (kumulatif)')
    _gaya(axs[1], 'Proyek TEPAT WAKTU: peringatan palsu', 'Sampai titik monitoring (% jadwal rencana)', '')
    for ax in axs:
        ax.set_xticks(x)
        ax.set_ylim(0, 100)
        ax.legend(fontsize=8, frameon=False, loc='upper left')
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_titik_ci(ci_titik, path):
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=PERMUKAAN)
    geser = dict(zip(MODEL, [-3, -1, 1, 3]))
    for m in MODEL:
        s = ci_titik[(ci_titik.Model == m) & (ci_titik.Kalibrasi == 'Raw')].sort_values(TITIK)
        x = s[TITIK].astype(float) * 100 + geser[m]
        for ax, nm in zip(axs, ['ROC_AUC', 'Brier']):
            ax.errorbar(x, s[nm], yerr=[s[nm] - s[nm + '_CI_Bawah'], s[nm + '_CI_Atas'] - s[nm]], color=WARNA[m],
                        ls=GARIS[m], lw=2, marker='o', ms=6, capsize=3, label=m)
    n = ci_titik[ci_titik.Model == NAIF].sort_values(TITIK)
    axs[1].plot(n[TITIK].astype(float) * 100, n.Brier, color=WARNA[NAIF], ls=GARIS[NAIF], lw=1.5, marker='o', ms=5,
                label=NAIF)
    _gaya(axs[0], 'ROC-AUC per titik (CI 95%, lebih besar lebih baik)', 'Titik monitoring (% jadwal rencana)', 'ROC-AUC')
    _gaya(axs[1], 'Brier per titik (CI 95%, lebih kecil lebih baik)', 'Titik monitoring (% jadwal rencana)', 'Brier Score')
    for ax in axs:
        ax.set_xticks([25, 50, 75])
        ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


# ============================================================
# RINGKASAN
# ============================================================

def ci_txt(r, nm, n=4):
    return f'{f(r[nm], n)} [{f(r[nm + "_CI_Bawah"], n)}; {f(r[nm + "_CI_Atas"], n)}]'


def tulis_ringkasan(path, info, ci, uji, kep_h, rek_uji, mur, ci_titik, u_titik, amb, det, sub, kep, rek, theta):
    L = ['# Ringkasan Analisis Data Eksperimen PRE-02 (Pertemuan 6)\n',
         '> Digenerate otomatis oleh `analisis_data.py` dari `hasil_eksperimen/tabel_prediksi_oof.csv`. Jangan diedit manual.\n',
         f'- {info}',
         f'- Selang kepercayaan (CI) 95%: bootstrap persentil, {N_BOOT} replikasi, resampling per iterasi simulasi '
         '(ketiga titik monitoring satu iterasi ikut bersama). CI menggambarkan variasi antar-iterasi untuk 8 subproyek '
         'yang sama; generalisasi ke subproyek lain dinilai dengan kolom konsistensi antarsubproyek.',
         f'- Uji hipotesis: selisih berpasangan satu arah, koreksi Holm atas {len(uji)} uji, α = {f(ALFA, 2)}.\n',
         '## Keputusan hipotesis\n', '| Hipotesis | Sumber | Pernyataan | Keputusan | Rincian |', '| :--- | :--- | :--- | :--- | :--- |']
    for _, r in kep_h.iterrows():
        L.append(f'| {r.Hipotesis} | {r.Sumber_Deskripsi} | {r.Pernyataan} | **{r.Keputusan}** | {r.Rincian} |')
    L += ['', '| Hipotesis | Konsistensi antarsubproyek (8 selisih per subproyek) |', '| :--- | :--- |']
    L += [f'| {r.Hipotesis} | {r.Konsistensi_Antarsubproyek} |' for _, r in kep_h.iterrows()]
    L += ['', '## Rincian uji\n',
          '| Uji | A | B | Metrik | A | B | Selisih [CI 95%] | p Holm | Subproyek searah | p Wilcoxon |',
          '| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for _, r in uji.iterrows():
        tanda = ' ✓' if r.Signifikan else (' ✗ (berlawanan)' if r.Arah_Berlawanan_Signifikan else '')
        L.append(f'| {r.Kode_Uji} | {r.A} | {r.B} | {r.Metrik} | {f(r.Nilai_A)} | {f(r.Nilai_B)} | '
                 f'{f(r.Selisih_A_minus_B)} [{f(r.CI_Bawah)}; {f(r.CI_Atas)}] | {f(r.p_Holm)}{tanda} | '
                 f'{r.Subproyek_Searah}/8 | {f(r.p_Wilcoxon_Subproyek)} |')
    L += ['', f'Tambahan (dua arah): {rek_uji["A"]} vs {rek_uji["B"]}, selisih Brier {f(rek_uji["Selisih_A_minus_B"])} '
              f'[{f(rek_uji["CI_Bawah"])}; {f(rek_uji["CI_Atas"])}], p = {f(rek_uji["p_Dua_Arah"])}.',
          '', '## Metrik dengan CI 95%\n',
          '| Model | Kalibrasi | Brier | BSS | ROC-AUC | ECE | Intercept kalibrasi | Slope kalibrasi |',
          '| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for _, r in ci.iterrows():
        L.append(f'| {r.Model} | {r.Kalibrasi} | {ci_txt(r, "Brier")} | {ci_txt(r, "BSS", 3)} | '
                 f'{ci_txt(r, "ROC_AUC", 3) if pd.notna(r.ROC_AUC) else "–"} | {ci_txt(r, "ECE")} | '
                 f'{ci_txt(r, "Intercept_Kalibrasi", 3) if pd.notna(r.Intercept_Kalibrasi) else "–"} | '
                 f'{ci_txt(r, "Slope_Kalibrasi", 3) if pd.notna(r.Slope_Kalibrasi) else "–"} |')
    L += ['', '## Dekomposisi Brier (Murphy)\n', '| Model | Kalibrasi | Brier | Reliability | Resolution | Uncertainty | Sisa dalam bin |',
          '| :--- | :--- | ---: | ---: | ---: | ---: | ---: |']
    for _, r in mur.iterrows():
        L.append(f'| {r.Model} | {r.Kalibrasi} | {f(r.Brier)} | {f(r.Reliability)} | {f(r.Resolution)} | '
                 f'{f(r.Uncertainty)} | {f(r.Sisa_Dalam_Bin)} |')
    L += ['', '## Per titik monitoring (CI 95%)\n', '| Titik | Model | ROC-AUC | Brier |', '| ---: | :--- | ---: | ---: |']
    for _, r in ci_titik[ci_titik.Model != NAIF].iterrows():
        L.append(f'| {pct(float(r[TITIK]), 0)} | {r.Model} + {r.Kalibrasi} | {ci_txt(r, "ROC_AUC", 3)} | {ci_txt(r, "Brier")} |')
    L += ['', '| Model | Perubahan | Metrik | Nilai | CI 95% |', '| :--- | :--- | :--- | ---: | ---: |']
    for _, r in u_titik.iterrows():
        L.append(f'| {r.Model} | {pct(r.Dari, 0)} → {pct(r.Ke, 0)} | {r.Metrik} | {f(r.Perubahan)} | '
                 f'[{f(r.CI_Bawah)}; {f(r.CI_Atas)}] |')
    L += ['', f'## Analisis ambang — {rek[0]} + {rek[1]}\n',
          '| Ambang | Keterangan | Titik | % diberi peringatan | Recall | Specificity | Precision | F1 |',
          '| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for _, r in amb[amb.Keterangan != ''].iterrows():
        t = 'Semua' if r.Titik_Monitoring == 'Semua' else pct(float(r.Titik_Monitoring), 0)
        L.append(f'| {f(r.Ambang, 3)} | {r.Keterangan} | {t} | {pct(r.Persen_Peringatan)} | {pct(r.Recall)} | '
                 f'{pct(r.Specificity)} | {pct(r.Precision)} | {f(r.F1, 3)} |')
    L += ['', '## Deteksi dini (kumulatif per iterasi)\n',
          '| Ambang | Telat diperingatkan s.d. 25% / 50% / 75% | Tepat waktu diperingatkan (palsu) s.d. 25% / 50% / 75% | '
          'Telat tak pernah diperingatkan | Sisa hari saat peringatan pertama (rata-rata / median) |',
          '| :--- | ---: | ---: | ---: | ---: |']
    for _, r in det.iterrows():
        L.append(f'| {r.Keterangan} ({f(r.Ambang, 3)}) | ' +
                 ' / '.join(pct(r[f'Telat_Diperingatkan_sd_{t}']) for t in (25, 50, 75)) + ' | ' +
                 ' / '.join(pct(r[f'Tepat_Diperingatkan_sd_{t}']) for t in (25, 50, 75)) +
                 f' | {pct(r.Telat_Tidak_Pernah_Diperingatkan)} | {f(r.Rata2_Sisa_Hari_Saat_Peringatan_Pertama, 1)} / '
                 f'{f(r.Median_Sisa_Hari_Saat_Peringatan_Pertama, 1)} |')
    L += ['', f'## Per subproyek — {rek[0]} + {rek[1]}\n',
          '| Subproyek | Prevalensi | Rata-rata prediksi | Prediksi naif | Brier | BSS | ECE | Reliability | Resolution | ROC-AUC |',
          '| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for _, r in sub.iterrows():
        L.append(f'| {r[GRUP]} | {pct(r.Prevalensi)} | {pct(r.Rata2_Prediksi_Model)} | {pct(r.Prediksi_Naif)} | '
                 f'{f(r.Brier)} | {f(r.BSS, 3)} | {f(r.ECE)} | {f(r.Reliability)} | {f(r.Resolution)} | '
                 f'{f(r.ROC_AUC, 3)} |')
    L += ['', f'## Kepentingan fitur — {rek[0]} + {rek[1]} (permutation, kenaikan Brier di subproyek uji)\n',
          '| Peringkat | Fitur | Rata-rata | SD antarlipatan | Lipatan positif |', '| ---: | :--- | ---: | ---: | ---: |']
    for _, r in kep.iterrows():
        L.append(f'| {r.Peringkat} | {r.Fitur} | {f(r.Rata2_Kenaikan_Brier, 5)} | {f(r.SD_Antar_Lipatan, 5)} | '
                 f'{r.Lipatan_Positif}/8 |')
    Path(path).write_text('\n'.join(L) + '\n', encoding='utf-8')


# ============================================================
# MAIN
# ============================================================

def main(argv=None):
    ap = argparse.ArgumentParser(description='Analisis data eksperimen PRE-02 (Pertemuan 6)')
    ap.add_argument('--keluaran', default=str(ep.HERE / 'hasil_analisis'))
    ap.add_argument('--n-boot', type=int, default=N_BOOT)
    ap.add_argument('--n-jobs', type=int, default=-1)
    ap.add_argument('--tanpa-kepentingan', action='store_true', help='lewati permutation importance (untuk uji cepat)')
    a = ap.parse_args(argv)
    out = Path(a.keluaran)
    out.mkdir(parents=True, exist_ok=True)
    mulai = time.time()

    print('[1/6] Muat prediksi out-of-fold & tabel eksperimen')
    path_pred = HASIL_EKSP / 'tabel_prediksi_oof.csv'
    p, klaster = muat_prediksi(path_pred)
    tabel_eksp = pd.read_csv(HASIL_EKSP / 'tabel_metrik_evaluasi.csv')
    r_rek = tabel_eksp[tabel_eksp.Rekomendasi == 1].iloc[0]
    rek, theta = (r_rek.Model, r_rek.Kalibrasi), float(r_rek.Ambang)
    data = ep.muat_data(ep.DATASET)
    assert (data[[GRUP, 'Iterasi', TITIK, LABEL]].to_numpy() == p[[GRUP, 'Iterasi', TITIK, LABEL]].to_numpy()).all(), \
        'Urutan dataset dan prediksi tidak sama'
    # θ* dihitung ulang dari prediksi berpresisi penuh (nilai di CSV dibulatkan 6 desimal dan bisa menggeser batas)
    theta = ep.ambang_youden(p[LABEL].to_numpy(), p[kolom(*rek)].to_numpy())[0]
    assert abs(theta - float(r_rek.Ambang)) < 1e-6, 'θ* tidak sama dengan Pertemuan 5'

    print(f'[2/6] Bootstrap klaster ({a.n_boot} replikasi)')
    butir = butir_bootstrap(p, klaster, rek)
    titik, boot = bootstrap(p, klaster, butir, a.n_boot, a.n_jobs)
    ci = tabel_ci(butir, titik, boot, 'Semua')
    ci_titik = pd.concat([tabel_ci(butir, titik, boot, t) for t in TITIK_LIST], ignore_index=True)

    print('[3/6] Uji hipotesis H1–H5')
    uji = tabel_uji(p, butir, titik, boot)
    kep_h = keputusan(uji, ci)
    rek_uji = uji_rekomendasi(butir, titik, boot, tabel_eksp)
    u_titik = uji_titik(butir, titik, boot, rek)

    print('[4/6] Dekomposisi Brier, ambang, deteksi dini, per subproyek')
    mur = tabel_murphy(p)
    amb = tabel_ambang(p, rek, theta)
    det = tabel_deteksi_dini(p, data, rek, theta)
    sub, profil = tabel_subproyek(p, data, rek)

    if a.tanpa_kepentingan:
        print('[5/6] Kepentingan fitur dilewati')
        kep = pd.DataFrame(columns=['Peringkat', 'Fitur', 'Rata2_Kenaikan_Brier', 'SD_Antar_Lipatan', 'Lipatan_Positif'])
    else:
        print(f'[5/6] Permutation importance {rek[0]} + {rek[1]} (8 lipatan)')
        kep = tabel_kepentingan(data, rek, a.n_jobs)

    print(f'[6/6] Tulis luaran ke {out}')
    b6 = lambda t: t.round(6)
    b6(ci).to_csv(out / 'tabel_ci_metrik.csv', index=False)
    b6(ci_titik).to_csv(out / 'tabel_ci_per_titik.csv', index=False)
    b6(uji).to_csv(out / 'tabel_uji_hipotesis.csv', index=False)
    kep_h.to_csv(out / 'tabel_keputusan_hipotesis.csv', index=False)
    b6(pd.DataFrame([rek_uji])).to_csv(out / 'tabel_uji_rekomendasi.csv', index=False)
    b6(u_titik).to_csv(out / 'tabel_perubahan_antartitik.csv', index=False)
    b6(mur).to_csv(out / 'tabel_dekomposisi_brier.csv', index=False)
    b6(amb).to_csv(out / 'tabel_analisis_ambang.csv', index=False)
    b6(det).to_csv(out / 'tabel_deteksi_dini.csv', index=False)
    b6(sub).to_csv(out / 'tabel_analisis_subproyek.csv', index=False)
    b6(profil).to_csv(out / 'tabel_profil_subproyek.csv', index=False)
    if not a.tanpa_kepentingan:
        b6(kep).to_csv(out / 'tabel_kepentingan_fitur_rekomendasi.csv', index=False)

    grafik_uji(uji, out / 'grafik_uji_hipotesis.png')
    grafik_murphy(mur, out / 'grafik_dekomposisi_brier.png')
    grafik_ambang(p, rek, theta, out / 'grafik_analisis_ambang.png')
    grafik_deteksi(det, out / 'grafik_deteksi_dini.png')
    grafik_titik_ci(ci_titik, out / 'grafik_metrik_per_titik_ci.png')
    info = (f'Sumber: `hasil_eksperimen/tabel_prediksi_oof.csv` (MD5 `{ep.md5(path_pred)}`), {len(p)} baris, '
            f'{klaster.max() + 1} iterasi; model rekomendasi Pertemuan 5: {rek[0]} + {rek[1]}, θ* = {f(theta, 3)}. '
            f'Dijalankan {datetime.now():%Y-%m-%d %H:%M}, {time.time() - mulai:.0f} detik.')
    tulis_ringkasan(out / '00_RINGKASAN_ANALISIS.md', info, ci, uji, kep_h, rek_uji, mur, ci_titik, u_titik, amb, det,
                    sub, kep, rek, theta)
    print('Selesai.')
    return {'ci': ci, 'uji': uji, 'keputusan': kep_h}


if __name__ == '__main__':
    main()
