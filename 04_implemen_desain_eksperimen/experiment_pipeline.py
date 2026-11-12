"""
PRE-02: Pipeline Eksperimen Prediksi Probabilitas Keterlambatan Proyek — versi 2
Studi kasus: 8 subproyek Super ERP Farm Nation Enterprise (FNE) 2026

Mengimplementasikan 01_Flow_dan_Skenario_Eksperimen.md versi 2:
  Skenario 0  Pembanding naif (proporsi telat di data latih)
  Skenario 1  Logistic Regression            Skenario 2  Random Forest (predict_proba)
  Skenario 3  Gradient Boosting              Skenario 4  MLP Neural Network (output sigmoid)
  Skenario 5  Kalibrasi Raw / Platt / Isotonic + rekomendasi model (Brier terendah; seri: ECE, Log Loss)
  Skenario 6  Analisis per titik monitoring (25%, 50%, 75%)
  Skenario 7  Analisis sensitivitas faktor dampak risiko (opsi --sensitivitas)

Data   : 06_simulasi_iterasi/dataset_ml/dataset_ml.csv (24.000 baris; 7 fitur Deskripsi Penelitian §2)
Label  : Telat_Lebih_5_Persen (PMP-01 §4.7.3)
Validasi: leave-one-subproject-out (8 lipatan). Kalibrator dilatih dengan inner GroupKFold(3) per subproyek
          di dalam data latih. Semua metrik dihitung dari prediksi out-of-fold.

Jalankan (dari folder ini):
  python experiment_pipeline.py                  # Skenario 0–6
  python experiment_pipeline.py --sensitivitas   # + Skenario 7 (butuh dataset sensitivitas, lihat pesan galat)
Kebutuhan: pandas, numpy, scikit-learn, matplotlib, joblib
"""

import argparse
import hashlib
import platform
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn
from joblib import Parallel, delayed
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score, roc_curve
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ============================================================
# 1. KONFIGURASI (dokumen desain Bagian 3, 5, 6)
# ============================================================

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATASET = ROOT / '06_simulasi_iterasi' / 'dataset_ml' / 'dataset_ml.csv'
DATASET_SENSITIVITAS = {f: ROOT / '06_simulasi_iterasi' / 'dataset_ml' / 'sensitivitas' / f'dataset_ml_faktor_{f}.csv'
                        for f in (0.2, 1.0)}
FAKTOR_DAMPAK_UTAMA = 0.4  # sama dengan FAKTOR_DAMPAK di 06_simulasi_iterasi/buat_dataset_ml.py

FITUR = ['SPI_Jadwal', 'Sisa_Waktu_Hari', 'Backlog_Sisa_Persen', 'Utilisasi_Resource',
         'Risiko_Belum_Dimitigasi', 'Frekuensi_CR', 'Pergeseran_Dependency_Hari']
LABEL = 'Telat_Lebih_5_Persen'
GRUP = 'Subproyek'
TITIK = 'Titik_Monitoring'
N_SUBPROYEK, BARIS_PER_SUBPROYEK = 8, 3000

SEED = 42
N_LIPATAN_DALAM = 3
N_BIN_ECE = 10
ZONA = (0.35, 0.65)  # Hijau < 0,35 <= Kuning < 0,65 <= Merah (desain Bagian 8)

NAIF = 'Pembanding Naif'
MODEL = ['Logistic Regression', 'Random Forest', 'Gradient Boosting', 'MLP Neural Network']
KALIBRASI = ['Raw', 'Platt', 'Isotonic']
METODE_SKLEARN = {'Platt': 'sigmoid', 'Isotonic': 'isotonic'}

# Warna kategori tetap (palet tervalidasi buta warna) + gaya garis sebagai pengenal kedua
WARNA = {'Logistic Regression': '#2a78d6', 'Random Forest': '#eb6834',
         'Gradient Boosting': '#1baf7a', 'MLP Neural Network': '#eda100', NAIF: '#52514e'}
GARIS = {'Logistic Regression': '-', 'Random Forest': '--', 'Gradient Boosting': '-.',
         'MLP Neural Network': ':', NAIF: (0, (1, 3))}
TINTA, TINTA_2, PERMUKAAN = '#0b0b0b', '#52514e', '#fcfcfb'


def buat_model(nama):
    """Pipeline(StandardScaler, model) dengan hyperparameter desain Bagian 6."""
    if nama == NAIF:
        est = DummyClassifier(strategy='prior')
    elif nama == 'Logistic Regression':
        est = LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000)  # penalti L2 (bawaan)
    elif nama == 'Random Forest':
        est = RandomForestClassifier(n_estimators=100, max_depth=3, max_features='sqrt', criterion='gini',
                                     random_state=SEED)
    elif nama == 'Gradient Boosting':
        est = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=2, subsample=0.8,
                                         random_state=SEED)
    elif nama == 'MLP Neural Network':
        est = MLPClassifier(hidden_layer_sizes=(16, 8), activation='relu', solver='adam', alpha=0.01,
                            learning_rate_init=0.01, max_iter=1000, random_state=SEED)
    else:
        raise ValueError(nama)
    return Pipeline([('skala', StandardScaler()), ('model', est)])


