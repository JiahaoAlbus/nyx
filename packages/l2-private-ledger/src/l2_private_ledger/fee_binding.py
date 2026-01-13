from __future__ import annotations

from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint, PrivateSpend
from l2_private_ledger.errors import ValidationError
from l2_private_ledger.types import ensure_bytes32, framed, sha256

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
    FeePayment = object  # type: ignore
    FeeReceipt = object  # type: ignore
    _IMPORT_ERROR = exc

    class FeeEngineError(Exception):
        pass

    class QuoteError(Exception):
        pass


def compute_action_hash(action: LedgerAction) -> bytes:
    if not isinstance(action, LedgerAction):
        raise ValidationError("action must be LedgerAction")
    if action.kind == ActionKind.PRIVATE_MINT:
        payload = action.payload
        assert isinstance(payload, PrivateMint)
        payload_bytes = ensure_bytes32(payload.commitment, "commitment")
    elif action.kind == ActionKind.PRIVATE_SPEND:
        payload = action.payload
        assert isinstance(payload, PrivateSpend)
        payload_bytes = ensure_bytes32(payload.nullifier, "nullifier")
    else:
        raise ValidationError("unsupported action kind")
    kind_bytes = action.kind.value.encode("utf-8")
    action_hash = sha256(
        framed([b"NYX:PL:ACTION_HASH:v1", kind_bytes, payload_bytes])
    )
    ensure_bytes32(action_hash, "action_hash")
    return action_hash


def quote_fee_for_private_action(
    engine: FeeEngineV0,
    action: LedgerAction,
    ledger_root: bytes,
    action_hash: bytes,
    payer: str,
) -> FeeQuote:
    _require_economics()
    if not isinstance(engine, FeeEngineV0):
        raise ValidationError("engine must be FeeEngineV0")
    if not isinstance(action, LedgerAction):
        raise ValidationError("action must be LedgerAction")
    root_bytes = ensure_bytes32(ledger_root, "ledger_root")
    hash_bytes = ensure_bytes32(action_hash, "action_hash")

    descriptor = ActionDescriptor(
        kind=FeeActionKind.STATE_MUTATION,
        module="l2.private_ledger",
        action=action.kind.value,
        payload={
            "ledger_root": root_bytes.hex(),
            "action_hash": hash_bytes.hex(),
            "action_kind": action.kind.value,
            "payload": _payload_for_action(action),
        },
        metadata=None,
    )
    try:
        return engine.quote(descriptor, payer)
    except (FeeEngineError, QuoteError) as exc:
        raise ValidationError(str(exc)) from exc


def enforce_fee_for_private_action(
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


def _payload_for_action(action: LedgerAction) -> dict[str, str]:
    if action.kind == ActionKind.PRIVATE_MINT:
        payload = action.payload
        assert isinstance(payload, PrivateMint)
        return {"commitment": payload.commitment.hex()}
    payload = action.payload
    assert isinstance(payload, PrivateSpend)
    return {"nullifier": payload.nullifier.hex()}


def _require_economics() -> None:
    if ActionDescriptor is None or FeeActionKind is None:
        raise ValidationError("l2-economics unavailable") from _IMPORT_ERROR
