# Q7 Audit Reproduction Commands

Purpose
- Provide the canonical commands to reproduce Q7 evidence deterministically.

Scope
- Local verification and evidence generation only.

Non-Scope
- No protocol changes.
- No network dependencies.

Commands
- Canonical tests:
  - python -m unittest discover -p "*_test.py" -v
- One-shot reproduction:
  - scripts/q7_repro_one_shot.sh

Evidence and Verification
- The one-shot script prints:
  - state_hash
  - receipt_hashes
  - replay_ok
- The export bundle is written to:
  - /tmp/nyx_q7_repro_export.zip

Freeze and Change Control
- These commands are normative for Q7 audits.
- Changes require a versioned update and regression evidence.
