# Leo

Leo is an AI tutor and copilot for DaVinci Resolve on Windows.

M0 foundation development on Windows 11. Leo is not yet a usable tutor. AI assists the editor; it does not make creative decisions for them.

## Development

Install Python 3.12 and uv, then run from the repository root:

```powershell
uv sync --frozen
uv run --frozen python -m leo
```

Leo remains resident in the Windows tray while diagnostics are hidden. Right-click its tray icon (check the tray overflow if needed) for `Show M0 diagnostics`, `Hide M0 diagnostics`, and `Quit Leo`.

Diagnostics refresh every 250 ms and display Resolve as active, inactive, or unavailable. Judge state after focusing Resolve or another app, without opening Leo's tray; opening the tray changes foreground focus. `Quit Leo` exits the application.

```powershell
uv lock --check
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen pytest
git diff --check
```

Leo-owned source is all-rights-reserved; see `LICENSE` and `THIRD_PARTY_NOTICES.md`. M0 does not authorize public binary distribution.

See:

- `docs/superpowers/specs/2026-09-04-leo-development-operating-model-design.md`
- `docs/superpowers/plans/2026-09-04-m0-leo-boots.md`
- `docs/architecture/windows-companion.md`
- `docs/dogfood/scenarios/m0-leo-boots.md`

M0 excludes audio/voice, screenshots/capture, models, pointer grounding, retrieval/tutoring, conversational memory, Resolve scripting/MCP or structured state, editing/action planning, mutation confirmation, installers/updaters, signing, websites and speculative future interfaces.
