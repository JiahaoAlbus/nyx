# Q9 Testnet Alpha Go / No-Go

## Purpose
Provide objective, verifiable criteria to determine Q9 Testnet Alpha RC readiness.

## Scope
Testnet Alpha only. No mainnet claims.

## Non-Scope
No protocol semantic changes. No operational guarantees.

## Go Criteria (All MUST be satisfied)
- Canonical verification commands pass:
  - python -m compileall packages/l0-identity/src
  - python scripts/nyx_run_all_unittests.py
  - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json
- Deterministic evidence bundles produced for Exchange, Chat, Marketplace, Entertainment actions.
- Evidence fields present and ordered per immutable contract.
- No fake live claims in UI or backend copy.
- Protocol fee remains > 0 for shared-state mutations; platform fee is additive only.

## No-Go Criteria (Any triggers No-Go)
- Any failed canonical verification command.
- Missing or malformed evidence fields.
- Evidence export not deterministic for fixed inputs.
- Any identity/account semantics present in UI or backend copy.
- Any path traversal or unsafe artifact access detected.

## Evidence Required
- nyx_conformance_report.json
- Testnet Alpha evidence bundles and deterministic zip exports
- CI status for Q9 PRs

## Freeze / Change Control
- RC is documentation- and evidence-only.
- No semantic changes to sealed baseline.
