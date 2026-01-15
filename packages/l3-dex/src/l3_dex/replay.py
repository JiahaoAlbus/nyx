from __future__ import annotations

from .receipts import DexReceipt
from .state import DexState


def replay_receipt(state: DexState, receipt: DexReceipt) -> DexState:
    raise NotImplementedError("DEX replay not implemented in skeleton")
