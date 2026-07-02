"""Jembatan JS (di dalam webview) <-> Python — satu-satunya objek js_api yang diterima
pywebview per window, jadi semua kebutuhan bridge (status tray, autostart, ukuran jendela)
ditaruh di sini sebagai method-method class yang sama, bukan objek terpisah.

absen-pribadi.html memanggil window.pywebview.api.laporkan_status(status, tooltip) tiap
detik lewat laporkanStatusKeTray() — nilai terakhir disimpan di sini, dibaca oleh loop tray
(__main__.py) untuk mengganti warna ikon & tooltip. Dikunci pakai threading.Lock karena
ditulis dari thread WebView2/pywebview dan dibaca dari thread loop tray yang berbeda.
"""
from __future__ import annotations

import threading
from pathlib import Path

from . import autostart, preferensi


class StatusBridge:
    def __init__(self, data_dir: Path):
        self._lock = threading.Lock()
        self._status = "belum"
        self._tooltip = "Absen Pribadi"
        self._data_dir = data_dir
        # Diisi AbsenTrayApp setelah window dibuat, supaya set_window_size() bisa resize
        # jendela yang sedang aktif, bukan cuma menyimpan preferensi buat sesi berikutnya.
        self.window = None

    def laporkan_status(self, status: str, tooltip: str) -> None:
        """Dipanggil dari JS lewat window.pywebview.api.laporkan_status(...)."""
        with self._lock:
            self._status = status
            self._tooltip = tooltip

    def _baca(self) -> tuple[str, str]:
        with self._lock:
            return self._status, self._tooltip

    def get_autostart(self) -> bool:
        try:
            return autostart.is_enabled()
        except OSError:
            return False

    def set_autostart(self, enabled: bool) -> bool:
        try:
            autostart.set_enabled(enabled)
        except OSError:
            pass
        # Baca ulang state sebenarnya (bukan asumsi sukses) — registry write bisa gagal
        # diam-diam, mis. di profil Windows terkelola yang membatasi HKCU write.
        return self.get_autostart()

    def get_window_size(self) -> dict:
        lebar, tinggi = preferensi.baca_ukuran_jendela(self._data_dir)
        return {"lebar": lebar, "tinggi": tinggi}

    def set_window_size(self, lebar: int, tinggi: int) -> dict:
        lebar, tinggi = preferensi.simpan_ukuran_jendela(self._data_dir, lebar, tinggi)
        if self.window is not None:
            self.window.resize(lebar, tinggi)
        return {"lebar": lebar, "tinggi": tinggi}
