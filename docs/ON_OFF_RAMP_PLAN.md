# ON_OFF_RAMP_PLAN

## Purpose
Define a non-production on/off integration plan with strict boundaries and evidence requirements.

## Scope
- Adapter boundary and evidence format for on/off integrations.
- Compliance hooks that do not alter core protocol rules.
- Operational controls and audit trails.

## Non-Scope
- Production compliance implementation.
- Custodial guarantees or identity verification flows.

## Invariants/Rules
- Core protocol rules MUST remain unchanged by on/off integrations.
- No shortcut is allowed around fee enforcement, replay, or proof checks.
- Integrations MUST NOT introduce address-based ownership semantics.

## Evidence/Verification
- conformance v3 drills include on/off shortcut detection (Q4-ONOFF-01).
- Audit pack commands must reproduce identical results.

## Freeze/Change Control
- Plan changes MUST follow `docs/CHANGE_CONTROL.md`.
- After freeze, only patch-only fixes or additive extensions are allowed.

## Evidence Format (Minimum)
- Action receipt with before/after hashes.
- Deterministic replay inputs.
- External adapter metadata kept separate from core evidence.
