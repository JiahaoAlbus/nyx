# AUDIT_PACK_MLC

## Purpose
Provide a deterministic, replayable audit pack for the DEX v0 launch candidate.

## Scope
- DEX v0 receipts and replay verification.
- Conformance v3 drills and report schema.
- Determinism guards and bounded explorer evidence.

## Non-Scope
- Production cryptography assurances.
- Production bridge or on/off integration implementation.

## Invariants/Rules
- Fee required for any shared-state mutation.
- Receipts and replay MUST be deterministic and reproducible.
- Context separation and verify-only enforcement remain intact.
- No address-based ownership semantics in DEX receipts.

## Evidence/Verification
Run the exact commands below:

```
python -m compileall packages/l0-identity/src
python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v
```

DEX demo (deterministic):

```
python demo/mlc_dex_demo.py --seed 1
```

Conformance runner with JSON output:

```
PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
```

## Freeze/Change Control
- Follow `docs/CHANGE_CONTROL.md` for any post-freeze changes.
- Patch-only or additive extensions only; no semantic changes.
