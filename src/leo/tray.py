from collections.abc import Callable

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon

from leo.overlay import LeoOverlay
from leo.windows.foreground_app import (
    ForegroundApp,
    ResolveForegroundState,
    classify_resolve_foreground,
    get_foreground_app,
)


class LeoTray(QSystemTrayIcon):
    def __init__(
        self,
        overlay: LeoOverlay,
        foreground_provider: Callable[[], ForegroundApp | None] = get_foreground_app,
    ) -> None:
        icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        super().__init__(icon)
        self._overlay = overlay
        self._foreground_provider = foreground_provider
        # QSystemTrayIcon does not own its menu; keep the Python reference alive.
        self.menu = QMenu()
        self.menu.addAction("Show M0 diagnostics", self.show_diagnostics)
        self.menu.addAction("Hide M0 diagnostics", overlay.clear_status)
        self.menu.addAction("Quit Leo", QApplication.instance().quit)
        self.setContextMenu(self.menu)

        self._timer = QTimer(self)
        self._timer.setInterval(250)
        self._timer.timeout.connect(self.refresh_status)
        self._timer.start()
        self.refresh_status()

    def refresh_status(self) -> None:
        state = classify_resolve_foreground(self._foreground_provider())
        status = "unavailable" if state is ResolveForegroundState.UNKNOWN else state.value
        text = f"Leo M0 — Resolve: {status}"
        self.setToolTip(text)
        if self._overlay.isVisible():
            self._overlay.show_status(text)

    def show_diagnostics(self) -> None:
        self.refresh_status()
        self._overlay.show_status(self.toolTip())
