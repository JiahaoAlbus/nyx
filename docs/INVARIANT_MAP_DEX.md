# DEX Invariant Map

## Purpose
Map DEX invariants to test and drill evidence.

## Scope
- DEX v0 invariants and evidence links.

## Non-Scope
- External bridge implementations.

## Invariants → Evidence
| Invariant | Evidence (tests/drills) |
| --- | --- |
| No Free Action for mutations | `packages/l3-dex/test/unit_fee_required_test.py`, conformance drills |
| Deterministic receipts | `packages/l3-dex/test/golden_vectors_test.py`, `packages/l3-dex/test/replay_test.py` |
| Non-negative reserves and LP | `packages/l3-dex/test/property_invariants_test.py` |
| Exit-right preserved | `packages/l3-dex/test/unit_exit_right_test.py` |
| Bounds reject invalid inputs | `packages/l3-dex/test/unit_amount_caps_test.py` |
| Replay fidelity | `packages/l3-dex/test/replay_test.py` |
| Conformance drills reject illegal shortcuts | `packages/conformance-v1/test/runtime_drills_v3_test.py` |

## Evidence / Verification
- Run CI-equivalent tests:
  - `python -m compileall packages/l0-identity/src`
  - `python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v`

## Freeze / Change Control
- Changes after freeze MUST follow `docs/CHANGE_CONTROL.md`.
