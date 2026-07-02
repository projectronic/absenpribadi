"""Entry point tray app.

Jalankan dari folder tray-app (setelah `pip install -r requirements.txt`):
    python -m absen_tray
"""
from __future__ import annotations

import threading
import tkinter as tk
from datetime import datetime

import pystray

from .icon import buat_icon_image
from .jadwal import hitung_target_pulang, jadwal_hari
from .state import Store
from .ui import StatusWindow


class AbsenTrayApp:
    def __init__(self):
        self.store = Store()
        self.root = tk.Tk()
        self.root.withdraw()  # tidak ada window utama yang terlihat — semua interaksi lewat popup/tray

        self.status_window: StatusWindow | None = None

        self.icon = pystray.Icon(
            "absen_pribadi",
            buat_icon_image("belum"),
            "Absen Pribadi",
            menu=pystray.Menu(
                pystray.MenuItem("Buka", self._minta_buka, default=True),
                pystray.MenuItem("Absen Masuk", self._minta_absen_masuk),
                pystray.MenuItem("Absen Pulang", self._minta_absen_pulang),
                pystray.MenuItem("Keluar", self._minta_keluar),
            ),
        )

        self._update_icon()
        self.root.after(1000, self._tick)

    # --- callback tray, jalan di thread pystray -> dijadwalkan ke main thread lewat root.after ---
    def _minta_buka(self, icon=None, item=None):
        self.root.after(0, self._buka_status)

    def _minta_absen_masuk(self, icon=None, item=None):
        self.root.after(0, self._absen_masuk_cepat)

    def _minta_absen_pulang(self, icon=None, item=None):
        self.root.after(0, self._absen_pulang_cepat)

    def _minta_keluar(self, icon=None, item=None):
        self.root.after(0, self._keluar)

    # --- eksekusi di main thread (aman untuk sentuh widget Tkinter) ---
    def _buka_status(self):
        if self.status_window is not None and self.status_window.winfo_exists():
            self.status_window.lift()
            self.status_window.focus_force()
            return
        self.status_window = StatusWindow(self.root, self.store, on_ubah=self._update_icon)

    def _absen_masuk_cepat(self):
        if not self.store.get_absen_masuk():
            self.store.set_absen_masuk(datetime.now())
            self._update_icon()
        self._buka_status()

    def _absen_pulang_cepat(self):
        absen_masuk = self.store.get_absen_masuk()
        if absen_masuk:
            self.store.tambah_riwayat(absen_masuk, datetime.now(), True)
            self.store.clear_absen_masuk()
            self._update_icon()
        self._buka_status()

    def _keluar(self):
        self.icon.stop()
        self.root.quit()

    def _tick(self):
        self._update_icon()
        self.root.after(1000, self._tick)

    def _update_icon(self):
        absen_masuk = self.store.get_absen_masuk()
        if not absen_masuk:
            status, tooltip = "belum", "Absen Pribadi — belum absen masuk"
        else:
            jadwal_hari_ini = jadwal_hari(absen_masuk, self.store.get_jadwal_kerja())
            if jadwal_hari_ini["libur"]:
                status = "libur"
                tooltip = f"Absen Pribadi — masuk {absen_masuk.strftime('%H:%M')} (hari libur)"
            else:
                jam_pulang = hitung_target_pulang(absen_masuk, jadwal_hari_ini, self.store.get_mode())
                sisa_detik = int((jam_pulang - datetime.now()).total_seconds())
                if sisa_detik <= 0:
                    status, tooltip = "boleh_pulang", "Absen Pribadi — sudah boleh pulang"
                else:
                    status = "bekerja"
                    j, sisa = divmod(sisa_detik, 3600)
                    m = sisa // 60
                    tooltip = f"Absen Pribadi — sisa {j}j {m}m menuju jam pulang"
        self.icon.icon = buat_icon_image(status)
        self.icon.title = tooltip

    def run(self):
        threading.Thread(target=self.icon.run, daemon=True).start()
        self.root.mainloop()


def main():
    AbsenTrayApp().run()


if __name__ == "__main__":
    main()
