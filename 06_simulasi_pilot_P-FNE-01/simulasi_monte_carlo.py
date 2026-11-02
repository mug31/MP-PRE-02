"""
PRE-02: Simulasi Monte Carlo Keterlambatan Proyek — Pilot Sub-Proyek P-FNE-01
(Foundation & Core Platform), sesuai arahan dosen pada bimbingan 7 Oktober 2026.

Alur (lihat catatan_dosen/revisi_7okt.md):
  1. Jadwal aktivitas rencana dari PMP-01 §4.2.1  -> data/jadwal_aktivitas_P-FNE-01.csv
  2. Resource per orang dari PMP-01 §4.6.1        -> data/resource_P-FNE-01.csv
  3. Penjadwalan per resource (antrian FCFS / SPT, dependensi wajib dipatuhi)
  4. Change request (CR) disimulasikan dengan bilangan random per aktivitas
  5. Diulang N_ITERASI kali, lalu dihitung probabilitas & sebaran keterlambatan

Aturan waktu (hari kerja, dosen [25:01–25:28], [37:06–37:31]):
  - aktivitas pertama mulai hari ke-1
  - arrival (siap) = selesai predecessor terakhir + 1
  - selesai = mulai + durasi - 1   (durasi 5 hari menempati hari 1..5)
  - mulai = hari pertama ketika aktivitas siap DAN ada orang dengan role-nya yang kosong

Keluaran: folder hasil/ (CSV, PNG, ringkasan Markdown) dan pilot_P-FNE-01.xlsx.
Kebutuhan: pip install openpyxl matplotlib
"""

import csv
import math
import random
import statistics
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / 'data'
OUT = HERE / 'hasil'

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
PRIORITAS_RANK = {'Must': 1, 'Should': 2, 'Could': 3}


# ============================================================
# 2. DATA
# ============================================================

