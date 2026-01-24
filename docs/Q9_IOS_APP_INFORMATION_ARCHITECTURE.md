# Q9 iOS App Information Architecture

## Purpose
Define the iOS Testnet Alpha information architecture and navigation for the NYX World app.

## Scope
Applies to the iOS shell only. No protocol semantics are changed.

## Non-Scope
No external wallet connect, no mainnet status, no live market data.

## Sections (Top-Level)
- World Home
- Wallet
- Exchange
- Marketplace
- Chat
- Entertainment
- Evidence Viewer
- Trust

## Normative Rules (MUST / MUST NOT)
- The iOS app MUST label all views as Testnet Alpha.
- The iOS app MUST use deterministic runs with explicit seed input.
- The iOS app MUST NOT compute or modify evidence fields.
- The iOS app MUST NOT include login or signup flows.
- The iOS app MUST NOT show live metrics or external network claims.
- Evidence viewing MUST display protocol_anchor, inputs, outputs, receipt_hashes, state_hash, replay_ok, stdout verbatim.

## Evidence and Verification
- iOS flows MUST be verified by deterministic tests and evidence export checks.
- Canonical verification commands:
  - python -m compileall packages/l0-identity/src
  - python scripts/nyx_run_all_unittests.py
  - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json

## Freeze / Change Control
- Q9 UI architecture is additive and must not alter sealed baseline semantics.
