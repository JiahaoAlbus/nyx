## Purpose
- Define Testnet Beta entertainment actions, receipts, and evidence rules.

## Scope
- Deterministic content items and state transitions.
- Evidence bundle export for entertainment actions.

## Non-Scope
- No live events or live streaming claims.
- No user profiles, rankings, or external integrations.
- No real-world rewards or payouts.

## Definitions
- "Content item": deterministic entry stored in testnet storage.
- "Action": deterministic interaction that updates testnet state.

## Normative Rules (MUST / MUST NOT)
- Entertainment actions MUST be deterministic for the same inputs.
- Each action MUST produce a receipt and evidence bundle.
- Evidence fields MUST be exported verbatim and in the required order.
- Evidence bundles MUST be deterministic and replayable.
- The module MUST NOT claim live network status or mainnet activity.
- The module MUST NOT store user profiles or balance data.
- Economic actions, if any, MUST preserve protocol fee > 0 and additive platform fee rules.

## Security and Abuse Boundaries
- Payloads MUST be size-bounded and validated.
- Rate limiting MUST be applied at the backend gateway.
- Error messages MUST be deterministic and MUST NOT include sensitive inputs.

## Evidence and Verification
- Required fields:
  - protocol_anchor, inputs, outputs, receipt_hashes, state_hash, replay_ok, stdout
- Replay validation MUST return replay_ok=True for valid evidence.

## Freeze and Change Control
- This specification is normative for Q10 Testnet Beta.
- Changes MUST be additive and MUST NOT alter existing evidence outputs.
