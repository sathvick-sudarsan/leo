# Leo Agent Rules

The approved operating model in `docs/superpowers/specs/2026-09-04-leo-development-operating-model-design.md` is authoritative. M0 implements `docs/architecture/windows-companion.md` through the approved M0 plan. Do not reopen approved design through brainstorming.

- AI assists the editor; it does not make creative decisions for them.
- Keep `main` runnable. Ship the smallest useful vertical slice; freeze issue scope once implementation begins except for impossibility, safety, invalid architecture assumptions, or explicit PM reprioritization.
- One Codex implementation writer owns `feat/m0-leo-boots` in `.worktrees/m0-leo-boots`. Execute serially; no nested worktree or delegated file modifications. Read-only investigation/review agents are allowed. Use executing-plans, TDD, and verification; do not use subagent-driven-development for M0.
- Keep execution evidence and rulings under `.superpowers/sdd/2026-09-04-m0-leo-boots/progress.md` (ignored).
- M0 owns exactly `leo.app`, `leo.tray`, `leo.overlay`, and `leo.windows.foreground_app`. Reuse stdlib, Qt, and installed dependencies; avoid speculative interfaces and unrelated refactoring.
- Windows foreground inspection uses explicitly typed ctypes calls, executable identity, and ACTIVE/INACTIVE/UNKNOWN. Unknown must never be presented as inactive.
- Overlay rendering must not steal focus or intercept mouse/keyboard input. Real Windows/Resolve dogfood proves native behavior; widget tests do not.
- Run focused behavioral tests with TDD and the full frozen verification gates in the plan at its checkpoints. Do not broaden tests without a concrete reason.
- No microphone/audio, voice input, screenshots, screen capture, VLM/model calls, pointer grounding, RAG/knowledge retrieval, tutoring, conversational memory, Resolve scripting, MCP, Fusion/Resolve structured state, editing operations, action planning, mutation confirmation flows, installer/updater, signing, website, or speculative future interfaces. Do not copy Clicky/ClickyWin code in M0.
- Public repository; Leo-owned source remains all-rights-reserved. Dependencies retain their licenses. M0 does not authorize public binary release.
- Technical architecture questions go to the Windows Companion Architect; routine implementation details stay with Codex. Product/scope decisions belong to the PM via the Architect.
- Review concrete correctness/security/reliability/regressions: P0/P1 block merge, P2 only if local, P3 cannot expand scope or automatically create backlog.
- After automated verification, STOP at `READY FOR ARCHITECT INITIAL DOGFOOD` with exact SHA and evidence. No push, PR, merge, or real-Resolve dogfood claim. Owner/Architect performs initial source and packaged dogfood; CI, Claude and available Greptile review follow; final dogfood follows accepted review fixes.