def baca_aktivitas():
    with open(DATA / 'jadwal_aktivitas_P-FNE-01.csv', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r['Durasi_Hari'] = int(r['Durasi_Hari'])
        r['Pred'] = [p for p in r['Predecessor'].split(';') if p]
    ids = {r['ID'] for r in rows}
    for r in rows:
        missing = [p for p in r['Pred'] if p not in ids]
        assert not missing, f"{r['ID']}: predecessor tidak dikenal {missing}"
    return rows


def baca_resource():
    with open(DATA / 'resource_P-FNE-01.csv', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r['Hari_Mulai'] = int(r['Hari_Mulai'])
        # kosong = tetap tersedia sampai proyek selesai (orang yang masih ada di bulan ke-5)
        r['Hari_Selesai'] = int(r['Hari_Selesai']) if r['Hari_Selesai'] else math.inf
    return rows


# ============================================================
# 3. PENJADWALAN
# ============================================================

def jadwal_tanpa_resource(aktivitas, durasi):
    """Jadwal rencana murni dari dependensi (rumus Excel dosen), tanpa batasan orang."""
    selesai, hasil = {}, {}
    while len(selesai) < len(aktivitas):  # urutan CSV belum tentu topologis (A23 bergantung pada A24–A33)
        for a in aktivitas:
            if a['ID'] in selesai or not all(p in selesai for p in a['Pred']):
                continue
            mulai = max((selesai[p] for p in a['Pred']), default=0) + 1
            selesai[a['ID']] = mulai + durasi[a['ID']] - 1
            hasil[a['ID']] = {'mulai': mulai, 'selesai': selesai[a['ID']]}
    return hasil


def jadwal_dengan_resource(aktivitas, durasi, orang, kebijakan):
    """
    Simulasi antrian per resource. Pada setiap hari t, tiap orang yang kosong mengambil
    aktivitas siap dengan role yang sama menurut kebijakan antrian:
      FCFS: yang siap paling awal dulu;  SPT: durasi paling pendek dulu.
    Seri ditentukan oleh prioritas MoSCoW lalu ID.
    """
    by_id = {a['ID']: a for a in aktivitas}
    kosong_mulai = {o['Orang']: o['Hari_Mulai'] for o in orang}
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

        for o in orang:
            nama = o['Orang']
            if not (kosong_mulai[nama] <= t and o['Hari_Mulai'] <= t <= o['Hari_Selesai']):
                continue
            kandidat = [i for i in siap if siap[i] <= t and by_id[i]['Role'] == o['Role'] and i in belum]
            if not kandidat:
                continue
            i = min(kandidat, key=kunci)
            akhir = t + durasi[i] - 1
            hasil[i] = {'siap': siap[i], 'mulai': t, 'selesai': akhir, 'orang': nama, 'tunggu': t - siap[i]}
            selesai[i] = akhir
            kosong_mulai[nama] = akhir + 1
            belum.discard(i)

        # lompat ke kejadian berikutnya: orang kosong, aktivitas siap, atau orang mulai bergabung
        kejadian = [h for h in kosong_mulai.values() if h > t]
        kejadian += [s for i, s in siap.items() if i in belum and s > t]
        kejadian += [o['Hari_Mulai'] for o in orang if o['Hari_Mulai'] > t]
        if belum and not kejadian:
            # masih ada yang siap tetapi belum terambil: coba hari berikutnya
            kejadian = [t + 1]
        if belum:
            t = min(kejadian)
            if t > 10_000:
                raise RuntimeError(f'Penjadwalan macet; sisa aktivitas: {sorted(belum)}')
    return hasil


def rantai_penentu(aktivitas, jadwal):
    """
    Telusuri mundur dari aktivitas yang selesai paling akhir: apa yang membuat tiap aktivitas
    mulai pada harinya — predecessor (jika tidak menunggu) atau pekerjaan sebelumnya
    milik orang yang sama (jika menunggu resource).
    """
    by_id = {a['ID']: a for a in aktivitas}
    per_orang = {}
    for i, j in jadwal.items():
        per_orang.setdefault(j['orang'], []).append(i)
    i = max(jadwal, key=lambda k: (jadwal[k]['selesai'], k))
    rantai = []
    while i:
        rantai.append(i)
        j = jadwal[i]
        if j['tunggu'] > 0:
            sebelumnya = [k for k in per_orang[j['orang']] if jadwal[k]['selesai'] == j['mulai'] - 1]
            i = sebelumnya[0] if sebelumnya else None
        else:
            pred = by_id[i]['Pred']
            i = max(pred, key=lambda p: (jadwal[p]['selesai'], p)) if pred else None
    return rantai


def himpunan_kritis(aktivitas, jadwal):
    """
    Seperti rantai_penentu, tetapi semua cabang yang seri ikut dihitung (mis. dua aktivitas paralel
    yang selesai di hari yang sama). Dipakai untuk indeks kekritisan agar tidak bias ke salah satu cabang.
    """
    by_id = {a['ID']: a for a in aktivitas}
    per_orang = {}
    for i, j in jadwal.items():
        per_orang.setdefault(j['orang'], []).append(i)
    akhir = max(j['selesai'] for j in jadwal.values())
    antre = [i for i, j in jadwal.items() if j['selesai'] == akhir]
    kritis = set()
    while antre:
        i = antre.pop()
        if i in kritis:
            continue
        kritis.add(i)
        j = jadwal[i]
        if j['tunggu'] > 0:
            antre += [k for k in per_orang[j['orang']] if jadwal[k]['selesai'] == j['mulai'] - 1]
        else:
            antre += [p for p in by_id[i]['Pred'] if jadwal[p]['selesai'] == j['siap'] - 1]
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


def jalankan():
    aktivitas = baca_aktivitas()
    orang = baca_resource()
    ids = [a['ID'] for a in aktivitas]
    durasi_rencana = {a['ID']: a['Durasi_Hari'] for a in aktivitas}

    rencana = {k: jadwal_dengan_resource(aktivitas, durasi_rencana, orang, k) for k in KEBIJAKAN}
    rencana_cpm = jadwal_tanpa_resource(aktivitas, durasi_rencana)
    selesai_rencana = {k: max(j['selesai'] for j in rencana[k].values()) for k in KEBIJAKAN}

    rng = random.Random(SEED)
    baris_iterasi = []
    agregat = {}  # (skenario, kebijakan, id) -> daftar nilai
    for it in range(1, N_ITERASI + 1):
        # bilangan random yang sama dipakai di semua skenario & kebijakan (perbandingan adil)
        undian = {i: (rng.random(), rng.random(), rng.random()) for i in ids}
        for skenario, kelas_cr in SKENARIO_CR.items():
            cr = {i: tarik_cr(kelas_cr, *undian[i]) for i in ids}
            tambahan = {i: math.ceil(durasi_rencana[i] * cr[i][1] - 1e-9) for i in ids}
            durasi = {i: durasi_rencana[i] + tambahan[i] for i in ids}
            for k in KEBIJAKAN:
                jadwal = jadwal_dengan_resource(aktivitas, durasi, orang, k)
                selesai = max(j['selesai'] for j in jadwal.values())
                rantai = rantai_penentu(aktivitas, jadwal)
                kritis = himpunan_kritis(aktivitas, jadwal)
                keterlambatan = selesai - selesai_rencana[k]
                baris_iterasi.append({
                    'Skenario_CR': skenario, 'Kebijakan': k, 'Iterasi': it,
                    'Selesai_Rencana': selesai_rencana[k], 'Selesai_Simulasi': selesai,
                    'Keterlambatan_Hari': keterlambatan, 'Telat': int(keterlambatan > 0),
                    'Jumlah_CR': sum(1 for i in ids if cr[i][0]),
                    'Tambahan_CR_Total_Hari': sum(tambahan.values()),
                    'Tambahan_CR_di_Rantai_Penentu': sum(tambahan[i] for i in rantai),
                    'Tunggu_Resource_di_Rantai_Penentu': sum(jadwal[i]['tunggu'] for i in rantai),
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
        if it % 200 == 0:
            print(f'  iterasi {it}/{N_ITERASI}')

    return aktivitas, orang, rencana, rencana_cpm, selesai_rencana, baris_iterasi, agregat


# ============================================================
# 5. RINGKASAN & EKSPOR
# ============================================================

def persentil(nilai, q):
    s = sorted(nilai)
    pos = (len(s) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def ringkas(baris_iterasi, selesai_rencana):
    hasil = []
    for skenario in SKENARIO_CR:
        for k in KEBIJAKAN:
            b = [r for r in baris_iterasi if r['Skenario_CR'] == skenario and r['Kebijakan'] == k]
            d = [r['Keterlambatan_Hari'] for r in b]
            n = len(b)
            p_telat = sum(r['Telat'] for r in b) / n
            cr_rantai = sum(r['Tambahan_CR_di_Rantai_Penentu'] for r in b)
            tunggu_rantai = sum(r['Tunggu_Resource_di_Rantai_Penentu'] for r in b)
            hasil.append({
                'Skenario_CR': skenario, 'Kebijakan': k, 'N_Iterasi': n,
                'Selesai_Rencana_Hari': selesai_rencana[k],
                'P_Telat': round(p_telat, 4),
                'SE_P_Telat': round(math.sqrt(p_telat * (1 - p_telat) / n), 4),
                'P_Telat_lebih_5_Hari': round(sum(1 for x in d if x > 5) / n, 4),
                'P_Telat_lebih_10_Persen': round(sum(1 for x in d if x > 0.1 * selesai_rencana[k]) / n, 4),
                'Rata2_Keterlambatan_Hari': round(statistics.mean(d), 2),
                'SD_Keterlambatan_Hari': round(statistics.stdev(d), 2),
                'P50_Hari': persentil(d, 0.5), 'P80_Hari': persentil(d, 0.8),
                'P90_Hari': persentil(d, 0.9), 'Maks_Hari': max(d),
                'Rata2_Jumlah_CR': round(statistics.mean(r['Jumlah_CR'] for r in b), 2),
                'Rata2_Tambahan_CR_di_Rantai_Hari': round(cr_rantai / n, 2),
                'Rata2_Tunggu_Resource_di_Rantai_Hari': round(tunggu_rantai / n, 2),
            })
    return hasil


def ringkas_per_aktivitas(aktivitas, agregat):
    hasil = []
    for skenario in SKENARIO_CR:
        for k in KEBIJAKAN:
            for a in aktivitas:
                v = agregat[(skenario, k, a['ID'])]
                kolom = list(zip(*v))
                n = len(v)
                hasil.append({
                    'Skenario_CR': skenario, 'Kebijakan': k, 'ID': a['ID'], 'Aktivitas': a['Aktivitas'],
                    'Role': a['Role'],
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


def gambar_histogram(baris_iterasi, ringkasan, path):
    biru, teks, teks2, grid, latar = '#2a78d6', '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
    fig, axes = plt.subplots(len(SKENARIO_CR), len(KEBIJAKAN), figsize=(10, 6.4), sharex=True, sharey=True)
    fig.patch.set_facecolor(latar)
    maks = max(r['Keterlambatan_Hari'] for r in baris_iterasi)
    # batang berpusat di bilangan bulat (keterlambatan dalam hari utuh)
    bins = [x - 0.5 for x in range(min(0, min(r['Keterlambatan_Hari'] for r in baris_iterasi)), maks + 2)]
    for bi, skenario in enumerate(SKENARIO_CR):
        for ki, k in enumerate(KEBIJAKAN):
            ax = axes[bi][ki]
            ax.set_facecolor(latar)
            d = [r['Keterlambatan_Hari'] for r in baris_iterasi if r['Skenario_CR'] == skenario and r['Kebijakan'] == k]
            ax.hist(d, bins=bins, color=biru, edgecolor=latar, linewidth=1)
            s = next(r for r in ringkasan if r['Skenario_CR'] == skenario and r['Kebijakan'] == k)
            ax.axvline(s['P80_Hari'], color=teks2, linewidth=1, linestyle='--')
            ax.text(0.98, 0.95, f"P(telat) = {s['P_Telat']:.1%}\nrata-rata = {s['Rata2_Keterlambatan_Hari']} hari\n"
                                f"P80 = {s['P80_Hari']:g} hari (garis putus)",
                    transform=ax.transAxes, ha='right', va='top', fontsize=8.5, color=teks)
            ax.set_title(f'CR {skenario} · antrian {k}', fontsize=10, color=teks, loc='left')
            ax.grid(axis='y', color=grid, linewidth=0.6)
            ax.set_axisbelow(True)
            for sisi in ('top', 'right'):
                ax.spines[sisi].set_visible(False)
            for sisi in ('left', 'bottom'):
                ax.spines[sisi].set_color(grid)
            ax.tick_params(colors=teks2, labelsize=8)
            if bi == len(SKENARIO_CR) - 1:
                ax.set_xlabel('Keterlambatan terhadap jadwal rencana (hari kerja)', fontsize=9, color=teks2)
            if ki == 0:
                ax.set_ylabel('Jumlah iterasi', fontsize=9, color=teks2)
    fig.suptitle(f'Sebaran keterlambatan P-FNE-01 ({N_ITERASI} iterasi per panel)', x=0.01, ha='left',
                 fontsize=12, color=teks)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor=latar)
    plt.close(fig)


def tulis_ringkasan_md(path, aktivitas, rencana, rencana_cpm, ringkasan, per_aktivitas):
    utama = [r for r in ringkasan if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS'][0]
    utama_akt = [r for r in per_aktivitas if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS']
    selalu = [r['ID'] for r in utama_akt if r['Indeks_Kekritisan'] == 1]
    kadang = sorted((r for r in utama_akt if 0 < r['Indeks_Kekritisan'] < 1),
                    key=lambda r: -r['Indeks_Kekritisan'])[:8]
    cpm = max(j['selesai'] for j in rencana_cpm.values())
    L = []
    L.append('# Ringkasan Hasil Simulasi Monte Carlo — Pilot P-FNE-01\n')
    L.append('> Digenerate otomatis oleh `simulasi_monte_carlo.py`. Jangan diedit manual; jalankan ulang script.\n')
    L.append('## Parameter\n')
    L.append(f'- Iterasi: **{N_ITERASI}**, seed {SEED}; peluang CR per aktivitas: **{P_CR:g}**')
    for s, kelas in SKENARIO_CR.items():
        uraian = ', '.join(f'{n} {p:.0%} (+{lo:.0%}–{hi:.0%})' if lo != hi else f'{n} {p:.0%} (+{lo:.0%})'
                           for n, p, (lo, hi) in kelas)
        L.append(f'- Skenario CR `{s}`: {uraian}')
    L.append('- Kebijakan antrian: FCFS (siap duluan dikerjakan duluan) dan SPT (durasi terpendek duluan)\n')
    L.append('## Jadwal Rencana\n')
    L.append(f'- Tanpa batasan resource (rumus dependensi dosen): selesai hari ke-**{cpm}** '
             f'(≈ {cpm / 5:.1f} minggu).')
    for k in KEBIJAKAN:
        f = max(j['selesai'] for j in rencana[k].values())
        L.append(f'- Dengan batasan resource PMP §4.6.1, antrian {k}: selesai hari ke-**{f}** (≈ {f / 5:.1f} minggu).')
    L.append('- PMP-01 §4.2.3 (Critical Path Analysis) menyebut 22 minggu (110 hari kerja). Selisihnya berasal '
             'dari tabel aktivitas §4.2.1 yang durasinya lebih panjang daripada ringkasan per fase di §4.2.3 '
             '(contoh: Fase 1 = 6 minggu kerja dengan rantai 5 minggu di §4.2.1, tetapi 4 minggu di §4.2.3). '
             'Patokan "telat" pada simulasi ini adalah jadwal rencana hasil §4.2.1 + resource, bukan angka 22 minggu.\n')
    L.append('## Hasil per Skenario\n')
    L.append('| Skenario CR | Antrian | Selesai rencana | P(telat) | P(telat > 5 hari) | P(telat > 10%) | Rata-rata | P80 | P90 | Maks |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for r in ringkasan:
        L.append(f"| {r['Skenario_CR']} | {r['Kebijakan']} | {r['Selesai_Rencana_Hari']} | {r['P_Telat']:.1%} "
                 f"| {r['P_Telat_lebih_5_Hari']:.1%} | {r['P_Telat_lebih_10_Persen']:.1%} "
                 f"| {r['Rata2_Keterlambatan_Hari']} | {r['P80_Hari']:g} | {r['P90_Hari']:g} | {r['Maks_Hari']} |")
    L.append('\nSatuan keterlambatan: hari kerja. P80 = 80% iterasi selesai dengan keterlambatan tidak lebih dari nilai ini.\n')
    L.append(f"## Aktivitas Paling Menentukan (skenario `{SKENARIO_UTAMA}`, FCFS)\n")
    L.append('Indeks kekritisan = proporsi iterasi di mana aktivitas berada pada rantai yang menentukan tanggal selesai '
             '(cabang paralel yang selesai bersamaan dihitung kritis semua).\n')
    L.append(f"- Selalu kritis (100% iterasi, {len(selalu)} aktivitas): {', '.join(selalu)}. "
             'CR di aktivitas ini pasti memundurkan tanggal selesai proyek.')
    L.append('- Kadang kritis (menjadi penentu hanya jika terkena CR yang cukup besar):\n')
    L.append('| ID | Aktivitas | Role | Indeks kekritisan | Delay sendiri (CR) | Geser karena predecessor | Geser karena antrian resource |')
    L.append('|---|---|---|---|---|---|---|')
    for r in kadang:
        L.append(f"| {r['ID']} | {r['Aktivitas']} | {r['Role']} | {r['Indeks_Kekritisan']:.0%} "
                 f"| {r['Rata2_Delay_Sendiri_CR_Hari']:.2f} | {r['dari_Predecessor_Hari']:.2f} "
                 f"| {r['dari_Antrian_Resource_Hari']:.2f} |")
    L.append('\nNilai delay/geser adalah rata-rata hari per iterasi. "Delay sendiri" = tambahan durasi karena CR di aktivitas itu; '
             '"geser" = mundurnya tanggal mulai dibanding rencana (rambatan).\n')
    L.append(f"## Penyebab Keterlambatan (skenario `{SKENARIO_UTAMA}`, FCFS)\n")
    L.append(f"- Rata-rata tambahan durasi CR yang berada di rantai penentu: **{utama['Rata2_Tambahan_CR_di_Rantai_Hari']} hari** per iterasi.")
    L.append(f"- Rata-rata waktu menunggu resource di rantai penentu: **{utama['Rata2_Tunggu_Resource_di_Rantai_Hari']} hari** per iterasi.")
    L.append(f"- Rata-rata jumlah CR per iterasi: {utama['Rata2_Jumlah_CR']} dari {len(aktivitas)} aktivitas.")
    if all(r['Rata2_Tunggu_Resource_di_Rantai_Hari'] == 0 for r in ringkasan):
        L.append('- **Batasan resource tidak pernah mengikat** pada pilot ini: dengan jumlah orang di PMP-01 §4.6.1 '
                 'dan asumsi 1 aktivitas dikerjakan 1 orang, tidak ada aktivitas di rantai penentu yang menunggu orang. '
                 'Karena itu hasil FCFS dan SPT identik, dan seluruh keterlambatan berasal dari CR beserta rambatannya. '
                 'Antrian resource baru berpengaruh jika orang dibagi antarsubproyek (portofolio 8 subproyek) '
                 'atau jika satu aktivitas membutuhkan lebih dari satu orang.')
    L.append('- P(telat) sama pada kedua skenario CR karena tambahan sekecil apa pun dibulatkan ke atas menjadi minimal '
             '1 hari, sehingga "telat" (> 0 hari) hanya bergantung pada ada/tidaknya CR di rantai penentu. '
             'Perbedaan skenario terlihat pada P(telat > 5 hari) dan sebarannya.\n')
    L.append('## Berkas\n')
    L.append('- `iterasi.csv` — satu baris per iterasi × skenario × kebijakan')
    L.append('- `ringkasan.csv` — tabel hasil per skenario')
    L.append('- `per_aktivitas.csv` — delay sendiri vs rambatan per aktivitas')
    L.append('- `jadwal_rencana.csv` — jadwal rencana per aktivitas (tanpa resource, FCFS, SPT)')
    L.append('- `histogram_keterlambatan.png` — sebaran keterlambatan')
    path.write_text('\n'.join(L) + '\n', encoding='utf-8')


def tulis_jadwal_rencana(path, aktivitas, rencana, rencana_cpm):
    rows = []
    for a in aktivitas:
        i = a['ID']
        r = {'ID': i, 'Aktivitas': a['Aktivitas'], 'Role': a['Role'], 'Durasi_Hari': a['Durasi_Hari'],
             'Predecessor': a['Predecessor'],
             'Mulai_TanpaResource': rencana_cpm[i]['mulai'], 'Selesai_TanpaResource': rencana_cpm[i]['selesai']}
        for k in KEBIJAKAN:
            j = rencana[k][i]
            r.update({f'Orang_{k}': j['orang'], f'Siap_{k}': j['siap'], f'Mulai_{k}': j['mulai'],
                      f'Selesai_{k}': j['selesai'], f'Tunggu_{k}': j['tunggu']})
        rows.append(r)
    tulis_csv(path, rows)


def main():
    OUT.mkdir(exist_ok=True)
    print(f'Simulasi {N_ITERASI} iterasi × {len(SKENARIO_CR)} skenario CR × {len(KEBIJAKAN)} kebijakan antrian ...')
    aktivitas, orang, rencana, rencana_cpm, selesai_rencana, baris_iterasi, agregat = jalankan()
    ringkasan = ringkas(baris_iterasi, selesai_rencana)
    per_aktivitas = ringkas_per_aktivitas(aktivitas, agregat)

    tulis_jadwal_rencana(OUT / 'jadwal_rencana.csv', aktivitas, rencana, rencana_cpm)
    tulis_csv(OUT / 'iterasi.csv', baris_iterasi)
    tulis_csv(OUT / 'ringkasan.csv', ringkasan)
    tulis_csv(OUT / 'per_aktivitas.csv', per_aktivitas)
    gambar_histogram(baris_iterasi, ringkasan, OUT / 'histogram_keterlambatan.png')
    tulis_ringkasan_md(OUT / '00_RINGKASAN_HASIL.md', aktivitas, rencana, rencana_cpm, ringkasan, per_aktivitas)

    from buat_excel import buat_workbook
    buat_workbook(HERE / 'pilot_P-FNE-01.xlsx', aktivitas, orang, rencana, rencana_cpm, ringkasan,
                  [r for r in baris_iterasi if r['Skenario_CR'] == SKENARIO_UTAMA and r['Kebijakan'] == 'FCFS'],
                  SKENARIO_CR[SKENARIO_UTAMA], P_CR)

    for r in ringkasan:
        print(f"  {r['Skenario_CR']:6s} {r['Kebijakan']:4s}  rencana hari {r['Selesai_Rencana_Hari']}  "
              f"P(telat)={r['P_Telat']:.1%}  rata2={r['Rata2_Keterlambatan_Hari']} hari  P90={r['P90_Hari']:g}")
    print(f'Selesai. Luaran di {OUT} dan pilot_P-FNE-01.xlsx')


if __name__ == '__main__':
    main()
