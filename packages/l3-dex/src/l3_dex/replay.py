from __future__ import annotations

from .actions import ActionKind, AddLiquidity, CreatePool, RemoveLiquidity, Swap
from .errors import ValidationError
from .hashing import compare_digest
from .kernel import apply_action
from .receipts import DexReceipt, receipt_hash_for_payload
from .state import DexState, state_hash


def _action_from_receipt(receipt: DexReceipt):
    inputs = receipt.inputs
    if receipt.action == ActionKind.CREATE_POOL:
        return CreatePool(
            pool_id=receipt.pool_id,
            asset_a=_require_text(inputs.get("asset_a")),
            asset_b=_require_text(inputs.get("asset_b")),
        )
    if receipt.action == ActionKind.ADD_LIQUIDITY:
        return AddLiquidity(
            pool_id=receipt.pool_id,
            amount_a=_require_int(inputs.get("amount_a")),
            amount_b=_require_int(inputs.get("amount_b")),
        )
    if receipt.action == ActionKind.REMOVE_LIQUIDITY:
        return RemoveLiquidity(
            pool_id=receipt.pool_id,
            lp_amount=_require_int(inputs.get("lp_amount")),
        )
    if receipt.action == ActionKind.SWAP:
        return Swap(
            pool_id=receipt.pool_id,
            amount_in=_require_int(inputs.get("amount_in")),
            min_out=_require_int(inputs.get("min_out")),
            asset_in=_require_text(inputs.get("asset_in")),
        )
    raise ValidationError("unknown action kind")


def replay_receipt(state: DexState, receipt: DexReceipt) -> DexState:
    before = state_hash(state)
    if not compare_digest(before, receipt.before_hash):
        raise ValidationError("before_hash mismatch")
    expected_hash = receipt_hash_for_payload(receipt.payload_dict())
    if not compare_digest(expected_hash, receipt.receipt_hash):
        raise ValidationError("receipt_hash mismatch")
    action = _action_from_receipt(receipt)
    new_state = apply_action(state, action)
    after = state_hash(new_state)
    if not compare_digest(after, receipt.after_hash):
        raise ValidationError("after_hash mismatch")
    return new_state


def _require_text(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError("text input required")
    return value


def _require_int(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError("int input required")
    return value
