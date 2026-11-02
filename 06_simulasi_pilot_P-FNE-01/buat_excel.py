"""
Membuat workbook pilot_P-FNE-01.xlsx untuk dipresentasikan ke dosen.

Sheet berisi RUMUS hidup (berubah setiap F9):
  - Jadwal_Rencana      : rumus dosen, mulai = MAX(selesai predecessor) + 1, selesai = mulai + durasi - 1
  - Simulasi_1_Iterasi  : satu putaran CR dengan RAND() dan IF(), delay sendiri vs rambatan
Sheet berisi NILAI dari simulasi_monte_carlo.py (karena antrian resource sulit dirumuskan di Excel):
  - Jadwal_Resource, Hasil_Iterasi, Ringkasan
Dipanggil dari simulasi_monte_carlo.py.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill('solid', fgColor='DCE8F7')
INPUT_FILL = PatternFill('solid', fgColor='FFF4D6')
BOLD = Font(bold=True)


def _header(ws, row, kolom):
    for c, nama in enumerate(kolom, start=1):
        cell = ws.cell(row=row, column=c, value=nama)
        cell.font = BOLD
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(wrap_text=True, vertical='top')


def _lebar(ws, lebar):
    for i, w in enumerate(lebar, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def sheet_petunjuk(wb):
    ws = wb.active
    ws.title = 'Petunjuk'
    teks = [
        'Pilot Simulasi Monte Carlo Keterlambatan — Sub-Proyek P-FNE-01 (Foundation & Core Platform)',
        '',
        'Urutan membaca (sesuai arahan dosen, bimbingan 7 Oktober 2026):',
        '1. Parameter — peluang CR dan kelas kesulitan (sel kuning boleh diubah).',
        '2. Jadwal_Rencana — aktivitas, durasi, predecessor dari PMP-01 §4.2.1; tanggal dihitung dengan rumus.',
        '3. Jadwal_Resource — jadwal per orang (PMP-01 §4.6.1) dengan antrian FCFS; dihitung oleh Python.',
        '4. Simulasi_1_Iterasi — satu putaran CR dengan RAND()/IF(). Tekan F9 untuk mengacak ulang.',
        '5. Hasil_Iterasi — 1000 putaran (skenario CR dosen, antrian FCFS, termasuk batasan resource).',
        '6. Ringkasan — probabilitas & sebaran keterlambatan untuk semua skenario.',
        '',
        'Catatan:',
        '- Satuan waktu = hari kerja; 1 minggu = 5 hari kerja; 0,5 minggu dibulatkan ke atas menjadi 3 hari.',
        '- Simulasi_1_Iterasi hanya memakai dependensi (tanpa antrian resource) agar rumusnya mudah diikuti;',
        '  versi lengkap dengan antrian resource ada di Hasil_Iterasi (simulasi_monte_carlo.py).',
        '- Jika ingin iterasi murni di Excel: Data > What-If Analysis > Data Table pada kolom berisi 1..1000,',
        '  dengan sel input kolom = sel kosong mana saja, dan rumus hasil = sel Telat di Simulasi_1_Iterasi.',
        '- Alokasi role per aktivitas adalah USULAN dan harus disepakati kelompok.',
    ]
    for i, t in enumerate(teks, start=1):
        ws.cell(row=i, column=1, value=t)
    ws['A1'].font = Font(bold=True, size=13)
    ws.column_dimensions['A'].width = 110


def sheet_parameter(wb, kelas_cr, p_cr):
    ws = wb.create_sheet('Parameter')
    ws['A1'] = 'Parameter simulasi (sel kuning dapat diubah)'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A3'], ws['B3'] = 'Peluang CR per aktivitas', p_cr
    ws['B3'].fill = INPUT_FILL
    ws['C3'] = 'Contoh dosen [50:35]: 10% → 0,1'
    _header(ws, 5, ['Kelas kesulitan', 'Peluang kelas', 'Tambahan min', 'Tambahan maks', 'Batas kumulatif'])
    for r, (nama, peluang, (lo, hi)) in enumerate(kelas_cr, start=6):
        ws.cell(row=r, column=1, value=nama)
        for c, v in ((2, peluang), (3, lo), (4, hi)):
            ws.cell(row=r, column=c, value=v).fill = INPUT_FILL
        ws.cell(row=r, column=5, value=f'=SUM($B$6:B{r})')
    ws['A10'] = 'Sumber angka contoh: dosen [52:04–53:21] (rendah 10–20%, sedang 30%, tinggi 50%). Peluang kelas = asumsi kelompok.'
    _lebar(ws, [26, 14, 14, 14, 16])


def sheet_jadwal_rencana(wb, aktivitas):
    ws = wb.create_sheet('Jadwal_Rencana')
    kolom = ['ID', 'Fase', 'Aktivitas', 'Durasi (minggu)', 'Durasi (hari)', 'Predecessor', 'Mulai (hari ke-)',
             'Selesai (hari ke-)', 'Role (usulan)', 'Prioritas', 'Dependensi di dokumen', 'Interpretasi', 'Sumber']
    _header(ws, 1, kolom)
    baris = {a['ID']: i for i, a in enumerate(aktivitas, start=2)}
    for a in aktivitas:
        r = baris[a['ID']]
        ws.cell(row=r, column=1, value=a['ID'])
        ws.cell(row=r, column=2, value=a['Fase'])
        ws.cell(row=r, column=3, value=a['Aktivitas'])
        ws.cell(row=r, column=4, value=float(a['Durasi_Minggu']))
        ws.cell(row=r, column=5, value=f'=ROUNDUP(D{r}*5,0)')
        ws.cell(row=r, column=6, value=a['Predecessor'].replace(';', ', '))
        if a['Pred']:
            ref = ','.join(f'H{baris[p]}' for p in a['Pred'])
            ws.cell(row=r, column=7, value=f'=MAX({ref})+1')
        else:
            ws.cell(row=r, column=7, value=1).fill = INPUT_FILL
        ws.cell(row=r, column=8, value=f'=G{r}+E{r}-1')
        ws.cell(row=r, column=9, value=a['Role'])
        ws.cell(row=r, column=10, value=a['Prioritas'])
        ws.cell(row=r, column=11, value=a['Dependensi_Dokumen'])
        ws.cell(row=r, column=12, value=a['Interpretasi_Dependensi'])
        ws.cell(row=r, column=13, value=a['Sumber'])
    akhir = len(aktivitas) + 1
    ws.cell(row=akhir + 2, column=7, value='Selesai proyek').font = BOLD
    ws.cell(row=akhir + 2, column=8, value=f'=MAX(H2:H{akhir})').font = BOLD
    ws.freeze_panes = 'D2'
    _lebar(ws, [6, 22, 40, 10, 9, 22, 10, 10, 12, 9, 16, 36, 40])
    return baris


def sheet_simulasi(wb, aktivitas, baris, n_kelas):
    ws = wb.create_sheet('Simulasi_1_Iterasi')
    kolom = ['ID', 'Aktivitas', 'Durasi rencana', 'Mulai rencana', 'Selesai rencana', 'Rand CR', 'Kena CR? (1/0)',
             'Rand kelas', 'Kelas CR', 'Tambahan %', 'Tambahan (hari)', 'Durasi aktual', 'Mulai aktual',
             'Selesai aktual', 'Delay sendiri (CR)', 'Rambatan dari predecessor']
    _header(ws, 1, kolom)
    p_cr = 'Parameter!$B$3'
    kelas = [(f'Parameter!$A${6 + i}', f'Parameter!$E${6 + i}', f'Parameter!$C${6 + i}', f'Parameter!$D${6 + i}')
             for i in range(n_kelas)]

    def if_kelas(i, isi):
        # IF bertingkat memilih kelas berdasarkan batas kumulatif peluang
        if i == n_kelas - 1:
            return isi(kelas[i])
        return f'IF(H{{r}}<{kelas[i][1]},{isi(kelas[i])},{if_kelas(i + 1, isi)})'

    for a in aktivitas:
        r = baris[a['ID']]
        jr = 'Jadwal_Rencana!'
        ws.cell(row=r, column=1, value=a['ID'])
        ws.cell(row=r, column=2, value=a['Aktivitas'])
        ws.cell(row=r, column=3, value=f'={jr}E{r}')
        ws.cell(row=r, column=4, value=f'={jr}G{r}')
        ws.cell(row=r, column=5, value=f'={jr}H{r}')
        ws.cell(row=r, column=6, value='=RAND()')
        ws.cell(row=r, column=7, value=f'=IF(F{r}<{p_cr},1,0)')
        ws.cell(row=r, column=8, value='=RAND()')
        ws.cell(row=r, column=9, value=f'=IF(G{r}=0,"-",' + if_kelas(0, lambda k: k[0]).format(r=r) + ')')
        ws.cell(row=r, column=10, value=f'=IF(G{r}=0,0,' +
                if_kelas(0, lambda k: f'{k[2]}+RAND()*({k[3]}-{k[2]})').format(r=r) + ')')
        ws.cell(row=r, column=11, value=f'=ROUNDUP(C{r}*J{r},0)')
        ws.cell(row=r, column=12, value=f'=C{r}+K{r}')
        if a['Pred']:
            ref = ','.join(f'N{baris[p]}' for p in a['Pred'])
            ws.cell(row=r, column=13, value=f'=MAX({ref})+1')
        else:
            ws.cell(row=r, column=13, value=1)
        ws.cell(row=r, column=14, value=f'=M{r}+L{r}-1')
        ws.cell(row=r, column=15, value=f'=K{r}')
        ws.cell(row=r, column=16, value=f'=M{r}-D{r}')
        ws.cell(row=r, column=10).number_format = '0%'
    akhir = len(aktivitas) + 1
    ringkas = [
        ('Selesai rencana (hari ke-)', f'=MAX(E2:E{akhir})'),
        ('Selesai simulasi (hari ke-)', f'=MAX(N2:N{akhir})'),
        ('Keterlambatan (hari)', f'=B{akhir + 4}-B{akhir + 3}'),
        ('Telat? (1 = ya)', f'=IF(B{akhir + 5}>0,1,0)'),
        ('Jumlah CR', f'=SUM(G2:G{akhir})'),
    ]
    for i, (label, rumus) in enumerate(ringkas, start=akhir + 3):
        ws.cell(row=i, column=1, value=label).font = BOLD
        ws.cell(row=i, column=2, value=rumus).font = BOLD
    ws.freeze_panes = 'C2'
    _lebar(ws, [26, 40, 9, 9, 9, 9, 9, 9, 10, 10, 10, 9, 9, 9, 10, 12])


def sheet_jadwal_resource(wb, aktivitas, orang, rencana):
    ws = wb.create_sheet('Jadwal_Resource')
    ws['A1'] = 'Jadwal per orang (rencana, tanpa CR, antrian FCFS) — dihitung oleh simulasi_monte_carlo.py'
    ws['A1'].font = Font(bold=True, size=12)
    _header(ws, 3, ['Orang', 'Role', 'Tersedia mulai (hari)', 'Tersedia sampai (hari)', 'Urutan pekerjaan',
                    'Total hari kerja', 'Sumber'])
    jadwal = rencana['FCFS']
    nama = {a['ID']: a['Aktivitas'] for a in aktivitas}
    for r, o in enumerate(orang, start=4):
        tugas = sorted((i for i in jadwal if jadwal[i]['orang'] == o['Orang']), key=lambda i: jadwal[i]['mulai'])
        ws.cell(row=r, column=1, value=o['Orang'])
        ws.cell(row=r, column=2, value=o['Role'])
        ws.cell(row=r, column=3, value=o['Hari_Mulai'])
        ws.cell(row=r, column=4, value=o['Hari_Selesai'] if o['Hari_Selesai'] != float('inf') else 'sampai selesai')
        ws.cell(row=r, column=5, value=' → '.join(f"{i} (h{jadwal[i]['mulai']}–{jadwal[i]['selesai']})" for i in tugas))
        ws.cell(row=r, column=6, value=sum(jadwal[i]['selesai'] - jadwal[i]['mulai'] + 1 for i in tugas))
        ws.cell(row=r, column=7, value=o['Sumber'])
    awal = len(orang) + 6
    _header(ws, awal, ['ID', 'Aktivitas', 'Orang', 'Siap (hari)', 'Mulai (hari)', 'Selesai (hari)', 'Menunggu resource (hari)'])
    for r, a in enumerate(aktivitas, start=awal + 1):
        j = jadwal[a['ID']]
        for c, v in enumerate([a['ID'], nama[a['ID']], j['orang'], j['siap'], j['mulai'], j['selesai'], j['tunggu']],
                              start=1):
            ws.cell(row=r, column=c, value=v)
    _lebar(ws, [10, 40, 12, 14, 70, 14, 40])


def sheet_hasil_iterasi(wb, baris_iterasi):
    ws = wb.create_sheet('Hasil_Iterasi')
    ws['A1'] = 'Hasil 1000 iterasi — skenario CR dosen, antrian FCFS, dengan batasan resource'
    ws['A1'].font = Font(bold=True, size=12)
    kolom = ['Iterasi', 'Selesai_Rencana', 'Selesai_Simulasi', 'Keterlambatan_Hari', 'Telat', 'Jumlah_CR',
             'Tambahan_CR_Total_Hari', 'Tambahan_CR_di_Rantai_Penentu', 'Tunggu_Resource_di_Rantai_Penentu',
             'Rantai_Penentu']
    mulai = 10
    _header(ws, mulai, kolom)
    for r, b in enumerate(baris_iterasi, start=mulai + 1):
        for c, k in enumerate(kolom, start=1):
            ws.cell(row=r, column=c, value=b[k])
    akhir = mulai + len(baris_iterasi)
    statistik = [
        ('P(telat) = jumlah telat ÷ N', f'=AVERAGE(E{mulai + 1}:E{akhir})', '0.0%'),
        ('Rata-rata keterlambatan (hari)', f'=AVERAGE(D{mulai + 1}:D{akhir})', '0.00'),
        ('P80 keterlambatan (hari)', f'=PERCENTILE(D{mulai + 1}:D{akhir},0.8)', '0.0'),
        ('P90 keterlambatan (hari)', f'=PERCENTILE(D{mulai + 1}:D{akhir},0.9)', '0.0'),
        ('Maksimum keterlambatan (hari)', f'=MAX(D{mulai + 1}:D{akhir})', '0'),
    ]
    for i, (label, rumus, fmt) in enumerate(statistik, start=3):
        ws.cell(row=i, column=1, value=label).font = BOLD
        cell = ws.cell(row=i, column=4, value=rumus)
        cell.font = BOLD
        cell.number_format = fmt
    ws.freeze_panes = f'A{mulai + 1}'
    _lebar(ws, [9, 12, 12, 14, 7, 10, 14, 16, 16, 120])


def sheet_ringkasan(wb, ringkasan):
    ws = wb.create_sheet('Ringkasan')
    kolom = list(ringkasan[0].keys())
    _header(ws, 1, kolom)
    for r, b in enumerate(ringkasan, start=2):
        for c, k in enumerate(kolom, start=1):
            ws.cell(row=r, column=c, value=b[k])
    _lebar(ws, [12] * len(kolom))


def buat_workbook(path, aktivitas, orang, rencana, rencana_cpm, ringkasan, iterasi_utama, kelas_cr, p_cr):
    wb = Workbook()
    sheet_petunjuk(wb)
    sheet_parameter(wb, kelas_cr, p_cr)
    baris = sheet_jadwal_rencana(wb, aktivitas)
    sheet_jadwal_resource(wb, aktivitas, orang, rencana)
    sheet_simulasi(wb, aktivitas, baris, len(kelas_cr))
    sheet_hasil_iterasi(wb, iterasi_utama)
    sheet_ringkasan(wb, ringkasan)
    wb.save(path)
