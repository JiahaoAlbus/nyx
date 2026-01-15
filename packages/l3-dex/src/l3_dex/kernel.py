from __future__ import annotations

from .actions import ActionKind, AddLiquidity, CreatePool, RemoveLiquidity, Swap
from .errors import ValidationError
from .invariants import check_invariants
from .receipts import DexReceipt, receipt_hash_for_payload
from .state import DexState, PoolState, MAX_AMOUNT, MAX_LP, MAX_RESERVE, state_hash


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
        _require_amount(action.amount_a, "amount_a")
        _require_amount(action.amount_b, "amount_b")
        pool = _find_pool(state, action.pool_id)
        if pool is None:
            raise ValidationError("pool missing")
        if pool.reserve_a + action.amount_a > MAX_RESERVE:
            raise ValidationError("reserve_a exceeds max")
        if pool.reserve_b + action.amount_b > MAX_RESERVE:
            raise ValidationError("reserve_b exceeds max")
        minted_lp = action.amount_a + action.amount_b
        if pool.total_lp > 0:
            minted_lp = min(
                action.amount_a * pool.total_lp // pool.reserve_a,
                action.amount_b * pool.total_lp // pool.reserve_b,
            )
        if minted_lp <= 0:
            raise ValidationError("minted lp must be positive")
        if pool.total_lp + minted_lp > MAX_LP:
            raise ValidationError("total_lp exceeds max")
        new_pool = PoolState(
            pool_id=pool.pool_id,
            asset_a=pool.asset_a,
            asset_b=pool.asset_b,
            reserve_a=pool.reserve_a + action.amount_a,
            reserve_b=pool.reserve_b + action.amount_b,
            total_lp=pool.total_lp + minted_lp,
        )
        new_state = _replace_pool(state, new_pool)
        check_invariants(new_state)
        return new_state

    if isinstance(action, RemoveLiquidity):
        _require_amount(action.lp_amount, "lp_amount")
        pool = _find_pool(state, action.pool_id)
        if pool is None:
            raise ValidationError("pool missing")
        if action.lp_amount > pool.total_lp:
            raise ValidationError("lp_amount exceeds total_lp")
        if pool.total_lp == 0:
            raise ValidationError("total_lp is zero")
        amount_a = pool.reserve_a * action.lp_amount // pool.total_lp
        amount_b = pool.reserve_b * action.lp_amount // pool.total_lp
        new_pool = PoolState(
            pool_id=pool.pool_id,
            asset_a=pool.asset_a,
            asset_b=pool.asset_b,
            reserve_a=pool.reserve_a - amount_a,
            reserve_b=pool.reserve_b - amount_b,
            total_lp=pool.total_lp - action.lp_amount,
        )
        new_state = _replace_pool(state, new_pool)
        check_invariants(new_state)
        return new_state

    if isinstance(action, Swap):
        _require_amount(action.amount_in, "amount_in")
        _require_nonneg(action.min_out, "min_out")
        pool = _find_pool(state, action.pool_id)
        if pool is None:
            raise ValidationError("pool missing")
        if action.asset_in not in (pool.asset_a, pool.asset_b):
            raise ValidationError("asset_in invalid")
        reserve_in, reserve_out = (
            (pool.reserve_a, pool.reserve_b)
            if action.asset_in == pool.asset_a
            else (pool.reserve_b, pool.reserve_a)
        )
        if reserve_in <= 0 or reserve_out <= 0:
            raise ValidationError("reserves must be positive for swap")
        amount_in_after_fee = _apply_fee(action.amount_in)
        if amount_in_after_fee <= 0:
            raise ValidationError("amount_in too small after fee")
        new_reserve_in = reserve_in + amount_in_after_fee
        if new_reserve_in > MAX_RESERVE:
            raise ValidationError("reserve_in exceeds max")
        k = reserve_in * reserve_out
        new_reserve_out = k // new_reserve_in
        amount_out = reserve_out - new_reserve_out
        if amount_out <= 0:
            raise ValidationError("amount_out must be positive")
        if amount_out < action.min_out:
            raise ValidationError("amount_out below min_out")
        if action.asset_in == pool.asset_a:
            new_pool = PoolState(
                pool_id=pool.pool_id,
                asset_a=pool.asset_a,
                asset_b=pool.asset_b,
                reserve_a=new_reserve_in,
                reserve_b=reserve_out - amount_out,
                total_lp=pool.total_lp,
            )
        else:
            new_pool = PoolState(
                pool_id=pool.pool_id,
                asset_a=pool.asset_a,
                asset_b=pool.asset_b,
                reserve_a=reserve_out - amount_out,
                reserve_b=new_reserve_in,
                total_lp=pool.total_lp,
            )
        new_state = _replace_pool(state, new_pool)
        check_invariants(new_state)
        return new_state

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


def _require_amount(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"{name} must be int")
    if value <= 0:
        raise ValidationError(f"{name} must be positive")
    if value > MAX_AMOUNT:
        raise ValidationError(f"{name} exceeds max")


def _apply_fee(amount_in: int) -> int:
    fee_bps = 30
    return amount_in * (10_000 - fee_bps) // 10_000


def _require_nonneg(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"{name} must be int")
    if value < 0:
        raise ValidationError(f"{name} must be non-negative")


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
