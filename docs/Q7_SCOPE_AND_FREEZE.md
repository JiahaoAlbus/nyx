# Q7 Scope and Freeze Rules

Purpose
- Define Q7 scope, exclusions, and freeze rules before any implementation.

Scope
- UI shell planning, SDK wrapper planning, and documentation structure.

Non-Scope
- Any protocol change or semantic change.
- Any UI implementation or SDK implementation.

IN SCOPE
- UI shell as a thin client for deterministic receipts and traces.
- SDK wrapper that exposes read-only and submit-only operations already defined by sealed protocol modules.
- Documentation for users and developers with reproducible commands.

OUT OF SCOPE
- Protocol changes of any kind.
- DEX semantics changes.
- Fee model changes.
- Any shortcut around sealed rules.

Freeze Rules
- UI MUST be a thin client and must not embed secrets.
- UI MUST not generate keys or store sensitive material.
- UI MUST rely on deterministic receipts and traces only.
- SDK MUST be a wrapper and must not redefine protocol semantics.
- SDK MUST not bypass fee enforcement or verification steps.

UI Strategy (Frozen)
- Location: `apps/nyx-reference-ui/`
- Mode: static HTML/CSS/JS with no build system.
- UI MUST NOT perform signing or key management.
- UI MUST render only deterministic artifacts.

SDK Strategy (Frozen)
- Location: `packages/l4-client-sdk/`
- Mode: thin wrapper over existing sealed modules, no new protocol logic.
- SDK MUST not alter receipts or traces.

Verification Commands (Frozen)
- `python -m compileall packages/l0-identity/src`
- `python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v`
- `PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json`

Freeze / Change Control
- Q7 Week 1 is structural and doc-only.
- Any change beyond this scope requires a new week gate and explicit review.
