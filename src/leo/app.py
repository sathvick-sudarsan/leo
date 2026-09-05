import sys

from PySide6.QtWidgets import QApplication

from leo.overlay import LeoOverlay
from leo.tray import LeoTray


def build_application(argv: list[str]) -> tuple[QApplication, LeoTray, LeoOverlay]:
    app = QApplication(argv)
    app.setApplicationName("Leo")
    app.setQuitOnLastWindowClosed(False)
    overlay = LeoOverlay()
    tray = LeoTray(overlay)
    tray.show()
    app.aboutToQuit.connect(tray.hide)
    app.aboutToQuit.connect(overlay.clear_status)
    return app, tray, overlay


def run(argv: list[str] | None = None) -> int:
    app, _tray, _overlay = build_application(list(sys.argv if argv is None else argv))
    return app.exec()
