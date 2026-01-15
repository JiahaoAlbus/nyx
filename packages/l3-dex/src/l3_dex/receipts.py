from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .actions import ActionKind
from .canonical import canonicalize
from .errors import ValidationError
from .hashing import sha256
from .types import ensure_bytes32, hex_from_bytes


@dataclass(frozen=True)
class DexReceipt:
    action: ActionKind
    pool_id: str
    inputs: dict[str, Any]
    before_hash: bytes
    after_hash: bytes
    receipt_hash: bytes

    def __post_init__(self) -> None:
        if not isinstance(self.pool_id, str) or not self.pool_id:
            raise ValidationError("pool_id must be non-empty string")
        if not isinstance(self.inputs, dict):
            raise ValidationError("inputs must be dict")
        ensure_bytes32(self.before_hash, "before_hash")
        ensure_bytes32(self.after_hash, "after_hash")
        ensure_bytes32(self.receipt_hash, "receipt_hash")

    def payload_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.value,
            "pool_id": self.pool_id,
            "inputs": self.inputs,
            "before_hash": hex_from_bytes(self.before_hash),
            "after_hash": hex_from_bytes(self.after_hash),
            "v": 1,
        }

    def canonical_bytes(self) -> bytes:
        return canonicalize(self.payload_dict())


def receipt_hash_for_payload(payload: dict[str, Any]) -> bytes:
    return sha256(canonicalize(payload))
