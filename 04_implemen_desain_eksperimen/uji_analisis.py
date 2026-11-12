"""
PRE-02: Uji analisis data (Pertemuan 6)

  python uji_analisis.py               # uji 1–7 (memakai luaran di hasil_analisis/)
  python uji_analisis.py --reproduksi  # + uji 8: jalankan ulang analisis dan bandingkan seluruh tabel (± 3 menit)

1. Konsistensi   : nilai titik di hasil_analisis/ sama dengan tabel Pertemuan 5 (13 kombinasi; per titik monitoring).
2. Metrik berbobot: Brier, Log Loss, ECE, ROC-AUC berbobot = metrik pada data yang barisnya diulang sesuai bobot,
                    dan ROC-AUC/Brier = scikit-learn dengan sample_weight.
3. Kalibrasi logistik: intercept & slope = LogisticRegression tanpa penalti (scikit-learn).
4. Selang kepercayaan: setiap CI memuat nilai titiknya.
5. Dekomposisi Brier: Reliability − Resolution + Uncertainty + sisa dalam bin = Brier.
6. Prosedur uji : Holm & Wilcoxon eksak benar pada contoh yang diketahui; bootstrap tidak menolak model vs dirinya
                  sendiri dan menolak prediksi 0,5 vs probabilitas benar pada data sintetis.
7. Ambang & deteksi dini: recall/specificity pada θ* = tabel Pertemuan 5; deteksi s.d. 25% = recall di titik 25%;
                  deteksi kumulatif tidak turun.
8. Reproduksi   : (opsional) dua kali jalan → seluruh tabel CSV identik.
"""

import argparse
import filecmp
import tempfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

import analisis_data as an
import experiment_pipeline as ep

HASIL = ep.HERE / 'hasil_analisis'
EKSP = ep.HERE / 'hasil_eksperimen'


def uji_konsistensi():
    ci = pd.read_csv(HASIL / 'tabel_ci_metrik.csv')
    t5 = pd.read_csv(EKSP / 'tabel_metrik_evaluasi.csv')
    m = ci.merge(t5, on=['Model', 'Kalibrasi'], suffixes=('', '_P5'))
    assert len(m) == 13
    for k in ['Brier', 'Log_Loss', 'ECE', 'BSS']:
        assert np.allclose(m[k], m[k + '_P5'], atol=2e-6), k
    nn = m.Model != ep.NAIF
    assert np.allclose(m.ROC_AUC[nn], m.ROC_AUC_P5[nn], atol=2e-6)
    ct = pd.read_csv(HASIL / 'tabel_ci_per_titik.csv')
    pt = pd.read_csv(EKSP / 'tabel_metrik_per_titik.csv')
    m2 = ct.merge(pt, on=[ep.TITIK, 'Model', 'Kalibrasi'], suffixes=('', '_P5'))
    assert len(m2) == len(ct) == 15
    for k in ['Brier', 'ECE']:
        assert np.allclose(m2[k], m2[k + '_P5'], atol=2e-6), k
    nn = m2.Model != ep.NAIF
    assert np.allclose(m2.ROC_AUC[nn], m2.ROC_AUC_P5[nn], atol=2e-6)
    return f'{len(m)} kombinasi & {len(m2)} baris per titik cocok dengan Pertemuan 5'


def uji_berbobot(p):
    rng = np.random.default_rng(1)
    y = p[ep.LABEL].to_numpy()
    for m, k in [('Gradient Boosting', 'Raw'), ('Random Forest', 'Isotonic'), ('MLP Neural Network', 'Raw')]:
        q = p[an.kolom(m, k)].to_numpy()
        w = rng.integers(0, 4, len(y))
        v = an.nilai(an.siapkan(y, q), w.astype(float), lengkap=False)
        yr, qr = np.repeat(y, w), np.repeat(q, w)
        ref = [brier_score_loss(yr, qr), log_loss(yr, np.clip(qr, 1e-15, 1 - 1e-15)), ep.ece(yr, qr), roc_auc_score(yr, qr)]
        assert np.allclose(v, ref, atol=1e-9), (m, k, v, ref)
        assert np.isclose(v[3], roc_auc_score(y, q, sample_weight=w)) and np.isclose(v[0], brier_score_loss(y, q, sample_weight=w))
    return 'Brier, Log Loss, ECE, ROC-AUC berbobot = data diulang = scikit-learn (3 kombinasi, termasuk nilai seri)'


