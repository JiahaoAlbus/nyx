# Q9 Testnet Fee Policy

Purpose
- Define fee rules for Q9 Testnet Alpha without changing sealed protocol semantics.

Scope
- Protocol fees for shared-state mutations.
- Additive platform fees collected at defined extension points.
- Routing to a testnet fee vault address provided by environment configuration.

Non-Scope
- Mainnet fee routing or production settlement.
- Fee waivers or special cases that bypass protocol fees.

Normative Rules (MUST / MUST NOT)
- Every shared-state mutation MUST incur a protocol fee greater than zero.
- Platform fees MUST be additive and MUST NOT replace or reduce protocol fees.
- Fee routing MUST use a testnet fee vault address supplied via environment configuration.
- Fee routing configuration MUST NOT be committed to the repository.
- The backend MUST reject fee processing if the testnet fee vault address is missing.

Evidence / Verification
- Unit tests must verify protocol fee non-zero and platform fee additivity.
- Conformance drills must reject any attempt to waive protocol fees.

Change Control
- Any change to fee semantics requires a versioned specification and regression evidence.
