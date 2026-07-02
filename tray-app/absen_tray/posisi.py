"""Hitung posisi popup supaya muncul menempel di pojok layar dekat taskbar.

Disederhanakan dibanding pendekatan usage-monitor-for-claude (yang mendeteksi
Shell_TrayWnd + MonitorFromWindow + GetMonitorInfoW supaya benar di semua posisi
taskbar & layout multi-monitor). Versi ini cuma menganggap taskbar ada di bawah
monitor utama — cukup untuk kebanyakan setup default Windows, tapi tidak akan pas
kalau taskbar dipindah ke kiri/kanan/atas atau popup perlu muncul di monitor kedua.
TODO: pakai pendekatan Win32 yang sama seperti referensi kalau butuh itu.
"""
from __future__ import annotations

import ctypes

MARGIN = 12
PERKIRAAN_TINGGI_TASKBAR = 48


def hitung_posisi(lebar: int, tinggi: int) -> tuple[int, int]:
    user32 = ctypes.windll.user32  # type: ignore[attr-defined]
    lebar_layar = user32.GetSystemMetrics(0)
    tinggi_layar = user32.GetSystemMetrics(1)
    x = lebar_layar - lebar - MARGIN
    y = tinggi_layar - tinggi - PERKIRAAN_TINGGI_TASKBAR - MARGIN
    return max(x, 0), max(y, 0)
