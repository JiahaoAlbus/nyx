## Purpose
- Provide an auditor-ready pack for Q10 Testnet Beta, with deterministic evidence and reproducible commands.

## Scope
- Testnet Beta flows: wallet, exchange, chat, marketplace, entertainment.
- Evidence bundles and replay verification.
- Treasury fee routing and additive platform fee rules.

## Non-Scope
- Mainnet claims or mainnet operations.
- External wallet integrations.
- KYC or identity systems.

## Required Evidence
- Evidence bundles for each module action with required fields:
  - protocol_anchor, inputs, outputs, receipt_hashes, state_hash, replay_ok, stdout
- Deterministic export artifacts (zip with fixed metadata).
- Conformance report output (nyx_conformance_report.json).

## Reproduction Steps (Canonical)
- python -m compileall packages/l0-identity/src
- python scripts/nyx_run_all_unittests.py
- PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json
- python scripts/q10_repro_one_shot.py

## Verification Criteria
- All tests must pass with TOTAL_TESTS non-zero.
- Conformance report must indicate ok.
- Evidence bundles must be deterministic and replayable.
- Fees for value-moving actions must be > 0 and routed to treasury.

## Freeze and Change Control
- This pack is normative for Q10 Testnet Beta audits.
- Changes MUST be additive and MUST NOT alter existing evidence outputs.
