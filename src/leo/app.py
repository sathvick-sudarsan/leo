import sys

from PySide6.QtWidgets import QApplication


def build_application(argv: list[str]) -> tuple[QApplication, None, None]:
    app = QApplication(argv)
    app.setApplicationName("Leo")
    app.setQuitOnLastWindowClosed(False)
    return app, None, None


def run(argv: list[str] | None = None) -> int:
    app, _tray, _overlay = build_application(list(sys.argv if argv is None else argv))
    return app.exec()