# ============================================================
# 2. DATA
# ============================================================

def md5(path):
    return hashlib.md5(Path(path).read_bytes()).hexdigest()


def muat_data(path):
    """Baca dataset dan pastikan sesuai kontrak data (README dataset)."""
    d = pd.read_csv(path)
    kurang = [c for c in FITUR + [LABEL, GRUP, TITIK, 'Iterasi'] if c not in d.columns]
    assert not kurang, f'Kolom tidak ada: {kurang}'
    assert not d[FITUR + [LABEL, GRUP, TITIK]].isna().any().any(), 'Ada nilai kosong'
    assert set(d[LABEL].unique()) <= {0, 1}, 'Label bukan biner'
    ukuran = d.groupby(GRUP).size()
    assert len(ukuran) == N_SUBPROYEK and (ukuran == BARIS_PER_SUBPROYEK).all(), f'Ukuran per subproyek: {ukuran}'
    return d.reset_index(drop=True)


# ============================================================
# 3. PEMBAGIAN DATA & PREDIKSI OUT-OF-FOLD (desain Bagian 5)
# ============================================================

def pembagian_luar(g):
    """Leave-one-subproject-out: 8 lipatan, satu subproyek uji per lipatan."""
    return list(LeaveOneGroupOut().split(np.zeros(len(g)), groups=g))


def pembagian_dalam(g_latih):
    """Inner GroupKFold(3) per subproyek, indeks relatif terhadap data latih (untuk kalibrator)."""
    return list(GroupKFold(n_splits=N_LIPATAN_DALAM).split(np.zeros(len(g_latih)), groups=g_latih))


def buat_estimator(nama, kalibrasi, g_latih):
    dasar = buat_model(nama)
    if kalibrasi == 'Raw':
        return dasar
    return CalibratedClassifierCV(dasar, method=METODE_SKLEARN[kalibrasi], cv=pembagian_dalam(g_latih),
                                  ensemble=False)


def _satu_lipatan(nama, kalibrasi, X, y, g, latih, uji):
    est = buat_estimator(nama, kalibrasi, g[latih])
    est.fit(X[latih], y[latih])
    return uji, est.predict_proba(X[uji])[:, 1]


def prediksi_oof(nama, kalibrasi, X, y, g, lipatan, n_jobs):
    hasil = Parallel(n_jobs=n_jobs)(delayed(_satu_lipatan)(nama, kalibrasi, X, y, g, tr, te) for tr, te in lipatan)
    oof = np.full(len(y), np.nan)
    hitung = np.zeros(len(y), dtype=int)
    for uji, p in hasil:
        oof[uji] = p
        hitung[uji] += 1
    assert (hitung == 1).all(), 'Setiap baris harus diprediksi tepat satu kali'
    return oof


# ============================================================
# 4. METRIK (desain Bagian 7)
# ============================================================

def ece(y, p, n_bin=N_BIN_ECE):
    """Expected Calibration Error dengan bin lebar sama (Guo et al., 2017)."""
    idx = np.minimum((p * n_bin).astype(int), n_bin - 1)
    total = 0.0
    for b in range(n_bin):
        m = idx == b
        if m.any():
            total += m.mean() * abs(y[m].mean() - p[m].mean())
    return total


def ambang_youden(y, p):
    """Ambang dengan statistik Youden J = Recall + Specificity − 1 maksimum."""
    fpr, tpr, thr = roc_curve(y, p)
    i = int(np.argmax(tpr - fpr))
    return float(min(thr[i], 1.0)), float(tpr[i] - fpr[i])


def metrik(y, p, brier_naif, ambang=None):
    dua_kelas = len(np.unique(y)) == 2
    bs = brier_score_loss(y, p)
    hasil = {'N': len(y), 'Prevalensi': y.mean(), 'Brier': bs,
             'BSS': 1 - bs / brier_naif if brier_naif > 0 else np.nan,
             'Log_Loss': log_loss(y, np.clip(p, 1e-15, 1 - 1e-15), labels=[0, 1]),
             'ECE': ece(y, p), 'ROC_AUC': roc_auc_score(y, p) if dua_kelas else np.nan}
    if ambang is not None:
        pred = (p >= ambang).astype(int)
        tp, fp = int(((pred == 1) & (y == 1)).sum()), int(((pred == 1) & (y == 0)).sum())
        tn, fn = int(((pred == 0) & (y == 0)).sum()), int(((pred == 0) & (y == 1)).sum())
        rec = tp / (tp + fn) if tp + fn else np.nan
        pre = tp / (tp + fp) if tp + fp else np.nan
        hasil.update({'Ambang': ambang, 'Recall': rec, 'Specificity': tn / (tn + fp) if tn + fp else np.nan,
                      'Precision': pre, 'F1': 2 * pre * rec / (pre + rec) if pre and rec else 0.0,
                      'Akurasi': (tp + tn) / len(y), 'TP': tp, 'FP': fp, 'TN': tn, 'FN': fn})
    return hasil


