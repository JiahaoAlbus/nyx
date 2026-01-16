# NYX Q4 Immutable Rules

## Purpose
Record immutable DEX v0 rules and allowed extensions.

## Scope
- DEX v0 semantics, interfaces, and invariants.

## Non-Scope
- New protocol versions with explicit semantic changes.

## Immutable Rules
- DEX v0 semantics MUST NOT change after Week 7 freeze.
- Shared-state mutation MUST enforce non-zero fees.
- Proof context separation MUST reject wrong context and statement.
- Client signing material MUST NOT define identity semantics.
- Receipts MUST be deterministic and replayable.
- No unauthorized override paths are permitted.

## Allowed Extensions
- Add new actions only by creating a new versioned protocol.
- Add new optional fields if they do not alter existing semantics.
- Add new drills and tests without removing existing ones.

## Break-Glass Conditions (Patch Only)
- A patch MUST be zero semantic change and include a regression test or drill.
- Any semantic change requires a new version and deployment.

## Evidence / Verification
- Determinism: `packages/l3-dex/test/golden_vectors_test.py`.
- Invariants: `packages/l3-dex/test/property_invariants_test.py`.
- Conformance drills: `packages/conformance-v1/test/runtime_drills_illegal_shortcuts_test.py`.

## Freeze / Change Control
- See `docs/CHANGE_CONTROL.md`.
- F1: DEX v0 behavior frozen at end of Week 7.
