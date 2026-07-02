"""Logika jadwal kerja & perhitungan target jam pulang.

Port langsung dari fungsi-fungsi terkait di absen-pribadi.html (jamStrKeMenit,
totalJamJadwal, jamPulangTarget, jamPulangTargetKerja, hitungTargetPulang) supaya
kedua versi aplikasi (HTML & tray app) menghasilkan target jam pulang yang sama.
"""
from __future__ import annotations

from datetime import datetime, timedelta

HARI_LIST = ["senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu"]
HARI_LABEL = {
    "senin": "Senin", "selasa": "Selasa", "rabu": "Rabu", "kamis": "Kamis",
    "jumat": "Jumat", "sabtu": "Sabtu", "minggu": "Minggu",
}

JADWAL_DEFAULT = {
    "senin":  {"libur": False, "masuk": "08:00", "istirahatMulai": "12:00", "istirahatSelesai": "13:00", "pulang": "17:00"},
    "selasa": {"libur": False, "masuk": "08:00", "istirahatMulai": "12:00", "istirahatSelesai": "13:00", "pulang": "17:00"},
    "rabu":   {"libur": False, "masuk": "08:00", "istirahatMulai": "12:00", "istirahatSelesai": "13:00", "pulang": "17:00"},
    "kamis":  {"libur": False, "masuk": "08:00", "istirahatMulai": "12:00", "istirahatSelesai": "13:00", "pulang": "17:00"},
    "jumat":  {"libur": False, "masuk": "08:00", "istirahatMulai": "11:00", "istirahatSelesai": "13:30", "pulang": "17:00"},
    "sabtu":  {"libur": True,  "masuk": "08:00", "istirahatMulai": "12:00", "istirahatSelesai": "13:00", "pulang": "17:00"},
    "minggu": {"libur": True,  "masuk": "08:00", "istirahatMulai": "12:00", "istirahatSelesai": "13:00", "pulang": "17:00"},
}

# "pulang": target jam pulang selalu jam pulang tetap dari jadwal hari itu.
# "kerja" : target jam pulang = jam absen masuk aktual + total durasi kerja (termasuk istirahat),
#           kecuali absen lebih awal dari jam masuk terjadwal -> tetap pakai jam pulang normal.
MODE_DEFAULT = "pulang"


def nama_hari(d: datetime) -> str:
    # Python: Monday=0..Sunday=6 -> sudah selaras urutan HARI_LIST (index 0 = Senin).
    return HARI_LIST[d.weekday()]


def jadwal_hari(d: datetime, jadwal_kerja: dict) -> dict:
    return jadwal_kerja[nama_hari(d)]


def _menit(jam_str: str) -> int:
    h, m = jam_str.split(":")
    return int(h) * 60 + int(m)


def total_jam_jadwal(jadwal: dict) -> timedelta:
    """Target durasi presensi satu hari: masuk s.d. pulang, TERMASUK istirahat.

    Menangani shift malam (jam pulang <= jam masuk) dengan menambah 24 jam,
    sama seperti totalJamJadwal() di versi HTML.
    """
    total_menit = _menit(jadwal["pulang"]) - _menit(jadwal["masuk"])
    if total_menit <= 0:
        total_menit += 24 * 60
    return timedelta(minutes=total_menit)


def jam_pulang_target(d: datetime, jadwal: dict) -> datetime:
    """Jam pulang TETAP sesuai jadwal hari itu (mode "pulang")."""
    h, m = (int(x) for x in jadwal["pulang"].split(":"))
    hasil = d.replace(hour=h, minute=m, second=0, microsecond=0)
    if _menit(jadwal["pulang"]) <= _menit(jadwal["masuk"]):
        hasil += timedelta(days=1)
    return hasil


def jam_pulang_target_kerja(absen_masuk: datetime, jadwal: dict) -> datetime:
    """Jam pulang mengambang (mode "kerja"): absen masuk aktual + total durasi kerja.

    Kalau absen lebih awal dari jam masuk terjadwal, jangan majukan target —
    pakai jam pulang normal, supaya datang pagi-pagi sekali tidak membuat pulang
    lebih cepat dari jam pulang standar.
    """
    h, m = (int(x) for x in jadwal["masuk"].split(":"))
    masuk_terjadwal = absen_masuk.replace(hour=h, minute=m, second=0, microsecond=0)
    if absen_masuk < masuk_terjadwal:
        return jam_pulang_target(absen_masuk, jadwal)
    return absen_masuk + total_jam_jadwal(jadwal)


def hitung_target_pulang(absen_masuk: datetime, jadwal: dict, mode: str) -> datetime:
    if mode == "kerja":
        return jam_pulang_target_kerja(absen_masuk, jadwal)
    return jam_pulang_target(absen_masuk, jadwal)


def fmt_jadwal_singkat(jadwal: dict) -> str:
    if jadwal["libur"]:
        return "Libur"
    return f"{jadwal['masuk']}–{jadwal['pulang']} (istirahat {jadwal['istirahatMulai']}–{jadwal['istirahatSelesai']})"
