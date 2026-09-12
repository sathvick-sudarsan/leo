import sys

from PySide6.QtCore import QTimer
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
    args = list(sys.argv if argv is None else argv)
    app, tray, overlay = build_application(args)
    if "--smoke-test" in args:
        QTimer.singleShot(0, tray.show_diagnostics)
        QTimer.singleShot(750, overlay.clear_status)
        QTimer.singleShot(1000, app.quit)
    return app.exec()
