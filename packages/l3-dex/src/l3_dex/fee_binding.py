from __future__ import annotations

from action import ActionDescriptor, ActionKind
from engine import FeeEngineV0
from quote import FeePayment, FeeQuote, FeeReceipt

from .actions import AddLiquidity, CreatePool, RemoveLiquidity, Swap
from .errors import ValidationError
from .state import DexState, state_hash


def _action_label(action) -> str:
    if isinstance(action, CreatePool):
        return "create_pool"
    if isinstance(action, AddLiquidity):
        return "add_liquidity"
    if isinstance(action, RemoveLiquidity):
        return "remove_liquidity"
    if isinstance(action, Swap):
        return "swap"
    raise ValidationError("unknown action")


def _payload_for_action(action, state: DexState) -> dict[str, object]:
    return {
        "action": _action_label(action),
        "pool_id": action.pool_id,
        "inputs": _inputs_for_action(action),
        "state_hash": state_hash(state).hex(),
        "v": 1,
    }


def _inputs_for_action(action) -> dict[str, object]:
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


def build_action_descriptor(action, state: DexState) -> ActionDescriptor:
    payload = _payload_for_action(action, state)
    return ActionDescriptor(
        kind=ActionKind.STATE_MUTATION,
        module="l3-dex",
        action=_action_label(action),
        payload=payload,
    )


def quote_fee_for_action(
    engine: FeeEngineV0,
    state: DexState,
    action,
    payer: str,
) -> FeeQuote:
    descriptor = build_action_descriptor(action, state)
    return engine.quote(descriptor, payer=payer)


def sponsor_quote(
    engine: FeeEngineV0,
    quote: FeeQuote,
    new_payer: str,
) -> FeeQuote:
    return engine.sponsor(quote, new_payer)


def enforce_fee_for_action(
    engine: FeeEngineV0,
    quote: FeeQuote,
    paid_vector,
    payer: str,
) -> FeeReceipt:
    payment = FeePayment(
        payer=payer,
        quote_hash=quote.quote_hash,
        paid_vector=paid_vector,
    )
    return engine.enforce(quote, payment)
