# BRIDGE_STRATEGY

## Purpose
Define the non-production bridge strategy, adapter boundary, and evidence format for DEX v0.

## Scope
- Adapter interface boundary and responsibilities.
- Evidence format expectations (receipt, state hash, replay inputs).
- Threat model highlights for bridge integration.

## Non-Scope
- Production bridge implementation.
- Custody assumptions or cross-chain finality guarantees.
- Any privileged trust model for adapter outputs.

## Invariants/Rules
- The adapter MUST be treated as untrusted input.
- Core validation MUST rely on deterministic replay and receipt checks.
- No shortcut is allowed around fee enforcement or replay verification.
- DEX receipts MUST NOT add address-based semantics.

## Evidence/Verification
- conformance v3 drills: Q4-BRIDGE-01, Q4-DEX-01..Q4-DEX-06.
- DEX replay tests and determinism guards in `packages/l3-dex/test`.

## Freeze/Change Control
- Strategy changes MUST follow `docs/CHANGE_CONTROL.md`.
- After freeze, only patch-only fixes or additive extensions are allowed.

## Selection Matrix (High-Level)
- Security posture: MUST remain untrusted and verifiable by replay.
- Evidence integrity: MUST include receipt, before/after hashes, and action payload.
- Operational risk: MUST be bounded with deterministic validation paths.
