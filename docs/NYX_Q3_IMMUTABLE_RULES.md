# NYX Q3 Immutable Rules

## Never Change (Immutable)
- Proof envelopes bind context, statement, nonce, and canonical public inputs.
- Context separation is mandatory; wrong context must fail verification.
- Nullifier reuse is forbidden and must fail deterministically.
- State mutation requires a non-zero fee.
- Sponsorship may change payer only; amounts are unchanged.
- Replayable traces must be deterministic and auditable.

## Extension Points (Allowed)
- Swap mock proof adapter for a real proof system.
- Extend public inputs with new fields while preserving existing bindings.
- Add new statement types without weakening current ones.
- Add new drills and guards without removing existing rules.

## Guard Coverage
- Guard tests enforce binding fields and context separation.
- Red-team drills validate rejection of illegal shortcut paths.
