# Q10 Release Window (Testnet Beta)

## Purpose
Define the Testnet Beta release window rules for Q10, with objective, auditable steps.

## Scope
Release-window procedures for Q10 Testnet Beta only.

## Non-Scope
- Mainnet authorization.
- Any protocol semantic changes.

## Rules (MUST / MUST NOT)
- The release window MUST be executed only after all Q10 PRs are merged.
- Only docs, evidence updates, or zero-semantic patches with regression tests are allowed during the window.
- No new features MAY be introduced in the release window.
- Verification commands MUST pass before any release label is applied.

## Evidence / Verification
Use the canonical verification commands defined in the Q10 audit reproduction documentation.

## Freeze / Change Control
Any change during the release window MUST be additive and explicitly documented with evidence.
