from __future__ import annotations

from .errors import ValidationError
from .state import DexState, MAX_LP, MAX_RESERVE


def check_invariants(state: DexState) -> None:
    pool_ids = set()
    for pool in state.pools:
        if not pool.pool_id:
            raise ValidationError("pool_id required")
        if pool.pool_id in pool_ids:
            raise ValidationError("duplicate pool_id")
        pool_ids.add(pool.pool_id)
        if pool.reserve_a < 0 or pool.reserve_b < 0 or pool.total_lp < 0:
            raise ValidationError("negative reserves or lp")
        if pool.reserve_a > MAX_RESERVE or pool.reserve_b > MAX_RESERVE:
            raise ValidationError("reserve exceeds max")
        if pool.total_lp > MAX_LP:
            raise ValidationError("total_lp exceeds max")
