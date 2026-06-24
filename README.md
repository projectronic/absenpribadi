# Absen Pribadi

Aplikasi sederhana untuk menghitung jam masuk dan jam pulang kerja, berjalan sepenuhnya offline di komputer Anda sendiri. Tidak perlu instalasi, tidak perlu server, tidak perlu internet — cukup satu file HTML yang bisa otomatis terbuka setiap kali Windows menyala.

Dibuat awalnya untuk kebutuhan pribadi, lalu dibuka sebagai open source karena mungkin berguna untuk orang lain dengan kebutuhan serupa.

> **Catatan:** ini adalah catatan absen **pribadi dan manual** — bukan sistem absensi resmi dan tidak terhubung/tersinkron dengan sistem HR atau absensi apa pun milik kantor Anda. Semua data hanya tersimpan di komputer Anda sendiri.

## Fitur

- **Absen masuk & pulang** — catat jam masuk otomatis dari jam komputer, dan jam pulang aktual saat Anda benar-benar pulang.
- **Jadwal kerja per hari** — atur jam masuk, istirahat, dan pulang untuk setiap hari (Senin–Minggu) secara independen lewat halaman Setting. Cocok untuk kantor dengan jam kerja yang berbeda di hari tertentu (misalnya jam Jumat yang lebih pendek karena ada waktu sholat Jumat).
- **Hari libur otomatis** — tandai hari tertentu sebagai libur (misalnya Sabtu/Minggu), dan aplikasi tetap mengizinkan absen di hari libur tanpa memaksakan target jam kerja.
- **Kalender libur nasional Indonesia** — tanggal merah dan cuti bersama (berdasarkan SKB 3 Menteri) sudah tertanam di dalam aplikasi, tidak perlu koneksi internet.
- **Riwayat absen** — semua riwayat dikelompokkan per periode kerja (mendukung cut-off tanggal kustom, misalnya tanggal 26–25 untuk siklus penggajian), dengan rekap total jam lebih/kurang per periode. Setiap entri bisa diedit atau dihapus.
- **Kalender bulanan** — lihat ringkasan bulan penuh: hari libur ditandai warna berbeda, hari yang ada catatan absen ditandai titik kecil. Klik tanggal mana pun untuk melihat detailnya.
- **Auto-start Windows** — bisa diatur agar otomatis terbuka setiap kali Windows login, dalam jendela kecil tanpa address bar (mirip aplikasi native).
- **100% offline & privat** — semua data tersimpan di `localStorage` browser Anda sendiri. Tidak ada data yang dikirim ke server mana pun.

## Cara Pakai

1. Download file [`absen-pribadi.html`](./absen-pribadi.html).
2. Buka langsung dua kali klik di browser apa saja (Chrome, Edge, Firefox).
3. Tekan **Absen Masuk** saat tiba, dan **Absen Pulang** saat pulang.

Untuk panduan instalasi lengkap (termasuk cara membuat aplikasi ini otomatis terbuka setiap Windows menyala, dengan ukuran jendela yang rapi), lihat [Panduan Instalasi](./PANDUAN-INSTALASI.md) yang ditulis untuk pengguna non-teknis — tersedia juga dalam format [PDF](./Panduan-Instalasi-Absen-Pribadi.pdf) untuk dicetak atau dibaca offline.

### Menyesuaikan jadwal kerja

Klik ikon ⚙️ di pojok kanan atas untuk membuka halaman **Setting**. Di sana Anda bisa atur untuk setiap hari:

- Tandai sebagai **Libur** (form jam akan otomatis tersembunyi), atau
- Atur jam **Masuk**, **Istirahat**, **Masuk Lagi**, dan **Pulang**.

Klik **Simpan** untuk menerapkan, atau **Reset ke jadwal default** untuk mengembalikan ke pengaturan awal.

## Teknologi

Satu file HTML — tanpa framework, tanpa build step, tanpa dependency eksternal apa pun saat runtime. Menggunakan:

- HTML, CSS, dan JavaScript vanilla
- `localStorage` browser untuk menyimpan data absen, riwayat, dan jadwal kerja
- Ikon [Material Symbols](https://github.com/google/material-design-icons) (Google, lisensi Apache 2.0) sebagai SVG inline — tidak ada permintaan jaringan untuk ikon
- Data libur nasional di-hardcode langsung di dalam file (lihat bagian `LIBUR_HARDCODE` di kode), bersumber dari [SKB 3 Menteri](https://holiday.forpublic.id/) — diperbarui manual setiap tahun, biasanya sekitar bulan September untuk tahun berikutnya

## Mengembangkan / Berkontribusi

Karena ini cuma satu file HTML, cara paling mudah untuk berkontribusi:

1. Fork repo ini.
2. Edit `absen-pribadi.html` langsung — buka di browser untuk melihat hasilnya secara langsung (tidak perlu build step).
3. Pastikan perubahan Anda tidak merusak fungsi yang sudah ada (absen masuk/pulang, kalender, riwayat, setting).
4. Kirim pull request.

Beberapa ide pengembangan yang mungkin berguna:

- Update data libur nasional untuk tahun-tahun berikutnya (cari bagian `LIBUR_HARDCODE`)
- Dukungan multi-bahasa (saat ini hanya Bahasa Indonesia)
- Ekspor riwayat ke CSV/Excel
- Dukungan multiple shift kerja dalam satu hari

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
