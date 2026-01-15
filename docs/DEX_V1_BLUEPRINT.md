# DEX v1 Blueprint

## Purpose
Freeze the DEX v1 interface and invariants and define the v0 strict subset.

## Scope
- DEX state model, actions, receipts, and replay hooks.
- Deterministic rules and bounds for integer arithmetic.

## Non-Scope
- Production bridge implementation.
- Any external liquidity routing.

## Module Boundaries and Interfaces
- `state.py`: PoolState and DEX state containers.
- `actions.py`: CreatePool, AddLiquidity, RemoveLiquidity, Swap.
- `receipts.py`: deterministic receipts and serialization.
- `replay.py`: deterministic replay from receipts.
- `invariants.py`: invariant checks for tests and explorers.

## Upgrade Boundaries and Emergency Brake Boundaries
- DEX v0 semantics MUST NOT change after freeze.
- Any emergency pause MUST NOT bypass fee enforcement.
- No privileged override paths are permitted.

## Governance Boundaries
- Governance may add new pools or assets only via defined actions.
- Governance MUST NOT alter state transition rules without a new version.

## DEX v0 Strict Subset Statement
- DEX v0 is a strict subset of the final DEX v1 interface.
- v0 omits any features not explicitly listed in this blueprint.

## Exit-Right Invariant
- RemoveLiquidity MUST always be available to redeem proportional assets.
- Exit-right MUST NOT be revoked by later actions.

## Rounding and Bounds Policies (Normative)
- All arithmetic is integer-only.
- Rounding MUST be explicit and tested (floor or ceil as defined).
- Input amounts MUST be bounded and invalid values MUST be rejected.

## Evidence / Verification
- Property tests: `packages/l3-dex/test/property_invariants_test.py`.
- Bounded explorer: `packages/l3-dex/test/bounded_explorer_test.py`.
- Conformance drills: `packages/conformance-v1/test/runtime_drills_v3_test.py`.

## Freeze / Change Control
- After Week 2, the DEX v0 interface and semantics are frozen.
- Post-freeze changes follow `docs/CHANGE_CONTROL.md`.
