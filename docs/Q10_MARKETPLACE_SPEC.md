## Purpose
- Define Testnet Beta marketplace boundaries, receipts, and fee rules.

## Scope
- Deterministic listing creation, purchase intent, and receipt generation.
- Evidence bundle export for listing and purchase actions.
- Platform fee metadata as additive overlay where configured.

## Non-Scope
- No real inventory or real payment processing.
- No external merchant integration.
- No user profiles or account reputation systems.

## Definitions
- "Listing": deterministic catalog entry stored in testnet storage.
- "Purchase intent": deterministic action referencing a listing and quantity.
- "Receipt": deterministic result produced by backend for listing or purchase.

## Normative Rules (MUST / MUST NOT)
- Listing creation MUST be deterministic for the same inputs.
- Purchase intent MUST be deterministic for the same inputs.
- Every listing and purchase action MUST produce a receipt and evidence bundle.
- Evidence bundle fields MUST be exported verbatim in required order.
- Protocol fee MUST remain non-zero for value-moving actions.
- Platform fee, if configured, MUST be additive and MUST NOT replace protocol fee.
- The marketplace MUST NOT claim real inventory, real delivery, or live merchant status.
- The marketplace MUST NOT store user profiles or balance data.

## Security and Abuse Boundaries
- Payloads MUST be size-bounded and validated.
- Rate limiting MUST be applied at the backend gateway.
- Error messages MUST be deterministic and MUST NOT include sensitive inputs.

## Evidence and Verification
- Required fields:
  - protocol_anchor, inputs, outputs, receipt_hashes, state_hash, replay_ok, stdout
- Evidence export MUST be deterministic and replayable.

## Freeze and Change Control
- This specification is normative for Q10 Testnet Beta.
- Changes MUST be additive and MUST NOT alter existing evidence outputs.
