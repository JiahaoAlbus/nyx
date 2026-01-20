# Q7 Execution Plan (Week 1 Freeze)

Purpose
- Freeze Q7 structure before any UI or SDK implementation.

Scope
- Locations, commands, scope boundaries, and invariant carry-over for Q7.

Non-Scope
- Any UI implementation or SDK implementation.
- Any protocol change or semantic change.

MUST and MUST NOT
- Q7 MUST keep protocol semantics sealed.
- Q7 MUST reuse existing verification commands.
- Q7 MUST NOT introduce new protocol behavior.
- Q7 MUST NOT embed secrets in any client-facing surface.

Q7 Objective
- Provide human-facing access to sealed protocol outputs through a thin client layer and a deterministic SDK wrapper.

Frozen Locations
- UI location (planned): `apps/nyx-reference-ui/`
- SDK location (planned): `packages/l4-client-sdk/`
- Q7 docs location: `docs/`

UI Strategy (Frozen)
- Strategy: zero-dependency static UI shell (HTML/CSS/JS), no build system.
- Rationale: aligns with existing `apps/` convention and minimizes toolchain risk.
- UI MUST NOT sign, store, or export secrets.
- UI MUST only render deterministic receipts and traces.

Verification Philosophy
- Canonical commands are reused from existing system verification:
  - `python -m compileall packages/l0-identity/src`
  - `python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v`
  - `PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json`

Week-by-Week Placeholders
- Week 01 — Structure freeze (this document)
- Week 02 — Placeholder (UI shell layout only)
- Week 03 — Placeholder (SDK wrapper shape only)
- Week 04 — Placeholder (docs and evidence mapping)
- Week 05 — Placeholder (integration rehearsal plan)
- Week 06 — Placeholder (execution rehearsal plan)
- Week 07 — Placeholder (determinism review plan)
- Week 08 — Placeholder (release readiness checklist)
- Week 09 — Placeholder (audit alignment plan)
- Week 10 — Placeholder (ops hardening plan)
- Week 11 — Placeholder (final review plan)
- Week 12 — Placeholder (release window plan)
- Week 13 — Placeholder (closeout plan)

Freeze / Change Control
- Q7 is structure-only until implementation is explicitly approved.
- Any protocol change remains out of scope and forbidden.
