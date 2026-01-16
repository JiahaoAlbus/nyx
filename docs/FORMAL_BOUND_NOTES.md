# Formal Bound Notes

## Purpose
Record the bounded exploration scope and claims for DEX v0.

## Scope
- Bounded explorer for CreatePool and AddLiquidity actions.

## Non-Scope
- Swap and RemoveLiquidity (covered in later expansions).

## Bounds Searched
- Pools: 1 pool id.
- Assets: 2 symbols ("A", "B").
- Amounts: {1, 2} for reserves.
- Sequence depth: 1 to 4 actions.
- Action set: CreatePool followed by AddLiquidity variants.

## Claims Within Bounds
- Invariants hold for all enumerated sequences.
- No negative reserves or total_lp.
- Pool ids remain unique.

## Evidence / Verification
Command:
- `python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v`

## Freeze / Change Control
- Bounds are recorded and MUST NOT be reduced without justification.
- Any expansion must update this note with new bounds.
