# Leo — Project Development Operating Model

**Status:** Approved  
**Date:** 2026-09-04  
**Repository:** `sathvick-sudarsan/leo`

## Product Principle

Leo removes software friction between an editor's intent and DaVinci Resolve. It helps the editor understand, navigate, debug, and eventually operate Resolve without replacing creative judgment.

> AI assists the artist. It does not create the art for them.

Leo is a shipping-oriented product project. Engineering decisions optimize for usefulness, reliability, development speed, and shipping velocity rather than pedagogical coverage.

## Repository Strategy

Leo begins as a clean standalone public repository rather than a GitHub fork. Existing MIT-licensed projects such as Clicky/ClickyWin and Resolve-control implementations may be selectively adapted, with attribution preserved in `THIRD_PARTY_NOTICES.md` and any required license notices.

Leo owns its important architectural interfaces so third-party implementations remain replaceable.

## Foundation Architecture

Leo starts as a Windows Python/PySide6 desktop application with a small product-owned core and adapter boundaries:

- interaction/orchestration owned by Leo;
- screen-context adapter;
- Resolve-context adapter;
- knowledge adapter;
- action planner and safety layer added later;
- third-party Clicky/Resolve implementations remain implementation details behind Leo interfaces.

Useful ClickyWin infrastructure may be selectively adapted for global push-to-talk, Windows screen capture, overlay rendering, tray behavior, audio client patterns, and packaging patterns. Leo owns orchestration, Resolve context representation, screen/state fusion, tutoring behavior, action planning, safety rules, and product evals.

## Resolve Integration

Leo exposes a small domain-oriented `ResolveAdapter` rather than reasoning over hundreds of raw MCP operations. MCP or an in-app Resolve bridge may implement the adapter, but MCP is infrastructure rather than Leo's product architecture. Resolve Free should remain a first-class target where practical.

## Engineering Invariants

1. `main` is always runnable.
2. Work is framed as user-visible vertical slices.
3. Automated tests are necessary but real Resolve dogfooding is part of verification.
4. Prefer proven infrastructure over rebuilding commodity layers.
5. Issue scope freezes once implementation begins except for impossibility, safety, invalid architecture assumptions, or explicit PM reprioritization.
6. Avoid speculative abstractions and opportunistic refactors.
7. Merge useful work immediately once acceptance, verification, review, and final dogfood pass.
8. AI assists the editor; it does not make creative decisions for them.

## Milestones

### M0 — Leo Boots

Establish the smallest viable Windows product chassis:

- clean repository;
- Python/PySide6 application;
- dependency/package setup;
- tests and CI;
- licensing and attribution;
- tray application;
- basic overlay rendering;
- DaVinci Resolve foreground detection;
- packaging skeleton.

No public release is required.

### M1 — Leo Can See, Hear, and Point

Complete the first end-to-end screenshot/voice/VLM/pointer interaction and release `v0.1.0-alpha`.

### M2 — Resolve Tutor

Add grounded Resolve/Fusion knowledge, conversational context, concise tutoring, uncertainty handling, and release `v0.2.0-alpha`. Gate advancement on whether Leo is voluntarily useful during editing.

### M3 — Fusion-Native Intelligence

Combine screenshots with structured Resolve/Fusion state and release `v0.3.0-alpha`.

### M4 — Safe Copilot

Add verified, confirmable Resolve mutations and release `v0.4.0-alpha`.

### M5 — Intent-Level Workflows

Add higher-level editing workflows based on real dogfood pain, targeting `v0.5.x`.

### M6 — Productization

Only after external demand, invest in installer/updater polish, diagnostics, privacy, compatibility hardening, website, signed binaries, onboarding, and related distribution work.

## Persistent Chat Topology

### Project Manager

Owns product vision, roadmap, milestone priorities, backlog prioritization, scope, release readiness, product tradeoffs, and consequential dogfood discoveries. Return to it at milestone boundaries or when a blocker, idea, or dogfood discovery may change product priority, scope, release criteria, or roadmap. It does not require PR-by-PR status reports.

### Subsystem Architects

Persistent per meaningful subsystem and created on demand. They own subsystem boundaries, interfaces, technical tradeoffs, architecture documents, and decomposition into implementation slices.

Architect escalation rule:

