"""
PRE-02: Pembuatan dataset untuk 4 model ML (Deskripsi Penelitian §2–§4) dari simulasi iterasi random.

Ide: tiap iterasi simulasi = satu "proyek" yang dijalankan sampai selesai. Proyek itu dipantau di beberapa
titik monitoring (25%, 50%, 75% dari jadwal rencana). Kondisi pada titik monitoring = FITUR; keterlambatan
di akhir proyek = LABEL. Fitur hanya memakai kejadian sampai hari monitoring, sehingga model memprediksi
masa depan (tidak ada kebocoran label).

Gangguan yang disimulasikan (FCFS, skenario CR "dosen"):
  1. Change request (CR) per aktivitas, persis seperti simulasi_iterasi.py.
  2. Kejadian risiko dari register risiko PMP (data/P-FNE-0X_risiko.csv, hanya Dipakai_Simulasi = 1):
     - risiko terjadi dengan peluang di register PMP (skala 1–5 dikonversi menurut PMP-01 §9.3.1);
     - waktu kejadian acak seragam di antara hari 1 dan hari selesai rencana;
     - mengenai satu aktivitas yang sedang berjalan saat itu (jika tidak ada, aktivitas berikutnya yang mulai);
     - durasi aktivitas itu bertambah: DAMPAK_RISIKO[level dampak] x durasi rencana, dengan skala dampak
       jadwal PMP-01 §9.3.1 dan faktor mitigasi yang dikalibrasi ke PMP-08 §9.6.2 (lihat kalibrasi_risiko.py);
     - risiko dihitung "belum dimitigasi" sejak terjadi sampai aktivitas yang terkena selesai.

Fitur (7 variabel Deskripsi Penelitian §2):
  SPI_Jadwal                  : progres aktual dibanding rencana = EV/PV (nilai = durasi rencana)
  Sisa_Waktu_Hari             : hari selesai rencana - hari monitoring
  Backlog_Sisa_Persen         : porsi pekerjaan (durasi rencana) yang belum dikerjakan
  Utilisasi_Resource          : hari-orang terpakai / hari-orang tersedia, dari hari 1 s.d. monitoring
  Risiko_Belum_Dimitigasi     : jumlah kejadian risiko yang belum selesai ditangani
  Frekuensi_CR                : jumlah CR pada aktivitas yang sudah dimulai
  Pergeseran_Dependency_Hari  : rata-rata pergeseran hari "siap" (menunggu predecessor) aktivitas yang sudah
                                dimulai, dibanding rencana (proksi kinerja dependency; dependency antarproyek
                                tidak tercatat terpisah di PMP)
Label:
  Keterlambatan_Akhir_Hari, Telat (>0 hari),
  Telat_Lebih_5_Persen  (LABEL UTAMA; PMP-01 change control: perubahan jadwal > 5% baseline harus ke Sponsor),
  Telat_Lebih_10_Persen (PMP-01: "Schedule Delay > 10% dari baseline" -> eskalasi ke Sponsor)

Jalankan:  python buat_dataset_ml.py          (butuh data/P-FNE-0X_risiko.csv dari ekstraksi_risiko.py)
"""

import csv
import random
import statistics
from pathlib import Path

import simulasi_iterasi as sim

HERE = Path(__file__).resolve().parent
OUT = HERE / 'dataset_ml'

N_ITERASI = sim.N_ITERASI
SKENARIO = 'dosen'
KEBIJAKAN = 'FCFS'
TITIK_MONITORING = [0.25, 0.50, 0.75]
# Parameter kejadian risiko — setiap angka punya rujukan dokumen:
# - FAKTOR_PELUANG = 1: peluang dipakai apa adanya dari register risiko PMP.
# - SKALA_DAMPAK: PMP-01 §9.3.1 Probability-Impact Matrix, "Dampak (Biaya, Jadwal, Kualitas)":
#   Very Low < 1%, Low 1–5%, Medium 5–10%, High 10–20%, Very High > 20%. Dipakai nilai tengah rentang;
#   untuk "> 20%" dipakai 25% (rentang 20–30%). Fraksi dikenakan pada durasi rencana aktivitas yang terkena.
# - FAKTOR_DAMPAK (faktor mitigasi): register memuat risiko sebelum respons, padahal semua risiko punya rencana
#   respons. Faktor dikalibrasi agar median keterlambatan P-FNE-08 sama dengan analisis kuantitatif PMP-08 §9.6.2
#   (target 20 minggu, P50 21 minggu = +5%). Pencarian nilainya: kalibrasi_risiko.py.
FAKTOR_PELUANG = 1.0
FAKTOR_DAMPAK = 0.4
SKALA_DAMPAK = {1: 0.005, 2: 0.03, 3: 0.075, 4: 0.15, 5: 0.25}
DAMPAK_RISIKO = {k: v * FAKTOR_DAMPAK for k, v in SKALA_DAMPAK.items()}
BATAS_LABEL_UTAMA = 0.05  # PMP-01 change control: perubahan jadwal > 5% baseline harus disetujui Sponsor

