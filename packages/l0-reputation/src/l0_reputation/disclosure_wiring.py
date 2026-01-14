from __future__ import annotations

from l0_reputation.errors import ValidationError
from l0_reputation.hashing import compare_digest, ensure_bytes32, hex_to_bytes32, sha256

try:
    from canonical import CanonicalizationError, canonicalize
    from envelope import ProofEnvelope
    from prover.mock import prove_mock
    from verifier import MockProofAdapter, verify as verify_envelope
except Exception as exc:  # pragma: no cover - handled at runtime
    ProofEnvelope = None  # type: ignore
    MockProofAdapter = object  # type: ignore
    _IMPORT_ERROR = exc

    def _missing(*_args, **_kwargs):
        raise ValidationError("l0-zk-id unavailable") from _IMPORT_ERROR

    canonicalize = _missing  # type: ignore
    prove_mock = _missing  # type: ignore
    verify_envelope = _missing  # type: ignore
    CanonicalizationError = ValidationError  # type: ignore

DEFAULT_DISCLOSE_CONTEXT_ID = sha256(b"NYX:CTX:Q3:REP_DISCLOSE:v1")
STATEMENT_ID_AT_LEAST = "NYX:STATEMENT:REP_AT_LEAST:v1"
STATEMENT_ID_TIER = "NYX:STATEMENT:REP_TIER:v1"
MAX_PUBLIC_INPUT_DEPTH = 20
MAX_PUBLIC_INPUT_BYTES = 65_536


def build_public_inputs_at_least(rep_root: bytes, pseudonym_id: bytes, k: int) -> dict[str, object]:
    rep_root_bytes = ensure_bytes32(rep_root, "rep_root")
    pseudonym_bytes = ensure_bytes32(pseudonym_id, "pseudonym_id")
    if not isinstance(k, int) or isinstance(k, bool):
        raise ValidationError("k must be int")
    if k < 0:
        raise ValidationError("k must be >= 0")
    return {
        "rep_root": rep_root_bytes.hex(),
        "pseudonym_id": pseudonym_bytes.hex(),
        "k": k,
        "v": 1,
    }


def build_public_inputs_tier(rep_root: bytes, pseudonym_id: bytes, tier: str) -> dict[str, object]:
    rep_root_bytes = ensure_bytes32(rep_root, "rep_root")
    pseudonym_bytes = ensure_bytes32(pseudonym_id, "pseudonym_id")
    if not isinstance(tier, str) or not tier:
        raise ValidationError("tier must be non-empty string")
    return {
        "rep_root": rep_root_bytes.hex(),
        "pseudonym_id": pseudonym_bytes.hex(),
        "tier": tier,
        "v": 1,
    }


def validate_public_inputs_shape(public_inputs: dict[str, object], statement_id: str) -> None:
    if not isinstance(public_inputs, dict):
        raise ValidationError("public_inputs must be dict")
    try:
        canonicalize(
            public_inputs,
            max_depth=MAX_PUBLIC_INPUT_DEPTH,
            max_bytes=MAX_PUBLIC_INPUT_BYTES,
        )
    except CanonicalizationError as exc:
        raise ValidationError(str(exc)) from exc

    base_required = {"rep_root", "pseudonym_id", "v"}
    if statement_id == STATEMENT_ID_AT_LEAST:
        required = base_required | {"k"}
    elif statement_id == STATEMENT_ID_TIER:
        required = base_required | {"tier"}
    else:
        raise ValidationError("statement_id not supported")

    allowed = set(required)
    allowed.add("_mock_witness_hash")
    if not required.issubset(public_inputs.keys()):
        raise ValidationError("public_inputs must include required fields")
    extra = set(public_inputs.keys()) - allowed
    if extra:
        raise ValidationError("public_inputs has unexpected fields")

    if public_inputs.get("v") != 1:
        raise ValidationError("v must be 1")

    _require_hex_bytes32("rep_root", public_inputs.get("rep_root"))
    _require_hex_bytes32("pseudonym_id", public_inputs.get("pseudonym_id"))

    if statement_id == STATEMENT_ID_AT_LEAST:
        k = public_inputs.get("k")
        if not isinstance(k, int) or isinstance(k, bool):
            raise ValidationError("k must be int")
        if k < 0:
            raise ValidationError("k must be >= 0")
    else:
        tier = public_inputs.get("tier")
        if not isinstance(tier, str) or not tier:
            raise ValidationError("tier must be non-empty string")


