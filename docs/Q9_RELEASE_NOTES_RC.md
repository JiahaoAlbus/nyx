# Q9 Testnet Alpha RC Release Notes

## Purpose
Provide a factual, reproducible record for the Q9 Testnet Alpha release candidate (RC).

## Scope
Covers Q9 Testnet Alpha features, evidence artifacts, and verification commands for RC status.

## Non-Scope
No protocol semantic changes. No mainnet claims. No new runtime behavior beyond Q9 additions.

## What Shipped (Facts)
- Testnet Alpha Exchange, Chat, Marketplace, Entertainment flows with deterministic evidence export.
- Evidence Truth Layer preserved with immutable fields and deterministic zip export.
- Backend gateway with strict validation and safe artifact handling.
- iOS client shell aligned to backend endpoints for Testnet Alpha.

## What Did Not Ship (Facts)
- No mainnet release.
- No login, wallet connect, balances, or real market data feeds.
- No UI claims of live operational status.

## Verification
Run the canonical verification commands:
- python -m compileall packages/l0-identity/src
- python scripts/nyx_run_all_unittests.py
- PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json

## Evidence Artifacts
- nyx_conformance_report.json
- Deterministic evidence bundles produced by Q9 flows

## Freeze / Change Control
- Q1–Q8 semantics remain sealed.
- Q9 RC allows documentation updates and zero-semantic patches only.
