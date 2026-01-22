# Q8 Release Notes (RC)

Purpose
- Record the Q8 release candidate scope and evidence without altering sealed protocol semantics.

Scope
- Ecosystem web portal, backend gateway, iOS reference client, and evidence export.

Non-Scope
- Protocol semantic changes or fee model changes.
- Production bridge or on/off ramp execution.

What Shipped
- Web portal routes with deterministic evidence export flows.
- Backend gateway with deterministic evidence bundle export.
- Reference iOS client shell using the same backend endpoints.
- Conformance drills for UI copy guard, path traversal, and fee additivity.

What Did Not Ship
- Production UI, login, wallet connect, or live market data.
- Real-time chat or marketplace inventory.

Verification
- python -m compileall packages/l0-identity/src
- python scripts/nyx_run_all_unittests.py
- PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
- python scripts/q8_repro_one_shot.py

Freeze and Change Control
- Q8 RC is additive only. Any semantic change requires a new version and regression evidence.
