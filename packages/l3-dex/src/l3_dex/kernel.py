from __future__ import annotations

from .actions import AddLiquidity, CreatePool, RemoveLiquidity, Swap
from .errors import ValidationError
from .invariants import check_invariants
from .state import DexState, PoolState


def _find_pool(state: DexState, pool_id: str) -> PoolState | None:
    for pool in state.pools:
        if pool.pool_id == pool_id:
            return pool
    return None


def _replace_pool(state: DexState, updated: PoolState) -> DexState:
    pools = tuple(pool for pool in state.pools if pool.pool_id != updated.pool_id)
    return DexState(pools=pools + (updated,))


def apply_action(state: DexState, action) -> DexState:
    if isinstance(action, CreatePool):
        if _find_pool(state, action.pool_id) is not None:
            raise ValidationError("pool exists")
        new_pool = PoolState(
            pool_id=action.pool_id,
            asset_a=action.asset_a,
            asset_b=action.asset_b,
            reserve_a=0,
            reserve_b=0,
            total_lp=0,
        )
        new_state = DexState(pools=state.pools + (new_pool,))
        check_invariants(new_state)
        return new_state

    if isinstance(action, AddLiquidity):
        if action.amount_a <= 0 or action.amount_b <= 0:
            raise ValidationError("amounts must be positive")
        pool = _find_pool(state, action.pool_id)
        if pool is None:
            raise ValidationError("pool missing")
        new_pool = PoolState(
            pool_id=pool.pool_id,
            asset_a=pool.asset_a,
            asset_b=pool.asset_b,
            reserve_a=pool.reserve_a + action.amount_a,
            reserve_b=pool.reserve_b + action.amount_b,
            total_lp=pool.total_lp + action.amount_a + action.amount_b,
        )
        new_state = _replace_pool(state, new_pool)
        check_invariants(new_state)
        return new_state

    if isinstance(action, RemoveLiquidity):
        raise ValidationError("remove not available in v0 skeleton")

    if isinstance(action, Swap):
        raise ValidationError("swap not available in v0 skeleton")

    raise ValidationError("unknown action")
