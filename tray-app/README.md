# Absen Pribadi — Tray App

Versi system-tray dari [`absen-pribadi.html`](../absen-pribadi.html): ikon di tray,
klik untuk buka popup status, klik kanan untuk menu cepat.

UI-nya bukan ditulis ulang pakai widget native — popup yang muncul memuat
`absen-pribadi.html` apa adanya lewat [pywebview](https://pywebview.flowrl.com/)
(Edge WebView2 di Windows), jadi tampilannya identik dengan versi HTML dan otomatis
ikut semua fiturnya (kalender, hari libur nasional, riwayat per periode, mode
**Waktu Pulang**/**Waktu Kerja**, dll) tanpa perlu port ulang logikanya ke Python.
State (absen masuk, riwayat, jadwal, setting) ikut localStorage bawaan WebView2.

## Menjalankan (development)

```bash
cd tray-app
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m absen_tray
```

Butuh Edge WebView2 runtime — sudah bawaan Windows 10/11, tidak perlu install manual.

## Build jadi satu file executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AbsenPribadi --add-data "../absen-pribadi.html;." run.py
```

(Di Linux/macOS, pemisah `--add-data` pakai `:` bukan `;`.)

Hasilnya ada di `dist/AbsenPribadi.exe` (Windows).

## Build otomatis lewat GitHub Actions

Tidak perlu install Python di Windows sama sekali — workflow
[`.github/workflows/build-tray-app.yml`](../.github/workflows/build-tray-app.yml) build
`.exe` otomatis di runner `windows-latest` tiap kali ada push ke `tray-app/**` atau
`absen-pribadi.html` di branch `main`, atau dipicu manual lewat tab **Actions** (tombol
"Run workflow").

Cara ambil hasilnya: buka repo di GitHub → tab **Actions** → pilih run terbaru dari
workflow "Build Absen Pribadi Tray App (Windows)" → download artifact
**AbsenPribadi-windows** di bagian bawah halaman run tersebut → extract, dapat
`AbsenPribadi.exe`.

## Struktur

```
tray-app/
  run.py                     entry point PyInstaller
  absen_tray/
    __main__.py                 setup tray icon (pystray) + window pywebview yang memuat ../absen-pribadi.html
    posisi.py                    hitung posisi popup menempel pojok layar (perkiraan taskbar di bawah)
    status_bridge.py              jembatan status dari JS (di dalam webview) ke Python, buat update ikon tray
    icon.py                       gambar ikon tray dinamis (Pillow), warna berubah sesuai status
```

## Keterbatasan

- Posisi popup (`posisi.py`) disederhanakan — cuma asumsi taskbar di bawah, monitor
  utama. Belum menangani taskbar di kiri/kanan/atas atau layout multi-monitor.
- Popup tidak bisa di-drag, dan tidak otomatis tertutup saat klik di luar jendela —
  toggle buka/tutup lewat klik ikon tray.
- Belum dites end-to-end di Windows sungguhan (dibuat & dicek sintaksnya dari
  lingkungan Linux tanpa display) — kemungkinan ada isu PyInstaller hidden-imports
  untuk backend WebView2 yang baru ketahuan saat build/run sungguhan.
