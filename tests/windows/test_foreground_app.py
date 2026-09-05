import ctypes
from ctypes import wintypes
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from leo.windows import foreground_app as module
from leo.windows.foreground_app import (
    ForegroundApp,
    ResolveForegroundState,
    classify_resolve_foreground,
    get_foreground_app,
)


@pytest.mark.parametrize(
    ("observation", "expected"),
    [
        (ForegroundApp(1, 2, r"C:\Program Files\Resolve.exe"), ResolveForegroundState.ACTIVE),
        (ForegroundApp(1, 2, r"C:\RESOLVE.EXE"), ResolveForegroundState.ACTIVE),
        (ForegroundApp(1, 2, r"C:\Windows\notepad.exe"), ResolveForegroundState.INACTIVE),
        (ForegroundApp(1, 2, r"C:\Resolve.exe.bak"), ResolveForegroundState.INACTIVE),
        (None, ResolveForegroundState.UNKNOWN),
        (ForegroundApp(1, 2, None), ResolveForegroundState.UNKNOWN),
    ],
)
def test_classification_uses_only_known_executable_identity(observation, expected):
    assert classify_resolve_foreground(observation) is expected


@pytest.mark.parametrize(
    ("hwnd", "pid", "opened", "queried", "expected"),
    [
        (None, 123, True, True, None),
        (0, 123, True, True, None),
        (99, 0, True, True, None),
        (99, 123, False, True, ForegroundApp(99, 123, None)),
        (99, 123, True, False, ForegroundApp(99, 123, None)),
        (99, 123, True, True, ForegroundApp(99, 123, r"C:\Resolve.exe")),
    ],
)
def test_win32_observation_and_handle_lifetime(monkeypatch, hwnd, pid, opened, queried, expected):
    handle = 0x123456789  # Detect accidental truncation assumptions in wrapper composition.

    def window_pid(window, output):
        assert window == hwnd
        ctypes.cast(output, ctypes.POINTER(wintypes.DWORD)).contents.value = pid
        return 456

    def query(process, flags, buffer, size):
        assert process == handle
        assert flags == 0
        assert ctypes.cast(size, ctypes.POINTER(wintypes.DWORD)).contents.value >= 260
        buffer.value = r"C:\Resolve.exe"
        return queried

    user32 = SimpleNamespace(
        GetForegroundWindow=Mock(return_value=hwnd),
        GetWindowThreadProcessId=Mock(side_effect=window_pid),
    )
    kernel32 = SimpleNamespace(
        OpenProcess=Mock(return_value=handle if opened else None),
        QueryFullProcessImageNameW=Mock(side_effect=query),
        CloseHandle=Mock(return_value=True),
    )
    monkeypatch.setattr(module, "_user32", user32)
    monkeypatch.setattr(module, "_kernel32", kernel32)

    assert get_foreground_app() == expected
    if hwnd and pid:
        kernel32.OpenProcess.assert_called_once_with(0x1000, False, pid)
    else:
        kernel32.OpenProcess.assert_not_called()
    if hwnd and pid and opened:
        kernel32.CloseHandle.assert_called_once_with(handle)
        kernel32.QueryFullProcessImageNameW.assert_called_once()
    else:
        kernel32.CloseHandle.assert_not_called()
        kernel32.QueryFullProcessImageNameW.assert_not_called()


def test_win32_function_prototypes_preserve_pointer_width():
    dword_pointer = ctypes.POINTER(wintypes.DWORD)
    for function, arguments, result in [
        (module._user32.GetForegroundWindow, [], wintypes.HWND),
        (module._user32.GetWindowThreadProcessId, [wintypes.HWND, dword_pointer], wintypes.DWORD),
        (
            module._kernel32.OpenProcess,
            [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD],
            wintypes.HANDLE,
        ),
        (
            module._kernel32.QueryFullProcessImageNameW,
            [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, dword_pointer],
            wintypes.BOOL,
        ),
        (module._kernel32.CloseHandle, [wintypes.HANDLE], wintypes.BOOL),
    ]:
        assert function.argtypes == arguments
        assert function.restype is result
