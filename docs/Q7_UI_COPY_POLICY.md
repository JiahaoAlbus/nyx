# Q7 UI Copy Policy

## Purpose
Define strict copy rules for Q7 reference UI to prevent implicit semantics or live claims.

## Scope
All UI text, labels, and placeholders in Q7 reference UI and backend responses.

## Non-Scope
Protocol semantics, fee rules, or receipt formats.

## Normative Rules (MUST/MUST NOT)
- UI copy MUST state that all views are preview-only with no live data.
- UI copy MUST NOT claim any live system status or operational metrics.
- UI copy MUST NOT imply authentication, accounts, or personal identity.
- UI copy MUST NOT mention trading, balances, or live market data as active behavior.
- UI copy MUST label all metrics as placeholders.
- UI copy MUST keep evidence fields verbatim and unmodified.

## Security and Abuse Boundaries
- UI copy MUST NOT imply the system is connected to live infrastructure.
- UI copy MUST NOT create trust expectations beyond the evidence bundle.

## Evidence and Enforcement
- Conformance checks SHOULD scan UI copy for prohibited claims.
- UI tests SHOULD assert that preview banners are present on every page.

## Change Control
This policy is normative. Changes require a version bump and explicit review.
