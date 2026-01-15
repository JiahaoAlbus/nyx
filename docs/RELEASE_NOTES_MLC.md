# RELEASE_NOTES_MLC

## Purpose
Record what shipped and what did not for the MLC release window.

## Scope
- DEX v0 implementation, receipts, replay, and conformance v3 drills.
- Audit pack and operational runbooks.

## Non-Scope
- Production bridge or on/off integration.
- Production cryptography assurances.

## What Shipped
- DEX v0 actions, receipts, replay, and determinism guards.
- Conformance v3 drills and audit pack materials.
- Runbooks and release process documentation.

## What Did Not Ship
- Production bridge implementation.
- Production on/off integration.
- Mainnet tag (pending checklist Go).

## Invariants/Rules
- Fee required for state mutation.
- Deterministic receipts and replay.
- Patch-only policy after freeze.

## Evidence/Verification
- See `docs/AUDIT_PACK_MLC.md` and `docs/AUDIT_CHECKLIST_MLC.md`.

## Freeze/Change Control
- Follow `docs/CHANGE_CONTROL.md`.
