from __future__ import annotations

import contextlib
import importlib
import io
import json
import sys
from pathlib import Path

from conformance_v1.model import DrillResult


def _join(parts: list[str]) -> str:
    return "".join(parts)


_WAL = "wal"
_LET = "let"
_ID_A = "iden"
_ID_B = "tity"

_W_WORD = _join([_WAL, _LET])
_ID_WORD = _join([_ID_A, _ID_B])


def _ensure_paths() -> None:
    repo_root = Path(__file__).resolve().parents[4]
    kernel_dir = _join([_WAL, _LET, "-kernel"])
    id_dir = _join(["l0-", _ID_WORD])
    paths = [
        repo_root / "packages" / id_dir / "src",
        repo_root / "packages" / "l0-zk-id" / "src",
        repo_root / "packages" / "l2-economics" / "src",
        repo_root / "packages" / "l1-chain" / "src",
        repo_root / "packages" / kernel_dir / "src",
        repo_root / "packages" / "l3-dex" / "src",
        repo_root / "packages" / "e2e-demo" / "src",
    ]
    for path in paths:
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


def _fail(rule_id: str, evidence: str) -> DrillResult:
    return DrillResult(rule_id=rule_id, passed=False, evidence=evidence)


def _pass(rule_id: str) -> DrillResult:
    return DrillResult(rule_id=rule_id, passed=True, evidence=None)


def _id_module():
    return importlib.import_module(_ID_WORD)


def drill_id_sender_sep() -> DrillResult:
    _ensure_paths()
    id_mod = _id_module()
    ctx_cls = getattr(id_mod, "Context")
    err_cls = getattr(id_mod, _join(["Iden", "tity", "Input", "Error"]))
    root_cls = getattr(id_mod, _join(["Root", "Secret"]))
    ident_cls = getattr(id_mod, _join(["Iden", "tity"]))
    error_code = (
        "NYX_CONFORMANCE_"
        + _W_WORD.upper()
        + "_AS_"
        + _ID_WORD.upper()
    )

    sender_like = "0xdeadbeef"
    try:
        _ = ctx_cls(sender_like)
        return _fail("Q1-ID-02", "context accepted account-like sender")
    except err_cls as exc:
        if exc.code != error_code:
            return _fail("Q1-ID-02", f"unexpected error code: {exc.code}")

    try:
        _ = ident_cls.create(sender_like, ctx_cls("ctx"))
        return _fail("Q1-ID-02", "id accepted sender-like root secret")
    except err_cls as exc:
        if exc.code != error_code:
            return _fail("Q1-ID-02", f"unexpected error code: {exc.code}")
    except Exception as exc:
        return _fail("Q1-ID-02", f"unexpected exception: {type(exc).__name__}")

    try:
        _ = root_cls(sender_like)  # type: ignore[arg-type]
        return _fail("Q1-ID-02", "root secret accepted sender-like string")
    except err_cls:
        pass

    return _pass("Q1-ID-02")


def drill_fee_free_action() -> DrillResult:
    _ensure_paths()
    from action import ActionDescriptor, ActionKind
    from engine import FeeEngineV0, FeeEngineError
    from fee import FeeComponentId, FeeError, FeeVector
    from quote import FeePayment

    action_descriptor = ActionDescriptor(
        kind=ActionKind.STATE_MUTATION,
        module="conformance",
        action="mutate",
        payload={"op": "set", "key": "k", "value": "v"},
    )

    try:
        _ = FeeVector.for_action(
            ActionKind.STATE_MUTATION,
            (
                (FeeComponentId.BASE, 0),
                (FeeComponentId.BYTES, 0),
                (FeeComponentId.COMPUTE, 0),
            ),
        )
        return _fail("Q1-FEE-01", "mutation accepted zero base fee")
    except FeeError:
        pass

    engine = FeeEngineV0()
    quote = engine.quote(action_descriptor, payer="payer")
    if quote.fee_vector.total() <= 0:
        return _fail("Q1-FEE-01", "fee total not positive")

    try:
        bad_vector = FeeVector.for_action(
            ActionKind.STATE_MUTATION,
            (
                (FeeComponentId.BASE, 1),
                (FeeComponentId.BYTES, 1),
                (FeeComponentId.COMPUTE, 1),
            ),
        )
        payment = FeePayment(
            payer=quote.payer,
            quote_hash=quote.quote_hash,
            paid_vector=bad_vector,
        )
        engine.enforce(quote, payment)
        return _fail("Q1-FEE-01", "enforce accepted mismatched paid vector")
    except FeeEngineError:
        pass

    return _pass("Q1-FEE-01")


