from __future__ import annotations

import hashlib
from typing import Iterable

from l3_router.actions import RouteSwap, RouterAction, RouterActionKind
from l3_router.errors import ValidationError
from l3_router.state import RouterState, state_hash

try:
    from action import ActionDescriptor, ActionKind as FeeActionKind
    from engine import FeeEngineV0, FeeEngineError
    from fee import FeeVector
    from quote import FeePayment, FeeQuote, FeeReceipt, QuoteError
except Exception as exc:  # pragma: no cover - handled at runtime
    ActionDescriptor = None  # type: ignore
    FeeActionKind = None  # type: ignore
    FeeEngineV0 = object  # type: ignore
    FeeVector = object  # type: ignore
    FeeQuote = object  # type: ignore
    FeeReceipt = object  # type: ignore
    _IMPORT_ERROR = exc

    class FeeEngineError(Exception):
        pass

    class QuoteError(Exception):
        pass


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _framed(parts: Iterable[bytes]) -> bytes:
    out = bytearray()
    for part in parts:
        out.extend(len(part).to_bytes(4, "big"))
        out.extend(part)
    return bytes(out)


def _ensure_bytes32(value: bytes, name: str) -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise ValidationError(f"{name} must be bytes")
    data = bytes(value)
    if len(data) != 32:
        raise ValidationError(f"{name} must be 32 bytes")
    return data


def compute_route_hash(route: RouteSwap) -> bytes:
    if not isinstance(route, RouteSwap):
        raise ValidationError("route must be RouteSwap")
    parts: list[bytes] = [b"NYX:ROUTER:ROUTE_HASH:v1"]
    for step in route.steps:
        parts.append(step.pool_id.encode("utf-8"))
        parts.append(step.asset_in.encode("utf-8"))
        parts.append(str(step.amount_in).encode("utf-8"))
        parts.append(str(step.min_out).encode("utf-8"))
    digest = _sha256(_framed(parts))
    return _ensure_bytes32(digest, "route_hash")


def quote_fee_for_route(
    engine: FeeEngineV0,
    state: RouterState,
    action: RouterAction,
    payer: str,
) -> FeeQuote:
    _require_economics()
    if not isinstance(engine, FeeEngineV0):
        raise ValidationError("engine must be FeeEngineV0")
    if not isinstance(state, RouterState):
        raise ValidationError("state must be RouterState")
    if not isinstance(action, RouterAction):
        raise ValidationError("action must be RouterAction")
    if action.kind is not RouterActionKind.ROUTE_SWAP:
        raise ValidationError("action kind unsupported")
    if not isinstance(payer, str) or not payer:
        raise ValidationError("payer must be non-empty string")

    route_hash = compute_route_hash(action.payload)
    state_hash_bytes = _ensure_bytes32(state_hash(state.dex_state), "state_hash")

    descriptor = ActionDescriptor(
        kind=FeeActionKind.STATE_MUTATION,
        module="l3.router",
        action=action.kind.value,
        payload={
            "route_hash": route_hash.hex(),
            "state_hash": state_hash_bytes.hex(),
            "steps": [
                {
                    "pool_id": step.pool_id,
                    "asset_in": step.asset_in,
                    "amount_in": step.amount_in,
                    "min_out": step.min_out,
                }
                for step in action.payload.steps
            ],
            "v": 1,
        },
        metadata=None,
    )
    try:
        return engine.quote(descriptor, payer)
    except (FeeEngineError, QuoteError) as exc:
        raise ValidationError(str(exc)) from exc


def enforce_fee_for_route(
    engine: FeeEngineV0,
    quote: FeeQuote,
    paid_vector: FeeVector,
    payer: str,
) -> FeeReceipt:
    _require_economics()
    if not isinstance(engine, FeeEngineV0):
        raise ValidationError("engine must be FeeEngineV0")
    if not isinstance(quote, FeeQuote):
        raise ValidationError("quote must be FeeQuote")
    if not isinstance(paid_vector, FeeVector):
        raise ValidationError("paid_vector must be FeeVector")
    if not isinstance(payer, str) or not payer:
        raise ValidationError("payer must be non-empty string")

    payment = FeePayment(payer=payer, quote_hash=quote.quote_hash, paid_vector=paid_vector)
    try:
        return engine.enforce(quote, payment)
    except (FeeEngineError, QuoteError) as exc:
        raise ValidationError(str(exc)) from exc


def _require_economics() -> None:
    if ActionDescriptor is None or FeeActionKind is None:
        raise ValidationError("l2-economics unavailable") from _IMPORT_ERROR
