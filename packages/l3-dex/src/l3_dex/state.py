from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .canonical import canonicalize
from .hashing import sha256


@dataclass(frozen=True)
class PoolState:
    pool_id: str
    asset_a: str
    asset_b: str
    reserve_a: int
    reserve_b: int
    total_lp: int


@dataclass(frozen=True)
class DexState:
    pools: Tuple[PoolState, ...]


def _pool_to_dict(pool: PoolState) -> dict[str, object]:
    return {
        "pool_id": pool.pool_id,
        "asset_a": pool.asset_a,
        "asset_b": pool.asset_b,
        "reserve_a": pool.reserve_a,
        "reserve_b": pool.reserve_b,
        "total_lp": pool.total_lp,
    }


def state_hash(state: DexState) -> bytes:
    pools = sorted(state.pools, key=lambda item: item.pool_id)
    payload = {
        "pools": [_pool_to_dict(pool) for pool in pools],
        "v": 1,
    }
    return sha256(canonicalize(payload))
MAX_AMOUNT = 10**12
MAX_RESERVE = 10**12
MAX_LP = 10**12
