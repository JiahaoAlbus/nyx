# DEX Security Case

## Purpose
Define security claims for DEX v0 and map each claim to evidence.

## Scope
- DEX v0 state transitions, receipts, and replay.
- Determinism, bounds, and conformance drills.

## Non-Scope
- Production bridge implementation.
- Production cryptography assurances beyond mock adapters.

## Assumptions
- Deterministic execution environment for tests and replay.
- Fee enforcement logic remains unchanged in the fee engine.
- Replay inputs are canonicalized and validated before use.

## Trust Boundaries
- DEX logic is deterministic and self-contained.
- Fee enforcement is a separate module; DEX must not bypass it.
- Bridge and on/off components are treated as untrusted adapters.

## Claims
1) No Free Action: any shared-state mutation requires non-zero fee.
2) Receipts are deterministic and replayable across machines.
3) State transitions reject invalid inputs and out-of-bounds values.
4) Conformance drills detect illegal shortcuts and reject them.
5) No secret material is present in receipts or logs.

## Evidence Mapping
- Claim 1: `packages/l3-dex/test/unit_fee_required_test.py`, conformance drills.
- Claim 2: `packages/l3-dex/test/golden_vectors_test.py`, `packages/l3-dex/test/replay_test.py`.
- Claim 3: `packages/l3-dex/test/unit_amount_caps_test.py`, `packages/l3-dex/test/unit_swap_boundary_test.py`.
- Claim 4: `packages/conformance-v1/test/runtime_drills_v3_test.py`.
- Claim 5: `packages/l3-dex/test/guard_no_secret_leak_test.py`.

## Residual Risk and Acceptance Criteria
- Residual risk is accepted only when bounded by tests and drills.
- Any regression MUST add a new test or drill proving no semantic drift.
