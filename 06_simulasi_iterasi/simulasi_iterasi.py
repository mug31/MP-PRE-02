"""
PRE-02: Simulasi Iterasi Random Keterlambatan Proyek — 8 Sub-Proyek Super ERP FNE
(sesuai arahan dosen pada bimbingan 7 Oktober 2026, lihat catatan_dosen/revisi_7okt.md).

Alur per subproyek:
  1. Jadwal aktivitas & resource dari PMP          -> data/P-FNE-0X_*.csv (dibuat ekstraksi_pmp.py)
  2. Penjadwalan dengan batasan resource (antrian FCFS / SPT, dependensi wajib dipatuhi)
  3. Change request (CR) disimulasikan dengan bilangan random per aktivitas
  4. Diulang N_ITERASI kali, lalu dihitung probabilitas & sebaran keterlambatan

Aturan waktu (hari kerja, dosen [25:01–25:28], [37:06–37:31]):
  - aktivitas pertama mulai hari ke-1
  - arrival (siap) = selesai predecessor terakhir + 1
  - selesai = mulai + durasi - 1   (durasi 5 hari menempati hari 1..5)
  - mulai = hari pertama ketika aktivitas siap DAN semua orang yang dibutuhkan kosong

Keluaran: hasil/ (per subproyek + ringkasan semua) dan excel/P-FNE-0X.xlsx.
Kebutuhan: pip install openpyxl matplotlib
Jalankan:  python simulasi_iterasi.py            (semua subproyek)
           python simulasi_iterasi.py 01 07      (subproyek tertentu)
"""

import csv
import math
import random
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / 'data'
OUT = HERE / 'hasil'
EXCEL = HERE / 'excel'
SUBPROYEK = ['01', '02', '03', '04', '05', '06', '07', '08']

# ============================================================
# 1. PARAMETER SIMULASI (keputusan kelompok — wajib dijustifikasi di Bab III)
# ============================================================

N_ITERASI = 1000
SEED = 42
P_CR = 0.10  # peluang tiap aktivitas terkena change request (contoh dosen [50:35])

# Kelas kesulitan CR: (nama, peluang kelas, (tambahan minimum, tambahan maksimum)) sebagai fraksi durasi rencana.
# Kelas dipilih secara acak, lalu besar tambahan diacak seragam di dalam rentangnya.
SKENARIO_CR = {
    # Contoh angka dosen [52:04–53:21]: rendah 10–20%, sedang 30%, tinggi 50%.
    'dosen': [('rendah', 0.6, (0.10, 0.20)), ('sedang', 0.3, (0.30, 0.30)), ('tinggi', 0.1, (0.50, 0.50))],
    # Kelas impact Change Control PMP-01 §2.5.1: kecil <= 5%, sedang <= 20%, besar > 20% (batas atas 50% asumsi).
    'pmp': [('kecil', 0.6, (0.00, 0.05)), ('sedang', 0.3, (0.05, 0.20)), ('besar', 0.1, (0.20, 0.50))],
}
SKENARIO_UTAMA = 'dosen'
KEBIJAKAN = ['FCFS', 'SPT']  # dosen [46:44–47:04]
PRIORITAS_RANK = {'Must': 1, 'Should': 2, 'Could': 3, '-': 9}
BATAS_TELAT_HARI = 5  # pelengkap P(telat > 0): keterlambatan yang dianggap berarti


# ============================================================
# 2. DATA
# ============================================================

