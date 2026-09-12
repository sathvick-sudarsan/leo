# Windows Companion Architecture — M0

Status: Approved by Windows Companion Architect — 2026-09-04

Authority: [approved operating model](../superpowers/specs/2026-09-04-leo-development-operating-model-design.md). Target: Windows 11, Python 3.12, PySide6, src layout. M0 is a development chassis, not a tutor or public binary release.

## Exactly four implementation ownership areas

1. `leo.app`: QApplication lifetime/composition, `setQuitOnLastWindowClosed(False)`, source entry point, development-only `--smoke-test`, and long-lived ownership of tray/overlay through the event loop.
2. `leo.tray`: resident tray, retained `QMenu` (QSystemTrayIcon does not own it), 250 ms foreground poll, tooltip state, and exactly the temporary actions `Show M0 diagnostics`, `Hide M0 diagnostics`, `Quit Leo`. Visible diagnostics refresh without tray interaction. Hiding diagnostics never quits Leo.
3. `leo.overlay`: rendering only, with `show_status(text: str) -> None` and `clear_status() -> None`. Tool, FramelessWindowHint, WindowStaysOnTopHint, WindowTransparentForInput, WindowDoesNotAcceptFocus; WA_TranslucentBackground, WA_ShowWithoutActivating; FocusPolicy.NoFocus. The diagnostic surface may span the available/virtual desktop to verify clicks elsewhere pass to Resolve. No native Win32 overlay hacks unless real dogfood proves Qt inadequate.
4. `leo.windows.foreground_app`: direct standard-library ctypes Win32 inspection. No psutil, title guessing, or speculative adapter hierarchy.

## Foreground contract

```python
from dataclasses import dataclass
from enum import Enum


class ResolveForegroundState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class ForegroundApp:
    hwnd: int
    pid: int
    executable: str | None


def get_foreground_app() -> ForegroundApp | None: ...


def classify_resolve_foreground(
    app: ForegroundApp | None,
) -> ResolveForegroundState: ...
```

Absent/zero HWND or zero PID yields no usable observation (`None`). No observation or unavailable executable is UNKNOWN. A successfully queried executable whose Windows basename case-insensitively equals `Resolve.exe` is ACTIVE; another known executable is INACTIVE. Process-query failure is `executable=None`, never a GUI crash or false inactive observation.

Every used Win32 function declares explicit `argtypes` and `restype`:

| Function | Arguments | Return |
| --- | --- | --- |
| GetForegroundWindow | none | wintypes.HWND |
| GetWindowThreadProcessId | HWND, pointer to DWORD | DWORD |
| OpenProcess | DWORD, BOOL, DWORD | wintypes.HANDLE |
| QueryFullProcessImageNameW | HANDLE, DWORD, LPWSTR, pointer to DWORD | BOOL |
| CloseHandle | HANDLE | BOOL |

Use `PROCESS_QUERY_LIMITED_INFORMATION = 0x1000`. Always close a successfully opened process handle, including query failure paths.

## Diagnostics and smoke

Diagnostics display `Leo M0 — Resolve: active`, `inactive`, or `unavailable` (UNKNOWN). The owner focuses Resolve or another app while the overlay updates. An opened tray menu cannot be the acceptance observer: opening it changes foreground focus. Tooltip state is supplementary; no disabled live-state menu item.

Both `uv run --frozen python -m leo --smoke-test` and `dist\Leo\Leo.exe --smoke-test` use the same real QApplication/tray/overlay composition as normal startup, enter the event loop, briefly show diagnostics, clear them, request normal quit, and exit 0 without interaction. No packaging-only fake application.

## Build and gates

Use the exact dependency ranges and CI pins in the [approved plan](../superpowers/plans/2026-09-04-m0-leo-boots.md), commit `uv.lock`, and build PyInstaller onedir with `console=False` to `dist/Leo/Leo.exe`. CI is windows-latest, uv 0.12.10, contents: read, with bounded source and packaged smoke. Executable existence alone is insufficient. No installer, signing, upload, or release infrastructure.

Follow the [source and packaged dogfood scenario](../dogfood/scenarios/m0-leo-boots.md) initially before PR and finally after accepted review fixes. Automated tests do not certify native click-through/focus or real Resolve transitions.

## Non-goals

No microphone/audio; voice input; screenshots; screen capture; VLM/model calls; pointer grounding; RAG/knowledge retrieval; tutoring; conversational memory; Resolve scripting; MCP; Fusion/Resolve structured state; editing operations; action planning; mutation confirmation flows; installer/updater; signing; website; speculative future interfaces. No Clicky/ClickyWin source copied or adapted in M0.
