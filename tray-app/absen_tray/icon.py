"""Menggambar ikon tray secara dinamis pakai Pillow — tanpa file .ico statis,
supaya warnanya bisa berubah sesuai status (belum absen / bekerja / boleh pulang / libur)."""
from __future__ import annotations

from PIL import Image, ImageDraw

WARNA = {
    "belum": "#64748b",        # abu-abu: belum absen masuk
    "bekerja": "#0f172a",      # dark: sedang bekerja, belum waktunya pulang
    "boleh_pulang": "#047857", # hijau: sudah lewat target jam pulang
    "libur": "#92400e",        # amber: hari libur
}


def buat_icon_image(status: str, size: int = 64) -> Image.Image:
    warna = WARNA.get(status, WARNA["belum"])
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = 4
    draw.ellipse((pad, pad, size - pad, size - pad), fill=warna)
    # Jarum jam sederhana supaya ikon terbaca sebagai "jam/absen", bukan cuma bulatan polos.
    cx = cy = size / 2
    draw.line((cx, cy, cx, size * 0.25), fill="white", width=4)
    draw.line((cx, cy, size * 0.68, cy), fill="white", width=4)
    return img
