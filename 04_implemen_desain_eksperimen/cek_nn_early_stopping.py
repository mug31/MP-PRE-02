"""Pemeriksaan tambahan: NN dengan early stopping (menjawab review naskah, Review_Opus.md bagian Diskusi).

NN utama di experiment_pipeline.py sengaja TIDAK diganti (hiperparameter ditetapkan sebelum eksperimen).
Skrip ini melatih ulang NN yang sama persis, hanya ditambah early_stopping=True, dengan validasi
leave-one-subproject-out yang sama, lalu membandingkannya dengan NN utama dan pembanding naif (tanpa kalibrasi).

Dua varian early stopping:
- 'acak'  : bawaan scikit-learn, 10% data latih diambil acak sebagai validasi (n_iter_no_change=10)
- 'grup'  : validasi = satu subproyek latih yang ditahan (paling dekat dengan kondisi uji per subproyek);
            epoch terbaik dipilih dari Brier pada subproyek tertahan, lalu model akhir dilatih ulang pada
            seluruh tujuh subproyek dengan jumlah epoch tersebut. Diulang dengan tiga pilihan subproyek
            validasi (pertama/tengah/terakhir) untuk melihat kepekaan hasil terhadap pilihan tersebut.

Luaran: hasil_analisis/tabel_cek_nn_early_stopping.csv
Jalankan: uv run -q --with scikit-learn --with pandas --with numpy --with joblib python cek_nn_early_stopping.py
"""
import warnings

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import brier_score_loss
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from experiment_pipeline import DATASET, FITUR, GRUP, LABEL, NAIF, SEED, buat_model, metrik, muat_data, pembagian_luar

warnings.filterwarnings('ignore', category=ConvergenceWarning)
KELUARAN = __import__('pathlib').Path(__file__).parent / 'hasil_analisis' / 'tabel_cek_nn_early_stopping.csv'
MAKS_EPOCH = 1000


def mlp(**kw):
    kw.setdefault('max_iter', MAKS_EPOCH)
    return MLPClassifier(hidden_layer_sizes=(16, 8), activation='relu', solver='adam', alpha=0.01,
                         learning_rate_init=0.01, random_state=SEED, **kw)


def oof_dengan(fungsi_latih, X, y, g, lipatan):
    oof = np.full(len(y), np.nan)
    info = []
    for latih, uji in lipatan:
        model, catatan = fungsi_latih(X[latih], y[latih], g[latih])
        oof[uji] = model.predict_proba(X[uji])[:, 1]
        info.append(catatan)
    assert not np.isnan(oof).any()
    return oof, info


def latih_utama(X, y, g):
    m = buat_model('MLP Neural Network').fit(X, y)
    return m, m.named_steps['model'].n_iter_


def latih_es_acak(X, y, g):
    m = Pipeline([('skala', StandardScaler()),
                  ('model', mlp(early_stopping=True, validation_fraction=0.1, n_iter_no_change=10))]).fit(X, y)
    return m, m.named_steps['model'].n_iter_


def latih_es_grup(X, y, g, pilih='pertama'):
    """Early stopping dengan validasi satu subproyek latih yang ditahan (pilih: pertama/tengah/terakhir menurut
    urutan nama, di antara subproyek latih yang memiliki dua kelas)."""
    kandidat = [s for s in sorted(np.unique(g)) if len(np.unique(y[g == s])) == 2]
    val = {'pertama': kandidat[0], 'tengah': kandidat[len(kandidat) // 2], 'terakhir': kandidat[-1]}[pilih]
    tr, va = g != val, g == val
    skala = StandardScaler().fit(X[tr])
    m = mlp(warm_start=True, max_iter=1)
    terbaik, epoch_terbaik, tanpa_perbaikan = np.inf, 1, 0
    for e in range(1, MAKS_EPOCH + 1):
        m.fit(skala.transform(X[tr]), y[tr])
        bs = brier_score_loss(y[va], m.predict_proba(skala.transform(X[va]))[:, 1])
        if bs < terbaik - 1e-6:
            terbaik, epoch_terbaik, tanpa_perbaikan = bs, e, 0
        else:
            tanpa_perbaikan += 1
            if tanpa_perbaikan >= 10:
                break
    akhir = Pipeline([('skala', StandardScaler()), ('model', mlp(max_iter=epoch_terbaik))]).fit(X, y)
    return akhir, epoch_terbaik


def main():
    d = muat_data(DATASET)
    X, y, g = d[FITUR].to_numpy(float), d[LABEL].to_numpy(int), d[GRUP].to_numpy()
    lip = pembagian_luar(g)
    naif, _ = oof_dengan(lambda X_, y_, g_: (buat_model(NAIF).fit(X_, y_), None), X, y, g, lip)
    bs_naif = brier_score_loss(y, naif)
    baris = []
    for nama, fn in [('NN utama (tanpa early stopping)', latih_utama),
                     ('NN early stopping (validasi acak 10%)', latih_es_acak),
                     ('NN early stopping (validasi subproyek pertama)', lambda *a: latih_es_grup(*a, 'pertama')),
                     ('NN early stopping (validasi subproyek tengah)', lambda *a: latih_es_grup(*a, 'tengah')),
                     ('NN early stopping (validasi subproyek terakhir)', lambda *a: latih_es_grup(*a, 'terakhir'))]:
        p, ep = oof_dengan(fn, X, y, g, lip)
        m = metrik(y, p, bs_naif)
        ekstrem = (p <= 0.01) | (p >= 0.99)
        salah = ekstrem & ((p >= 0.5).astype(int) != y)
        per_sub = pd.DataFrame({'g': g, 'y': y, 'p': p}).groupby('g').apply(
            lambda t: metrik(t.y.to_numpy(), t.p.to_numpy(), 1.0)['ECE'], include_groups=False)
        baris.append({'Varian': nama, **{k: m[k] for k in ('Brier', 'BSS', 'Log_Loss', 'ECE', 'ROC_AUC')},
                      'ECE_Rata_Subproyek': per_sub.mean(), 'Persen_Ekstrem': ekstrem.mean(),
                      'Persen_Ekstrem_Salah_Arah': salah.sum() / max(ekstrem.sum(), 1),
                      'Epoch_Median': float(np.median(ep)), 'Epoch_Min': int(min(ep)), 'Epoch_Maks': int(max(ep))})
        print(baris[-1])
    pd.DataFrame(baris).to_csv(KELUARAN, index=False)
    print('tersimpan', KELUARAN)


if __name__ == '__main__':
    main()
