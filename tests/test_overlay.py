from PySide6.QtCore import Qt

from leo.overlay import LeoOverlay


def test_show_update_clear_and_repeat(qtbot):
    overlay = LeoOverlay()
    qtbot.addWidget(overlay)
    assert not overlay.isVisible()
    for text in ["Leo M0 — Resolve: active", "Leo M0 — Resolve: unavailable"]:
        overlay.show_status(text)
        assert overlay.label.text() == text
        assert overlay.isVisible()
        overlay.show_status("Updated")
        assert overlay.label.text() == "Updated"
        overlay.clear_status()
        assert overlay.label.text() == ""
        assert not overlay.isVisible()


def test_overlay_requests_native_input_transparency_and_no_focus(qtbot):
    overlay = LeoOverlay()
    qtbot.addWidget(overlay)
    overlay.show_status("Leo M0")
    flags = overlay.windowFlags()
    assert flags & Qt.WindowType.WindowType_Mask == Qt.WindowType.Tool
    for flag in [
        Qt.WindowType.FramelessWindowHint,
        Qt.WindowType.WindowStaysOnTopHint,
        Qt.WindowType.WindowTransparentForInput,
        Qt.WindowType.WindowDoesNotAcceptFocus,
    ]:
        assert flags & flag
    assert overlay.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    assert overlay.testAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
    assert overlay.focusPolicy() == Qt.FocusPolicy.NoFocus
