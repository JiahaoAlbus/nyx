# Change Control

## Purpose
Define the change policy after Q4 freeze to prevent semantic drift.

## Scope
- DEX v0 semantics, interfaces, and invariants.
- Conformance rules and determinism guarantees.

## Non-Scope
- New protocol versions that explicitly change semantics.

## Rules
- Semantic changes after freeze are rejected by default.
- Only two categories are permitted:
  1) Patch: zero semantic change, plus a regression test or drill.
  2) Additive extension: new optional surface that does not alter frozen semantics.
- Any semantic change requires a new protocol version and deployment.
- Every patch MUST add a test or drill that would have caught the issue.

## Evidence / Verification
- PRs MUST include exact commands executed and results.
- Regression tests MUST be in the CI-discovered test set.

## Freeze / Change Control
- Immutable rules are indexed in `docs/NYX_Q4_IMMUTABLE_RULES.md`.
- Violations require a new version and explicit approval.
