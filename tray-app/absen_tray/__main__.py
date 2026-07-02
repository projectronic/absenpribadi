"""Entry point tray app.

Menampilkan ../absen-pribadi.html apa adanya di dalam popup borderless dekat
taskbar (lewat pywebview + Edge WebView2), jadi tampilannya identik dengan
versi HTML — dark card, rounded corners — bukan widget native yang digambar ulang.

Jalankan dari folder tray-app (setelah `pip install -r requirements.txt`):
    python -m absen_tray
"""
from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

import pystray
import webview

from .icon import buat_icon_image
from .posisi import hitung_posisi
from .status_bridge import StatusBridge

LEBAR_JENDELA = 380
TINGGI_JENDELA = 640


def _cari_html_path() -> Path:
    if getattr(sys, "frozen", False):
        # Dijalankan sebagai exe hasil PyInstaller — absen-pribadi.html disertakan
        # lewat --add-data (lihat README.md), diekstrak ke folder sementara sys._MEIPASS.
        return Path(sys._MEIPASS) / "absen-pribadi.html"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent.parent / "absen-pribadi.html"


class AbsenTrayApp:
    def __init__(self):
        self.bridge = StatusBridge()
        self.window: webview.Window | None = None
        self.icon: pystray.Icon | None = None
        self._terlihat = False

    def _buat_window(self) -> None:
        html_path = _cari_html_path()
        x, y = hitung_posisi(LEBAR_JENDELA, TINGGI_JENDELA)
        self.window = webview.create_window(
            "Absen Pribadi",
            url=html_path.as_uri(),
            js_api=self.bridge,
            width=LEBAR_JENDELA,
            height=TINGGI_JENDELA,
            x=x,
            y=y,
            frameless=True,
            easy_drag=False,
            on_top=True,
            hidden=True,
        )

    # --- callback tray, jalan di thread pystray. Method Window pywebview aman dipanggil
    # dari thread lain karena pywebview marshal otomatis ke thread GUI-nya. ---
    def _toggle_jendela(self, icon=None, item=None) -> None:
        if self.window is None:
            return
        if self._terlihat:
            self.window.hide()
        else:
            x, y = hitung_posisi(LEBAR_JENDELA, TINGGI_JENDELA)
            self.window.move(x, y)
            self.window.show()
        self._terlihat = not self._terlihat

    def _minta_keluar(self, icon=None, item=None) -> None:
        if self.icon is not None:
            self.icon.stop()
        if self.window is not None:
            self.window.destroy()

    def _loop_status_tray(self) -> None:
        while True:
            status, tooltip = self.bridge._baca()
            if self.icon is not None:
                self.icon.icon = buat_icon_image(status)
                self.icon.title = tooltip
            time.sleep(1)

    def _jalankan_tray(self) -> None:
        self.icon = pystray.Icon(
            "absen_pribadi",
            buat_icon_image("belum"),
            "Absen Pribadi",
            menu=pystray.Menu(
                pystray.MenuItem("Buka/Tutup", self._toggle_jendela, default=True),
                pystray.MenuItem("Keluar", self._minta_keluar),
            ),
        )
        threading.Thread(target=self._loop_status_tray, daemon=True).start()
        self.icon.run()

    def run(self) -> None:
        threading.Thread(target=self._jalankan_tray, daemon=True).start()
        self._buat_window()
        webview.start()


def main() -> None:
    AbsenTrayApp().run()


if __name__ == "__main__":
    main()
