# Absen Pribadi

Aplikasi tray Windows untuk mencatat jam masuk dan jam pulang kerja, berjalan sepenuhnya offline di komputer Anda sendiri. Muncul sebagai ikon kecil di tray — klik untuk buka popup, klik ikon lagi untuk menutup. Tidak perlu instalasi berat, tidak perlu server, tidak perlu internet untuk fungsi intinya.

Dibuat awalnya untuk kebutuhan pribadi, lalu dibuka sebagai open source karena mungkin berguna untuk orang lain dengan kebutuhan serupa.

> **Catatan:** ini adalah catatan absen **pribadi dan manual** — bukan sistem absensi resmi dan tidak terhubung/tersinkron dengan sistem HR atau absensi apa pun milik kantor Anda. Semua data hanya tersimpan di komputer Anda sendiri.

## Cara Pakai

1. Download `AbsenPribadi.exe` dari **[Releases](https://github.com/projectronic/absenpribadi/releases/latest/download/AbsenPribadi.exe)** (build terbaru, otomatis ter-update tiap ada perubahan di branch `main`).
2. Jalankan — ikonnya muncul di tray (dekat jam, pojok kanan bawah taskbar).
3. Klik ikon tray untuk buka popup. Tekan **Absen Masuk** saat tiba, dan **Absen Pulang** saat pulang.
4. Klik kanan ikon tray untuk menu cepat (Buka/Tutup, Keluar).

## Fitur

- **Absen masuk & pulang** — catat jam masuk otomatis dari jam komputer, dan jam pulang aktual saat Anda benar-benar pulang.
- **Jadwal kerja per hari** — atur jam masuk, istirahat, dan pulang untuk setiap hari (Senin–Minggu) secara independen lewat halaman Setting. Cocok untuk kantor dengan jam kerja yang berbeda di hari tertentu (misalnya jam Jumat yang lebih pendek karena ada waktu sholat Jumat).
- **Mode target jam pulang** — pilih **Waktu Pulang** (target selalu jam pulang tetap sesuai jadwal) atau **Waktu Kerja** (target = jam masuk aktual + total durasi kerja, tanpa dimajukan kalau datang lebih awal dari jadwal).
- **Hari libur otomatis** — tandai hari tertentu sebagai libur (misalnya Sabtu/Minggu), dan aplikasi tetap mengizinkan absen di hari libur tanpa memaksakan target jam kerja.
- **Kalender libur nasional Indonesia** — diperbarui otomatis dari internet tiap minggu saat online, dengan daftar hardcode sebagai fallback offline.
- **Hari libur tambahan** — tambahkan tanggal libur sendiri lewat Setting (mis. cuti bersama internal kantor) di luar kalender nasional.
- **Riwayat absen** — dikelompokkan per periode kerja, dengan tanggal cut-off yang bisa diatur sendiri lewat Setting (default tanggal 25), beserta rekap total jam lebih/kurang per periode. Setiap entri bisa diedit atau dihapus.
- **Kalender bulanan** — lihat ringkasan bulan penuh: hari libur ditandai warna berbeda, hari yang ada catatan absen ditandai titik kecil. Klik tanggal mana pun untuk melihat detailnya.
- **Tema gelap/terang** — toggle di Setting, ikut preferensi sistem secara default saat pertama kali dibuka.
- **Autostart Windows** — toggle di Setting, aplikasi otomatis terbuka setiap kali login Windows.
- **100% offline & privat** — semua data tersimpan lokal (lihat [Data & Privasi](#data--privasi) di bawah). Tidak ada data yang dikirim ke server mana pun, kecuali fetch kalender libur nasional (request GET publik ke [date.nager.at](https://date.nager.at/), tanpa data pribadi apa pun yang dikirim).

### Menyesuaikan jadwal & preferensi

Klik ikon ⚙️ di pojok kanan atas untuk membuka halaman **Setting**. Preferensi aplikasi (tema, autostart, ukuran jendela) langsung berlaku saat diubah. Jadwal kerja, mode target jam pulang, dan tanggal cut-off periode gajian perlu ditekan **Simpan** dulu untuk diterapkan — atau **Reset ke jadwal default** untuk mengembalikan jadwal ke pengaturan awal.

## Data & Privasi

Semua data (absen masuk/pulang, riwayat, jadwal kerja, setting) tersimpan lokal di:

```
%LOCALAPPDATA%\AbsenPribadi\
```

Untuk reset total, tutup aplikasi lalu hapus folder tersebut. Tidak ada data yang pernah dikirim ke server mana pun — satu-satunya request jaringan yang aplikasi ini lakukan adalah fetch kalender libur nasional dari API publik [date.nager.at](https://date.nager.at/) (read-only, tanpa autentikasi, tanpa data pribadi yang dikirim), dan itu pun opsional — kalau gagal/offline, aplikasi tetap jalan normal pakai daftar libur bawaan.

## Cara Lama (buka langsung di browser)

Sebelum jadi aplikasi tray, project ini berupa satu file HTML (`absen-pribadi.html`) yang dibuka langsung di browser. Cara ini masih didukung (berguna kalau bukan di Windows, atau tidak mau install apa pun) tapi bukan lagi cara pakai utama — lihat [Panduan Instalasi lama](./docs/legacy-browser/PANDUAN-INSTALASI.md) (tersedia juga dalam format [PDF](./docs/legacy-browser/Panduan-Instalasi-Absen-Pribadi.pdf)).

## Teknologi

- **UI**: `absen-pribadi.html` — HTML/CSS/JavaScript vanilla, tanpa framework atau build step. Tema light/dark pakai token CSS bergaya [shadcn/ui](https://ui.shadcn.com/). Ikon [Material Symbols](https://github.com/google/material-design-icons) (Google, lisensi Apache 2.0) sebagai SVG inline.
- **Tray app**: `absen_tray/` — Python, [pystray](https://github.com/moses-palmer/pystray) untuk ikon tray, [pywebview](https://pywebview.flowrl.com/) (Edge WebView2) untuk menampilkan `absen-pribadi.html` apa adanya di dalam popup. Autostart lewat Windows Registry (`winreg`, stdlib).
- Data libur nasional: fetch mingguan dari [date.nager.at](https://date.nager.at/) (sumber: [SKB 3 Menteri](https://holiday.forpublic.id/)), dengan daftar hardcode (`LIBUR_HARDCODE` di kode) sebagai fallback offline — tetap perlu di-update manual tiap akhir tahun sebagai jaring pengaman.

## Struktur

```
absenpribadi/
  absen-pribadi.html      UI aplikasi (dipakai baik oleh tray app maupun cara lama/browser)
  absen_tray/              tray app Python
    __main__.py               setup tray icon (pystray) + window pywebview yang memuat absen-pribadi.html
    posisi.py                  hitung posisi popup menempel pojok layar dekat taskbar
    status_bridge.py            jembatan JS <-> Python (status tray, autostart, ukuran jendela)
    autostart.py                baca/tulis Windows Registry Run key
    preferensi.py                simpan preferensi ukuran jendela (dibutuhkan sebelum webview jalan)
    icon.py                      gambar ikon tray dinamis (Pillow), warna berubah sesuai status
  run.py                   entry point PyInstaller
  requirements.txt
  docs/legacy-browser/     panduan instalasi cara lama (buka langsung di browser)
  .github/workflows/       CI: build .exe & publish ke GitHub Releases
```

## Menjalankan dari Source (Development)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m absen_tray
```

Butuh Edge WebView2 runtime — sudah bawaan Windows 10/11, tidak perlu install manual.

## Build Jadi Satu File Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AbsenPribadi --add-data "absen-pribadi.html;." run.py
```

(Di Linux/macOS, pemisah `--add-data` pakai `:` bukan `;`.) Hasilnya ada di `dist/AbsenPribadi.exe`.

### Build otomatis lewat GitHub Actions

Tidak perlu install Python di Windows sama sekali — workflow [`.github/workflows/build-tray-app.yml`](.github/workflows/build-tray-app.yml) build `.exe` otomatis di runner `windows-latest` tiap ada push ke `main`, lalu publish ulang sebagai **GitHub Release** bertag `latest` (link download permanen: `.../releases/latest/download/AbsenPribadi.exe`). Build mentah (belum di-publish sebagai release) juga tetap bisa diambil lewat tab **Actions** kalau perlu.

## Mengembangkan / Berkontribusi

1. Fork repo ini.
2. Untuk UI/logic: edit `absen-pribadi.html` langsung — bisa dibuka di browser untuk lihat hasilnya cepat tanpa perlu jalankan tray app (tapi fitur yang butuh bridge Python, seperti autostart & ukuran jendela, cuma aktif di dalam tray app).
3. Untuk perilaku tray/window: edit modul di `absen_tray/`.
4. Pastikan perubahan Anda tidak merusak fungsi yang sudah ada (absen masuk/pulang, kalender, riwayat, setting).
5. Kirim pull request.

Beberapa ide pengembangan yang mungkin berguna:

- Update data libur nasional untuk tahun-tahun berikutnya (cari bagian `LIBUR_HARDCODE`)
- Dukungan multi-bahasa (saat ini hanya Bahasa Indonesia)
- Ekspor riwayat ke CSV/Excel
- Dukungan multiple shift kerja dalam satu hari
- Posisi popup yang lebih akurat lintas multi-monitor & taskbar di posisi non-default (lihat `posisi.py`)

## Lisensi

```
Absen Pribadi
Copyright (C) 2026 Vicky Andhika
```

Proyek ini dilisensikan di bawah **GNU General Public License v3.0**. Lihat file [LICENSE](./LICENSE) untuk detail lengkap.

Singkatnya: Anda bebas menggunakan, memodifikasi, dan mendistribusikan ulang aplikasi ini — termasuk untuk tujuan komersial — selama versi modifikasi Anda juga tetap open source dengan lisensi yang sama.

## Disclaimer

Aplikasi ini dibuat untuk kebutuhan pencatatan personal dan bukan pengganti sistem absensi resmi perusahaan. Selalu ikuti kebijakan dan sistem absensi resmi yang ditetapkan oleh tempat kerja Anda.

---

Dibuat dengan ❤️ oleh Vicky Andhika.
