# Q8 Release Window

Purpose
- Define the Q8 release window rules and required evidence for the ecosystem layer.

Scope
- Release window operations for the Q8 web portal, backend gateway, and iOS reference client.

Non-Scope
- Any protocol semantic changes or fee rule changes.
- Any live operational claims.

Rules (MUST / MUST NOT)
- Releases MUST use the canonical verification commands and produce deterministic outputs.
- Changes during the release window MUST be docs-only or zero-semantic patches with regression evidence.
- The UI MUST remain a thin client and MUST NOT compute or modify evidence fields.
- Evidence exports MUST remain identical to the Q7 evidence format v1.
- The release window MUST NOT introduce identity, accounts, or live data claims.

Evidence / Verification
- python -m compileall packages/l0-identity/src
- python scripts/nyx_run_all_unittests.py
- PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
- python scripts/q8_repro_one_shot.py

Freeze / Change Control
- After Q8 closeout, only additive extensions or zero-semantic patches with regression evidence are allowed.
