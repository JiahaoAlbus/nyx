# Q9 Data and Identity Boundary

Purpose
- Define the data boundary for Q9 Testnet Alpha and prohibit identity semantics.

Scope
- Testnet data storage for orders, messages, listings, purchases, and evidence runs.
- Deterministic evidence generation and export.

Non-Scope
- Any identity system or persistent user profiles.
- Any real-time messaging network or live market data.

Normative Rules (MUST / MUST NOT)
- The system MUST NOT treat sender metadata as identity.
- The UI MUST NOT display or store personal profiles or persistent user accounts.
- Evidence artifacts MUST exclude any secret material and MUST be deterministic.
- Testnet data MUST be labeled as Testnet Alpha and MUST NOT claim mainnet status.

Evidence / Verification
- Guard tests must detect forbidden identity semantics in UI copy and backend responses.
- Determinism tests must confirm evidence outputs are stable for identical inputs.

Change Control
- Any extension that introduces user accounts or identity semantics requires a new versioned specification.
