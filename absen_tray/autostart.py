"""Autostart lewat Windows Registry Run key (HKCU) — Windows-only, tanpa sys.platform
guard, konsisten dengan gaya posisi.py yang juga pakai Win32 API tanpa guard.
"""
from __future__ import annotations

import sys
import winreg
from pathlib import Path

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
NAMA_VALUE = "AbsenPribadi"


def _perintah_jalan() -> str:
    if getattr(sys, "frozen", False):
        # Exe hasil PyInstaller --onefile: sys.executable menunjuk ke exe asli (bukan
        # folder ekstrak sementara), aman dipakai langsung sebagai perintah autostart.
        return f'"{sys.executable}"'
    run_py = Path(__file__).resolve().parent.parent / "run.py"
    return f'"{sys.executable}" "{run_py}"'


def is_enabled() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, NAMA_VALUE)
            return True
    except FileNotFoundError:
        return False


def set_enabled(enabled: bool) -> None:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
        if enabled:
            winreg.SetValueEx(key, NAMA_VALUE, 0, winreg.REG_SZ, _perintah_jalan())
        else:
            try:
                winreg.DeleteValue(key, NAMA_VALUE)
            except FileNotFoundError:
                pass
