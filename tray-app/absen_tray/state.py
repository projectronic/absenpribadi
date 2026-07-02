"""Penyimpanan state lokal — pengganti localStorage di versi HTML.

Disimpan sebagai satu file JSON di folder home user, dimuat sekali saat start
dan ditulis ulang tiap ada perubahan (absen masuk/pulang, riwayat, setting).
"""
from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from .jadwal import HARI_LIST, JADWAL_DEFAULT, MODE_DEFAULT

CONFIG_DIR = Path.home() / ".absen_pribadi"
STATE_FILE = CONFIG_DIR / "state.json"


def _default_state() -> dict:
    return {
        "absen_masuk": None,  # epoch ms, atau None kalau belum absen
        "riwayat": [],  # list of {id, masuk, pulang, aktual}
        "jadwal_kerja": {h: dict(v) for h, v in JADWAL_DEFAULT.items()},
        "mode": MODE_DEFAULT,
    }


def _muat() -> dict:
    hasil = _default_state()
    if not STATE_FILE.exists():
        return hasil
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return hasil
    hasil["absen_masuk"] = data.get("absen_masuk")
    hasil["riwayat"] = data.get("riwayat", [])
    hasil["mode"] = data.get("mode") if data.get("mode") in ("pulang", "kerja") else MODE_DEFAULT
    # Gabungkan jadwal tersimpan dengan default supaya field yang belum ada (versi lama) tetap terisi.
    jadwal_tersimpan = data.get("jadwal_kerja", {})
    for hari in HARI_LIST:
        hasil["jadwal_kerja"][hari] = {**JADWAL_DEFAULT[hari], **jadwal_tersimpan.get(hari, {})}
    return hasil


def _simpan(state: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


class Store:
    """Wrapper tipis di atas state.json — satu instance dipakai selama app berjalan."""

    def __init__(self):
        self._state = _muat()

    # --- absen masuk ---
    def get_absen_masuk(self) -> Optional[datetime]:
        v = self._state.get("absen_masuk")
        return datetime.fromtimestamp(v / 1000) if v else None

    def set_absen_masuk(self, d: datetime) -> None:
        self._state["absen_masuk"] = d.timestamp() * 1000
        _simpan(self._state)

    def clear_absen_masuk(self) -> None:
        self._state["absen_masuk"] = None
        _simpan(self._state)

    # --- riwayat ---
    def get_riwayat(self) -> list:
        return self._state["riwayat"]

    def tambah_riwayat(self, masuk: datetime, pulang: datetime, aktual: bool) -> None:
        self._state["riwayat"].insert(0, {
            "id": str(int(time.time() * 1000)),
            "masuk": masuk.timestamp() * 1000,
            "pulang": pulang.timestamp() * 1000,
            "aktual": bool(aktual),
        })
        _simpan(self._state)

    def hapus_riwayat(self, id_: str) -> None:
        self._state["riwayat"] = [r for r in self._state["riwayat"] if r["id"] != id_]
        _simpan(self._state)

    # --- jadwal & mode ---
    def get_jadwal_kerja(self) -> dict:
        return self._state["jadwal_kerja"]

    def set_jadwal_kerja(self, jadwal: dict) -> None:
        self._state["jadwal_kerja"] = jadwal
        _simpan(self._state)

    def get_mode(self) -> str:
        return self._state["mode"]

    def set_mode(self, mode: str) -> None:
        self._state["mode"] = mode
        _simpan(self._state)
