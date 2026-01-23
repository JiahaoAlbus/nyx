# Q9 Economy and Fees

## Purpose
Define testnet economic rules and fee routing for Q9 with immutable invariants.

## Scope
Applies to testnet economic actions: transfer, trade, purchase, and paid interactions.

## Non-Scope
No protocol fee formula changes. No mainnet policies.

## Definitions
- Protocol fee: The mandatory fee enforced by core NYX economic rules.
- Platform fee: An additive overlay fee that MUST NOT replace protocol fee.
- Treasury address: The testnet fee destination loaded from NYX_TESTNET_FEE_ADDRESS.

## Normative Rules (MUST / MUST NOT)
- Protocol fee MUST remain > 0 for any shared-state mutation.
- Platform fee MUST be additive only and MUST NOT reduce or waive protocol fee.
- Fee routing MUST credit the treasury address from NYX_TESTNET_FEE_ADDRESS.
- Economic actions MUST record deterministic receipts and evidence artifacts.
- Fee calculations MUST be deterministic and integer-only.
- If the treasury address is missing, actions that require fees MUST fail deterministically.

## Evidence and Verification
- Fee behavior MUST be verified by unit tests and conformance drills.
- Canonical verification commands:
  - python -m compileall packages/l0-identity/src
  - python scripts/nyx_run_all_unittests.py
  - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json

## Freeze / Change Control
- Fee invariants are sealed for Q9 Testnet Alpha.
- Any change to fee routing MUST include regression evidence.
