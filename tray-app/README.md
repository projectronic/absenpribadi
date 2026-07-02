# Absen Pribadi — Tray App (scaffold)

Versi system-tray dari [`absen-pribadi.html`](../absen-pribadi.html), dibangun seperti
[Usage Monitor for Claude](https://github.com/jens-duttke/usage-monitor-for-claude):
ikon di tray/menu bar, klik untuk buka popup status, klik kanan untuk menu cepat.

Logika jadwal kerja (`absen_tray/jadwal.py`) adalah port langsung dari fungsi-fungsi
di `absen-pribadi.html`, termasuk mode **Waktu Pulang** (target tetap sesuai jadwal)
dan **Waktu Kerja** (target = jam masuk aktual + durasi kerja).

## Menjalankan (development)

```bash
cd tray-app
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m absen_tray
```

**Linux**: `tkinter` bukan bagian dari `pip install`, biasanya perlu paket sistem
terpisah, mis. `sudo apt install python3-tk` (Debian/Ubuntu) sebelum menjalankan.
Windows & macOS umumnya sudah menyertakan `tkinter` di instalasi Python resmi.

## Build jadi satu file executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AbsenPribadi run.py
```

Hasilnya ada di `dist/AbsenPribadi.exe` (Windows) atau `dist/AbsenPribadi` (Linux/macOS).

## Build otomatis lewat GitHub Actions

Tidak perlu install Python di Windows sama sekali — workflow
[`.github/workflows/build-tray-app.yml`](../.github/workflows/build-tray-app.yml) build
`.exe` otomatis di runner `windows-latest` tiap kali ada push ke `tray-app/**` di branch
`main`, atau dipicu manual lewat tab **Actions** (tombol "Run workflow").

Cara ambil hasilnya: buka repo di GitHub → tab **Actions** → pilih run terbaru dari
workflow "Build Absen Pribadi Tray App (Windows)" → download artifact
**AbsenPribadi-windows** di bagian bawah halaman run tersebut → extract, dapat
`AbsenPribadi.exe`.

## Struktur

```
tray-app/
  run.py                 entry point untuk PyInstaller
  absen_tray/
    __main__.py           setup tray icon (pystray) + main loop Tkinter
    jadwal.py              logika jadwal kerja & target jam pulang (port dari .html)
    state.py                penyimpanan state (JSON di ~/.absen_pribadi/state.json)
    icon.py                 gambar ikon tray dinamis (Pillow), warna berubah sesuai status
    ui.py                   jendela Tkinter: status popup, riwayat, setting
```

State disimpan di `~/.absen_pribadi/state.json` — kalau butuh reset total, hapus file
ini (mirip clear localStorage di versi HTML).

## Yang belum diimplementasikan (dibanding versi HTML)

Ini scaffold/MVP, bukan port 1:1. Yang sengaja belum dibawa ke sini:

- Kalender bulanan & integrasi hari libur nasional (`LIBUR_HARDCODE` / fetch nager.at).
- Pengelompokan riwayat per periode gajian (cut-off tgl 26–25) beserta rekap per periode.
- Edit jam masuk/pulang pada entri riwayat yang sudah tercatat (saat ini cuma bisa dihapus).

Semua fitur di atas ada & jalan penuh di `absen-pribadi.html` — dua versi ini independen,
tidak saling sinkron datanya (state tray app terpisah dari localStorage browser).
