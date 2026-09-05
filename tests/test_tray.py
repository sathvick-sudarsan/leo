import gc
from unittest.mock import Mock

import pytest

from leo.overlay import LeoOverlay
from leo.tray import LeoTray
from leo.windows.foreground_app import ForegroundApp


@pytest.fixture
def runtime(qtbot, qapp, monkeypatch):
    quit_spy = Mock()
    monkeypatch.setattr(qapp, "quit", quit_spy)
    overlay = LeoOverlay()
    qtbot.addWidget(overlay)
    observation = [None]
    tray = LeoTray(overlay, foreground_provider=lambda: observation[0])
    tray.show()
    yield tray, overlay, observation, quit_spy
    tray._timer.stop()
    tray.hide()
    tray.menu.deleteLater()
    tray.deleteLater()


@pytest.mark.parametrize(
    ("observation", "text"),
    [
        (ForegroundApp(1, 2, r"C:\Resolve.exe"), "Leo M0 — Resolve: active"),
        (ForegroundApp(1, 2, r"C:\notepad.exe"), "Leo M0 — Resolve: inactive"),
        (None, "Leo M0 — Resolve: unavailable"),
        (ForegroundApp(1, 2, None), "Leo M0 — Resolve: unavailable"),
    ],
)
def test_diagnostics_and_tooltip_present_foreground_state(runtime, observation, text):
    tray, overlay, current, _quit = runtime
    current[0] = observation
    tray.menu.actions()[0].trigger()
    assert overlay.isVisible()
    assert overlay.label.text() == text
    assert tray.toolTip() == text


def test_timer_updates_visible_diagnostics_without_tray_interaction(runtime, qtbot):
    tray, overlay, current, _quit = runtime
    tray.menu.actions()[0].trigger()
    assert tray._timer.interval() == 250
    for observation, text in [
        (ForegroundApp(1, 2, r"C:\Resolve.exe"), "Leo M0 — Resolve: active"),
        (ForegroundApp(1, 2, r"C:\notepad.exe"), "Leo M0 — Resolve: inactive"),
        (None, "Leo M0 — Resolve: unavailable"),
    ]:
        current[0] = observation
        qtbot.waitUntil(lambda text=text: overlay.label.text() == text, timeout=1000)
        assert tray.toolTip() == text


def test_menu_survives_collection_and_hide_keeps_tray_resident(runtime):
    tray, overlay, _current, quit_spy = runtime
    gc.collect()
    assert tray.contextMenu() is tray.menu
    show, hide, quit_action = tray.menu.actions()
    assert [action.text() for action in tray.menu.actions()] == [
        "Show M0 diagnostics",
        "Hide M0 diagnostics",
        "Quit Leo",
    ]
    for _ in range(2):
        show.trigger()
        assert overlay.isVisible()
        hide.trigger()
        tray.refresh_status()
        assert not overlay.isVisible()
        assert overlay.label.text() == ""
        assert tray.isVisible()
        quit_spy.assert_not_called()
    quit_action.trigger()
    quit_spy.assert_called_once_with()
