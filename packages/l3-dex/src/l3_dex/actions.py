from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActionKind(str, Enum):
    CREATE_POOL = "CREATE_POOL"
    ADD_LIQUIDITY = "ADD_LIQUIDITY"
    REMOVE_LIQUIDITY = "REMOVE_LIQUIDITY"
    SWAP = "SWAP"


@dataclass(frozen=True)
class CreatePool:
    pool_id: str
    asset_a: str
    asset_b: str


@dataclass(frozen=True)
class AddLiquidity:
    pool_id: str
    amount_a: int
    amount_b: int


@dataclass(frozen=True)
class RemoveLiquidity:
    pool_id: str
    lp_amount: int


@dataclass(frozen=True)
class Swap:
    pool_id: str
    amount_in: int
    min_out: int
    asset_in: str
