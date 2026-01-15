from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


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
