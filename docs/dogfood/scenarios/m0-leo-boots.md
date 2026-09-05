# M0 Dogfood — Leo Boots

Environment: Windows 11 with real DaVinci Resolve installed. Record Windows version, actual installed Resolve version, branch/commit, source/package results, and any defects in the issue/PR. Automated smoke is not real-Resolve dogfood.

Perform this full scenario twice: initial dogfood before the PR; final dogfood after all accepted review fixes. The owner supplies actual results to the Windows Companion Architect.

## Source run

1. Sync the frozen environment: `uv sync --frozen`.
2. Start `uv run --frozen python -m leo`.
3. Confirm Leo remains resident and a tray icon exists.
4. Use `Show M0 diagnostics`.
5. Return focus to a real DaVinci Resolve window.
6. Do NOT interact with Leo's tray while judging foreground state.
7. Within one second diagnostics must settle to `Resolve: active`.
8. Alt+Tab to an ordinary application such as Notepad/File Explorer.
9. Within one second diagnostics must settle to `Resolve: inactive`.
10. Alt+Tab back to Resolve; it must return to `active`.
11. While diagnostics remain visible and Resolve is active, click a real Resolve control and use a normal keyboard interaction such as Space/playback. Confirm Resolve receives the input and Leo does not take focus.
12. Use `Hide M0 diagnostics`; confirm the overlay disappears and Leo remains resident.
13. Use `Show M0 diagnostics` again; confirm it can be shown repeatedly.
14. Hide it again.
15. Choose `Quit Leo`.
16. Confirm the source process/event loop exits and the terminal returns cleanly.

The transient state observed while opening the tray itself is explicitly irrelevant because interacting with the tray changes foreground focus. UNKNOWN is displayed as `Resolve: unavailable`, never as inactive.

## Packaged run

Launch the freshly built `dist\Leo\Leo.exe`.

Repeat the same tray residency, diagnostics, Resolve -> other app -> Resolve transitions, click-through, keyboard-focus, hide/show, and Quit checks above.

After packaged Quit:

```powershell
Get-Process Leo -ErrorAction SilentlyContinue
```

must return no running Leo process. Record the actual installed Resolve version.

## Results to record

- Stage: initial / final; date; tester; Windows version; Resolve version.
- Exact commit SHA and source/package build used.
- Source steps 1–16: pass/fail and observations.
- Packaged repetition and no remaining Leo process: pass/fail.
- Any defect: reproduction, expected/actual behavior, severity, Architect ruling.

No real-Resolve results have been claimed by this scenario document.
