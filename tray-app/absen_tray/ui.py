"""Jendela Tkinter: status popup, riwayat, & setting jadwal.

Catatan lingkup (MVP — belum sepenuhnya menyamai versi HTML):
  - Riwayat ditampilkan flat (belum dikelompokkan per periode gajian tgl 26-25).
  - Item riwayat cuma bisa dihapus dari sini, belum bisa diedit jam masuk/pulangnya.
  - Kalender & integrasi hari libur nasional belum diimplementasikan.
Semua bagian di atas ada di absen-pribadi.html kalau butuh fitur lengkap.
"""
from __future__ import annotations

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk
from typing import Optional

from .jadwal import (
    HARI_LABEL,
    HARI_LIST,
    JADWAL_DEFAULT,
    fmt_jadwal_singkat,
    hitung_target_pulang,
    jadwal_hari,
    total_jam_jadwal,
)


def _fmt_jam_singkat(d: datetime, beda_hari: int = 0) -> str:
    jam = d.strftime("%H:%M")
    return f"{jam} (+{beda_hari}h)" if beda_hari > 0 else jam


def _fmt_durasi(delta: timedelta) -> str:
    total_menit = round(delta.total_seconds() / 60)
    j, m = divmod(total_menit, 60)
    return f"{j} jam {m} menit"


def _fmt_sisa(delta: timedelta) -> str:
    total_detik = int(delta.total_seconds())
    if total_detik <= 0:
        return "Sudah boleh pulang"
    j, sisa = divmod(total_detik, 3600)
    m, s = divmod(sisa, 60)
    return f"{j:02d}:{m:02d}:{s:02d}"


def _fmt_selisih(durasi: timedelta, target: Optional[timedelta]) -> str:
    if target is None:
        return "Tidak ada target (hari libur)"
    selisih_detik = durasi.total_seconds() - target.total_seconds()
    abs_menit = round(abs(selisih_detik) / 60)
    j, m = divmod(abs_menit, 60)
    teks = f"{j} jam {m} menit"
    if abs(selisih_detik) < 60:
        return "Pas, sesuai target"
    return f"Lebih {teks}" if selisih_detik > 0 else f"Kurang {teks}"


