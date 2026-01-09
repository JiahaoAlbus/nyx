# L0 Identity Skeleton

Purpose
- Define the non-account-based Identity boundary for L0.
- Provide Root Secret generation, context-bound derivation, and lifecycle rules.

Boundary and interfaces
- Creation and use accept only RootSecret and Context types.
- No string-based identity identifiers are accepted.
- Runtime guard rejects account-like identifiers (0x..., did:pkh, eip155) with code NYX_CONFORMANCE_WALLET_AS_IDENTITY.

Root Secret
- Generated locally only; no import from external identifiers.
- Export/serialization is prohibited; only redacted output is permitted.

Context
- Required for every derive/serialize call.
- Domain separation is enforced with a fixed tag; no default context exists.

Serialization
- Requires explicit Context input.
- Output is context-bound and non-stable across time.

State machine
- Created -> Active -> Rotated -> Destroyed
- Illegal transitions fail.
- Destroyed is terminal; derive/serialize/use is forbidden.
- Rotation retires previous material; old tokens are rejected.

Prohibited identifiers
- address
- account
- wallet
- pubkey
- globalId

Tests
- Same context yields stable derivation; different contexts and roots diverge.
- Serialization is context-bound and non-stable.
- Lifecycle and guardrails are enforced.