def zona(p):
    return np.where(p < ZONA[0], 'Hijau', np.where(p < ZONA[1], 'Kuning', 'Merah'))


# ============================================================
# 5. EKSPERIMEN UTAMA (Skenario 0–6)
# ============================================================

def jalankan_semua(d, n_jobs, log):
    X, y, g = d[FITUR].to_numpy(float), d[LABEL].to_numpy(int), d[GRUP].to_numpy()
    lipatan = pembagian_luar(g)
    for tr, te in lipatan:
        assert not set(g[tr]) & set(g[te]), 'Subproyek uji bocor ke data latih'
    oof, durasi = {}, {}
    kombinasi = [(NAIF, 'Raw')] + [(m, k) for m in MODEL for k in KALIBRASI]
    for nama, kal in kombinasi:
        t = time.time()
        oof[(nama, kal)] = prediksi_oof(nama, kal, X, y, g, lipatan, n_jobs)
        durasi[(nama, kal)] = time.time() - t
        log.append(f'- {nama} / {kal}: {durasi[(nama, kal)]:.1f} detik')
        print(f'  {nama:<20} {kal:<9} {durasi[(nama, kal)]:6.1f} s  Brier {brier_score_loss(y, oof[(nama, kal)]):.4f}')
    return X, y, g, lipatan, oof


def tabel_utama(y, oof):
    bs_naif = brier_score_loss(y, oof[(NAIF, 'Raw')])
    baris = []
    for (nama, kal), p in oof.items():
        a, j = ambang_youden(y, p)
        baris.append({'Skenario': 0 if nama == NAIF else MODEL.index(nama) + 1, 'Model': nama, 'Kalibrasi': kal,
                      **metrik(y, p, bs_naif, a), 'Youden_J': j})
    t = pd.DataFrame(baris)
    kandidat = t[t.Model != NAIF].sort_values(['Brier', 'ECE', 'Log_Loss'])
    t['Rekomendasi'] = 0
    t.loc[kandidat.index[0], 'Rekomendasi'] = 1
    return t


def tabel_per_kelompok(d, y, oof, kolom):
    baris = []
    for nilai, idx in d.groupby(kolom).indices.items():
        bs_naif = brier_score_loss(y[idx], oof[(NAIF, 'Raw')][idx])
        for (nama, kal), p in oof.items():
            baris.append({kolom: nilai, 'Model': nama, 'Kalibrasi': kal, **metrik(y[idx], p[idx], bs_naif)})
    return pd.DataFrame(baris)


def tabel_zona(d, y, p, ambang):
    z = zona(p)
    baris = []
    kelompok = [('Semua', 'Semua', np.arange(len(y)))]
    kelompok += [('Semua', t, idx) for t, idx in d.groupby(TITIK).indices.items()]
    kelompok += [(s, t, idx) for (s, t), idx in d.groupby([GRUP, TITIK]).indices.items()]
    for sub, titik, idx in kelompok:
        telat, tepat = y[idx] == 1, y[idx] == 0
        r = {GRUP: sub, TITIK: titik, 'N': len(idx), 'Prevalensi': y[idx].mean(),
             **{f'Persen_{k}': (z[idx] == k).mean() for k in ('Hijau', 'Kuning', 'Merah')},
             'Telat_di_Merah': (z[idx][telat] == 'Merah').mean() if telat.any() else np.nan,
             'Tepat_di_Merah': (z[idx][tepat] == 'Merah').mean() if tepat.any() else np.nan,
             'Telat_di_atas_Ambang': (p[idx][telat] >= ambang).mean() if telat.any() else np.nan,
             'Tepat_di_atas_Ambang': (p[idx][tepat] >= ambang).mean() if tepat.any() else np.nan}
        baris.append(r)
    return pd.DataFrame(baris)


def _perm_lipatan(X, y, latih, uji):
    m = buat_model('Random Forest').fit(X[latih], y[latih])
    r = permutation_importance(m, X[uji], y[uji], scoring='neg_brier_score', n_repeats=5, random_state=SEED)
    return r.importances_mean


