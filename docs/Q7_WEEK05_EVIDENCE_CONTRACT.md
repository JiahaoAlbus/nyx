# Q7 Week 05 Evidence Contract

## Purpose
Define the exact evidence fields and export structure required for the Week 05 reference UI and backend.

## Scope
The Week 05 reference UI and backend evidence export only.

## Non-Scope
- Protocol semantics or fee rules.
- UI presentation beyond evidence display.

## Evidence Fields (MUST)
The evidence response MUST include these fields and values:
- protocol_anchor
- inputs
- outputs
- receipt_hashes
- state_hash
- replay_ok
- stdout

## Deterministic Export Structure (MUST)
- Export MUST include all required evidence fields exactly as produced.
- Export MUST include the raw stdout text from the run.
- Export MUST be deterministic and stable across machines for the same inputs.

## Deterministic ZIP Rules (MUST)
- File order MUST be lexicographic.
- ZIP timestamps MUST be fixed to a constant.
- File contents MUST contain no timestamps or environment metadata.
- Newlines MUST be LF only.

## Evidence Truth Layer (MUST)
- UI MUST display evidence fields verbatim and unmodified.
- UI MUST NOT compute or override any evidence fields.

## Change Control
This contract is normative for Week 05 and later. Changes require a version bump and explicit migration evidence.
