from __future__ import annotations

from .errors import ValidationError
from .state import DexState


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