- implementation detail -> send to Codex;
- subsystem design decision -> resolve in Architect chat;
- product/milestone decision -> escalate to Project Manager.

Escalations include Problem, Evidence, Impact, Options, Technical recommendation, and Decision required from PM.

### Codex Threads

Disposable, one per worktree/slice, sole writer for that worktree. Receive the issue, relevant architecture, constraints, acceptance criteria, dogfood scenario, and non-goals.

### Claude Review Threads

Disposable and read-only. Every PR gets review for concrete correctness, security, reliability, regression, or maintainability issues. Review must not expand scope or demand speculative abstractions or unrelated cleanup.

### Greptile

Optional ambient reviewer in parallel with Claude and CI; not a serial gate and not an authority by score.

## Durable State Ownership

- Product vision and priorities: Project Manager.
- Backlog/execution status: GitHub Issues and Milestones.
- Shipped work: Git history and Releases.
- Architecture: Architect chats plus committed docs.
- Implementation behavior: code.
- Acceptance criteria: GitHub Issue.
- Dogfood results: Issue/PR.
- Review findings: PR.
- Agent rules: `AGENTS.md`.

> Chats reason. The repository remembers.

## GitHub Structure

Use Issues, Milestones, Pull Requests, and Releases. Do not add a GitHub Projects/Kanban board until real complexity demonstrates a need.

Expected documentation structure:

```text
docs/
├── architecture/
├── decisions/
├── dogfood/
│   └── scenarios/
└── superpowers/
    ├── specs/
    └── plans/

AGENTS.md
README.md
LICENSE
THIRD_PARTY_NOTICES.md
```

## Two-Tier Design Process

Architectural work uses an Architect chat, Superpowers architectural brainstorming, durable spec, and implementation plan. Ordinary vertical slices that fit an approved subsystem architecture use a concise GitHub issue with acceptance criteria, a dogfood test, non-goals, and Codex implementation without a new architecture session.

## Parallel Development

Parallel implementation is encouraged when all are true:

1. slices modify different ownership boundaries;
2. they depend only on stable interfaces;
3. either branch could merge first without invalidating the other.

Otherwise serialize.

> Parallelize independent implementation. Serialize shared architectural decisions.

## Worktree Protocol

Each slice gets `feat/<short-name>` and `.worktrees/<short-name>` with one Codex thread as sole writer. Parallel worktrees should branch from a known common `main` state where practical.

## Issue Format

Each issue includes:

- Goal;
- Why now;
- Relevant architecture;
- Acceptance criteria;
- Dogfood scenario;
- Non-goals.

## Verification Protocol

Every meaningful PR requires relevant automated checks, initial real-Resolve dogfood, CI + Claude + Greptile review in parallel, in-scope fixes, automated verification again, and final real-Resolve dogfood.

Review findings:

- P0: must fix — safety, corruption, data loss, major breakage;
- P1: fix before merge — concrete bug, regression, race, failed acceptance;
- P2: fix if local — small reliability/maintainability issue without scope expansion;
- P3: not this PR — speculative improvement, unrelated refactor, new abstraction, future feature.

P3 does not block merge and does not automatically become backlog work.

## Definition of Done

A Leo slice is complete only when:

- user-visible goal is satisfied;
- acceptance criteria pass;
- relevant automated tests/evals pass;
- initial real-Resolve dogfood passes;
- Claude review completes;
- Greptile review completes when available;
- valid P0/P1 findings are resolved;
- scope has not expanded unnecessarily;
- final real-Resolve dogfood passes;
- `main` will remain runnable after merge.

## Release Strategy

Source is public from the beginning. Development builds are dogfooded continuously. Public binaries ship at meaningful milestone boundaries. Use `main` as the always-runnable branch, temporary feature branches, and release tags. Do not introduce a permanent `develop` branch or release branches initially.

## Milestone Completion

A milestone is not complete merely because planned issues are closed. At the boundary, the Project Manager evaluates whether the promised experience works, whether Leo is voluntarily useful, major frustrations, failed assumptions, release blockers, and whether dogfooding changes the next priority. The PM chooses release, patch, extend milestone, or revise roadmap.

## Governing Optimization

> Ship the smallest capability that materially improves the DaVinci Resolve experience, verify it in real Resolve, merge it, and resist work that does not move Leo toward the next useful state.