def uji_kalibrasi_logistik(p):
    y = p[ep.LABEL].to_numpy().astype(float)
    hasil = []
    for m, k in [('Logistic Regression', 'Raw'), ('Random Forest', 'Raw'), ('MLP Neural Network', 'Raw')]:
        L = an.siapkan(y, p[an.kolom(m, k)].to_numpy())['L']
        _, b = an.intercept_slope(L, y, np.ones(len(y)))
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            ref = LogisticRegression(C=np.inf, tol=1e-12, max_iter=10000).fit(L[:, None], y).coef_[0][0]
        assert abs(b - ref) < 1e-4, (m, b, ref)
        hasil.append(f'{an.SINGKAT[m]} {b:.3f}')
    # data sintetis terkalibrasi sempurna → intercept ≈ 0, slope ≈ 1
    rng = np.random.default_rng(2)
    q = rng.uniform(0.02, 0.98, 200000)
    ys = (rng.uniform(size=q.size) < q).astype(float)
    a, b = an.intercept_slope(np.log(q / (1 - q)), ys, np.ones(q.size))
    assert abs(a) < 0.03 and abs(b - 1) < 0.03, (a, b)
    return f'slope = scikit-learn ({", ".join(hasil)}); data terkalibrasi sempurna → intercept {a:.3f}, slope {b:.3f}'


def uji_ci():
    n = 0
    for nama in ['tabel_ci_metrik.csv', 'tabel_ci_per_titik.csv']:
        t = pd.read_csv(HASIL / nama)
        for c in [c for c in t.columns if c.endswith('_CI_Bawah')]:
            k = c[:-len('_CI_Bawah')]
            ok = t[[k, c, k + '_CI_Atas']].dropna()
            assert ((ok[c] <= ok[k] + 1e-9) & (ok[k] <= ok[k + '_CI_Atas'] + 1e-9)).all(), (nama, k)
            n += len(ok)
    u = pd.read_csv(HASIL / 'tabel_uji_hipotesis.csv')
    assert ((u.CI_Bawah <= u.Selisih_A_minus_B) & (u.Selisih_A_minus_B <= u.CI_Atas)).all()
    return f'{n + len(u)} selang memuat nilai titiknya'


def uji_murphy():
    t = pd.read_csv(HASIL / 'tabel_dekomposisi_brier.csv')
    assert np.allclose(t.Reliability - t.Resolution + t.Uncertainty + t.Sisa_Dalam_Bin, t.Brier, atol=5e-6)
    assert (t.Reliability >= 0).all() and (t.Resolution >= 0).all()
    assert t.Uncertainty.nunique() == 1
    return f'identitas Murphy berlaku pada {len(t)} kombinasi; sisa dalam bin maks {t.Sisa_Dalam_Bin.abs().max():.4f}'


def uji_prosedur():
    # Holm: contoh buku teks
    assert np.allclose(an.holm([0.01, 0.04, 0.03, 0.005]), [0.03, 0.06, 0.06, 0.02])
    # Wilcoxon eksak satu arah: semua 8 selisih negatif → p = 1/256; semua positif → p = 1
    assert np.isclose(an.wilcoxon_eksak(-np.arange(1, 9)), 1 / 256)
    assert np.isclose(an.wilcoxon_eksak(np.arange(1, 9)), 1.0)
    # bootstrap pada data sintetis 8000 klaster × 3
    rng = np.random.default_rng(3)
    n_k = 4000
    q = rng.uniform(0.05, 0.95, n_k * 3)
    y = (rng.uniform(size=q.size) < q).astype(int)
    kl = np.repeat(np.arange(n_k), 3)
    p = pd.DataFrame({ep.LABEL: y})
    sb, sq, s5 = an.siapkan(y, q), an.siapkan(y, q.copy()), an.siapkan(y, np.full(q.size, 0.5))
    counts = rng.multinomial(n_k, np.full(n_k, 1 / n_k), size=300)
    b = an._hitung_chunk([(sb, None, False), (sq, None, False), (s5, None, False)], kl, counts)
    sama = b[:, 0, 0] - b[:, 1, 0]
    beda = b[:, 0, 0] - b[:, 2, 0]
    p_sama = (1 + (sama >= 0).sum()) / 301
    p_beda = (1 + (beda >= 0).sum()) / 301
    assert p_sama == 1.0 and p_beda < 0.01, (p_sama, p_beda)
    return f'Holm & Wilcoxon benar; bootstrap: model vs dirinya p = {p_sama:.2f}, benar vs 0,5 p = {p_beda:.4f}'