KOLOM = ['Subproyek', 'Iterasi', 'Titik_Monitoring', 'Hari_Monitoring',
         'SPI_Jadwal', 'Sisa_Waktu_Hari', 'Backlog_Sisa_Persen', 'Utilisasi_Resource',
         'Risiko_Belum_Dimitigasi', 'Frekuensi_CR', 'Pergeseran_Dependency_Hari',
         'Keterlambatan_Akhir_Hari', 'Telat', 'Telat_Lebih_5_Persen', 'Telat_Lebih_10_Persen']
FITUR = KOLOM[4:11]
LABEL = KOLOM[11:]


def baca_risiko(kode):
    with open(sim.DATA / f'P-FNE-{kode}_risiko.csv', encoding='utf-8') as f:
        return [r for r in csv.DictReader(f) if r['Dipakai_Simulasi'] == '1']


def progres(j, durasi_diketahui, t):
    """Porsi aktivitas yang sudah dikerjakan pada akhir hari t (aktivitas menempati selang (mulai-1, selesai])."""
    if j['selesai'] <= t:
        return 1.0
    return min(max((t - (j['mulai'] - 1)) / durasi_diketahui, 0.0), 1.0)


def fitur(t, aktivitas, rencana, jadwal, durasi_cr, orang, cr, risiko_terjadi, selesai_rencana):
    """Kondisi proyek pada akhir hari t. Hanya memakai informasi yang sudah terjadi sampai hari t:
    durasi aktivitas yang sedang berjalan = durasi rencana + CR + dampak risiko yang terjadi <= t."""
    nilai = {a['ID']: a['Durasi_Hari'] for a in aktivitas}
    total = sum(nilai.values())
    diketahui = dict(durasi_cr)
    for tau, i, tambah in risiko_terjadi:
        if tau <= t:
            diketahui[i] += tambah
    ev = sum(nilai[i] * progres(jadwal[i], diketahui[i], t) for i in nilai)
    pv = sum(nilai[i] * progres(rencana[i], nilai[i], t) for i in nilai)

    tersedia = sum(max(0.0, min(t, o['Hari_Selesai']) - (o['Hari_Mulai'] - 1)) for o in orang)
    terpakai = sum(len(j['orang']) * max(0.0, min(j['selesai'], t) - (j['mulai'] - 1)) for j in jadwal.values())

    mulai = [i for i in nilai if jadwal[i]['mulai'] <= t]
    geser = [jadwal[i]['siap'] - rencana[i]['siap'] for i in mulai]
    return {
        'SPI_Jadwal': round(ev / pv, 4) if pv else 1.0,
        'Sisa_Waktu_Hari': round(selesai_rencana - t, 4),
        'Backlog_Sisa_Persen': round(1 - ev / total, 4),
        'Utilisasi_Resource': round(terpakai / tersedia, 4) if tersedia else 0.0,
        'Risiko_Belum_Dimitigasi': sum(1 for tau, i, _ in risiko_terjadi if tau <= t < jadwal[i]['selesai']),
        'Frekuensi_CR': sum(1 for i in mulai if cr[i]),
        'Pergeseran_Dependency_Hari': round(statistics.fmean(geser), 4) if geser else 0.0,
    }