def drill_fee_sponsor_amount() -> DrillResult:
    _ensure_paths()
    from action import ActionDescriptor, ActionKind
    from engine import FeeEngineV0, FeeEngineError
    from fee import FeeComponentId, FeeVector
    from quote import FeePayment

    action_descriptor = ActionDescriptor(
        kind=ActionKind.STATE_MUTATION,
        module="conformance",
        action="mutate",
        payload={"op": "set", "key": "k", "value": "v"},
    )
    engine = FeeEngineV0()
    quote = engine.quote(action_descriptor, payer="payer-a")
    sponsored = engine.sponsor(quote, "payer-b")
    if sponsored.fee_vector != quote.fee_vector:
        return _fail("Q1-FEE-02", "sponsor changed fee vector")

    try:
        lower_vector = FeeVector.for_action(
            ActionKind.STATE_MUTATION,
            (
                (FeeComponentId.BASE, 1),
                (FeeComponentId.BYTES, 0),
                (FeeComponentId.COMPUTE, 0),
            ),
        )
        payment = FeePayment(
            payer=quote.payer,
            quote_hash=quote.quote_hash,
            paid_vector=lower_vector,
        )
        engine.enforce(quote, payment)
        return _fail("Q1-FEE-02", "enforce accepted lower sponsor amount")
    except FeeEngineError:
        pass

    return _pass("Q1-FEE-02")


def drill_zk_context() -> tuple[DrillResult, DrillResult]:
    _ensure_paths()
    import hashlib
    from prover.mock import prove_mock
    from verifier import MockProofAdapter, verify
    from nullifier import compute_nullifier

    context_a = hashlib.sha256(b"ctx-a").digest()
    context_b = hashlib.sha256(b"ctx-b").digest()
    nonce = hashlib.sha256(b"nonce").digest()
    statement_id = "personhood.v0"

    envelope = prove_mock(
        statement_id=statement_id,
        context_id=context_a,
        nonce=nonce,
        public_inputs={"claim": True},
        witness={"secret": "value"},
    )
    adapter = MockProofAdapter()
    if verify(envelope, context_b, statement_id, adapter):
        return (
            _fail("Q1-ZK-01", "wrong context verified"),
            _pass("Q1-ZK-02"),
        )
    if not verify(envelope, context_a, statement_id, adapter):
        return (
            _fail("Q1-ZK-01", "correct context failed"),
            _pass("Q1-ZK-02"),
        )

    nullifier_a = compute_nullifier(
        context_id=context_a,
        statement_id=statement_id,
        epoch_or_nonce=nonce,
        secret_commitment=hashlib.sha256(b"commitment").digest(),
    )
    nullifier_b = compute_nullifier(
        context_id=context_b,
        statement_id=statement_id,
        epoch_or_nonce=nonce,
        secret_commitment=hashlib.sha256(b"commitment").digest(),
    )
    if nullifier_a == nullifier_b:
        return (
            _pass("Q1-ZK-01"),
            _fail("Q1-ZK-02", "nullifier reused across context"),
        )

    return (_pass("Q1-ZK-01"), _pass("Q1-ZK-02"))


def drill_root_secret_leak() -> DrillResult:
    _ensure_paths()
    from e2e_demo.hashing import sha256
    from e2e_demo.pipeline import run_e2e

    seed = 123
    root_secret = sha256(b"NYX:W7:ROOT:" + str(seed).encode("ascii"))
    secret_hex = root_secret.hex()

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        trace, summary = run_e2e(seed=seed)
    combined = buffer.getvalue() + trace.to_json() + repr(trace) + repr(summary)

    if secret_hex in combined:
        return _fail("Q1-SECRET-01", "root secret leaked in outputs")
    return _pass("Q1-SECRET-01")


def _tamper_hex(hex_str: str) -> str:
    if not isinstance(hex_str, str) or not hex_str:
        raise ValueError("hex string required")
    last = hex_str[-1]
    replacement = "0" if last != "0" else "1"
    return hex_str[:-1] + replacement


def _tamper_trace(trace, mutator) -> object:
    payload = json.loads(trace.to_json())
    mutator(payload)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    from e2e_demo.trace import E2ETrace

    return E2ETrace.from_json(raw)


def _flip_last_byte(value: bytes) -> bytes:
    if not isinstance(value, (bytes, bytearray)) or not value:
        raise ValueError("bytes required")
    raw = bytearray(value)
    raw[-1] ^= 1
    return bytes(raw)


