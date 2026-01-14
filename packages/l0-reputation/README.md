# L0 Reputation

Kernel v1 for pseudonymous reputation with deterministic roots and fee binding.

## Scope
- Context-bound pseudonym id
- RepEvent and RepState with deterministic root recompute
- Fee binding via l2-economics (mutation => non-zero fee)

## Invariants
- Pseudonym ids are bound to a context id
- Root recomputation is deterministic and order-independent
- State mutation requires a non-zero fee
- Sponsor changes payer only, never the amount

## Disclosure wiring (mock)
- Statements: REP_AT_LEAST, REP_TIER
- Public inputs include rep_root, pseudonym_id, and v=1 plus k or tier
- Verify path uses l0-zk-id verification (mock prover only for generation)

## Non-goals
- UI or client workflows
- Production cryptography claims
- Proof integration (tracked in later weeks)