def iterasi(rng, aktivitas, orang, risiko, kelas_cr, selesai_rencana):
    ids = [a['ID'] for a in aktivitas]
    durasi_rencana = {a['ID']: a['Durasi_Hari'] for a in aktivitas}
    # 1) CR: urutan undian sama dengan simulasi_iterasi.py (3 bilangan per aktivitas)
    cr, durasi = {}, {}
    for i in ids:
        nama, fraksi = sim.tarik_cr(kelas_cr, rng.random(), rng.random(), rng.random())
        cr[i] = nama is not None
        durasi[i] = durasi_rencana[i] + round(durasi_rencana[i] * fraksi, 4)
    # 2) kejadian risiko: 3 bilangan per risiko (terjadi?, kapan?, aktivitas mana?)
    kejadian = []
    for r in risiko:
        u_terjadi, u_waktu, u_pilih = rng.random(), rng.random(), rng.random()
        if u_terjadi < FAKTOR_PELUANG * float(r['Peluang']):
            kejadian.append((1 + u_waktu * (selesai_rencana - 1), u_pilih, int(r['Level_Dampak'])))
    kejadian.sort()

    durasi_cr = dict(durasi)
    jadwal = sim.jadwal_dengan_resource(aktivitas, durasi, orang, KEBIJAKAN)
    terjadi = []  # (hari kejadian, ID aktivitas yang terkena, tambahan hari)
    for tau, u_pilih, level in kejadian:
        berjalan = sorted(i for i, j in jadwal.items() if j['mulai'] - 1 < tau <= j['selesai'])
        if not berjalan:
            berikut = [i for i, j in jadwal.items() if j['mulai'] - 1 >= tau]
            if not berikut:
                continue  # proyek sudah selesai: risiko tidak lagi berdampak
            awal = min(jadwal[i]['mulai'] for i in berikut)
            berjalan = sorted(i for i in berikut if jadwal[i]['mulai'] == awal)
        kena = berjalan[min(int(u_pilih * len(berjalan)), len(berjalan) - 1)]
        tambah = round(durasi_rencana[kena] * DAMPAK_RISIKO[level], 4)
        durasi[kena] = round(durasi[kena] + tambah, 4)
        # Penjadwalan FCFS tidak melihat ke depan, sehingga jadwal sebelum tau tidak berubah.
        jadwal = sim.jadwal_dengan_resource(aktivitas, durasi, orang, KEBIJAKAN)
        terjadi.append((tau, kena, tambah))
    return cr, durasi_cr, jadwal, terjadi


def proses(kode):
    aktivitas = sim.baca_aktivitas(kode)
    orang = sim.baca_resource(kode)
    risiko = baca_risiko(kode)
    durasi_rencana = {a['ID']: a['Durasi_Hari'] for a in aktivitas}
    rencana = sim.jadwal_dengan_resource(aktivitas, durasi_rencana, orang, KEBIJAKAN)
    selesai_rencana = max(j['selesai'] for j in rencana.values())
    kelas_cr = sim.SKENARIO_CR[SKENARIO]

    rng = random.Random(f'{sim.SEED}-ml-{kode}')
    baris = []
    for it in range(1, N_ITERASI + 1):
        cr, durasi_cr, jadwal, terjadi = iterasi(rng, aktivitas, orang, risiko, kelas_cr, selesai_rencana)
        telat = round(max(j['selesai'] for j in jadwal.values()) - selesai_rencana, 4)
        label = {'Keterlambatan_Akhir_Hari': telat, 'Telat': int(telat > 0),
                 'Telat_Lebih_5_Persen': int(telat > BATAS_LABEL_UTAMA * selesai_rencana),
                 'Telat_Lebih_10_Persen': int(telat > 0.10 * selesai_rencana)}
        for titik in TITIK_MONITORING:
            t = round(titik * selesai_rencana, 4)
            baris.append({'Subproyek': f'P-FNE-{kode}', 'Iterasi': it, 'Titik_Monitoring': titik,
                          'Hari_Monitoring': t,
                          **fitur(t, aktivitas, rencana, jadwal, durasi_cr, orang, cr, terjadi, selesai_rencana),
                          **label})
    return baris, selesai_rencana, len(risiko)


def main():
    OUT.mkdir(exist_ok=True)
    semua = []
    for kode in sim.SUBPROYEK:
        baris, selesai, n_risiko = proses(kode)
        semua += baris
        akhir = [b for b in baris if b['Titik_Monitoring'] == TITIK_MONITORING[0]]
        p = {k: sum(b[k] for b in akhir) / len(akhir) for k in LABEL[1:]}
        print(f'P-FNE-{kode}: selesai rencana {selesai:g}, risiko {n_risiko}, '
              f'P(telat) {p["Telat"]:.1%}, P(>5%) {p["Telat_Lebih_5_Persen"]:.1%}, '
              f'P(>10%) {p["Telat_Lebih_10_Persen"]:.1%}')
    with open(OUT / 'dataset_ml.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=KOLOM)
        w.writeheader()
        w.writerows(semua)
    print(f'{len(semua)} baris -> {OUT / "dataset_ml.csv"}')


if __name__ == '__main__':
    main()