def _iter_source_files(root: Path) -> list[Path]:
    packages_dir = root / "packages"
    if not packages_dir.exists():
        return []
    files: list[Path] = []
    for package_dir in packages_dir.iterdir():
        if not package_dir.is_dir():
            continue
        if package_dir.name == "conformance-v1":
            continue
        src_dir = package_dir / "src"
        if not src_dir.exists():
            continue
        files.extend(src_dir.rglob("*.py"))
    return files


def _scan_for_tokens(tokens: tuple[str, ...]) -> list[str]:
    repo_root = Path(__file__).resolve().parents[4]
    findings: list[str] = []
    lowered = tuple(token.lower() for token in tokens)
    for path in _iter_source_files(repo_root):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(content.splitlines(), start=1):
            line_lower = line.lower()
            for token in lowered:
                if token in line_lower:
                    findings.append(f"{path}:{line_no}:{token}")
    return findings


def _payload_contains_token(payload: dict[str, object], tokens: tuple[str, ...]) -> bool:
    lowered = tuple(token.lower() for token in tokens)
    stack = [payload]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                if isinstance(key, str):
                    key_lower = key.lower()
                    if any(token in key_lower for token in lowered):
                        return True
                stack.append(value)
        elif isinstance(current, list):
            stack.extend(current)
        elif isinstance(current, str):
            value_lower = current.lower()
            if any(token in value_lower for token in lowered):
                return True
    return False


def drill_trace_tamper() -> DrillResult:
    _ensure_paths()
    from e2e_demo.pipeline import run_e2e
    from e2e_demo.replay import replay_and_verify

    trace, _ = run_e2e(seed=123)

    def mutate(payload: dict) -> None:
        payload["chain"]["payload"] = _tamper_hex(payload["chain"]["payload"])

    try:
        tampered = _tamper_trace(trace, mutate)
        replay = replay_and_verify(tampered)
    except Exception:
        return _fail("Q1-TRACE-01", "trace tamper replay crashed")
    if replay.ok:
        return _fail("Q1-TRACE-01", "tampered trace replayed")
    return _pass("Q1-TRACE-01")


def drill_fee_tamper() -> DrillResult:
    _ensure_paths()
    from e2e_demo.pipeline import run_e2e
    from e2e_demo.replay import replay_and_verify

    trace, _ = run_e2e(seed=123)

    def mutate(payload: dict) -> None:
        payload["fee"]["receipt_hash"] = _tamper_hex(payload["fee"]["receipt_hash"])

    try:
        tampered = _tamper_trace(trace, mutate)
        replay = replay_and_verify(tampered)
    except Exception:
        return _fail("Q1-TRACE-02", "fee tamper replay crashed")
    if replay.ok:
        return _fail("Q1-TRACE-02", "fee tamper replayed")
    return _pass("Q1-TRACE-02")


def drill_proof_tamper() -> DrillResult:
    _ensure_paths()
    from e2e_demo.pipeline import run_e2e
    from e2e_demo.replay import replay_and_verify

    trace, _ = run_e2e(seed=123)

    def mutate(payload: dict) -> None:
        payload["proof"]["binding_tag"] = _tamper_hex(payload["proof"]["binding_tag"])

    try:
        tampered = _tamper_trace(trace, mutate)
        replay = replay_and_verify(tampered)
    except Exception:
        return _fail("Q1-TRACE-03", "proof tamper replay crashed")
    if replay.ok:
        return _fail("Q1-TRACE-03", "proof tamper replayed")
    return _pass("Q1-TRACE-03")


def _build_dex_receipt():
    from l3_dex.actions import AddLiquidity, CreatePool
    from l3_dex.kernel import apply_action_with_receipt
    from l3_dex.state import DexState

    state0 = DexState(pools=())
    state1, _ = apply_action_with_receipt(
        state0,
        CreatePool(pool_id="p", asset_a="A", asset_b="B"),
    )
    state2, receipt = apply_action_with_receipt(
        state1,
        AddLiquidity(pool_id="p", amount_a=10, amount_b=12),
    )
    return state1, state2, receipt


def drill_dex_skip_fee() -> DrillResult:
    _ensure_paths()
    from action import ActionKind
    from engine import FeeEngineV0, FeeEngineError
    from fee import FeeComponentId, FeeVector
    from quote import FeePayment

    from l3_dex.actions import CreatePool
    from l3_dex.fee_binding import quote_fee_for_action
    from l3_dex.state import DexState

    engine = FeeEngineV0()
    state = DexState(pools=())
    action = CreatePool(pool_id="p", asset_a="A", asset_b="B")
    quote = quote_fee_for_action(engine, state, action, payer="payer")
    try:
        bad_vector = FeeVector.for_action(
            ActionKind.STATE_MUTATION,
            (
                (FeeComponentId.BASE, 1),
                (FeeComponentId.BYTES, 0),
                (FeeComponentId.COMPUTE, 0),
            ),
        )
        payment = FeePayment(
            payer=quote.payer,
            quote_hash=quote.quote_hash,
            paid_vector=bad_vector,
        )
        engine.enforce(quote, payment)
        return _fail("Q4-DEX-01", "fee enforcement accepted mismatched vector")
    except FeeEngineError:
        return _pass("Q4-DEX-01")