def tabel_kepentingan(X, y, lipatan, n_jobs):
    """Koefisien LR & MDI RF (dilatih pada seluruh data); permutation importance RF pada subproyek uji tiap lipatan."""
    lr = buat_model('Logistic Regression').fit(X, y)
    rf = buat_model('Random Forest').fit(X, y)
    perm = np.array(Parallel(n_jobs=n_jobs)(delayed(_perm_lipatan)(X, y, tr, te) for tr, te in lipatan))
    koef = lr.named_steps['model'].coef_[0]
    return pd.DataFrame({'Fitur': FITUR, 'Koefisien_LR': koef, 'Odds_Ratio_LR': np.exp(koef),
                         'MDI_RF': rf.named_steps['model'].feature_importances_,
                         'Permutation_RF_Rata2': perm.mean(0), 'Permutation_RF_SD': perm.std(0)})


# ============================================================
# 6. SENSITIVITAS (Skenario 7)
# ============================================================

def jalankan_sensitivitas(rek, data_utama, oof_utama, n_jobs):
    baris = []
    for faktor, path in [(FAKTOR_DAMPAK_UTAMA, DATASET)] + sorted(DATASET_SENSITIVITAS.items()):
        if faktor == FAKTOR_DAMPAK_UTAMA:
            d, oof_rek, oof_naif = data_utama, oof_utama[rek], oof_utama[(NAIF, 'Raw')]
        else:
            if not path.exists():
                raise SystemExit(f'Dataset sensitivitas belum ada: {path}\nBuat dengan (dari 06_simulasi_iterasi/):\n'
                                 f'  python buat_dataset_ml.py --faktor-dampak {faktor} '
                                 f'--keluaran dataset_ml/sensitivitas/{path.name}')
            d = muat_data(path)
            X, y, g = d[FITUR].to_numpy(float), d[LABEL].to_numpy(int), d[GRUP].to_numpy()
            lip = pembagian_luar(g)
            oof_rek = prediksi_oof(*rek, X, y, g, lip, n_jobs)
            oof_naif = prediksi_oof(NAIF, 'Raw', X, y, g, lip, n_jobs)
        y = d[LABEL].to_numpy(int)
        m = metrik(y, oof_rek, brier_score_loss(y, oof_naif))
        baris.append({'Faktor_Dampak': faktor, 'Model': rek[0], 'Kalibrasi': rek[1], 'Dataset': path.name,
                      'MD5_Dataset': md5(path), **m,
                      **{f'Prevalensi_{s}': v for s, v in d.groupby(GRUP)[LABEL].mean().items()}})
        print(f'  faktor {faktor}: prevalensi {m["Prevalensi"]:.3f}, Brier {m["Brier"]:.4f}, BSS {m["BSS"]:.3f}, '
              f'AUC {m["ROC_AUC"]:.3f}')
    return pd.DataFrame(baris)


# ============================================================
# 7. GRAFIK
# ============================================================

def _gaya(ax, judul, xl, yl):
    ax.set_facecolor(PERMUKAAN)
    ax.set_title(judul, fontsize=11, color=TINTA, loc='left')
    ax.set_xlabel(xl, fontsize=9, color=TINTA_2)
    ax.set_ylabel(yl, fontsize=9, color=TINTA_2)
    ax.tick_params(colors=TINTA_2, labelsize=8)
    ax.grid(color='#e6e5e0', linewidth=0.6)
    ax.set_axisbelow(True)  # grid di belakang batang/garis data
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#c3c2b7')


