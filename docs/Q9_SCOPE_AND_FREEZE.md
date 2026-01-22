# Q9 Scope and Freeze

Purpose
- Define the Q9 Testnet Alpha scope and the freeze rules for delivery.

Scope
- iOS-first ecosystem alpha with Exchange, Chat, Marketplace, and Entertainment flows.
- Backend gateway with deterministic evidence export and testnet fee routing.
- Evidence remains aligned with the Q7 Evidence Format v1 and Q7 output contract.

Non-Scope
- Any change to sealed protocol semantics.
- Any UI feature that introduces accounts, wallets, or user profiles.
- Any live mainnet claims or real-time market data feeds.

Freeze Rules (MUST / MUST NOT)
- Q9 MUST NOT alter Q1–Q5 sealed semantics or deterministic outputs for existing flows.
- Evidence fields and ordering MUST remain identical to Evidence Format v1.
- The UI MUST remain a thin client that renders evidence verbatim.
- The backend MUST treat the evidence generator as the source of truth.
- Q9 MUST NOT introduce login/signup flows or persistent user state.

Evidence / Verification
- python -m compileall packages/l0-identity/src
- python scripts/nyx_run_all_unittests.py
- PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json

Change Control
- After Q9 kickoff, changes are limited to docs, execution evidence, or zero-semantic patches with regression proof.
