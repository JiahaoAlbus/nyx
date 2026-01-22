# Q8 Closeout Report

Purpose
- Record objective evidence and status for the Q8 ecosystem delivery.

Scope
- Q8 web portal, backend gateway, and iOS reference client, including evidence export and replay.

Non-Scope
- Protocol semantic changes or fee rule changes.
- Live operational claims or external service dependencies.

Closeout Checklist (Facts Only)
- Canonical verification commands executed with green results.
- Conformance runner executed and report produced.
- Evidence exports verified deterministic for fixed inputs.
- UI copy guard and path traversal guard remain enforced.

Evidence / Verification
- Canonical commands:
  - python -m compileall packages/l0-identity/src
  - python scripts/nyx_run_all_unittests.py
  - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
  - python scripts/q8_repro_one_shot.py
- Evidence artifacts:
  - /tmp/nyx_conformance_report.json
  - apps/nyx-backend/repro/* (deterministic exports)

Freeze / Change Control
- Q8 closeout only records evidence. Any future changes must be additive or zero-semantic with regression proof.
