# Panduan Instalasi — Absen Pribadi

Aplikasi sederhana penghitung jam masuk & jam pulang kerja, otomatis terbuka setiap komputer Windows dinyalakan.

> **Catatan:** ini aplikasi pencatatan pribadi & manual, bukan sistem absensi resmi kantor. Tidak ada data yang dikirim ke server mana pun — semuanya tersimpan di komputer Anda sendiri.

Panduan ini ditulis untuk pengguna awam — tidak perlu pengalaman teknis.

## Daftar Isi

- [Bagian 1 — Yang Anda Butuhkan](#bagian-1--yang-anda-butuhkan)
- [Bagian 2 — Memasang File](#bagian-2--memasang-file)
- [Bagian 3 — Membuat Shortcut Otomatis](#bagian-3--membuat-shortcut-otomatis)
- [Bagian 4 — Cara Menggunakan](#bagian-4--cara-menggunakan)
- [Bagian 5 — Menyesuaikan Jam Kerja](#bagian-5--menyesuaikan-jam-kerja)
- [Bagian 6 — Mengatasi Masalah Umum](#bagian-6--mengatasi-masalah-umum)

---

## Bagian 1 — Yang Anda Butuhkan

Sebelum mulai, pastikan beberapa hal berikut:

| Kebutuhan | Keterangan |
|---|---|
| Komputer Windows 10 / 11 | Sudah terpasang secara default di semua laptop/PC Windows |
| Browser Microsoft Edge atau Google Chrome | Edge sudah ada di Windows secara default |
| File `absen-pribadi.html` | File aplikasi yang akan Anda terima (dari teman/rekan kerja, atau download dari repo ini) |

> **Tidak perlu internet.** Aplikasi ini berjalan sepenuhnya di komputer Anda sendiri, tidak mengirim data ke mana pun.

---

## Bagian 2 — Memasang File

### 1. Buat folder khusus

Buat folder baru di komputer Anda untuk menyimpan aplikasi ini. Lokasi yang disarankan:

```
C:\Users\NamaAnda\AbsenPribadi
```

Ganti `NamaAnda` dengan nama folder pengguna Windows Anda (biasanya ini sudah otomatis terisi saat Anda membuka File Explorer).

### 2. Simpan file aplikasi

Pindahkan / simpan file `absen-pribadi.html` yang Anda terima ke dalam folder `AbsenPribadi` tersebut.

> **Tips:** Pastikan nama file dan lokasi foldernya Anda catat — Anda akan membutuhkannya di langkah berikutnya.

---

## Bagian 3 — Membuat Shortcut Otomatis

Langkah ini membuat aplikasi otomatis terbuka setiap kali Windows Anda dinyalakan / login, dengan ukuran jendela yang pas.

### 1. Buka folder Startup Windows

Tekan tombol `Windows` + `R` secara bersamaan, lalu ketik:

```
shell:startup
```

Tekan **Enter**. Sebuah folder akan terbuka — ini adalah folder khusus yang isinya otomatis dijalankan setiap Windows menyala.

### 2. Buat shortcut baru

Di area kosong folder tadi, klik kanan mouse, lalu pilih:

**New** → **Shortcut**

### 3. Isi lokasi shortcut

Akan muncul kotak isian "Type the location of the item". Salin (copy-paste) salah satu baris berikut, sesuai browser yang Anda pakai:

**Jika pakai Microsoft Edge:**

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app="file:///C:/Users/NamaAnda/AbsenPribadi/absen-pribadi.html" --window-size=430,502 --window-position=750,100 --user-data-dir="C:\Users\NamaAnda\AbsenPribadi\EdgeProfile"
```

**Jika pakai Google Chrome:**

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --app="file:///C:/Users/NamaAnda/AbsenPribadi/absen-pribadi.html" --window-size=430,502 --window-position=750,100 --user-data-dir="C:\Users\NamaAnda\AbsenPribadi\ChromeProfile"
```

> **Penting:** Ganti semua tulisan `NamaAnda` dengan nama folder pengguna Windows Anda yang sebenarnya (lihat langkah 1 di Bagian 2). Jangan ada bagian yang masih bertuliskan "NamaAnda" secara harfiah.

Klik **Next**, lalu beri nama shortcut ini misalnya *"Absen Pribadi"*, lalu klik **Finish**.

### 4. Coba jalankan

Klik dua kali (double-click) shortcut yang baru dibuat. Jendela aplikasi "Absen Pribadi" akan muncul. Jika muncul dengan ukuran kecil dan rapi (tidak memenuhi layar), berarti berhasil.

> **Tips posisi jendela:** Jika posisi jendela kurang pas di layar Anda, geser (drag) manual title bar-nya ke posisi yang nyaman, lalu tutup. Buka lagi untuk mengecek apakah posisinya tersimpan. Kalau ternyata jendela tetap muncul memenuhi layar (maximized) walau sudah pakai `--window-size`, lihat solusinya di [Bagian 6](#bagian-6--mengatasi-masalah-umum).

---

## Bagian 4 — Cara Menggunakan

### 1. Saat tiba di kantor

Buka aplikasi (otomatis terbuka jika komputer baru dinyalakan, atau klik shortcut-nya). Tekan tombol **"Absen Masuk"**. Jam masuk akan tercatat otomatis dari jam komputer Anda saat itu.

### 2. Selama bekerja

Aplikasi akan menampilkan hitungan mundur (*countdown*) menuju jam pulang sesuai jadwal hari itu, beserta jam masuk dan jam pulang target.

### 3. Saat pulang kerja

Tekan tombol **"Absen Pulang"** saat Anda benar-benar akan pulang. Jam pulang sebenarnya akan tercatat, dan otomatis tersimpan ke riwayat.

> **Lupa tekan "Absen Pulang"?** Tidak masalah — tekan tombol kecil *"Lupa absen pulang?"* di bawahnya. Sistem akan mencatat jam pulang sesuai jadwal target hari itu.

### 4. Melihat riwayat

Tekan tombol **"Lihat Riwayat"** untuk melihat catatan absen Anda. Riwayat dikelompokkan per periode kerja (tanggal 26 hingga 25 bulan berikutnya), beserta total jam lebih atau kurang dalam periode tersebut.

Setiap catatan harian bisa di-**Edit** (jika salah catat jam) atau **Hapus** melalui tombol yang tersedia di tiap baris.

### 5. Melihat kalender

Klik ikon kalender (📅) di pojok kiri atas untuk melihat ringkasan bulan penuh. Hari libur ditandai warna kuning, hari yang ada catatan absen ditandai titik kecil. Klik tanggal mana pun untuk melihat detailnya.

---

## Bagian 5 — Menyesuaikan Jam Kerja

Aplikasi ini sudah punya halaman **Setting** bawaan untuk mengatur jam kerja — Anda tidak perlu mengedit kode atau file apa pun.

### 1. Buka halaman Setting

Klik ikon gerigi (⚙️) di pojok kanan atas jendela aplikasi.

### 2. Atur jadwal per hari

Anda akan melihat daftar tujuh hari (Senin–Minggu). Untuk setiap hari, ada dua pilihan:

- **Tandai sebagai Libur** — centang kotak "Libur" jika hari itu tidak ada jadwal kerja (misalnya Sabtu/Minggu). Form jam akan otomatis tersembunyi.
- **Atur jam kerja** — isi empat kolom waktu: **Masuk**, **Istirahat** (mulai), **Masuk Lagi** (selesai istirahat), dan **Pulang**.

Ini juga berguna untuk hari dengan jadwal khusus, misalnya Jumat dengan jam istirahat lebih panjang karena ada waktu sholat Jumat (contoh: masuk 08:00, istirahat 11:00–13:30, pulang 17:00).

### 3. Simpan

Klik tombol **Simpan** di bagian bawah untuk menerapkan perubahan. Jika ingin mengembalikan ke pengaturan awal, klik **"Reset ke jadwal default"**.

> **Catatan:** hari yang ditandai libur tetap mengizinkan Anda menekan "Absen Masuk" jika kebetulan masuk kerja di hari itu — hanya saja tidak akan ada target jam pulang otomatis, dan riwayatnya tidak dihitung sebagai kelebihan/kekurangan jam.

---

## Bagian 6 — Mengatasi Masalah Umum

### 1. Jendela muncul terlalu besar / memenuhi layar

Tutup aplikasinya. Hapus folder `EdgeProfile` (atau `ChromeProfile`) di dalam folder `AbsenPribadi` Anda, lalu buka kembali lewat shortcut.

Jika masih bermasalah, coba tambahkan parameter `--user-data-dir` yang mengarah ke folder profil baru/bersih (lihat contoh command di [Bagian 3](#bagian-3--membuat-shortcut-otomatis)) — ini memastikan Edge/Chrome tidak memakai pengaturan ukuran jendela lama yang tersimpan dari sesi sebelumnya.

### 2. Shortcut tidak bisa dibuka / error "file tidak ditemukan"

Periksa kembali isi shortcut (klik kanan shortcut → **Properties** → lihat kolom **Target**). Pastikan:

- Nama folder pengguna (`NamaAnda`) sudah diganti dengan benar
- Lokasi file `absen-pribadi.html` sesuai dengan tempat Anda menyimpannya
- Tidak ada huruf atau tanda kutip yang hilang saat disalin

### 3. Data riwayat hilang

Data tersimpan di dalam folder `EdgeProfile`/`ChromeProfile` pada folder aplikasi Anda. Jangan menghapus atau memindahkan folder ini secara terpisah dari file `absen-pribadi.html`.

> **Mau pindah komputer?** Salin seluruh folder `AbsenPribadi` (termasuk folder profil di dalamnya) ke komputer baru, lalu buat ulang shortcut-nya mengikuti [Bagian 3](#bagian-3--membuat-shortcut-otomatis).

### 4. Ikon kalender/setting samar atau hari/tanggal tidak terlihat

Pastikan Anda memakai versi file `absen-pribadi.html` terbaru dari repo ini — beberapa perbaikan tampilan (kontras ikon, tanggal di header) ditambahkan setelah versi awal.

---

Selesai — selamat menggunakan Absen Pribadi!
