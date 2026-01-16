from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ClientConfig:
    seed: int
    steps: int
    out_path: str


@dataclass(frozen=True)
class RouteStepView:
    pool_id: str
    asset_in: str
    amount_in: int
    min_out: int

    def to_dict(self) -> dict:
        return {
            "pool_id": self.pool_id,
            "asset_in": self.asset_in,
            "amount_in": self.amount_in,
            "min_out": self.min_out,
        }


@dataclass(frozen=True)
class ClientReport:
    steps: Tuple[RouteStepView, ...]
    state_hash_hex: str
    receipt_chain_hex: str

    def to_dict(self) -> dict:
        return {
            "steps": [step.to_dict() for step in self.steps],
            "state_hash_hex": self.state_hash_hex,
            "receipt_chain_hex": self.receipt_chain_hex,
        }


@dataclass(frozen=True)
class ClientSummary:
    state_hash_hex: str
    receipt_chain_hex: str
    replay_ok: bool
