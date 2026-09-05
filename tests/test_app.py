import subprocess
import sys

from leo.app import build_application


def test_last_window_close_does_not_quit(qapp, monkeypatch):
    monkeypatch.setattr("leo.app.QApplication", lambda argv: qapp)
    app, _tray, _overlay = build_application(["leo"])
    assert app is qapp
    assert not app.quitOnLastWindowClosed()


def test_run_enters_real_event_loop_and_propagates_exit_code():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from PySide6.QtCore import QTimer; "
            "from PySide6.QtWidgets import QApplication; "
            "import leo.app as module; "
            "runtime = module.build_application(['leo']); "
            "module.build_application = lambda argv: runtime; "
            "QTimer.singleShot(0, lambda: QApplication.instance().exit(7)); "
            "raise SystemExit(module.run(['leo']))",
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 7, result.stdout + result.stderr
