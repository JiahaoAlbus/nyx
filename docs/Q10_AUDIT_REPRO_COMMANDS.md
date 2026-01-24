## Purpose
- Define the single canonical reproduction commands for Q10 Testnet Beta.

## Canonical Verification Commands
- python -m compileall packages/l0-identity/src
- python scripts/nyx_run_all_unittests.py
- PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json

## One-Shot Reproduction
- python scripts/q10_repro_one_shot.py

## Expected Signals
- TOTAL_TESTS is non-zero and all tests pass.
- Conformance report indicates ok.
- One-shot script prints state_hash, receipt_hashes, replay_ok.

## Determinism Rules
- Explicit seed is required for deterministic runs.
- No timestamps in evidence artifacts.
- Evidence outputs must be byte-for-byte stable for the same inputs.
