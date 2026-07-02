"""Preferensi ringan yang harus tersedia SEBELUM webview jalan (mis. ukuran jendela) —
tidak bisa disimpan di localStorage (baru bisa dibaca Python lewat bridge setelah webview
jalan, sudah terlambat buat ukuran jendela awal). Disimpan sebagai file JSON kecil di
folder data aplikasi, terpisah dari folder WebView2 (lihat _data_dir() di __main__.py).
"""
from __future__ import annotations

import json
from pathlib import Path

LEBAR_DEFAULT = 380
TINGGI_DEFAULT = 640

LEBAR_MIN, LEBAR_MAX = 300, 600
TINGGI_MIN, TINGGI_MAX = 400, 900


def _clamp(nilai: int, minimum: int, maksimum: int) -> int:
    return max(minimum, min(maksimum, nilai))


def _file_preferensi(data_dir: Path) -> Path:
    return data_dir / "preferensi.json"


def baca_ukuran_jendela(data_dir: Path) -> tuple[int, int]:
    try:
        data = json.loads(_file_preferensi(data_dir).read_text(encoding="utf-8"))
        lebar = _clamp(int(data["lebar"]), LEBAR_MIN, LEBAR_MAX)
        tinggi = _clamp(int(data["tinggi"]), TINGGI_MIN, TINGGI_MAX)
        return lebar, tinggi
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return LEBAR_DEFAULT, TINGGI_DEFAULT


def simpan_ukuran_jendela(data_dir: Path, lebar: int, tinggi: int) -> tuple[int, int]:
    lebar = _clamp(int(lebar), LEBAR_MIN, LEBAR_MAX)
    tinggi = _clamp(int(tinggi), TINGGI_MIN, TINGGI_MAX)
    data_dir.mkdir(parents=True, exist_ok=True)
    _file_preferensi(data_dir).write_text(json.dumps({"lebar": lebar, "tinggi": tinggi}), encoding="utf-8")
    return lebar, tinggi