def grafik_roc(y, oof, tabel, path):
    fig, ax = plt.subplots(figsize=(6.4, 5.2), facecolor=PERMUKAAN)
    for nama in MODEL:
        fpr, tpr, _ = roc_curve(y, oof[(nama, 'Raw')])
        auc = tabel.query('Model == @nama and Kalibrasi == "Raw"').ROC_AUC.iloc[0]
        ax.plot(fpr, tpr, color=WARNA[nama], ls=GARIS[nama], lw=2, label=f'{nama} (AUC {f(auc, 3)})')
    ax.plot([0, 1], [0, 1], color=WARNA[NAIF], ls=GARIS[NAIF], lw=1.5, label='Tebakan acak (AUC 0,5)')
    _gaya(ax, 'Kurva ROC — prediksi out-of-fold (tanpa kalibrasi)', 'False positive rate (1 − specificity)',
          'True positive rate (recall)')
    ax.legend(fontsize=8, frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_kalibrasi(y, oof, rek, path):
    fig, axs = plt.subplots(1, 2, figsize=(11, 5), facecolor=PERMUKAAN)
    for ax in axs:
        ax.plot([0, 1], [0, 1], color=WARNA[NAIF], ls=GARIS[NAIF], lw=1.5, label='Kalibrasi sempurna')
    for nama in MODEL:
        fp, mp = calibration_curve(y, oof[(nama, 'Raw')], n_bins=N_BIN_ECE, strategy='uniform')
        axs[0].plot(mp, fp, color=WARNA[nama], ls=GARIS[nama], lw=2, marker='o', ms=4, label=nama)
    gaya_kal = {'Raw': '-', 'Platt': '--', 'Isotonic': ':'}
    for kal in KALIBRASI:
        fp, mp = calibration_curve(y, oof[(rek[0], kal)], n_bins=N_BIN_ECE, strategy='uniform')
        axs[1].plot(mp, fp, color=WARNA[rek[0]], ls=gaya_kal[kal], lw=2, marker='o', ms=4, label=kal,
                    alpha=1.0 if kal == rek[1] else 0.6)
    _gaya(axs[0], 'Reliability diagram — 4 model tanpa kalibrasi', 'Rata-rata probabilitas prediksi',
          'Proporsi telat aktual')
    _gaya(axs[1], f'Efek kalibrasi — {rek[0]} (rekomendasi: {rek[1]})', 'Rata-rata probabilitas prediksi',
          'Proporsi telat aktual')
    for ax in axs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.legend(fontsize=8, frameon=False, loc='upper left')
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_kepentingan(kep, path):
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.6), facecolor=PERMUKAAN)
    urut = kep.reindex(kep.Permutation_RF_Rata2.sort_values().index)
    pos = np.arange(len(urut))
    panel = [('Koefisien_LR', None, 'Logistic Regression: koefisien\n(per simpangan baku fitur)', WARNA['Logistic Regression']),
             ('MDI_RF', None, 'Random Forest: MDI\n(dilatih pada seluruh data)', WARNA['Random Forest']),
             ('Permutation_RF_Rata2', 'Permutation_RF_SD',
              'Random Forest: permutation\n(kenaikan Brier, subproyek uji)', WARNA['Random Forest'])]
    for ax, (kol, sd, judul, warna) in zip(axs, panel):
        ax.barh(pos, urut[kol], height=0.6, color=warna, xerr=urut[sd] if sd else None,
                error_kw={'ecolor': TINTA_2, 'lw': 1})
        ax.axvline(0, color=TINTA_2, lw=0.8)
        ax.set_yticks(pos, urut.Fitur, fontsize=8)
        _gaya(ax, judul, '', '')
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def grafik_per_titik(per_titik, terbaik_per_model, path):
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=PERMUKAAN)
    for nama, kal in [(NAIF, 'Raw')] + terbaik_per_model:
        s = per_titik.query('Model == @nama and Kalibrasi == @kal').sort_values(TITIK)
        x = s[TITIK] * 100
        label = nama if nama == NAIF else f'{nama} ({kal})'
        axs[0].plot(x, s.Brier, color=WARNA[nama], ls=GARIS[nama], lw=2, marker='o', ms=6, label=label)
        if nama != NAIF:
            axs[1].plot(x, s.ROC_AUC, color=WARNA[nama], ls=GARIS[nama], lw=2, marker='o', ms=6, label=label)
    _gaya(axs[0], 'Brier Score per titik monitoring (lebih kecil lebih baik)', 'Titik monitoring (% jadwal rencana)',
          'Brier Score')
    _gaya(axs[1], 'ROC-AUC per titik monitoring (lebih besar lebih baik)', 'Titik monitoring (% jadwal rencana)',
          'ROC-AUC')
    for ax in axs:
        ax.set_xticks([25, 50, 75])
        ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


# ============================================================
# 8. LAPORAN
# ============================================================

def f(x, n=4):
    return 'n/a' if pd.isna(x) else f'{x:.{n}f}'.replace('.', ',')


def pct(x, n=1):
    return 'n/a' if pd.isna(x) else f'{100 * x:.{n}f}%'.replace('.', ',')


