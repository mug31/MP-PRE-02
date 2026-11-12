"""
PRE-02: Uji pipeline eksperimen (01_Flow_dan_Skenario_Eksperimen.md Bagian 9.3).

  python uji_pipeline.py               # uji 1–5 (memakai luaran di hasil_eksperimen/)
  python uji_pipeline.py --reproduksi  # + uji 6: jalankan ulang pipeline dan bandingkan seluruh tabel (beberapa menit)

1. Pemisahan data : tidak ada subproyek di sisi latih & uji sekaligus (lipatan luar dan dalam); tiap baris diuji
                    tepat sekali; lipatan dalam hanya memakai indeks data latih.
2. Pembanding naif: prediksi = proporsi telat di data latih tiap lipatan; BSS pembanding naif = 0.
3. Label acak     : jika label diacak, ROC-AUC Logistic Regression ≈ 0,5 (0,45–0,55).
4. Arah koefisien : koefisien LR SPI_Jadwal negatif dan Pergeseran_Dependency_Hari positif.
5. Konsistensi    : prediksi out-of-fold yang disimpan menghasilkan ulang metrik di tabel_metrik_evaluasi.csv.
6. Reproduksi     : (opsional) dua kali jalan → seluruh tabel CSV identik.
"""

import argparse
import filecmp
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, roc_auc_score

import experiment_pipeline as ep

HASIL = ep.HERE / 'hasil_eksperimen'


def uji_pemisahan(d):
    g = d[ep.GRUP].to_numpy()
    luar = ep.pembagian_luar(g)
    assert len(luar) == ep.N_SUBPROYEK
    hitung = np.zeros(len(g), int)
    for tr, te in luar:
        assert not set(g[tr]) & set(g[te]) and len(set(g[te])) == 1
        hitung[te] += 1
        dalam = ep.pembagian_dalam(g[tr])
        assert len(dalam) == ep.N_LIPATAN_DALAM
        hitung_dalam = np.zeros(len(tr), int)
        for a, b in dalam:
            assert max(a.max(), b.max()) < len(tr), 'indeks lipatan dalam keluar dari data latih'
            assert not set(g[tr][a]) & set(g[tr][b])
            assert {g[te[0]]}.isdisjoint(set(g[tr][a]) | set(g[tr][b])), 'subproyek uji ikut melatih kalibrator'
            hitung_dalam[b] += 1
        assert (hitung_dalam == 1).all()
    assert (hitung == 1).all()
    return f'{len(luar)} lipatan luar × {ep.N_LIPATAN_DALAM} lipatan dalam: tidak ada subproyek bocor; tiap baris diuji sekali'


def uji_naif(d):
    X, y, g = d[ep.FITUR].to_numpy(float), d[ep.LABEL].to_numpy(int), d[ep.GRUP].to_numpy()
    luar = ep.pembagian_luar(g)
    oof = ep.prediksi_oof(ep.NAIF, 'Raw', X, y, g, luar, n_jobs=1)
    for tr, te in luar:
        assert np.allclose(oof[te], y[tr].mean())
    t = pd.read_csv(HASIL / 'tabel_metrik_evaluasi.csv')
    bss = t[t.Model == ep.NAIF].BSS.iloc[0]
    assert abs(bss) < 1e-9, bss
    return 'prediksi = proporsi telat data latih di 8 lipatan; BSS pembanding naif = 0'


def uji_label_acak(d):
    X, g = d[ep.FITUR].to_numpy(float), d[ep.GRUP].to_numpy()
    y = np.random.default_rng(ep.SEED).permutation(d[ep.LABEL].to_numpy(int))
    oof = ep.prediksi_oof('Logistic Regression', 'Raw', X, y, g, ep.pembagian_luar(g), n_jobs=-1)
    auc = roc_auc_score(y, oof)
    assert 0.45 <= auc <= 0.55, auc
    return f'ROC-AUC Logistic Regression dengan label diacak = {auc:.3f}'


def uji_arah_koefisien():
    k = pd.read_csv(HASIL / 'tabel_feature_importance.csv').set_index('Fitur').Koefisien_LR
    assert k['SPI_Jadwal'] < 0 and k['Pergeseran_Dependency_Hari'] > 0, k.to_dict()
    return (f'SPI_Jadwal {k["SPI_Jadwal"]:+.3f} (negatif), Pergeseran_Dependency_Hari '
            f'{k["Pergeseran_Dependency_Hari"]:+.3f} (positif)')


def uji_konsistensi():
    t = pd.read_csv(HASIL / 'tabel_metrik_evaluasi.csv')
    p = pd.read_csv(HASIL / 'tabel_prediksi_oof.csv')
    y = p[ep.LABEL].to_numpy()
    for _, r in t.iterrows():
        kol = f'P_{r.Model.replace(" ", "_")}_{r.Kalibrasi}'
        bs = brier_score_loss(y, p[kol])
        assert abs(bs - r.Brier) < 1e-5, (kol, bs, r.Brier)
        if r.Model != ep.NAIF:
            assert abs(roc_auc_score(y, p[kol]) - r.ROC_AUC) < 1e-4, kol
    assert t.Rekomendasi.sum() == 1
    rek = t[t.Rekomendasi == 1].iloc[0]
    kandidat = t[t.Model != ep.NAIF].sort_values(['Brier', 'ECE', 'Log_Loss']).iloc[0]
    assert (rek.Model, rek.Kalibrasi) == (kandidat.Model, kandidat.Kalibrasi)
    return f'{len(t)} kombinasi: Brier & AUC dari prediksi tersimpan cocok; rekomendasi = Brier terendah ({rek.Model} + {rek.Kalibrasi})'


def uji_reproduksi():
    with tempfile.TemporaryDirectory() as tmp:
        ep.main(['--keluaran', tmp] + (['--sensitivitas'] if (HASIL / 'tabel_sensitivitas.csv').exists() else []))
        berkas = sorted(p.name for p in HASIL.glob('*.csv'))
        beda = [b for b in berkas if not filecmp.cmp(HASIL / b, Path(tmp) / b, shallow=False)]
        assert not beda, f'berbeda: {beda}'
    return f'{len(berkas)} tabel CSV identik pada jalan ulang'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--reproduksi', action='store_true')
    a = ap.parse_args()
    d = ep.muat_data(ep.DATASET)
    uji = [('Pemisahan data', lambda: uji_pemisahan(d)), ('Pembanding naif', lambda: uji_naif(d)),
           ('Label acak', lambda: uji_label_acak(d)), ('Arah koefisien LR', uji_arah_koefisien),
           ('Konsistensi luaran', uji_konsistensi)]
    if a.reproduksi:
        uji.append(('Reproduksi', uji_reproduksi))
    for nama, fungsi in uji:
        print(f'[LULUS] {nama}: {fungsi()}')
