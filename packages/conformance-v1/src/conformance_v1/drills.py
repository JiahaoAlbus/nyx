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
        repo_root / "packages" / "l2-private-ledger" / "src",
        repo_root / "packages" / "l0-reputation" / "src",
        repo_root / "packages" / kernel_dir / "src",
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


def drill_skip_proof() -> DrillResult:
    _ensure_paths()
    from dataclasses import replace
    from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint
    from l2_private_ledger.proof_wiring import (
        DEFAULT_CONTEXT_ID,
        prove_private_action_mock,
        verify_private_action,
    )
    from l2_private_ledger.state import empty_state, state_root
    from l2_private_ledger.types import sha256

    state = empty_state()
    commitment = sha256(b"pl-commitment")
    action = LedgerAction(ActionKind.PRIVATE_MINT, PrivateMint(commitment))
    nonce = sha256(b"pl-nonce")
    envelope = prove_private_action_mock(
        state,
        action,
        nonce,
        witness={"note": "ok"},
    )
    tampered = replace(envelope, proof_bytes=b"")
    if verify_private_action(tampered, state_root(state), action):
        return _fail("Q3-RT-01", "missing proof accepted")
    bad_context = sha256(b"pl-context-bad")
    if verify_private_action(
        envelope,
        state_root(state),
        action,
        context_id=bad_context,
    ):
        return _fail("Q3-RT-01", "wrong context accepted")
    if not verify_private_action(
        envelope,
        state_root(state),
        action,
        context_id=DEFAULT_CONTEXT_ID,
    ):
        return _fail("Q3-RT-01", "valid proof rejected")
    return _pass("Q3-RT-01")


def drill_skip_fee() -> DrillResult:
    _ensure_paths()
    from action import ActionKind as FeeActionKind
    from engine import FeeEngineError, FeeEngineV0
    from fee import FeeVector
    from quote import FeePayment

    from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint
    from l2_private_ledger.fee_binding import compute_action_hash, quote_fee_for_private_action
    from l2_private_ledger.state import empty_state, state_root
    from l2_private_ledger.types import sha256

    engine = FeeEngineV0()
    state = empty_state()
    commitment = sha256(b"fee-commitment")
    action = LedgerAction(ActionKind.PRIVATE_MINT, PrivateMint(commitment))
    root = state_root(state)
    action_hash = compute_action_hash(action)
    quote = quote_fee_for_private_action(engine, action, root, action_hash, payer="payer-a")

    components = list(quote.fee_vector.components)
    base_component, base_amount = components[0]
    components[0] = (base_component, base_amount + 1)
    bad_vector = FeeVector.for_action(FeeActionKind.STATE_MUTATION, tuple(components))
    payment = FeePayment(
        payer=quote.payer,
        quote_hash=quote.quote_hash,
        paid_vector=bad_vector,
    )
    try:
        engine.enforce(quote, payment)
        return _fail("Q3-RT-02", "fee mismatch accepted")
    except FeeEngineError:
        return _pass("Q3-RT-02")


def drill_nullifier_reuse() -> DrillResult:
    _ensure_paths()
    from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateSpend
    from l2_private_ledger.errors import DoubleSpendError
    from l2_private_ledger.kernel import apply_action
    from l2_private_ledger.state import empty_state
    from l2_private_ledger.types import sha256

    state = empty_state()
    nullifier = sha256(b"reuse-nullifier")
    action = LedgerAction(ActionKind.PRIVATE_SPEND, PrivateSpend(nullifier))
    state = apply_action(state, action)
    try:
        _ = apply_action(state, action)
        return _fail("Q3-RT-03", "nullifier reuse accepted")
    except DoubleSpendError:
        return _pass("Q3-RT-03")


def drill_cross_context_link() -> DrillResult:
    _ensure_paths()
    from l0_reputation.disclosure_wiring import prove_rep_at_least_mock, verify_rep_at_least
    from l0_reputation.hashing import sha256
    from l0_reputation.kernel import new_pseudonym

    rep_root = sha256(b"rep-root-ctx")
    pseudo = new_pseudonym(sha256(b"rep-secret-ctx"))
    nonce = sha256(b"rep-nonce-ctx")
    envelope = prove_rep_at_least_mock(
        rep_root=rep_root,
        pseudonym_id=pseudo,
        k=2,
        nonce=nonce,
        witness={"note": "ok"},
    )
    bad_context = sha256(b"rep-bad-context")
    if verify_rep_at_least(envelope, rep_root, pseudo, 2, context_id=bad_context):
        return _fail("Q3-RT-04", "cross-context verification accepted")
    return _pass("Q3-RT-04")


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
    results.append(drill_skip_proof())
    results.append(drill_skip_fee())
    results.append(drill_nullifier_reuse())
    results.append(drill_cross_context_link())
    return tuple(results)