def uji_ambang():
    t5 = pd.read_csv(EKSP / 'tabel_metrik_evaluasi.csv')
    r = t5[t5.Rekomendasi == 1].iloc[0]
    a = pd.read_csv(HASIL / 'tabel_analisis_ambang.csv')
    s = a[(a.Keterangan == 'θ* Youden') & (a.Titik_Monitoring == 'Semua')].iloc[0]
    assert abs(s.Recall - r.Recall) < 1e-6 and abs(s.Specificity - r.Specificity) < 1e-6
    d = pd.read_csv(HASIL / 'tabel_deteksi_dini.csv')
    for _, x in d.iterrows():
        rec25 = a[(a.Keterangan == x.Keterangan) & (a.Titik_Monitoring == '0.25')].iloc[0].Recall
        assert abs(x.Telat_Diperingatkan_sd_25 - rec25) < 1e-6
        for nm in ('Telat', 'Tepat'):
            v = [x[f'{nm}_Diperingatkan_sd_{t}'] for t in (25, 50, 75)]
            assert v[0] <= v[1] <= v[2]
        assert abs(1 - x.Telat_Diperingatkan_sd_75 - x.Telat_Tidak_Pernah_Diperingatkan) < 1e-6
    z = pd.read_csv(EKSP / 'tabel_zona_peringatan.csv')
    zm = z[(z.Subproyek == 'Semua') & (z.Titik_Monitoring == '0.25')].iloc[0]
    merah = d[d.Keterangan == 'Batas Merah'].iloc[0]
    assert abs(merah.Telat_Diperingatkan_sd_25 - zm.Telat_di_Merah) < 1e-6
    return f'θ* recall {s.Recall:.4f} & specificity {s.Specificity:.4f} = Pertemuan 5; deteksi dini konsisten'


def uji_reproduksi():
    with tempfile.TemporaryDirectory() as tmp:
        an.main(['--keluaran', tmp])
        beda = [f.name for f in sorted(HASIL.glob('*.csv')) if not filecmp.cmp(f, Path(tmp) / f.name, shallow=False)]
        n = len(list(HASIL.glob('*.csv')))
    assert not beda, f'Tabel berbeda: {beda}'
    return f'{n} tabel CSV identik pada jalan ulang'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reproduksi', action='store_true')
    a = ap.parse_args()
    p, _ = an.muat_prediksi(EKSP / 'tabel_prediksi_oof.csv')
    uji = [('Konsistensi dengan Pertemuan 5', uji_konsistensi), ('Metrik berbobot', lambda: uji_berbobot(p)),
           ('Kalibrasi logistik', lambda: uji_kalibrasi_logistik(p)), ('Selang kepercayaan', uji_ci),
           ('Dekomposisi Brier', uji_murphy), ('Prosedur uji', uji_prosedur), ('Ambang & deteksi dini', uji_ambang)]
    if a.reproduksi:
        uji.append(('Reproduksi', uji_reproduksi))
    gagal = 0
    for nama, fn in uji:
        try:
            print(f'[LULUS] {nama}: {fn()}')
        except AssertionError as e:
            gagal += 1
            print(f'[GAGAL] {nama}: {e}')
    raise SystemExit(1 if gagal else 0)


if __name__ == '__main__':
    main()
