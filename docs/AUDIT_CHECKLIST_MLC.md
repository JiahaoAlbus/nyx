# AUDIT_CHECKLIST_MLC

## Purpose
Provide a step-by-step, deterministic audit checklist for DEX v0.

## Scope
- Local verification of tests, replay, and conformance drills.

## Non-Scope
- Production deployment approval or key ceremony execution.

## Invariants/Rules
- All checks MUST pass before release consideration.
- Any failure MUST halt the process.

## Evidence/Verification

Phase 0 — Clean Room
[ ] Working tree clean
    - git status
[ ] Baseline updated
    - git checkout main && git pull
[ ] Record HEAD
    - git rev-parse HEAD

Phase 1 — CI-Equivalent Gate
[ ] Compile check
    - python -m compileall packages/l0-identity/src
[ ] Full test suite
    - python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v
    PASS: final line shows "OK" and no failures

Phase 2 — DEX Demo
[ ] Run deterministic demo
    - python demo/mlc_dex_demo.py --seed 1
    PASS: output includes replay_ok=True

Phase 3 — Conformance
[ ] Conformance runner
    - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
    PASS: exit code 0 and report file exists

## Freeze/Change Control
- Follow `docs/CHANGE_CONTROL.md` for any changes.
- Patch-only or additive extensions only after freeze.
