import subprocess
import sys
import textwrap

from leo.app import build_application


def test_composition_keeps_tray_resident_and_last_window_close_disabled(qapp, qtbot, monkeypatch):
    monkeypatch.setattr("leo.app.QApplication", lambda argv: qapp)
    app, tray, overlay = build_application(["leo"])
    assert app is qapp
    assert not app.quitOnLastWindowClosed()
    assert tray.isVisible()
    qtbot.addWidget(overlay)
    assert not overlay.isVisible()
    tray._timer.stop()
    tray.hide()
    tray.menu.deleteLater()
    tray.deleteLater()


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


def test_run_retains_tray_and_overlay_through_event_loop(qapp, monkeypatch):
    import gc
    import weakref

    import leo.app as module

    references = []
    original_build = module.build_application
    monkeypatch.setattr(module, "QApplication", lambda argv: qapp)

    def build(argv):
        runtime = original_build(argv)
        references.extend(weakref.ref(component) for component in runtime[1:])
        return runtime

    def event_loop():
        gc.collect()
        tray, overlay = (reference() for reference in references)
        assert tray is not None
        assert overlay is not None
        assert tray.isVisible()
        tray._timer.stop()
        tray.hide()
        tray.menu.deleteLater()
        tray.deleteLater()
        overlay.deleteLater()
        return 0

    monkeypatch.setattr(module, "build_application", build)
    monkeypatch.setattr(qapp, "exec", event_loop)
    assert module.run(["leo"]) == 0


def test_source_smoke_entry_point_exits_successfully():
    result = subprocess.run(
        [sys.executable, "-m", "leo", "--smoke-test"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_smoke_shows_and_clears_real_overlay_inside_event_loop_before_quit():
    script = textwrap.dedent("""
        from PySide6.QtCore import QThread
        import leo.app as module

        events = []
        class ObservedOverlay(module.LeoOverlay):
            def show_status(self, text):
                super().show_status(text)
                assert QThread.currentThread().loopLevel() > 0
                assert self.isVisible() and self.label.text()
                events.append('show')

            def clear_status(self):
                super().clear_status()
                assert not self.isVisible() and not self.label.text()
                events.append('clear')

        module.LeoOverlay = ObservedOverlay
        original_build = module.build_application
        def build(argv):
            runtime = original_build(argv)
            app, tray, overlay = runtime
            assert tray.isVisible()
            assert not app.quitOnLastWindowClosed()
            app.aboutToQuit.connect(lambda: events.append('quit'))
            return runtime

        module.build_application = build
        assert module.run(['leo', '--smoke-test']) == 0
        assert events[0] == 'show', events
        assert events.index('clear') < events.index('quit'), events
        assert events[-1] == 'quit', events
    """)
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=15
    )
    assert result.returncode == 0, result.stdout + result.stderr
