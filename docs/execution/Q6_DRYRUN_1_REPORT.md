# Q6 Dry Run 1 Report

Purpose
- Record the first controlled dry run of Q6 execution steps.

Scope
- Evidence of command execution, outputs, and deterministic checks.

Non-Scope
- Any protocol change or semantic change.

MUST and MUST NOT
- The dry run MUST record exact commands and outputs.
- The dry run MUST NOT include secrets or sensitive material.
- The dry run MUST NOT claim Go if evidence is incomplete.

Run Summary
- Status: Completed
- Operator: local execution (no CI)
- Date (UTC): 2026-01-19
- Environment: macOS local run, Python stdlib only

Executed Commands
- Command: `python -m compileall packages/l0-identity/src`
  Output summary: `Listing 'packages/l0-identity/src'...` (no errors)
- Command: `python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v`
  Output summary: `Ran 262 tests in 15.810s` and `OK`
  PROPERTY_N: `PROPERTY_N=2000` (observed in output)
- Command: `PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json`
  Output summary: `conformance ok`
- Command: `python packages/e2e-private-transfer/src/e2e_private_transfer/run_demo.py --out /tmp/nyx_q6_private_trace.json --seed 123`
  Output summary: `fee_total=390 tx_hash=5ef0ff12c065 block_hash=5d6a7bb290f4 state_root=b7e876a7e0b2 receipt_hash=6b9e84d92d66 replay_ok=True`

Evidence Artifacts
- Conformance report path: `/tmp/nyx_conformance_report.json`
- Demo stdout: `docs/execution/q6_demo_out.txt`
- Demo trace summary: `docs/execution/q6_e2e_demo_trace.json`
- Hashes:
  - `docs/execution/q6_demo_out.txt` sha256 `a37f600b3441821e69e430f3bf9b7373f4fedecab515674eb2d3716f8cf7d688`
  - `docs/execution/q6_e2e_demo_trace.json` sha256 `8f4abee0fabef51ea7e79137b576cf4c7e8bb6a8b6f80775d090fb36684ad6ed`
  - `/tmp/nyx_conformance_report.json` sha256 `25c4e5ad5086ef44111d5c50862669ff93899f40b1c33c7515d5608fedbedff8`
- Notes: Deterministic demo output captured; no secrets included.

Evidence / Verification
- Canonical commands are listed in `docs/AUDIT_REPRO_COMMANDS.md`.

Freeze / Change Control
- Execution-only report; no protocol changes.
