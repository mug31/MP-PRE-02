"""Gambar 1-4 naskah paper, versi satu kolom jurnal.

Gambar di folder eksperimen dibuat untuk slide: dua panel berdampingan, label bahasa Inggris, dan
terlalu kecil bila dimuat ke satu kolom jurnal (7,6 cm). Skrip ini menggambar ulang keempatnya dari
CSV hasil yang sudah ada (tanpa menjalankan ulang eksperimen) dengan panel (a) di atas dan (b) di
bawah, huruf lebih besar, label berbahasa Indonesia, dan desimal koma.

Masukan : ../04_implemen_desain_eksperimen/hasil_eksperimen/tabel_prediksi_oof.csv
          ../04_implemen_desain_eksperimen/hasil_analisis/tabel_uji_hipotesis.csv
          ../04_implemen_desain_eksperimen/hasil_analisis/tabel_ci_per_titik.csv
          ../04_implemen_desain_eksperimen/hasil_analisis/tabel_deteksi_dini.csv
Keluaran: gambar/gambar_1_kalibrasi.png ... gambar/gambar_4_deteksi_dini.png
Kebutuhan: numpy, pandas, matplotlib
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
EKSP = HERE.parent / '04_implemen_desain_eksperimen'
KELUAR = HERE / 'gambar'

NAIF = 'Pembanding Naif'
MODEL = ['Logistic Regression', 'Random Forest', 'Gradient Boosting', 'MLP Neural Network']
SINGKAT = {'Logistic Regression': 'LR', 'Random Forest': 'RF', 'Gradient Boosting': 'GB',
           'MLP Neural Network': 'NN', NAIF: 'Naif'}
REKOMENDASI = ('Gradient Boosting', 'Raw')          # model rekomendasi pada naskah (Brier score terendah)
N_BIN = 10                                          # sama dengan ECE di eksperimen
WARNA = {'Logistic Regression': '#2a78d6', 'Random Forest': '#eb6834',
         'Gradient Boosting': '#1baf7a', 'MLP Neural Network': '#eda100', NAIF: '#52514e'}
GARIS = {'Logistic Regression': '-', 'Random Forest': '--', 'Gradient Boosting': '-.',
         'MLP Neural Network': ':', NAIF: (0, (1, 2))}
TINTA, TINTA_2 = '#111111', '#444444'
LEBAR = 3.15                                        # inci; dimuat 7,6 cm sehingga huruf hampir 1:1

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Times New Roman', 'Liberation Serif', 'DejaVu Serif'],
    'mathtext.fontset': 'stix', 'font.size': 7.5, 'axes.titlesize': 8, 'axes.labelsize': 7.5,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 6.8, 'axes.unicode_minus': True,
})
KOMA = FuncFormatter(lambda v, _: f'{v:g}'.replace('-', '−').replace('.', ','))


def gaya(ax, judul, xl, yl):
    ax.set_title(judul, loc='left', color=TINTA, pad=4)
    ax.set_xlabel(xl, color=TINTA_2)
    ax.set_ylabel(yl, color=TINTA_2)
    ax.tick_params(colors=TINTA_2, length=2.5, width=0.6)
    ax.grid(color='#e4e4e4', linewidth=0.5)
    ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#999999')
        ax.spines[s].set_linewidth(0.6)
    ax.xaxis.set_major_formatter(KOMA)
    ax.yaxis.set_major_formatter(KOMA)


def simpan(fig, nama):
    KELUAR.mkdir(exist_ok=True)
    fig.savefig(KELUAR / nama, dpi=300, bbox_inches='tight', pad_inches=0.03, facecolor='white')
    plt.close(fig)


def kurva_kalibrasi(y, p):
    """Sama dengan sklearn calibration_curve(strategy='uniform'): bin kosong dibuang."""
    tepi = np.linspace(0, 1, N_BIN + 1)
    idx = np.searchsorted(tepi[1:-1], p)
    n = np.bincount(idx, minlength=N_BIN)
    ada = n > 0
    return (np.bincount(idx, p, N_BIN)[ada] / n[ada]), (np.bincount(idx, y, N_BIN)[ada] / n[ada])


def gambar_1():
    d = pd.read_csv(EKSP / 'hasil_eksperimen' / 'tabel_prediksi_oof.csv')
    y = d['Telat_Lebih_5_Persen'].to_numpy(float)
    kol = lambda m, k: f'P_{m.replace(" ", "_")}_{k}'
    fig, axs = plt.subplots(2, 1, figsize=(LEBAR, 5.6))
    for ax in axs:
        ax.plot([0, 1], [0, 1], color=WARNA[NAIF], ls=GARIS[NAIF], lw=1, label='Kalibrasi sempurna')
    for m in MODEL:
        x, f = kurva_kalibrasi(y, d[kol(m, 'Raw')].to_numpy())
        axs[0].plot(x, f, color=WARNA[m], ls=GARIS[m], lw=1.4, marker='o', ms=2.8, label=SINGKAT[m])
    for k, g in [('Raw', '-'), ('Platt', '--'), ('Isotonic', ':')]:
        x, f = kurva_kalibrasi(y, d[kol(REKOMENDASI[0], k)].to_numpy())
        axs[1].plot(x, f, color=WARNA[REKOMENDASI[0]], ls=g, lw=1.4, marker='o', ms=2.8,
                    alpha=1 if k == REKOMENDASI[1] else 0.65, label=k)
    gaya(axs[0], '(a) Empat model tanpa kalibrasi', 'Rata-rata probabilitas prediksi', 'Proporsi terlambat aktual')
    gaya(axs[1], '(b) Efek kalibrasi pada GB', 'Rata-rata probabilitas prediksi', 'Proporsi terlambat aktual')
    for ax in axs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.legend(frameon=False, loc='upper left', handlelength=2.6)
    fig.tight_layout(h_pad=1.2)
    simpan(fig, 'gambar_1_kalibrasi.png')


def label_uji(r):
    a, b = r.A.split(' + '), r.B.split(' + ')
    sa = SINGKAT[a[0]] + ('' if a[1] == 'Raw' else f' {a[1]}')
    sb = SINGKAT[b[0]] + ('' if b[1] == 'Raw' else f' {b[1]}')
    return f'{r.Kode_Uji}: {sa} − {sb}'


def gambar_2():
    uji = pd.read_csv(EKSP / 'hasil_analisis' / 'tabel_uji_hipotesis.csv')
    bag = [('Brier', '(a) Selisih Brier score (A − B)'), ('ECE', '(b) Selisih ECE (A − B)')]
    n = [int((uji.Metrik == m).sum()) for m, _ in bag]
    fig, axs = plt.subplots(2, 1, figsize=(LEBAR, 0.19 * sum(n) + 2.0), gridspec_kw={'height_ratios': n})
    biru = WARNA['Logistic Regression']
    for ax, (m, judul) in zip(axs, bag):
        s = uji[uji.Metrik == m].iloc[::-1]
        pos = np.arange(len(s))
        for yy, (_, r) in zip(pos, s.iterrows()):
            ax.plot([r.CI_Bawah, r.CI_Atas], [yy, yy], color=biru, lw=1.4, solid_capstyle='round')
            if r.Signifikan:
                ax.plot(r.Selisih_A_minus_B, yy, 'o', ms=4, mec=biru, mew=1.2, mfc=biru)
            elif r.Arah_Berlawanan_Signifikan:
                ax.plot(r.Selisih_A_minus_B, yy, 'X', ms=5, mec=biru, mew=0.6, mfc=biru)
            else:
                ax.plot(r.Selisih_A_minus_B, yy, 'o', ms=4, mec=biru, mew=1.2, mfc='white')
        ax.axvline(0, color=TINTA_2, lw=0.8)
        gaya(ax, judul, '← A lebih baik  |  B lebih baik →', '')
        ax.set_yticks(pos, [label_uji(r) for _, r in s.iterrows()])   # setelah gaya() agar label tidak ditimpa
        ax.set_ylim(-0.7, len(s) - 0.3)
        ax.grid(axis='y', visible=False)
    h = [plt.Line2D([], [], marker='o', ms=4, ls='-', color=biru, mfc=biru, label='Signifikan (Holm, α = 0,05)'),
         plt.Line2D([], [], marker='X', ms=5, ls='-', color=biru, label='Signifikan berlawanan arah'),
         plt.Line2D([], [], marker='o', ms=4, ls='-', color=biru, mfc='white', label='Tidak signifikan')]
    fig.tight_layout(h_pad=1.2, rect=(0, 0.05, 1, 1))
    fig.legend(handles=h, loc='lower center', ncol=2, frameon=False, columnspacing=1.0, handlelength=1.8)
    simpan(fig, 'gambar_2_uji_hipotesis.png')


def gambar_3():
    ci = pd.read_csv(EKSP / 'hasil_analisis' / 'tabel_ci_per_titik.csv')
    fig, axs = plt.subplots(2, 1, figsize=(LEBAR, 5.2))
    geser = dict(zip(MODEL, [-2.4, -0.8, 0.8, 2.4]))
    for m in MODEL:
        s = ci[(ci.Model == m) & (ci.Kalibrasi == 'Raw')].sort_values('Titik_Monitoring')
        x = s.Titik_Monitoring * 100 + geser[m]
        for ax, nm in zip(axs, ['ROC_AUC', 'Brier']):
            ax.errorbar(x, s[nm], yerr=[s[nm] - s[nm + '_CI_Bawah'], s[nm + '_CI_Atas'] - s[nm]], color=WARNA[m],
                        ls=GARIS[m], lw=1.3, marker='o', ms=3, capsize=2, elinewidth=0.9, label=SINGKAT[m])
    nf = ci[ci.Model == NAIF].sort_values('Titik_Monitoring')
    axs[1].plot(nf.Titik_Monitoring * 100, nf.Brier, color=WARNA[NAIF], ls=GARIS[NAIF], lw=1, marker='o', ms=2.5,
                label='Naif')
    gaya(axs[0], '(a) ROC-AUC (makin besar makin baik)', 'Titik monitoring (% jadwal rencana)', 'ROC-AUC')
    gaya(axs[1], '(b) Brier score (makin kecil makin baik)', 'Titik monitoring (% jadwal rencana)', 'Brier score')
    for ax in axs:
        ax.set_xticks([25, 50, 75])
        ax.set_xlim(15, 85)
    axs[0].legend(frameon=False, loc='lower right', ncol=2, handlelength=2.6)
    axs[1].legend(frameon=False, loc='lower left', ncol=3, handlelength=2.6)
    fig.tight_layout(h_pad=1.2)
    simpan(fig, 'gambar_3_metrik_per_titik.png')


def gambar_4():
    det = pd.read_csv(EKSP / 'hasil_analisis' / 'tabel_deteksi_dini.csv')
    fig, axs = plt.subplots(2, 1, figsize=(LEBAR, 5.0))
    x = [25, 50, 75]
    for (_, r), m in zip(det.iterrows(), ['Logistic Regression', 'Random Forest', 'Gradient Boosting']):
        ket = r.Keterangan.replace('θ*', r'$\theta^*$')
        lbl = f'{ket} ({r.Ambang:.2f})'.replace('.', ',')
        for ax, nm in zip(axs, ['Telat', 'Tepat']):
            ax.plot(x, [100 * r[f'{nm}_Diperingatkan_sd_{t}'] for t in x], color=WARNA[m], ls=GARIS[m], lw=1.4,
                    marker='o', ms=3, label=lbl)
    gaya(axs[0], '(a) Proyek terlambat yang sudah diperingatkan', 'Sampai titik monitoring (% jadwal rencana)',
         '% iterasi (kumulatif)')
    gaya(axs[1], '(b) Proyek tepat waktu yang menerima peringatan palsu', 'Sampai titik monitoring (% jadwal rencana)',
         '% iterasi (kumulatif)')
    for ax, loc in zip(axs, ['lower right', 'upper left']):
        ax.set_xticks(x)
        ax.set_ylim(0, 100)
        ax.legend(frameon=False, loc=loc, handlelength=2.6)
    fig.tight_layout(h_pad=1.2)
    simpan(fig, 'gambar_4_deteksi_dini.png')


if __name__ == '__main__':
    gambar_1(); gambar_2(); gambar_3(); gambar_4()
    print('Gambar 1-4 tersimpan di', KELUAR)
