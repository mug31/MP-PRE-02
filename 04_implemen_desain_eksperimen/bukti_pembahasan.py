"""
PRE-02: Cek bukti untuk pembahasan (Pertemuan 7)

Setiap penjelasan "mengapa" di draf Bab V harus didukung data. Skrip ini menghitung bukti tersebut dari luaran
Pertemuan 5–6 dan dataset, tanpa mengubah hasil utama. Bagian E5 adalah analisis post-hoc (model dilatih ulang
dengan fitur relatif) dan diberi label demikian di semua luaran.

  E1  Overconfidence NN           : porsi prediksi ekstrem (≤ 0,01 atau ≥ 0,99) dan ketepatannya
  E2  Transfer kalibrasi           : Platt yang dilatih di 7 subproyek lain vs Platt "oracle" di subproyek itu sendiri
  E3  Slope LR latih vs uji         : calibration slope LR pada data latih dan pada subproyek uji tiap lipatan
  E4  Perbedaan antarsubproyek      : baseline T, ambang telat 5% dalam hari, prevalensi, rata-rata prediksi
  E5  Post-hoc fitur relatif        : GB dengan fitur yang dinormalisasi terhadap T (khusus kasus P-FNE-08)
  E6  Variabel lemah                : korelasi Spearman X5–X7 dengan label dan dengan SPI, gabungan & dalam subproyek
  E7  Contoh kasus peringatan dini  : lintasan probabilitas dua iterasi (telat terdeteksi dini; peringatan palsu)
  E8  Sifat peringatan palsu        : keterlambatan akhir proyek tepat waktu yang pernah vs tidak pernah diperingatkan

Jalankan (dari folder ini, setelah analisis_data.py):  python bukti_pembahasan.py
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

import analisis_data as an
import experiment_pipeline as ep
from experiment_pipeline import FITUR, GRUP, LABEL, MODEL, NAIF, SEED, TITIK, ZONA, f, pct

KELUARAN = ep.HERE / 'hasil_analisis' / 'bukti_pembahasan'
EKSTREM = 0.01


def muat():
    p, _ = an.muat_prediksi(an.HASIL_EKSP / 'tabel_prediksi_oof.csv')
    d = ep.muat_data(ep.DATASET)
    assert (d[[GRUP, 'Iterasi', TITIK, LABEL]].to_numpy() == p[[GRUP, 'Iterasi', TITIK, LABEL]].to_numpy()).all()
    d['T_Rencana'] = d['Hari_Monitoring'] / d[TITIK]
    return p, d


def logit(q):
    q = np.clip(q, 1e-6, 1 - 1e-6)
    return np.log(q / (1 - q))


def platt(q_latih, y_latih, q_uji):
    """Platt scaling pada logit probabilitas: y ~ a + b·logit(q)."""
    from sklearn.linear_model import LogisticRegression
    m = LogisticRegression(C=np.inf, max_iter=1000).fit(logit(q_latih)[:, None], y_latih)
    return m.predict_proba(logit(q_uji)[:, None])[:, 1]


# ---------------------------------------------------------------- E1
def e1_ekstrem(p):
    y = p[LABEL].to_numpy()
    baris = []
    for m in MODEL:
        q = p[an.kolom(m, 'Raw')].to_numpy()
        eks = (q <= EKSTREM) | (q >= 1 - EKSTREM)
        salah = eks & ((q >= 0.5) != (y == 1))
        baris.append({'Model': m, 'Persen_Prediksi_Ekstrem': eks.mean(),
                      'Persen_Ekstrem_yang_Salah': salah.sum() / eks.sum() if eks.any() else np.nan,
                      'Log_Loss_Kontribusi_Ekstrem_Salah': (-np.log(np.clip(np.where(y == 1, q, 1 - q), 1e-15, 1))[salah]).sum() / len(y)})
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- E2
def e2_transfer_kalibrasi(p):
    """Untuk tiap subproyek uji: ECE Raw, ECE setelah Platt dari 7 subproyek lain (prediksi out-of-fold mereka),
    dan ECE setelah Platt 'oracle' yang dilatih di subproyek itu sendiri (batas atas, bukan skenario nyata)."""
    y_all = p[LABEL].to_numpy()
    g = p[GRUP].to_numpy()
    baris = []
    for m in MODEL:
        q_all = p[an.kolom(m, 'Raw')].to_numpy()
        for sub in sorted(np.unique(g)):
            uji, latih = g == sub, g != sub
            y, q = y_all[uji], q_all[uji]
            q_lain = platt(q_all[latih], y_all[latih], q)
            q_oracle = platt(q, y, q) if 0 < y.sum() < len(y) else q
            baris.append({'Model': m, GRUP: sub, 'ECE_Raw': ep.ece(y, q), 'ECE_Platt_Subproyek_Lain': ep.ece(y, q_lain),
                          'ECE_Platt_Oracle': ep.ece(y, q_oracle),
                          'Brier_Raw': np.mean((q - y) ** 2), 'Brier_Platt_Subproyek_Lain': np.mean((q_lain - y) ** 2),
                          'Brier_Platt_Oracle': np.mean((q_oracle - y) ** 2)})
    t = pd.DataFrame(baris)
    ring = t.groupby('Model')[[c for c in t.columns if c.startswith(('ECE', 'Brier'))]].mean().reset_index()
    return t, ring


# ---------------------------------------------------------------- E3
def _slope_lipatan(X, y, g, latih, uji):
    m = ep.buat_model('Logistic Regression').fit(X[latih], y[latih])
    hasil = {}
    for nama, idx in [('Latih', latih), ('Uji', uji)]:
        q = m.predict_proba(X[idx])[:, 1]
        a, b = an.intercept_slope(an.siapkan(y[idx], q)['L'], y[idx].astype(float), np.ones(len(idx)))
        hasil[f'Slope_{nama}'], hasil[f'Intercept_{nama}'] = b, a
    hasil[GRUP] = g[uji][0]
    return hasil


def e3_slope_lr(d, n_jobs):
    X, y, g = d[FITUR].to_numpy(), d[LABEL].to_numpy(), d[GRUP].to_numpy()
    lip = ep.pembagian_luar(g)
    return pd.DataFrame(Parallel(n_jobs=n_jobs)(delayed(_slope_lipatan)(X, y, g, tr, te) for tr, te in lip))


# ---------------------------------------------------------------- E4
def e4_profil(p, d):
    rek = an.tabel_subproyek(p, d, ('Gradient Boosting', 'Raw'))[0]
    prof = d.groupby(GRUP).agg(T_Rencana=('T_Rencana', 'first'), Rata2_Keterlambatan_Hari=('Keterlambatan_Akhir_Hari', 'mean'),
                               Utilisasi=('Utilisasi_Resource', 'mean'), Sisa_Waktu_Rata2=('Sisa_Waktu_Hari', 'mean'))
    prof['Ambang_Telat_5pct_Hari'] = 0.05 * prof['T_Rencana']
    prof = prof.reset_index().merge(rek[[GRUP, 'Prevalensi', 'Rata2_Prediksi_Model', 'Selisih_Prediksi_Prevalensi', 'BSS']], on=GRUP)
    # jarak profil fitur tiap subproyek terhadap 7 subproyek lain (rata-rata |z| fitur)
    mu = d.groupby(GRUP)[FITUR].mean()
    sd = d[FITUR].std()
    jarak = {s: (np.abs(mu.loc[s] - mu.drop(s).mean()) / sd).mean() for s in mu.index}
    prof['Jarak_Profil_Fitur'] = prof[GRUP].map(jarak)
    return prof


# ---------------------------------------------------------------- E5 (post-hoc)
FITUR_RELATIF = ['SPI_Jadwal', 'Sisa_Waktu_Relatif', 'Backlog_Sisa_Persen', 'Utilisasi_Resource',
                 'Risiko_Belum_Dimitigasi', 'Frekuensi_CR', 'Pergeseran_Dependency_Relatif']


def _lip_gb(X, y, latih, uji):
    m = ep.buat_model('Gradient Boosting').fit(X[latih], y[latih])
    return uji, m.predict_proba(X[uji])[:, 1]


def e5_fitur_relatif(p, d, n_jobs):
    d = d.copy()
    d['Sisa_Waktu_Relatif'] = d['Sisa_Waktu_Hari'] / d['T_Rencana']
    d['Pergeseran_Dependency_Relatif'] = d['Pergeseran_Dependency_Hari'] / d['T_Rencana']
    X, y, g = d[FITUR_RELATIF].to_numpy(), d[LABEL].to_numpy(), d[GRUP].to_numpy()
    q = np.full(len(y), np.nan)
    for uji, pr in Parallel(n_jobs=n_jobs)(delayed(_lip_gb)(X, y, tr, te) for tr, te in ep.pembagian_luar(g)):
        q[uji] = pr
    q0 = p[an.kolom('Gradient Boosting', 'Raw')].to_numpy()
    naif = p[an.kolom(NAIF, 'Raw')].to_numpy()
    baris = []
    for sub in ['Semua'] + sorted(np.unique(g)):
        m = np.ones(len(y), bool) if sub == 'Semua' else g == sub
        bn = np.mean((naif[m] - y[m]) ** 2)
        for nama, qq in [('Fitur asli (hasil utama)', q0), ('Fitur relatif (post-hoc)', q)]:
            bs = np.mean((qq[m] - y[m]) ** 2)
            baris.append({GRUP: sub, 'Varian': nama, 'Prevalensi': y[m].mean(), 'Rata2_Prediksi': qq[m].mean(),
                          'Brier': bs, 'BSS': 1 - bs / bn, 'ECE': ep.ece(y[m], qq[m]),
                          'ROC_AUC': ep.roc_auc_score(y[m], qq[m]) if 0 < y[m].sum() < m.sum() else np.nan})
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- E6
def spearman(a, b):
    ra, rb = pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy()
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def e6_korelasi(d):
    baris = []
    for fit in ['Risiko_Belum_Dimitigasi', 'Frekuensi_CR', 'Pergeseran_Dependency_Hari', 'Utilisasi_Resource', 'SPI_Jadwal']:
        for t in ['Semua'] + list(an.TITIK_LIST):
            s = d if t == 'Semua' else d[d[TITIK] == t]
            dalam_label = [spearman(x[fit], x[LABEL]) for _, x in s.groupby(GRUP)]
            dalam_spi = [spearman(x[fit], x['SPI_Jadwal']) for _, x in s.groupby(GRUP)]
            baris.append({'Fitur': fit, TITIK: t, 'Rho_Label_Gabungan': spearman(s[fit], s[LABEL]),
                          'Rho_Label_Median_Dalam_Subproyek': np.nanmedian(dalam_label),
                          'Rho_SPI_Gabungan': spearman(s[fit], s['SPI_Jadwal']),
                          'Rho_SPI_Median_Dalam_Subproyek': np.nanmedian(dalam_spi)})
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- E7
def e7_contoh(p, d, theta):
    q = p.pivot_table(index=[GRUP, 'Iterasi'], columns=TITIK, values=an.kolom('Gradient Boosting', 'Raw'))[an.TITIK_LIST]
    y = p.groupby([GRUP, 'Iterasi'])[LABEL].first().reindex(q.index)
    telat = d.groupby([GRUP, 'Iterasi'])['Keterlambatan_Akhir_Hari'].first().reindex(q.index)
    T = d.groupby([GRUP, 'Iterasi'])['T_Rencana'].first().reindex(q.index)
    # (a) telat, sudah merah sejak 25%, probabilitas naik; ambil yang probabilitas 25%-nya paling dekat median kelompok itu
    a = q[(y == 1) & (q[0.25] >= ZONA[1]) & (q[0.75] >= q[0.25])]
    pa = a.iloc[(a[0.25] - a[0.25].median()).abs().argsort().iloc[:1]]
    # (b) tepat waktu tetapi pernah ≥ θ* (peringatan palsu); ambil yang maksimumnya paling dekat median kelompok itu
    b = q[(y == 0) & (q.max(axis=1) >= theta)]
    pb = b.iloc[(b.max(axis=1) - b.max(axis=1).median()).abs().argsort().iloc[:1]]
    baris = []
    for jenis, x in [('Telat, terdeteksi dini', pa), ('Tepat waktu, peringatan palsu', pb)]:
        idx = x.index[0]
        r = {'Jenis': jenis, GRUP: idx[0], 'Iterasi': idx[1], 'T_Rencana': T[idx],
             'Keterlambatan_Akhir_Hari': telat[idx], 'Telat_Persen': telat[idx] / T[idx]}
        for t in an.TITIK_LIST:
            r[f'P_{int(t * 100)}'] = x.loc[idx, t]
            r[f'Zona_{int(t * 100)}'] = ep.zona(np.array([x.loc[idx, t]]))[0]
        fit = d[(d[GRUP] == idx[0]) & (d['Iterasi'] == idx[1])].sort_values(TITIK)
        for t, (_, fr) in zip(an.TITIK_LIST, fit.iterrows()):
            r[f'SPI_{int(t * 100)}'] = fr['SPI_Jadwal']
        baris.append(r)
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- E8
def e8_alarm_palsu(p, d, theta):
    q = p.pivot_table(index=[GRUP, 'Iterasi'], columns=TITIK, values=an.kolom('Gradient Boosting', 'Raw'))[an.TITIK_LIST]
    y = p.groupby([GRUP, 'Iterasi'])[LABEL].first().reindex(q.index)
    tp = (d.groupby([GRUP, 'Iterasi'])['Keterlambatan_Akhir_Hari'].first() /
          d.groupby([GRUP, 'Iterasi'])['T_Rencana'].first()).reindex(q.index)
    baris = []
    for a, ket in an.ambang_khusus(theta):
        alarm = q.max(axis=1) >= a
        for nama, m in [('Tepat waktu, pernah diperingatkan', (y == 0) & alarm), ('Tepat waktu, tidak pernah diperingatkan', (y == 0) & ~alarm)]:
            baris.append({'Ambang': a, 'Keterangan': ket, 'Kelompok': nama, 'N_Iterasi': int(m.sum()),
                          'Median_Telat_Persen': tp[m].median(), 'Persen_Telat_di_atas_3pct': (tp[m] > 0.03).mean()})
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- RINGKASAN
def tulis(path, e1, e2r, e3, e4, e5, e6, e7, e8):
    L = ['# Bukti untuk Pembahasan (Pertemuan 7)\n',
         '> Digenerate otomatis oleh `bukti_pembahasan.py`. Hasil utama Pertemuan 5–6 tidak berubah; E5 adalah analisis '
         '**post-hoc**.\n', '## E1. Prediksi ekstrem (≤ 0,01 atau ≥ 0,99), keluaran mentah\n',
         '| Model | Porsi prediksi ekstrem | Porsi ekstrem yang salah arah | Sumbangan ke Log Loss |', '| :--- | ---: | ---: | ---: |']
    L += [f'| {r.Model} | {pct(r.Persen_Prediksi_Ekstrem)} | {pct(r.Persen_Ekstrem_yang_Salah)} | {f(r.Log_Loss_Kontribusi_Ekstrem_Salah)} |'
          for _, r in e1.iterrows()]
    L += ['', '## E2. Transfer kalibrasi Platt (rata-rata 8 subproyek uji)\n',
          '| Model | ECE Raw | ECE Platt dari 7 subproyek lain | ECE Platt oracle (subproyek sendiri) | Brier Raw | Brier Platt lain | Brier Platt oracle |',
          '| :--- | ---: | ---: | ---: | ---: | ---: | ---: |']
    L += [f'| {r.Model} | {f(r.ECE_Raw)} | {f(r.ECE_Platt_Subproyek_Lain)} | {f(r.ECE_Platt_Oracle)} | {f(r.Brier_Raw)} | '
          f'{f(r.Brier_Platt_Subproyek_Lain)} | {f(r.Brier_Platt_Oracle)} |' for _, r in e2r.iterrows()]
    L += ['', 'Oracle = kalibrator dilatih dan diuji pada subproyek yang sama (batas atas, tidak mungkin dilakukan sebelum proyek berjalan).',
          '', '## E3. Calibration slope Logistic Regression: data latih vs subproyek uji\n',
          '| Subproyek uji | Slope latih | Slope uji | Intercept latih | Intercept uji |', '| :--- | ---: | ---: | ---: | ---: |']
    L += [f'| {r[GRUP]} | {f(r.Slope_Latih, 3)} | {f(r.Slope_Uji, 3)} | {f(r.Intercept_Latih, 3)} | {f(r.Intercept_Uji, 3)} |'
          for _, r in e3.iterrows()]
    L += ['', '## E4. Profil subproyek\n',
          '| Subproyek | T (hari) | Ambang 5% (hari) | Rata-rata telat (hari) | Prevalensi | Rata-rata prediksi GB | Selisih | BSS GB | Utilisasi | Jarak profil fitur |',
          '| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    L += [f'| {r[GRUP]} | {f(r.T_Rencana, 0)} | {f(r.Ambang_Telat_5pct_Hari, 1)} | {f(r.Rata2_Keterlambatan_Hari, 1)} | '
          f'{pct(r.Prevalensi)} | {pct(r.Rata2_Prediksi_Model)} | {f(r.Selisih_Prediksi_Prevalensi, 3)} | {f(r.BSS, 3)} | '
          f'{f(r.Utilisasi, 3)} | {f(r.Jarak_Profil_Fitur, 2)} |' for _, r in e4.iterrows()]
    L += ['', '## E5. Post-hoc: GB dengan fitur relatif terhadap T\n',
          'Sisa_Waktu_Hari → Sisa_Waktu_Hari / T; Pergeseran_Dependency_Hari → Pergeseran_Dependency_Hari / T; fitur lain tetap.\n',
          '| Subproyek | Varian | Prevalensi | Rata-rata prediksi | Brier | BSS | ECE | ROC-AUC |',
          '| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |']
    L += [f'| {r[GRUP]} | {r.Varian} | {pct(r.Prevalensi)} | {pct(r.Rata2_Prediksi)} | {f(r.Brier)} | {f(r.BSS, 3)} | '
          f'{f(r.ECE)} | {f(r.ROC_AUC, 3)} |' for _, r in e5.iterrows()]
    L += ['', '## E6. Korelasi Spearman\n',
          '| Fitur | Titik | ρ dengan label (gabungan) | ρ dengan label (median dalam subproyek) | ρ dengan SPI (gabungan) | ρ dengan SPI (median dalam subproyek) |',
          '| :--- | :--- | ---: | ---: | ---: | ---: |']
    L += [f'| {r.Fitur} | {r[TITIK] if r[TITIK] == "Semua" else pct(float(r[TITIK]), 0)} | {f(r.Rho_Label_Gabungan, 3)} | '
          f'{f(r.Rho_Label_Median_Dalam_Subproyek, 3)} | {f(r.Rho_SPI_Gabungan, 3)} | {f(r.Rho_SPI_Median_Dalam_Subproyek, 3)} |'
          for _, r in e6.iterrows()]
    L += ['', '## E7. Contoh kasus (GB + Raw)\n',
          '| Jenis | Subproyek | Iterasi | Telat akhir | P 25% | P 50% | P 75% | Zona 25/50/75 | SPI 25/50/75 |',
          '| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :--- | :--- |']
    L += [f'| {r.Jenis} | {r[GRUP]} | {r.Iterasi} | {f(r.Keterlambatan_Akhir_Hari, 1)} hari ({pct(r.Telat_Persen)}) | '
          f'{f(r.P_25, 3)} | {f(r.P_50, 3)} | {f(r.P_75, 3)} | {r.Zona_25}/{r.Zona_50}/{r.Zona_75} | '
          f'{f(r.SPI_25, 3)}/{f(r.SPI_50, 3)}/{f(r.SPI_75, 3)} |' for _, r in e7.iterrows()]
    L += ['', '## E8. Peringatan palsu: seberapa dekat proyek tepat waktu dengan ambang 5%\n',
          '| Ambang | Kelompok | Jumlah iterasi | Median keterlambatan akhir (% T) | Porsi telat > 3% |', '| :--- | :--- | ---: | ---: | ---: |']
    L += [f'| {r.Keterangan} ({f(r.Ambang, 3)}) | {r.Kelompok} | {r.N_Iterasi} | {pct(r.Median_Telat_Persen)} | {pct(r.Persen_Telat_di_atas_3pct)} |'
          for _, r in e8.iterrows()]
    Path(path).write_text('\n'.join(L) + '\n', encoding='utf-8')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluaran', default=str(KELUARAN))
    ap.add_argument('--n-jobs', type=int, default=-1)
    a = ap.parse_args(argv)
    out = Path(a.keluaran)
    out.mkdir(parents=True, exist_ok=True)
    p, d = muat()
    theta = ep.ambang_youden(p[LABEL].to_numpy(), p[an.kolom('Gradient Boosting', 'Raw')].to_numpy())[0]
    e1 = e1_ekstrem(p)
    e2, e2r = e2_transfer_kalibrasi(p)
    e3 = e3_slope_lr(d, a.n_jobs)
    e4 = e4_profil(p, d)
    e5 = e5_fitur_relatif(p, d, a.n_jobs)
    e6 = e6_korelasi(d)
    e7 = e7_contoh(p, d, theta)
    e8 = e8_alarm_palsu(p, d, theta)
    for nama, t in [('e1_prediksi_ekstrem', e1), ('e2_transfer_kalibrasi', e2), ('e2_transfer_kalibrasi_ringkas', e2r),
                    ('e3_slope_lr_latih_uji', e3), ('e4_profil_subproyek', e4), ('e5_posthoc_fitur_relatif', e5),
                    ('e6_korelasi_variabel', e6), ('e7_contoh_kasus', e7), ('e8_alarm_palsu', e8)]:
        t.round(6).to_csv(out / f'{nama}.csv', index=False)
    tulis(out / '00_RINGKASAN_BUKTI.md', e1, e2r, e3, e4, e5, e6, e7, e8)
    print('Selesai:', out)


if __name__ == '__main__':
    main()
