from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QLabel, QWidget


class LeoOverlay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.label = QLabel(self)
        self.label.setStyleSheet(
            "color: white; background-color: rgba(24, 24, 24, 220);"
            "padding: 10px; border-radius: 6px; font-size: 16px;"
        )

    def show_status(self, text: str) -> None:
        screen = QGuiApplication.primaryScreen()
        self.setGeometry(screen.virtualGeometry())
        position = screen.availableGeometry().topLeft() - self.geometry().topLeft()
        self.label.move(position.x() + 16, position.y() + 16)
        self.label.setText(text)
        self.label.adjustSize()
        self.show()

    def clear_status(self) -> None:
        self.label.clear()
        self.hide()
