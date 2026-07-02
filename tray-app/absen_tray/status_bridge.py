"""Jembatan status dari JS (di dalam webview) ke Python, buat update ikon tray.

absen-pribadi.html memanggil window.pywebview.api.laporkan_status(status, tooltip)
tiap detik lewat laporkanStatusKeTray() — lihat perubahan di HTML tsb. Nilai terakhir
disimpan di sini, dibaca oleh loop tray (__main__.py) untuk mengganti warna ikon &
tooltip. Dikunci pakai threading.Lock karena ditulis dari thread WebView2/pywebview
dan dibaca dari thread loop tray yang berbeda.
"""
from __future__ import annotations

import threading


class StatusBridge:
    def __init__(self):
        self._lock = threading.Lock()
        self._status = "belum"
        self._tooltip = "Absen Pribadi"

    def laporkan_status(self, status: str, tooltip: str) -> None:
        """Dipanggil dari JS lewat window.pywebview.api.laporkan_status(...)."""
        with self._lock:
            self._status = status
            self._tooltip = tooltip

    def _baca(self) -> tuple[str, str]:
        with self._lock:
            return self._status, self._tooltip