def baca_aktivitas(kode):
    with open(DATA / f'P-FNE-{kode}_aktivitas.csv', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r['Durasi_Hari'] = int(r['Durasi_Hari'])
        r['Pred'] = [p for p in r['Predecessor'].split(';') if p]
        r['Butuh'] = {}
        for item in filter(None, r['Kebutuhan_Resource'].split(';')):
            role, n = item.rsplit(':', 1)
            r['Butuh'][role] = int(n)
    ids = {r['ID'] for r in rows}
    for r in rows:
        missing = [p for p in r['Pred'] if p not in ids]
        assert not missing, f"P-FNE-{kode} {r['ID']}: predecessor tidak dikenal {missing}"
    return rows


def baca_resource(kode):
    with open(DATA / f'P-FNE-{kode}_resource.csv', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r['Hari_Mulai'] = int(r['Hari_Mulai'])
        # kosong = tersedia sampai proyek selesai
        r['Hari_Selesai'] = int(r['Hari_Selesai']) if r['Hari_Selesai'] else math.inf
    return rows


# ============================================================
# 3. PENJADWALAN
# ============================================================

def jadwal_tanpa_resource(aktivitas, durasi):
    """Jadwal rencana murni dari dependensi (rumus Excel dosen), tanpa batasan orang."""
    selesai, hasil = {}, {}
    while len(selesai) < len(aktivitas):  # urutan CSV belum tentu topologis
        maju = False
        for a in aktivitas:
            if a['ID'] in selesai or not all(p in selesai for p in a['Pred']):
                continue
            mulai = max((selesai[p] for p in a['Pred']), default=0) + 1
            selesai[a['ID']] = mulai + durasi[a['ID']] - 1
            hasil[a['ID']] = {'mulai': mulai, 'selesai': selesai[a['ID']]}
            maju = True
        if not maju:
            raise RuntimeError('Dependensi melingkar')
    return hasil


def jadwal_dengan_resource(aktivitas, durasi, orang, kebijakan):
    """
    Simulasi antrian resource. Pada setiap hari t, aktivitas yang sudah siap diurutkan menurut kebijakan
    antrian (FCFS: siap paling awal dulu; SPT: durasi paling pendek dulu; seri: prioritas lalu ID).
    Aktivitas dimulai jika SEMUA orang yang dibutuhkan (per role) kosong dan berada dalam jendela
    ketersediaannya; jika tidak, aktivitas berikutnya di antrian boleh mulai bila resource-nya ada.
    """
    by_id = {a['ID']: a for a in aktivitas}
    kosong_mulai = {o['Orang']: o['Hari_Mulai'] for o in orang}
    per_role = {}
    for o in orang:
        per_role.setdefault(o['Role'], []).append(o)
    selesai, hasil = {}, {}
    belum = set(by_id)
    t = 1
    while belum:
        siap = {}
        for i in belum:
            pred = by_id[i]['Pred']
            if all(p in selesai for p in pred):
                siap[i] = max((selesai[p] for p in pred), default=0) + 1

        def kunci(i):
            prio = PRIORITAS_RANK[by_id[i]['Prioritas']]
            if kebijakan == 'SPT':
                return (durasi[i], siap[i], prio, i)
            return (siap[i], prio, i)

        for i in sorted((i for i in siap if siap[i] <= t), key=kunci):
            pilih = []
            for role, n in by_id[i]['Butuh'].items():
                bebas = [o['Orang'] for o in per_role[role]
                         if kosong_mulai[o['Orang']] <= t and o['Hari_Mulai'] <= t <= o['Hari_Selesai']]
                if len(bebas) < n:
                    pilih = None
                    break
                pilih += bebas[:n]
            if pilih is None:
                continue
            akhir = t + durasi[i] - 1
            hasil[i] = {'siap': siap[i], 'mulai': t, 'selesai': akhir, 'orang': pilih, 'tunggu': t - siap[i]}
            selesai[i] = akhir
            for nama in pilih:
                kosong_mulai[nama] = akhir + 1
            belum.discard(i)

        # lompat ke kejadian berikutnya: orang kosong, aktivitas siap, atau orang mulai bergabung
        kejadian = [h for h in kosong_mulai.values() if h > t]
        kejadian += [s for i, s in siap.items() if i in belum and s > t]
        kejadian += [o['Hari_Mulai'] for o in orang if o['Hari_Mulai'] > t]
        if belum:
            t = min(kejadian) if kejadian else t + 1
            if t > 20_000:
                raise RuntimeError(f'Penjadwalan macet; sisa aktivitas: {sorted(belum)[:10]}')
    return hasil


def _pemicu(i, jadwal, by_id, pakai_orang):
    """Aktivitas yang menentukan hari mulai i: rekan resource (jika menunggu) atau predecessor."""
    j = jadwal[i]
    if j['tunggu'] > 0:
        orang = set(j['orang'])
        return [k for k in pakai_orang
                if jadwal[k]['selesai'] == j['mulai'] - 1 and orang & set(jadwal[k]['orang'])]
    return [p for p in by_id[i]['Pred'] if jadwal[p]['selesai'] == j['siap'] - 1]


def rantai_penentu(aktivitas, jadwal):
    """Satu rantai mundur dari aktivitas yang selesai paling akhir sampai awal proyek."""
    by_id = {a['ID']: a for a in aktivitas}
    i = max(jadwal, key=lambda k: (jadwal[k]['selesai'], k))
    rantai = []
    while i:
        rantai.append(i)
        pemicu = _pemicu(i, jadwal, by_id, jadwal)
        i = max(pemicu, key=lambda k: (jadwal[k]['selesai'], k)) if pemicu else None
    return rantai


def himpunan_kritis(aktivitas, jadwal):
    """Seperti rantai_penentu, tetapi semua cabang yang seri ikut dihitung (untuk indeks kekritisan)."""
    by_id = {a['ID']: a for a in aktivitas}
    akhir = max(j['selesai'] for j in jadwal.values())
    antre = [i for i, j in jadwal.items() if j['selesai'] == akhir]
    kritis = set()
    while antre:
        i = antre.pop()
        if i not in kritis:
            kritis.add(i)
            antre += _pemicu(i, jadwal, by_id, jadwal)
    return kritis


# ============================================================
# 4. SIMULASI CHANGE REQUEST & ITERASI
# ============================================================

def tarik_cr(kelas_cr, r_cr, r_kelas, r_besar):
    """Satu aktivitas: kena CR? kelas apa? tambahan berapa fraksi?"""
    if r_cr >= P_CR:
        return None, 0.0
    batas = 0.0
    for nama, peluang, (lo, hi) in kelas_cr:
        batas += peluang
        if r_kelas < batas:
            return nama, lo + r_besar * (hi - lo)
    nama, _, (lo, hi) = kelas_cr[-1]
    return nama, lo + r_besar * (hi - lo)


def jalankan(kode):
    aktivitas = baca_aktivitas(kode)
    orang = baca_resource(kode)
    ids = [a['ID'] for a in aktivitas]
    durasi_rencana = {a['ID']: a['Durasi_Hari'] for a in aktivitas}

    rencana = {k: jadwal_dengan_resource(aktivitas, durasi_rencana, orang, k) for k in KEBIJAKAN}
    rencana_cpm = jadwal_tanpa_resource(aktivitas, durasi_rencana)
    selesai_rencana = {k: max(j['selesai'] for j in rencana[k].values()) for k in KEBIJAKAN}

    rng = random.Random(f'{SEED}-{kode}')
    baris_iterasi = []
    agregat = {}  # (skenario, kebijakan, id) -> daftar nilai
    for it in range(1, N_ITERASI + 1):
        # bilangan random yang sama dipakai di semua skenario & kebijakan (perbandingan adil)
        undian = {i: (rng.random(), rng.random(), rng.random()) for i in ids}
        for skenario, kelas_cr in SKENARIO_CR.items():
            cr = {i: tarik_cr(kelas_cr, *undian[i]) for i in ids}
            # Tambahan durasi TIDAK dibulatkan ke hari utuh: pembulatan ke atas membuat CR "+10%" pada aktivitas
            # 1 hari menjadi +100%, sehingga PMP yang rinciannya halus (banyak aktivitas 1–2 hari) dirugikan.
            tambahan = {i: round(durasi_rencana[i] * cr[i][1], 4) for i in ids}
            durasi = {i: durasi_rencana[i] + tambahan[i] for i in ids}
            for k in KEBIJAKAN:
                jadwal = jadwal_dengan_resource(aktivitas, durasi, orang, k)
                selesai = max(j['selesai'] for j in jadwal.values())
                rantai = rantai_penentu(aktivitas, jadwal)
                kritis = himpunan_kritis(aktivitas, jadwal)
                keterlambatan = round(selesai - selesai_rencana[k], 4)
                baris_iterasi.append({
                    'Subproyek': f'P-FNE-{kode}', 'Skenario_CR': skenario, 'Kebijakan': k, 'Iterasi': it,
                    'Selesai_Rencana': selesai_rencana[k], 'Selesai_Simulasi': round(selesai, 4),
                    'Keterlambatan_Hari': keterlambatan, 'Telat': int(keterlambatan > 0),
                    'Jumlah_CR': sum(1 for i in ids if cr[i][0]),
                    'Tambahan_CR_Total_Hari': round(sum(tambahan.values()), 4),
                    'Tambahan_CR_di_Rantai_Penentu': round(sum(tambahan[i] for i in rantai), 4),
                    'Tunggu_Resource_di_Rantai_Penentu': round(sum(jadwal[i]['tunggu'] for i in rantai), 4),
                    'Rantai_Penentu': '>'.join(reversed(rantai)),
                })
                p = rencana[k]
                for i in ids:
                    s = jadwal[i]
                    agregat.setdefault((skenario, k, i), []).append((
                        1 if cr[i][0] else 0,
                        tambahan[i],
                        s['mulai'] - p[i]['mulai'],
                        s['siap'] - p[i]['siap'],
                        s['tunggu'] - p[i]['tunggu'],
                        1 if i in kritis else 0,
                        1 if s['selesai'] > p[i]['selesai'] else 0,
                    ))
    return aktivitas, orang, rencana, rencana_cpm, selesai_rencana, baris_iterasi, agregat


# ============================================================
# 5. RINGKASAN & EKSPOR
# ============================================================

def persentil(nilai, q):
    s = sorted(nilai)
    pos = (len(s) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def ringkas(kode, aktivitas, rencana, rencana_cpm, baris_iterasi, selesai_rencana):
    hasil = []
    cpm = max(j['selesai'] for j in rencana_cpm.values())
    tunggu_rencana = {k: sum(rencana[k][i]['tunggu'] for i in rantai_penentu(aktivitas, rencana[k])) for k in KEBIJAKAN}
    for skenario in SKENARIO_CR:
        for k in KEBIJAKAN:
            b = [r for r in baris_iterasi if r['Skenario_CR'] == skenario and r['Kebijakan'] == k]
            d = [r['Keterlambatan_Hari'] for r in b]
            n = len(b)
            p_telat = sum(r['Telat'] for r in b) / n
            hasil.append({
                'Subproyek': f'P-FNE-{kode}', 'Skenario_CR': skenario, 'Kebijakan': k, 'N_Iterasi': n,
                'Jumlah_Aktivitas': len(aktivitas),
                'Selesai_Tanpa_Resource_Hari': cpm,
                'Selesai_Rencana_Hari': selesai_rencana[k],
                'P_Telat': round(p_telat, 4),
                'SE_P_Telat': round(math.sqrt(p_telat * (1 - p_telat) / n), 4),
                f'P_Telat_lebih_{BATAS_TELAT_HARI}_Hari': round(sum(1 for x in d if x > BATAS_TELAT_HARI) / n, 4),
                'P_Telat_lebih_10_Persen': round(sum(1 for x in d if x > 0.1 * selesai_rencana[k]) / n, 4),
                'Rata2_Keterlambatan_Hari': round(statistics.mean(d), 2),
                'SD_Keterlambatan_Hari': round(statistics.stdev(d), 2),
                'P50_Hari': round(persentil(d, 0.5), 2), 'P80_Hari': round(persentil(d, 0.8), 2),
                'P90_Hari': round(persentil(d, 0.9), 2), 'Maks_Hari': round(max(d), 2),
                'Rata2_Jumlah_CR': round(statistics.mean(r['Jumlah_CR'] for r in b), 2),
                'Rata2_Tambahan_CR_di_Rantai_Hari': round(statistics.mean(r['Tambahan_CR_di_Rantai_Penentu'] for r in b), 2),
                'Tunggu_Resource_di_Rantai_Rencana_Hari': tunggu_rencana[k],
                'Rata2_Tunggu_Resource_di_Rantai_Hari': round(statistics.mean(r['Tunggu_Resource_di_Rantai_Penentu'] for r in b), 2),
                'Iterasi_Lebih_Cepat_dari_Rencana': sum(1 for x in d if x < 0),
            })
    return hasil


def ringkas_per_aktivitas(kode, aktivitas, agregat):
    hasil = []
    for skenario in SKENARIO_CR:
        for k in KEBIJAKAN:
            for a in aktivitas:
                v = agregat[(skenario, k, a['ID'])]
                kolom = list(zip(*v))
                n = len(v)
                hasil.append({
                    'Subproyek': f'P-FNE-{kode}', 'Skenario_CR': skenario, 'Kebijakan': k, 'ID': a['ID'],
                    'Aktivitas': a['Aktivitas'], 'Kebutuhan_Resource': a['Kebutuhan_Resource'],
                    'P_Kena_CR': round(sum(kolom[0]) / n, 4),
                    'Rata2_Delay_Sendiri_CR_Hari': round(sum(kolom[1]) / n, 3),
                    'Rata2_Pergeseran_Mulai_Hari': round(sum(kolom[2]) / n, 3),
                    'dari_Predecessor_Hari': round(sum(kolom[3]) / n, 3),
                    'dari_Antrian_Resource_Hari': round(sum(kolom[4]) / n, 3),
                    'Indeks_Kekritisan': round(sum(kolom[5]) / n, 4),
                    'P_Selesai_Lewat_Rencana': round(sum(kolom[6]) / n, 4),
                })
    return hasil


def tulis_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def tulis_jadwal_rencana(path, aktivitas, rencana, rencana_cpm):
    rows = []
    for a in aktivitas:
        i = a['ID']
        r = {'ID': i, 'Aktivitas': a['Aktivitas'], 'Kebutuhan_Resource': a['Kebutuhan_Resource'],
             'Durasi_Hari': a['Durasi_Hari'], 'Predecessor': a['Predecessor'],
             'Mulai_TanpaResource': rencana_cpm[i]['mulai'], 'Selesai_TanpaResource': rencana_cpm[i]['selesai']}
        for k in KEBIJAKAN:
            j = rencana[k][i]
            r.update({f'Orang_{k}': ';'.join(j['orang']), f'Siap_{k}': j['siap'], f'Mulai_{k}': j['mulai'],
                      f'Selesai_{k}': j['selesai'], f'Tunggu_{k}': j['tunggu']})
        rows.append(r)
    tulis_csv(path, rows)


# --- grafik ---------------------------------------------------------------

BIRU, TEKS, TEKS2, GRID, LATAR = '#2a78d6', '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'


def _gaya(ax):
    ax.set_facecolor(LATAR)
    ax.grid(axis='y', color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for sisi in ('top', 'right'):
        ax.spines[sisi].set_visible(False)
    for sisi in ('left', 'bottom'):
        ax.spines[sisi].set_color(GRID)
    ax.tick_params(colors=TEKS2, labelsize=8)


def _histogram(ax, d, s, judul):
    bins = list(range(min(0, math.floor(min(d))), math.ceil(max(d)) + 2))  # lebar batang 1 hari
    ax.hist(d, bins=bins, color=BIRU, edgecolor=LATAR, linewidth=1 if len(bins) < 60 else 0)
    ax.axvline(s['P80_Hari'], color=TEKS2, linewidth=1, linestyle='--')
    ax.text(0.98, 0.95, f"P(telat) = {s['P_Telat']:.1%}\n"
                        f"P(telat > {BATAS_TELAT_HARI} hari) = {s[f'P_Telat_lebih_{BATAS_TELAT_HARI}_Hari']:.1%}\n"
                        f"rata-rata = {s['Rata2_Keterlambatan_Hari']} hari\nP80 = {s['P80_Hari']:g} hari (garis putus)",
            transform=ax.transAxes, ha='right', va='top', fontsize=8, color=TEKS)
    ax.set_title(judul, fontsize=10, color=TEKS, loc='left')
    _gaya(ax)


def gambar_histogram_subproyek(kode, baris_iterasi, ringkasan, path):
    fig, axes = plt.subplots(len(SKENARIO_CR), len(KEBIJAKAN), figsize=(10, 6.4), sharex=True, sharey=True)
    fig.patch.set_facecolor(LATAR)
    for bi, skenario in enumerate(SKENARIO_CR):
        for ki, k in enumerate(KEBIJAKAN):
            ax = axes[bi][ki]
            d = [r['Keterlambatan_Hari'] for r in baris_iterasi if r['Skenario_CR'] == skenario and r['Kebijakan'] == k]
            s = next(r for r in ringkasan if r['Skenario_CR'] == skenario and r['Kebijakan'] == k)
            _histogram(ax, d, s, f'CR {skenario} · antrian {k}')
            if bi == len(SKENARIO_CR) - 1:
                ax.set_xlabel('Keterlambatan terhadap jadwal rencana (hari kerja)', fontsize=9, color=TEKS2)
            if ki == 0:
                ax.set_ylabel('Jumlah iterasi', fontsize=9, color=TEKS2)
    fig.suptitle(f'Sebaran keterlambatan P-FNE-{kode} ({N_ITERASI} iterasi per panel)', x=0.01, ha='left',
                 fontsize=12, color=TEKS)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=LATAR)
    plt.close(fig)


def gambar_histogram_semua(semua_iterasi, semua_ringkasan, path):
    fig, axes = plt.subplots(2, 4, figsize=(15, 6.6))
    fig.patch.set_facecolor(LATAR)
    for n, kode in enumerate(SUBPROYEK):
        ax = axes[n // 4][n % 4]
        sp = f'P-FNE-{kode}'
        d = [r['Keterlambatan_Hari'] for r in semua_iterasi
             if r['Subproyek'] == sp and r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS']
        if not d:
            ax.set_visible(False)
            continue
        s = next(r for r in semua_ringkasan
                 if r['Subproyek'] == sp and r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS')
        _histogram(ax, d, s, f"{sp} · {s['Jumlah_Aktivitas']} aktivitas")
        if n // 4 == 1:
            ax.set_xlabel('Keterlambatan (hari kerja)', fontsize=9, color=TEKS2)
        if n % 4 == 0:
            ax.set_ylabel('Jumlah iterasi', fontsize=9, color=TEKS2)
    fig.suptitle(f'Sebaran keterlambatan 8 subproyek — skenario CR {SKENARIO_UTAMA}, antrian FCFS '
                 f'({N_ITERASI} iterasi per panel; sumbu tiap panel berbeda)', x=0.01, ha='left', fontsize=12,
                 color=TEKS)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=LATAR)
    plt.close(fig)


# --- ringkasan markdown ----------------------------------------------------

def _tabel_hasil(ringkasan):
    kol = f'P_Telat_lebih_{BATAS_TELAT_HARI}_Hari'
    L = [f'| Subproyek | Skenario CR | Antrian | Aktivitas | Selesai rencana | P(telat) | P(telat > {BATAS_TELAT_HARI} hari) '
         '| P(telat > 10%) | Rata-rata | P80 | P90 | Maks |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in ringkasan:
        L.append(f"| {r['Subproyek']} | {r['Skenario_CR']} | {r['Kebijakan']} | {r['Jumlah_Aktivitas']} "
                 f"| {r['Selesai_Rencana_Hari']} | {r['P_Telat']:.1%} | {r[kol]:.1%} "
                 f"| {r['P_Telat_lebih_10_Persen']:.1%} | {r['Rata2_Keterlambatan_Hari']} "
                 f"| {r['P80_Hari']:g} | {r['P90_Hari']:g} | {r['Maks_Hari']} |")
    return L


def tulis_ringkasan_subproyek(path, kode, aktivitas, rencana, rencana_cpm, ringkasan, per_aktivitas):
    utama = next(r for r in ringkasan if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS')
    utama_akt = [r for r in per_aktivitas if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS']
    selalu = [r['ID'] for r in utama_akt if r['Indeks_Kekritisan'] == 1]
    kadang = sorted((r for r in utama_akt if 0 < r['Indeks_Kekritisan'] < 1), key=lambda r: -r['Indeks_Kekritisan'])[:10]
    cpm = max(j['selesai'] for j in rencana_cpm.values())
    L = [f'# Hasil Simulasi Iterasi Random — P-FNE-{kode}\n',
         '> Digenerate otomatis oleh `simulasi_iterasi.py`. Jangan diedit manual; jalankan ulang script.\n',
         '## Jadwal Rencana\n',
         f'- {len(aktivitas)} aktivitas (sumber: `data/P-FNE-{kode}_aktivitas.csv`).',
         f'- Tanpa batasan resource: selesai hari kerja ke-**{cpm}**.']
    for k in KEBIJAKAN:
        f = max(j['selesai'] for j in rencana[k].values())
        L.append(f'- Dengan batasan resource, antrian {k}: selesai hari kerja ke-**{f}**.')
    L += ['', '## Hasil\n'] + _tabel_hasil(ringkasan) + ['']
    L.append(f"## Aktivitas Paling Menentukan (skenario `{SKENARIO_UTAMA}`, FCFS)\n")
    L.append('Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal '
             'selesai (cabang paralel yang selesai bersamaan dihitung kritis semua).\n')
    L.append(f"- Selalu kritis (100% iterasi, {len(selalu)} aktivitas): {', '.join(selalu) or '-'}.")
    if kadang:
        L += ['- Kadang kritis:\n',
              '| ID | Aktivitas | Indeks kekritisan | Delay sendiri (CR) | Geser karena predecessor | Geser karena antrian resource |',
              '|---|---|---|---|---|---|']
        for r in kadang:
            L.append(f"| {r['ID']} | {r['Aktivitas']} | {r['Indeks_Kekritisan']:.0%} "
                     f"| {r['Rata2_Delay_Sendiri_CR_Hari']:.2f} | {r['dari_Predecessor_Hari']:.2f} "
                     f"| {r['dari_Antrian_Resource_Hari']:.2f} |")
    L += ['', f"## Penyebab Keterlambatan (skenario `{SKENARIO_UTAMA}`, FCFS)\n",
          f"- Rata-rata tambahan durasi CR di rantai penentu: **{utama['Rata2_Tambahan_CR_di_Rantai_Hari']} hari** per iterasi.",
          f"- Waktu menunggu resource di rantai penentu: **{utama['Tunggu_Resource_di_Rantai_Rencana_Hari']} hari** pada "
          f"jadwal rencana, rata-rata **{utama['Rata2_Tunggu_Resource_di_Rantai_Hari']} hari** per iterasi simulasi "
          "(antrean karena orang yang sama mengerjakan beberapa aktivitas).",
          f"- Rata-rata jumlah CR per iterasi: {utama['Rata2_Jumlah_CR']} dari {len(aktivitas)} aktivitas."]
    if all(r['Rata2_Tunggu_Resource_di_Rantai_Hari'] == 0 for r in ringkasan):
        L.append('- Batasan resource tidak pernah membuat aktivitas di rantai penentu menunggu, sehingga hasil FCFS '
                 'dan SPT sama; seluruh keterlambatan berasal dari CR beserta rambatannya.')
    negatif = [r for r in ringkasan if r['Iterasi_Lebih_Cepat_dari_Rencana'] > 0]
    if negatif:
        uraian = ', '.join(f"{r['Skenario_CR']}/{r['Kebijakan']} {r['Iterasi_Lebih_Cepat_dari_Rencana']} iterasi"
                           for r in negatif)
        L.append(f'- Ada iterasi yang selesai **lebih cepat** dari rencana ({uraian}). Ini bukan galat: pada '
                 'penjadwalan berbasis aturan antrian, memperpanjang satu aktivitas dapat mengubah urutan antrian '
                 'sehingga orang terpakai lebih efisien (anomali penjadwalan Graham). Artinya jadwal rencana dengan '
                 'aturan antrian ini belum optimal; ada ruang perbaikan lewat resource leveling.')
    path.write_text('\n'.join(L + ['']) + '\n', encoding='utf-8')


def tulis_ringkasan_semua(path, semua_ringkasan):
    L = ['# Ringkasan Hasil Simulasi Iterasi Random — 8 Subproyek Super ERP FNE\n',
         '> Digenerate otomatis oleh `simulasi_iterasi.py`. Jangan diedit manual; jalankan ulang script.\n',
         '## Parameter\n',
         f'- Iterasi: **{N_ITERASI}** per subproyek per skenario; seed `{SEED}-<kode>`; peluang CR per aktivitas: **{P_CR:g}**']
    for s, kelas in SKENARIO_CR.items():
        uraian = ', '.join(f'{n} {p:.0%} (+{lo:.0%}–{hi:.0%})' if lo != hi else f'{n} {p:.0%} (+{lo:.0%})'
                           for n, p, (lo, hi) in kelas)
        L.append(f'- Skenario CR `{s}`: {uraian}')
    L += ['- Kebijakan antrian: FCFS (siap duluan dikerjakan duluan) dan SPT (durasi terpendek duluan)', '',
          f'## Hasil Utama (skenario `{SKENARIO_UTAMA}`, FCFS)\n']
    L += _tabel_hasil([r for r in semua_ringkasan if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS'])
    L += ['', '**Perhatian:** jumlah aktivitas tiap subproyek berbeda (mengikuti tingkat detail tiap PMP), '
          'sehingga P(telat) antarsubproyek tidak bisa dibandingkan mentah-mentah: subproyek dengan lebih banyak '
          'aktivitas di rantai kritis lebih sering terkena CR. Untuk perbandingan, gunakan P(telat > 10%) dan '
          'sebaran keterlambatannya.', '',
          '## Semua Skenario\n'] + _tabel_hasil(semua_ringkasan)
    L += ['', '## Berkas\n',
          '- `ringkasan_semua.csv` — tabel di atas',
          '- `histogram_semua.png` — sebaran keterlambatan 8 subproyek',
          '- `P-FNE-0X/` — per subproyek: ringkasan, iterasi, per aktivitas, jadwal rencana, histogram']
    path.write_text('\n'.join(L) + '\n', encoding='utf-8')


def proses(kode):
    print(f'P-FNE-{kode}: simulasi {N_ITERASI} iterasi × {len(SKENARIO_CR)} skenario × {len(KEBIJAKAN)} antrian ...')
    aktivitas, orang, rencana, rencana_cpm, selesai_rencana, baris_iterasi, agregat = jalankan(kode)
    ringkasan = ringkas(kode, aktivitas, rencana, rencana_cpm, baris_iterasi, selesai_rencana)
    per_aktivitas = ringkas_per_aktivitas(kode, aktivitas, agregat)

    d = OUT / f'P-FNE-{kode}'
    d.mkdir(parents=True, exist_ok=True)
    tulis_jadwal_rencana(d / 'jadwal_rencana.csv', aktivitas, rencana, rencana_cpm)
    tulis_csv(d / 'iterasi.csv', baris_iterasi)
    tulis_csv(d / 'ringkasan.csv', ringkasan)
    tulis_csv(d / 'per_aktivitas.csv', per_aktivitas)
    gambar_histogram_subproyek(kode, baris_iterasi, ringkasan, d / 'histogram_keterlambatan.png')
    tulis_ringkasan_subproyek(d / '00_RINGKASAN.md', kode, aktivitas, rencana, rencana_cpm, ringkasan, per_aktivitas)

    from buat_excel import buat_workbook
    EXCEL.mkdir(exist_ok=True)
    buat_workbook(EXCEL / f'P-FNE-{kode}.xlsx', kode, aktivitas, orang, rencana, ringkasan,
                  [r for r in baris_iterasi if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS'],
                  SKENARIO_CR[SKENARIO_UTAMA], P_CR)
    for r in ringkasan:
        print(f"  {r['Skenario_CR']:6s} {r['Kebijakan']:4s} rencana hari {r['Selesai_Rencana_Hari']:4d}  "
              f"P(telat)={r['P_Telat']:.1%}  P(>{BATAS_TELAT_HARI}h)={r[f'P_Telat_lebih_{BATAS_TELAT_HARI}_Hari']:.1%}  "
              f"rata2={r['Rata2_Keterlambatan_Hari']} hari")
    return ringkasan, baris_iterasi


def main():
    pilihan = sys.argv[1:] or SUBPROYEK
    semua_ringkasan, semua_iterasi = [], []
    for kode in pilihan:
        r, it = proses(kode)
        semua_ringkasan += r
        semua_iterasi += it
    if pilihan == SUBPROYEK:
        tulis_csv(OUT / 'ringkasan_semua.csv', semua_ringkasan)
        gambar_histogram_semua(semua_iterasi, semua_ringkasan, OUT / 'histogram_semua.png')
        tulis_ringkasan_semua(OUT / '00_RINGKASAN_SEMUA.md', semua_ringkasan)
    print(f'Selesai. Luaran di {OUT} dan {EXCEL}')


if __name__ == '__main__':
    main()