def prove_rep_at_least_mock(
    *,
    rep_root: bytes,
    pseudonym_id: bytes,
    k: int,
    nonce: bytes,
    witness: object,
    context_id: bytes = DEFAULT_DISCLOSE_CONTEXT_ID,
    statement_id: str = STATEMENT_ID_AT_LEAST,
) -> ProofEnvelope:
    if ProofEnvelope is None:
        raise ValidationError("l0-zk-id unavailable")
    if statement_id != STATEMENT_ID_AT_LEAST:
        raise ValidationError("statement_id mismatch")
    ensure_bytes32(context_id, "context_id")
    ensure_bytes32(nonce, "nonce")
    public_inputs = build_public_inputs_at_least(rep_root, pseudonym_id, k)
    validate_public_inputs_shape(public_inputs, statement_id)
    return prove_mock(
        statement_id=statement_id,
        context_id=context_id,
        nonce=nonce,
        public_inputs=public_inputs,
        witness=witness,
    )


def prove_rep_tier_mock(
    *,
    rep_root: bytes,
    pseudonym_id: bytes,
    tier: str,
    nonce: bytes,
    witness: object,
    context_id: bytes = DEFAULT_DISCLOSE_CONTEXT_ID,
    statement_id: str = STATEMENT_ID_TIER,
) -> ProofEnvelope:
    if ProofEnvelope is None:
        raise ValidationError("l0-zk-id unavailable")
    if statement_id != STATEMENT_ID_TIER:
        raise ValidationError("statement_id mismatch")
    ensure_bytes32(context_id, "context_id")
    ensure_bytes32(nonce, "nonce")
    public_inputs = build_public_inputs_tier(rep_root, pseudonym_id, tier)
    validate_public_inputs_shape(public_inputs, statement_id)
    return prove_mock(
        statement_id=statement_id,
        context_id=context_id,
        nonce=nonce,
        public_inputs=public_inputs,
        witness=witness,
    )


def verify_rep_at_least(
    envelope: ProofEnvelope,
    expected_rep_root: bytes,
    expected_pseudonym_id: bytes,
    k: int,
    *,
    context_id: bytes = DEFAULT_DISCLOSE_CONTEXT_ID,
    statement_id: str = STATEMENT_ID_AT_LEAST,
    verifier_adapter: object | None = None,
) -> bool:
    if ProofEnvelope is None:
        return False
    if not isinstance(envelope, ProofEnvelope):
        return False
    if statement_id != STATEMENT_ID_AT_LEAST:
        return False
    try:
        expected_root = ensure_bytes32(expected_rep_root, "expected_rep_root")
        expected_pseudo = ensure_bytes32(expected_pseudonym_id, "expected_pseudonym_id")
        ensure_bytes32(context_id, "context_id")
    except ValidationError:
        return False
    try:
        validate_public_inputs_shape(envelope.public_inputs, statement_id)
    except ValidationError:
        return False

    public_inputs = envelope.public_inputs
    try:
        rep_root = _require_hex_bytes32("rep_root", public_inputs.get("rep_root"))
        pseudonym_id = _require_hex_bytes32(
            "pseudonym_id", public_inputs.get("pseudonym_id")
        )
    except ValidationError:
        return False
    if not compare_digest(rep_root, expected_root):
        return False
    if not compare_digest(pseudonym_id, expected_pseudo):
        return False
    if public_inputs.get("k") != k:
        return False

    adapter = verifier_adapter if verifier_adapter is not None else MockProofAdapter()
    try:
        return bool(verify_envelope(envelope, context_id, statement_id, adapter))
    except Exception:
        return False


def verify_rep_tier(
    envelope: ProofEnvelope,
    expected_rep_root: bytes,
    expected_pseudonym_id: bytes,
    tier: str,
    *,
    context_id: bytes = DEFAULT_DISCLOSE_CONTEXT_ID,
    statement_id: str = STATEMENT_ID_TIER,
    verifier_adapter: object | None = None,
) -> bool:
    if ProofEnvelope is None:
        return False
    if not isinstance(envelope, ProofEnvelope):
        return False
    if statement_id != STATEMENT_ID_TIER:
        return False
    try:
        expected_root = ensure_bytes32(expected_rep_root, "expected_rep_root")
        expected_pseudo = ensure_bytes32(expected_pseudonym_id, "expected_pseudonym_id")
        ensure_bytes32(context_id, "context_id")
    except ValidationError:
        return False
    if not isinstance(tier, str) or not tier:
        return False
    try:
        validate_public_inputs_shape(envelope.public_inputs, statement_id)
    except ValidationError:
        return False

    public_inputs = envelope.public_inputs
    try:
        rep_root = _require_hex_bytes32("rep_root", public_inputs.get("rep_root"))
        pseudonym_id = _require_hex_bytes32(
            "pseudonym_id", public_inputs.get("pseudonym_id")
        )
    except ValidationError:
        return False
    if not compare_digest(rep_root, expected_root):
        return False
    if not compare_digest(pseudonym_id, expected_pseudo):
        return False
    if public_inputs.get("tier") != tier:
        return False

    adapter = verifier_adapter if verifier_adapter is not None else MockProofAdapter()
    try:
        return bool(verify_envelope(envelope, context_id, statement_id, adapter))
    except Exception:
        return False


def _require_hex_bytes32(name: str, value: object) -> bytes:
    return hex_to_bytes32(value, name)