class StatusWindow(tk.Toplevel):
    """Jendela utama: jam berjalan, status absen hari ini, & tombol aksi."""

    def __init__(self, master, store, on_ubah):
        super().__init__(master)
        self.store = store
        self.on_ubah = on_ubah  # dipanggil tiap state berubah, supaya ikon tray ikut ter-update
        self.title("Absen Pribadi")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.frame = ttk.Frame(self, padding=16)
        self.frame.pack(fill="both", expand=True)

        self._tick_id = None
        self._render()
        self._tick()

    def destroy(self):
        if self._tick_id is not None:
            self.after_cancel(self._tick_id)
        super().destroy()

    def _tick(self):
        self._render()
        self._tick_id = self.after(1000, self._tick)

    def _render(self):
        for w in self.frame.winfo_children():
            w.destroy()

        now = datetime.now()
        ttk.Label(self.frame, text=now.strftime("%H:%M:%S"), font=("Segoe UI", 20, "bold")).pack()
        ttk.Label(self.frame, text=now.strftime("%A, %d %B %Y")).pack(pady=(0, 12))

        absen_masuk = self.store.get_absen_masuk()
        if not absen_masuk:
            ttk.Button(self.frame, text="Absen Masuk", command=self._absen_masuk).pack(fill="x", pady=4)
            baris = ttk.Frame(self.frame)
            baris.pack(fill="x", pady=(4, 0))
            ttk.Button(baris, text="Riwayat", command=self._buka_riwayat).pack(side="left", expand=True, fill="x", padx=(0, 4))
            ttk.Button(baris, text="Setting", command=self._buka_setting).pack(side="left", expand=True, fill="x", padx=(4, 0))
            return

        jadwal_kerja = self.store.get_jadwal_kerja()
        jadwal_hari_ini = jadwal_hari(absen_masuk, jadwal_kerja)
        ada_target = not jadwal_hari_ini["libur"]
        mode = self.store.get_mode()

        info = ttk.Frame(self.frame)
        info.pack(fill="x", pady=(0, 8))
        ttk.Label(info, text="Jam Masuk").grid(row=0, column=0, padx=8)
        ttk.Label(info, text=_fmt_jam_singkat(absen_masuk), font=("Segoe UI", 12, "bold")).grid(row=1, column=0, padx=8)

        if ada_target:
            jam_pulang = hitung_target_pulang(absen_masuk, jadwal_hari_ini, mode)
            beda_hari = (jam_pulang.date() - absen_masuk.date()).days
            sisa = jam_pulang - now
            ttk.Label(info, text="Jam Pulang").grid(row=0, column=1, padx=8)
            ttk.Label(info, text=_fmt_jam_singkat(jam_pulang, beda_hari), font=("Segoe UI", 12, "bold")).grid(row=1, column=1, padx=8)
            ttk.Label(self.frame, text=("Status" if sisa.total_seconds() <= 0 else "Sisa waktu")).pack()
            ttk.Label(self.frame, text=_fmt_sisa(sisa), font=("Segoe UI", 16, "bold")).pack(pady=(0, 8))
            catatan = f"Jadwal hari ini: {fmt_jadwal_singkat(jadwal_hari_ini)}"
            if mode == "kerja":
                catatan += " · mode: waktu kerja"
            ttk.Label(self.frame, text=catatan, wraplength=260, justify="center").pack(pady=(0, 8))
        else:
            durasi = now - absen_masuk
            ttk.Label(self.frame, text="Sudah berjalan").pack()
            ttk.Label(self.frame, text=_fmt_durasi(durasi), font=("Segoe UI", 16, "bold")).pack(pady=(0, 8))
            ttk.Label(
                self.frame,
                text="Hari ini tidak ada jadwal kerja (libur) — absen tetap tercatat tanpa target jam pulang.",
                wraplength=260, justify="center",
            ).pack(pady=(0, 8))

        ttk.Button(self.frame, text="Absen Pulang", command=self._absen_pulang).pack(fill="x", pady=4)
        baris = ttk.Frame(self.frame)
        baris.pack(fill="x")
        ttk.Button(baris, text="Riwayat", command=self._buka_riwayat).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(baris, text="Lupa Pulang?", command=self._lupa_pulang).pack(side="left", expand=True, fill="x", padx=(4, 0))
        ttk.Button(self.frame, text="Setting Jadwal", command=self._buka_setting).pack(fill="x", pady=(8, 0))

    def _absen_masuk(self):
        self.store.set_absen_masuk(datetime.now())
        self._render()
        self.on_ubah()

    def _absen_pulang(self):
        absen_masuk = self.store.get_absen_masuk()
        self.store.tambah_riwayat(absen_masuk, datetime.now(), True)
        self.store.clear_absen_masuk()
        self._render()
        self.on_ubah()

    def _lupa_pulang(self):
        # Kalau ada target terjadwal, jam pulang tercatat = target. Kalau hari libur
        # (tidak ada target), jam pulang tercatat = waktu sekarang. Sama seperti versi HTML.
        absen_masuk = self.store.get_absen_masuk()
        jadwal_kerja = self.store.get_jadwal_kerja()
        jadwal_hari_ini = jadwal_hari(absen_masuk, jadwal_kerja)
        ada_target = not jadwal_hari_ini["libur"]
        if ada_target:
            pulang = hitung_target_pulang(absen_masuk, jadwal_hari_ini, self.store.get_mode())
            aktual = False
        else:
            pulang = datetime.now()
            aktual = True
        self.store.tambah_riwayat(absen_masuk, pulang, aktual)
        self.store.clear_absen_masuk()
        self._render()
        self.on_ubah()

    def _buka_riwayat(self):
        RiwayatWindow(self, self.store)

    def _buka_setting(self):
        SettingWindow(self, self.store)