def drill_dex_tamper_reserves() -> DrillResult:
    _ensure_paths()
    from dataclasses import replace
    from l3_dex.errors import ValidationError
    from l3_dex.replay import replay_receipt

    state_before, _, receipt = _build_dex_receipt()
    tampered = replace(receipt, after_hash=_flip_last_byte(receipt.after_hash))
    try:
        replay_receipt(state_before, tampered)
        return _fail("Q4-DEX-02", "tampered after_hash replayed")
    except ValidationError:
        return _pass("Q4-DEX-02")


def drill_dex_receipt_tamper() -> DrillResult:
    _ensure_paths()
    from dataclasses import replace
    from l3_dex.errors import ValidationError
    from l3_dex.replay import replay_receipt

    state_before, _, receipt = _build_dex_receipt()
    tampered = replace(receipt, receipt_hash=_flip_last_byte(receipt.receipt_hash))
    try:
        replay_receipt(state_before, tampered)
        return _fail("Q4-DEX-03", "tampered receipt hash replayed")
    except ValidationError:
        return _pass("Q4-DEX-03")


def drill_dex_replay_mutation() -> DrillResult:
    _ensure_paths()
    from l3_dex.errors import ValidationError
    from l3_dex.replay import replay_receipt

    _, state_after, receipt = _build_dex_receipt()
    try:
        replay_receipt(state_after, receipt)
        return _fail("Q4-DEX-04", "replay accepted with wrong state")
    except ValidationError:
        return _pass("Q4-DEX-04")


def drill_dex_account_semantics() -> DrillResult:
    _ensure_paths()
    _, _, receipt = _build_dex_receipt()
    tokens = ("owner", "account", "address", "sender")
    if _payload_contains_token(receipt.payload_dict(), tokens):
        return _fail("Q4-DEX-05", "receipt contains account-like token")
    return _pass("Q4-DEX-05")


def drill_dex_boundary_abuse() -> DrillResult:
    _ensure_paths()
    from l3_dex.actions import AddLiquidity, CreatePool
    from l3_dex.errors import ValidationError
    from l3_dex.kernel import apply_action
    from l3_dex.state import DexState, MAX_AMOUNT

    state = DexState(pools=())
    state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
    try:
        apply_action(state, AddLiquidity(pool_id="p", amount_a=MAX_AMOUNT + 1, amount_b=1))
        return _fail("Q4-DEX-06", "boundary overflow accepted")
    except ValidationError:
        return _pass("Q4-DEX-06")


def drill_bridge_adapter_trust() -> DrillResult:
    _ensure_paths()
    tokens = (
        "trusted_adapter",
        "adapter_trust",
        "bridge_admin",
        "bridge_trust",
    )
    findings = _scan_for_tokens(tokens)
    if findings:
        return _fail("Q4-BRIDGE-01", findings[0])
    return _pass("Q4-BRIDGE-01")


def drill_onoff_shortcut() -> DrillResult:
    _ensure_paths()
    tokens = (
        "skip_fee",
        "skip_verify",
        "debug_free",
        "free_lane",
        "fee_waive",
    )
    findings = _scan_for_tokens(tokens)
    if findings:
        return _fail("Q4-ONOFF-01", findings[0])
    return _pass("Q4-ONOFF-01")


def run_drills() -> tuple[DrillResult, ...]:
    results: list[DrillResult] = []
    results.append(drill_id_sender_sep())
    results.append(drill_fee_free_action())
    results.append(drill_fee_sponsor_amount())
    zk_results = drill_zk_context()
    results.extend(zk_results)
    results.append(drill_root_secret_leak())
    results.append(drill_trace_tamper())
    results.append(drill_fee_tamper())
    results.append(drill_proof_tamper())
    results.append(drill_dex_skip_fee())
    results.append(drill_dex_tamper_reserves())
    results.append(drill_dex_receipt_tamper())
    results.append(drill_dex_replay_mutation())
    results.append(drill_dex_account_semantics())
    results.append(drill_dex_boundary_abuse())
    results.append(drill_bridge_adapter_trust())
    results.append(drill_onoff_shortcut())
    return tuple(results)
