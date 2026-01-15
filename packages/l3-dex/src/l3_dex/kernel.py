from __future__ import annotations

from .actions import ActionKind, AddLiquidity, CreatePool, RemoveLiquidity, Swap
from .errors import ValidationError
from .invariants import check_invariants
from .receipts import DexReceipt, receipt_hash_for_payload
from .state import DexState, PoolState, state_hash


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


def _receipt_inputs(action) -> dict[str, object]:
    if isinstance(action, CreatePool):
        return {"asset_a": action.asset_a, "asset_b": action.asset_b}
    if isinstance(action, AddLiquidity):
        return {"amount_a": action.amount_a, "amount_b": action.amount_b}
    if isinstance(action, RemoveLiquidity):
        return {"lp_amount": action.lp_amount}
    if isinstance(action, Swap):
        return {
            "amount_in": action.amount_in,
            "min_out": action.min_out,
            "asset_in": action.asset_in,
        }
    raise ValidationError("unknown action")


_ACTION_KIND_MAP = {
    CreatePool: ActionKind.CREATE_POOL,
    AddLiquidity: ActionKind.ADD_LIQUIDITY,
    RemoveLiquidity: ActionKind.REMOVE_LIQUIDITY,
    Swap: ActionKind.SWAP,
}


def apply_action_with_receipt(state: DexState, action) -> tuple[DexState, DexReceipt]:
    before_hash = state_hash(state)
    new_state = apply_action(state, action)
    after_hash = state_hash(new_state)
    kind = _ACTION_KIND_MAP.get(type(action))
    if kind is None:
        raise ValidationError("unknown action")
    payload = {
        "action": kind.value,
        "pool_id": action.pool_id,
        "inputs": _receipt_inputs(action),
        "before_hash": before_hash.hex(),
        "after_hash": after_hash.hex(),
        "v": 1,
    }
    receipt = DexReceipt(
        action=kind,
        pool_id=action.pool_id,
        inputs=_receipt_inputs(action),
        before_hash=before_hash,
        after_hash=after_hash,
        receipt_hash=receipt_hash_for_payload(payload),
    )
    return new_state, receipt
