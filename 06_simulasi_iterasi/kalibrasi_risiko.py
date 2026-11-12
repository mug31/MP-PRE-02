"""
PRE-02: Kalibrasi faktor mitigasi dampak risiko (FAKTOR_DAMPAK di buat_dataset_ml.py).

Rujukan: PMP-08 §9.6.2 Quantitative Risk Analysis Result, "Monte Carlo Simulation Results":
  Project Completion Date — target 20 minggu, P20 19,5 / P50 21,0 / P80 22,5 minggu, peluang tepat waktu 55%.
  Jadi median keterlambatan = +5% dan P80 = +12,5% dari target.

Cara: P-FNE-08 disimulasikan (FCFS, CR skenario dosen, risiko dari register PMP-08 dengan skala PMP-01 §9.3.1)
untuk beberapa nilai faktor; dipilih faktor yang median keterlambatannya paling dekat dengan +5%.
Hanya median yang dipakai sebagai sasaran: simulasi hanya menambah durasi (CR, risiko) sehingga tidak dapat
menghasilkan penyelesaian lebih cepat dari rencana seperti P20 PMP-08 (-2,5%), dan sebarannya lebih sempit.

Luaran: dataset_ml/kalibrasi_risiko.csv
Jalankan:  python kalibrasi_risiko.py
"""

import csv
import random

import buat_dataset_ml as ml
import simulasi_iterasi as sim

KODE = '08'
TARGET = {'P20': -0.025, 'P50': 0.05, 'P80': 0.125, 'P_Tepat_Waktu': 0.55}
GRID = [round(0.1 * i, 1) for i in range(0, 11)]


def sebaran(faktor, n=ml.N_ITERASI):
    akt, org = sim.baca_aktivitas(KODE), sim.baca_resource(KODE)
    risiko = ml.baca_risiko(KODE)
    dr = {a['ID']: a['Durasi_Hari'] for a in akt}
    sr = max(j['selesai'] for j in sim.jadwal_dengan_resource(akt, dr, org, ml.KEBIJAKAN).values())
    ml.DAMPAK_RISIKO = {k: v * faktor for k, v in ml.SKALA_DAMPAK.items()}
    rng = random.Random(f'{sim.SEED}-kalibrasi-{KODE}')
    tl = sorted((max(j['selesai'] for j in ml.iterasi(rng, akt, org, risiko, sim.SKENARIO_CR[ml.SKENARIO], sr)[2]
                     .values()) - sr) / sr for _ in range(n))
    q = lambda p: tl[round(p * (n - 1))]
    return {'P20': q(0.2), 'P50': q(0.5), 'P80': q(0.8), 'P_Tepat_Waktu': sum(x <= 0 for x in tl) / n}


def main():
    asli = dict(ml.DAMPAK_RISIKO)
    rows = []
    print(f'Sasaran PMP-08 §9.6.2: P50 {TARGET["P50"]:+.1%}, P80 {TARGET["P80"]:+.1%}')
    for f in GRID:
        s = sebaran(f)
        rows.append({'Faktor_Dampak': f, **{k: round(v, 4) for k, v in s.items()},
                     'Selisih_P50': round(abs(s['P50'] - TARGET['P50']), 4)})
        print(f'  faktor {f:.1f}: P20 {s["P20"]:+.1%}  P50 {s["P50"]:+.1%}  P80 {s["P80"]:+.1%}  '
              f'tepat waktu {s["P_Tepat_Waktu"]:.0%}')
    terbaik = min(rows, key=lambda r: r['Selisih_P50'])
    for r in rows:
        r['Dipilih'] = int(r is terbaik)
    ml.DAMPAK_RISIKO = asli
    with open(ml.OUT / 'kalibrasi_risiko.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f'Faktor terpilih: {terbaik["Faktor_Dampak"]} (P50 {terbaik["P50"]:+.1%}); '
          f'dipakai di buat_dataset_ml.py: {ml.FAKTOR_DAMPAK}')
    assert terbaik['Faktor_Dampak'] == ml.FAKTOR_DAMPAK, 'FAKTOR_DAMPAK di buat_dataset_ml.py belum sesuai kalibrasi'


if __name__ == '__main__':
    main()
