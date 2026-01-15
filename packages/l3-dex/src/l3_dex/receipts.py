from __future__ import annotations

from dataclasses import dataclass

from .actions import ActionKind


@dataclass(frozen=True)
class DexReceipt:
    action: ActionKind
    pool_id: str
    state_hash: bytes