class RiwayatWindow(tk.Toplevel):
    """Daftar riwayat absen (flat, terbaru di atas) — bisa dihapus per baris."""

    def __init__(self, master, store):
        super().__init__(master)
        self.store = store
        self.title("Riwayat Absen")
        self.geometry("520x360")

        kolom = ("tanggal", "masuk", "pulang", "durasi", "selisih")
        judul = ("Tanggal", "Masuk", "Pulang", "Durasi", "Selisih")
        self.tree = ttk.Treeview(self, columns=kolom, show="headings")
        for k, j, lebar in zip(kolom, judul, (110, 60, 60, 110, 160)):
            self.tree.heading(k, text=j)
            self.tree.column(k, width=lebar, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        ttk.Button(self, text="Hapus yang dipilih", command=self._hapus).pack(pady=(0, 8))
        self._muat()

    def _muat(self):
        self.tree.delete(*self.tree.get_children())
        jadwal_kerja = self.store.get_jadwal_kerja()
        for item in self.store.get_riwayat():
            masuk = datetime.fromtimestamp(item["masuk"] / 1000)
            pulang = datetime.fromtimestamp(item["pulang"] / 1000)
            durasi = pulang - masuk
            jadwal_hari_ini = jadwal_hari(masuk, jadwal_kerja)
            target = None if jadwal_hari_ini["libur"] else total_jam_jadwal(jadwal_hari_ini)
            self.tree.insert("", "end", iid=item["id"], values=(
                masuk.strftime("%d %b %Y"), masuk.strftime("%H:%M"), pulang.strftime("%H:%M"),
                _fmt_durasi(durasi), _fmt_selisih(durasi, target),
            ))

    def _hapus(self):
        for iid in self.tree.selection():
            self.store.hapus_riwayat(iid)
        self._muat()


class SettingWindow(tk.Toplevel):
    """Setting mode perhitungan target jam pulang & jadwal kerja per hari."""

    def __init__(self, master, store):
        super().__init__(master)
        self.store = store
        self.title("Setting Jadwal Kerja")
        self.resizable(False, False)

        self.mode_var = tk.StringVar(value=store.get_mode())
        mode_frame = ttk.LabelFrame(self, text="Mode target jam pulang", padding=8)
        mode_frame.pack(fill="x", padx=8, pady=8)
        ttk.Radiobutton(mode_frame, text="Waktu Pulang — tetap sesuai jadwal", value="pulang", variable=self.mode_var).pack(anchor="w")
        ttk.Radiobutton(mode_frame, text="Waktu Kerja — jam masuk + durasi kerja", value="kerja", variable=self.mode_var).pack(anchor="w")

        jadwal_frame = ttk.LabelFrame(self, text="Jadwal per hari (masuk / istirahat mulai / masuk lagi / pulang)", padding=8)
        jadwal_frame.pack(fill="both", padx=8, pady=(0, 8))

        self.draft = {h: dict(v) for h, v in store.get_jadwal_kerja().items()}
        self.widgets = {}
        for row, hari in enumerate(HARI_LIST):
            j = self.draft[hari]
            ttk.Label(jadwal_frame, text=HARI_LABEL[hari], width=8).grid(row=row, column=0, sticky="w", pady=2)
            libur_var = tk.BooleanVar(value=j["libur"])
            ttk.Checkbutton(jadwal_frame, text="Libur", variable=libur_var).grid(row=row, column=1)
            entri = {}
            for col, field in enumerate(("masuk", "istirahatMulai", "istirahatSelesai", "pulang"), start=2):
                var = tk.StringVar(value=j[field])
                ttk.Entry(jadwal_frame, textvariable=var, width=6).grid(row=row, column=col, padx=2)
                entri[field] = var
            self.widgets[hari] = {"libur": libur_var, **entri}

        tombol = ttk.Frame(self)
        tombol.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Button(tombol, text="Simpan", command=self._simpan).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(tombol, text="Reset Default", command=self._reset_default).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def _simpan(self):
        jadwal_baru = {}
        for hari, w in self.widgets.items():
            jadwal_baru[hari] = {
                "libur": w["libur"].get(),
                "masuk": w["masuk"].get(),
                "istirahatMulai": w["istirahatMulai"].get(),
                "istirahatSelesai": w["istirahatSelesai"].get(),
                "pulang": w["pulang"].get(),
            }
        self.store.set_jadwal_kerja(jadwal_baru)
        self.store.set_mode(self.mode_var.get())
        self.destroy()

    def _reset_default(self):
        for hari, w in self.widgets.items():
            j = JADWAL_DEFAULT[hari]
            w["libur"].set(j["libur"])
            for field in ("masuk", "istirahatMulai", "istirahatSelesai", "pulang"):
                w[field].set(j[field])