def tulis_ringkasan(path, d, tabel, per_titik, per_sub, zona_t, kep, sens, rek):
    r = tabel[tabel.Rekomendasi == 1].iloc[0]
    m_rek, k_rek = rek
    naif = tabel[tabel.Model == NAIF].iloc[0]
    raw = tabel[(tabel.Kalibrasi == 'Raw') & (tabel.Model != NAIF)]
    L = ['# Ringkasan Temuan Eksperimen PRE-02 (versi 2)\n',
         '> Digenerate otomatis oleh `experiment_pipeline.py`. Semua angka berasal dari prediksi out-of-fold '
         '*leave-one-subproject-out* (8 lipatan) pada `dataset_ml.csv`. Jangan diedit manual.\n',
         f'- Data: {len(d)} baris, {d[GRUP].nunique()} subproyek, label `{LABEL}` = 1 pada {pct(d[LABEL].mean())} baris',
         f'- Pembanding naif: Brier {f(naif.Brier)}, AUC {f(naif.ROC_AUC, 3)}',
         f'- **Model rekomendasi: {r.Model} + {r.Kalibrasi}** — Brier {f(r.Brier)}, Brier Skill Score {f(r.BSS, 3)}, '
         f'ROC-AUC {f(r.ROC_AUC, 3)}, ECE {f(r.ECE)}, Log Loss {f(r.Log_Loss)}\n',
         '## Skenario 0–5: perbandingan model\n',
         '| Model | Kalibrasi | Brier | BSS | Log Loss | ECE | ROC-AUC | Ambang Youden | Recall | Specificity | F1 |',
         '| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for _, t in tabel.sort_values(['Skenario', 'Kalibrasi'], key=lambda c: c.map(KALIBRASI.index) if c.name == 'Kalibrasi' else c).iterrows():
        tebal = '**' if t.Rekomendasi else ''
        L.append(f'| {tebal}{t.Model}{tebal} | {t.Kalibrasi} | {f(t.Brier)} | {f(t.BSS, 3)} | {f(t.Log_Loss)} | '
                 f'{f(t.ECE)} | {f(t.ROC_AUC, 3)} | {f(t.Ambang, 3)} | {pct(t.Recall)} | {pct(t.Specificity)} | {f(t.F1, 3)} |')
    terbaik_auc = raw.sort_values('ROC_AUC', ascending=False).iloc[0]
    L += ['',
          f'- Semua model berada di atas pembanding naif: BSS terendah di antara 12 kombinasi = '
          f'{f(tabel[tabel.Model != NAIF].BSS.min(), 3)}.' if (tabel[tabel.Model != NAIF].BSS > 0).all() else
          f'- Ada kombinasi dengan BSS ≤ 0 (tidak lebih baik dari pembanding naif): '
          f'{", ".join(tabel[(tabel.Model != NAIF) & (tabel.BSS <= 0)].apply(lambda t: t.Model + "/" + t.Kalibrasi, axis=1))}.',
          f'- ROC-AUC tertinggi tanpa kalibrasi: {terbaik_auc.Model} ({f(terbaik_auc.ROC_AUC, 3)}).',
          *[(f'- {m}: Platt maupun Isotonic tidak memperbaiki Brier (Raw {f(raw_m.Brier)} tetap terbaik).'
             if b.Kalibrasi == 'Raw' else
             f'- {m}: kalibrasi terbaik menurut Brier = {b.Kalibrasi} (Brier Raw {f(raw_m.Brier)} → '
             f'{f(b.Brier)}; ROC-AUC Raw {f(raw_m.ROC_AUC, 3)} → {f(b.ROC_AUC, 3)}).')
            for m in MODEL
            for b, raw_m in [(tabel[tabel.Model == m].sort_values(['Brier', 'ECE', 'Log_Loss']).iloc[0],
                              tabel[(tabel.Model == m) & (tabel.Kalibrasi == 'Raw')].iloc[0])]],
          '- ROC-AUC gabungan dapat berubah setelah kalibrasi walaupun kalibrasi bersifat monoton: setiap lipatan '
          'memakai pemetaan kalibrasi sendiri (dilatih pada subproyek lain), sehingga urutan prediksi antarsubproyek '
          'berubah, dan isotonic menghasilkan nilai seri.\n',
          '## Skenario 6: per titik monitoring (model rekomendasi)\n',
          '| Titik | Prevalensi | Brier | BSS | ROC-AUC | ECE |', '| ---: | ---: | ---: | ---: | ---: | ---: |']
    for _, t in per_titik.query('Model == @m_rek and Kalibrasi == @k_rek').sort_values(TITIK).iterrows():
        L.append(f'| {pct(t[TITIK], 0)} | {pct(t.Prevalensi)} | {f(t.Brier)} | {f(t.BSS, 3)} | {f(t.ROC_AUC, 3)} | {f(t.ECE)} |')
    L += ['', '## Brier per subproyek uji (model rekomendasi vs pembanding naif)\n',
          '| Subproyek | Prevalensi | Brier model | Brier naif | BSS |', '| :--- | ---: | ---: | ---: | ---: |']
    for sub in sorted(d[GRUP].unique()):
        m = per_sub.query(f'{GRUP} == @sub and Model == @m_rek and Kalibrasi == @k_rek').iloc[0]
        n = per_sub.query(f'{GRUP} == @sub and Model == @NAIF').iloc[0]
        L.append(f'| {sub} | {pct(m.Prevalensi)} | {f(m.Brier)} | {f(n.Brier)} | {f(m.BSS, 3)} |')
    kalah = per_sub.query('Model == @m_rek and Kalibrasi == @k_rek and BSS <= 0')[GRUP].tolist()
    L += ['', f'Model rekomendasi lebih buruk dari pembanding naif (BSS ≤ 0) pada: {", ".join(kalah)}.' if kalah else
          'Model rekomendasi lebih baik dari pembanding naif (BSS > 0) pada semua subproyek uji.']
    L += ['', '## Peringatan dini (model rekomendasi)\n',
          f'Ambang Youden θ* = {f(r.Ambang, 3)} (Recall {pct(r.Recall)}, Specificity {pct(r.Specificity)}). '
          f'Zona: Hijau < {f(ZONA[0], 2)} ≤ Kuning < {f(ZONA[1], 2)} ≤ Merah.\n',
          '| Titik | Proyek yang akhirnya telat & sudah di zona Merah | Proyek tepat waktu yang masuk zona Merah | '
          'Telat terdeteksi ≥ θ* | Tepat waktu ≥ θ* |', '| ---: | ---: | ---: | ---: | ---: |']
    for _, t in zona_t[(zona_t[GRUP] == 'Semua') & (zona_t[TITIK] != 'Semua')].iterrows():
        L.append(f'| {pct(float(t[TITIK]), 0)} | {pct(t.Telat_di_Merah)} | {pct(t.Tepat_di_Merah)} | '
                 f'{pct(t.Telat_di_atas_Ambang)} | {pct(t.Tepat_di_atas_Ambang)} |')
    L += ['', '## Kepentingan fitur\n',
          '| Fitur | Koefisien LR | Odds ratio LR | MDI RF | Permutation RF (± SD) |', '| :--- | ---: | ---: | ---: | ---: |']
    for _, t in kep.sort_values('Permutation_RF_Rata2', ascending=False).iterrows():
        L.append(f'| {t.Fitur} | {f(t.Koefisien_LR, 3)} | {f(t.Odds_Ratio_LR, 3)} | {f(t.MDI_RF, 3)} | '
                 f'{f(t.Permutation_RF_Rata2)} (± {f(t.Permutation_RF_SD)}) |')
    if sens is not None:
        L += ['', '## Skenario 7: sensitivitas faktor dampak risiko\n',
              f'Model {rek[0]} + {rek[1]} dijalankan ulang pada dataset dengan faktor dampak berbeda.\n',
              '| Faktor dampak | Prevalensi label | Brier | BSS | ROC-AUC | ECE |', '| ---: | ---: | ---: | ---: | ---: | ---: |']
        for _, t in sens.iterrows():
            utama = ' (utama)' if t.Faktor_Dampak == FAKTOR_DAMPAK_UTAMA else ''
            L.append(f'| {f(t.Faktor_Dampak, 1)}{utama} | {pct(t.Prevalensi)} | {f(t.Brier)} | {f(t.BSS, 3)} | '
                     f'{f(t.ROC_AUC, 3)} | {f(t.ECE)} |')
    L += ['', '## Catatan membaca\n',
          '- BSS (Brier Skill Score) = 1 − Brier model / Brier pembanding naif; > 0 berarti lebih baik dari menebak '
          'proporsi telat.',
          '- Ambang Youden dipilih pada prediksi out-of-fold yang sama dengan yang dievaluasi, sehingga Recall/Specificity '
          'pada ambang itu sedikit optimistis; metrik probabilitas (Brier, Log Loss, ECE, AUC) tidak bergantung ambang.',
          '- ROC-AUC pembanding naif di bawah 0,5 adalah konsekuensi validasi per subproyek: prediksinya = proporsi telat '
          'di 7 subproyek latih, yang justru lebih rendah ketika subproyek uji banyak telat (dan sebaliknya). Pembanding '
          'naif dipakai untuk Brier/BSS, bukan untuk AUC.',
          '- P-FNE-02 dan P-FNE-04 hampir satu kelas pada label ini; ROC-AUC per subproyek tidak dilaporkan.']
    Path(path).write_text('\n'.join(L) + '\n', encoding='utf-8')


def tulis_log(path, d, tabel, log, mulai, sens):
    import joblib
    L = ['# Log Pelaksanaan Eksperimen PRE-02 (versi 2)\n',
         '> Digenerate otomatis oleh `experiment_pipeline.py`.\n',
         f'- Waktu jalan: {mulai:%Y-%m-%d %H:%M}, durasi total {time.time() - mulai.timestamp():.0f} detik',
         f'- Lingkungan: Python {platform.python_version()}, scikit-learn {sklearn.__version__}, numpy {np.__version__}, '
         f'pandas {pd.__version__}, joblib {joblib.__version__}',
         f'- Dataset: `{DATASET.relative_to(ROOT)}` (MD5 `{md5(DATASET)}`), {len(d)} baris',
         f'- Fitur ({len(FITUR)}): {", ".join(FITUR)}', f'- Label: {LABEL}; grup validasi: {GRUP}', f'- Seed: {SEED}',
         '- Pembagian luar: LeaveOneGroupOut (8 lipatan); pembagian dalam kalibrasi: GroupKFold(3) per subproyek',
         '- Pemeriksaan otomatis: kolom & ukuran data sesuai kontrak; tidak ada subproyek uji di data latih; '
         'setiap baris diprediksi tepat satu kali\n',
         '## Durasi per model × kalibrasi (8 lipatan, paralel)\n', *log,
         f'\n## Model rekomendasi\n\n{tabel[tabel.Rekomendasi == 1].iloc[0].Model} + '
         f'{tabel[tabel.Rekomendasi == 1].iloc[0].Kalibrasi} (Brier terendah; seri: ECE, lalu Log Loss)']
    if sens is not None:
        L += ['\n## Dataset sensitivitas\n'] + [f'- faktor {t.Faktor_Dampak}: `{t.Dataset}` (MD5 `{t.MD5_Dataset}`)'
                                                for _, t in sens.iterrows()]
    Path(path).write_text('\n'.join(L) + '\n', encoding='utf-8')


# ============================================================
# 9. MAIN
# ============================================================

def main(argv=None):
    ap = argparse.ArgumentParser(description='Pipeline eksperimen PRE-02 versi 2')
    ap.add_argument('--sensitivitas', action='store_true', help='jalankan juga Skenario 7')
    ap.add_argument('--keluaran', default=str(HERE / 'hasil_eksperimen'), help='folder luaran')
    ap.add_argument('--n-jobs', type=int, default=-1, help='jumlah proses paralel (bawaan: semua inti)')
    a = ap.parse_args(argv)
    out = Path(a.keluaran)
    out.mkdir(parents=True, exist_ok=True)
    mulai = datetime.now()
    log = []

    print(f'[1/6] Muat data: {DATASET}')
    d = muat_data(DATASET)
    print('[2/6] Skenario 0–5: prediksi out-of-fold (leave-one-subproject-out)')
    X, y, g, lipatan, oof = jalankan_semua(d, a.n_jobs, log)

    print('[3/6] Evaluasi')
    tabel = tabel_utama(y, oof)
    rek = tuple(tabel[tabel.Rekomendasi == 1].iloc[0][['Model', 'Kalibrasi']])
    per_titik = tabel_per_kelompok(d, y, oof, TITIK)
    per_sub = tabel_per_kelompok(d, y, oof, GRUP)
    ambang = float(tabel[tabel.Rekomendasi == 1].iloc[0].Ambang)
    zona_t = tabel_zona(d, y, oof[rek], ambang)
    print(f'      rekomendasi: {rek[0]} + {rek[1]}')

    print('[4/6] Kepentingan fitur')
    kep = tabel_kepentingan(X, y, lipatan, a.n_jobs)

    sens = None
    if a.sensitivitas:
        print('[5/6] Skenario 7: sensitivitas')
        sens = jalankan_sensitivitas(rek, d, oof, a.n_jobs)
    else:
        print('[5/6] Skenario 7 dilewati (tambahkan --sensitivitas)')

    print(f'[6/6] Tulis luaran ke {out}')
    bulat = lambda t: t.round(6)
    bulat(tabel).to_csv(out / 'tabel_metrik_evaluasi.csv', index=False)
    bulat(per_titik).to_csv(out / 'tabel_metrik_per_titik.csv', index=False)
    bulat(per_sub).to_csv(out / 'tabel_metrik_per_subproyek.csv', index=False)
    bulat(zona_t).to_csv(out / 'tabel_zona_peringatan.csv', index=False)
    bulat(kep).to_csv(out / 'tabel_feature_importance.csv', index=False)
    pred = d[[GRUP, 'Iterasi', TITIK, LABEL]].copy()
    for (nama, kal), p in oof.items():
        pred[f'P_{nama.replace(" ", "_")}_{kal}'] = p
    pred['Zona_Rekomendasi'] = zona(oof[rek])
    # presisi penuh: pembulatan membuat probabilitas MLP yang sangat dekat 1 menjadi seri dan mengubah ROC-AUC
    pred.to_csv(out / 'tabel_prediksi_oof.csv', index=False, float_format='%.17g')
    if sens is not None:
        bulat(sens).to_csv(out / 'tabel_sensitivitas.csv', index=False)

    terbaik_per_model = [tuple(tabel[tabel.Model == m].sort_values(['Brier', 'ECE', 'Log_Loss']).iloc[0][['Model', 'Kalibrasi']])
                         for m in MODEL]
    grafik_roc(y, oof, tabel, out / 'kurva_roc_perbandingan.png')
    grafik_kalibrasi(y, oof, rek, out / 'kurva_kalibrasi_probabilitas.png')
    grafik_kepentingan(kep, out / 'feature_importance_comparison.png')
    grafik_per_titik(per_titik, terbaik_per_model, out / 'metrik_per_titik.png')
    tulis_ringkasan(out / '00_RINGKASAN_TEMUAN_EKSPERIMEN.md', d, tabel, per_titik, per_sub, zona_t, kep, sens, rek)
    tulis_log(out / 'log_pelaksanaan_eksperimen.md', d, tabel, log, mulai, sens)
    print('Selesai.')
    return tabel


if __name__ == '__main__':
    main()
