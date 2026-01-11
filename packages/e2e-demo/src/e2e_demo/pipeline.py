from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from action import ActionDescriptor, ActionKind
from engine import FeeEngineV0
from fee import FeeComponentId
from quote import FeePayment
from verifier import MockProofAdapter, verify
from prover.mock import prove_mock

from l1_chain.devnet.adapter import (
    DeterministicInMemoryChainAdapter,
    encode_payload_set,
)
from l1_chain.types import ChainAccount, ChainId

from wallet_kernel.keystore import InMemoryKeyStore
from wallet_kernel.kernel import WalletKernel
from wallet_kernel.secrets import SecretBytes
from wallet_kernel.signing import HMACSigner
from wallet_kernel.tx_plumbing import InMemoryNonceSource

from e2e_demo.hashing import compare_digest, sha256
from e2e_demo.trace import (
    ActionTrace,
    ChainTrace,
    E2ETrace,
    FeeTrace,
    IdentityTrace,
    ProofEnvelopeTrace,
    SanityTrace,
    StateProofTrace,
    TraceMeta,
)


class E2EError(ValueError):
    pass


@dataclass(frozen=True)
class Summary:
    identity_commitment_prefix: str
    fee_total: int
    tx_hash_prefix: str
    block_hash_prefix: str
    state_root_prefix: str
    receipt_hash_prefix: str


class Prover:
    def prove(
        self,
        *,
        statement_id: str,
        context_id: bytes,
        nonce: bytes,
        public_inputs: dict,
        witness: dict,
    ):
        raise NotImplementedError


class Verifier:
    def verify(self, envelope, context_id: bytes, statement_id: str) -> bool:
        raise NotImplementedError


class L0MockProver(Prover):
    def prove(
        self,
        *,
        statement_id: str,
        context_id: bytes,
        nonce: bytes,
        public_inputs: dict,
        witness: dict,
    ):
        return prove_mock(
            statement_id=statement_id,
            context_id=context_id,
            nonce=nonce,
            public_inputs=public_inputs,
            witness=witness,
        )


class L0MockVerifier(Verifier):
    def __init__(self, adapter: MockProofAdapter) -> None:
        self._adapter = adapter

    def verify(self, envelope, context_id: bytes, statement_id: str) -> bool:
        return verify(envelope, context_id, statement_id, self._adapter)


def _seed_bytes(seed: int) -> bytes:
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise E2EError("seed must be int")
    return str(seed).encode("ascii")


def _derive_root_secret(seed: int) -> bytes:
    return sha256(b"NYX:W7:ROOT:" + _seed_bytes(seed))


def _commitment(root_secret: bytes) -> bytes:
    return sha256(b"NYX:IDENTITY:COMMITMENT:v1" + root_secret)


def _repo_head() -> str:
    repo_root = Path(__file__).resolve().parents[4]
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        )
        return output.strip()
    except Exception:
        return "unknown"


def run_e2e(
    seed: int = 123,
    *,
    prover: Prover | None = None,
    verifier: Verifier | None = None,
    repo_head: str | None = None,
) -> tuple[E2ETrace, Summary]:
    root_secret = _derive_root_secret(seed)
    identity_commitment = _commitment(root_secret)
    context_id = sha256(b"NYX:CTX:E2E:W7")
    statement_id = "NYX:STATEMENT:IDENTITY_OWNERSHIP:v1"
    nonce = sha256(b"NYX:W7:NONCE:" + _seed_bytes(seed))

    public_inputs = {"identity_commitment": identity_commitment.hex()}
    witness = {"root_secret": root_secret.hex()}

    adapter = MockProofAdapter()
    if prover is None:
        prover = L0MockProver()
    if verifier is None:
        verifier = L0MockVerifier(adapter)

    envelope = prover.prove(
        statement_id=statement_id,
        context_id=context_id,
        nonce=nonce,
        public_inputs=public_inputs,
        witness=witness,
    )

    wrong_context = sha256(b"NYX:CTX:E2E:W7:WRONG")
    wrong_ok = verifier.verify(envelope, wrong_context, statement_id)
    if wrong_ok:
        raise E2EError("wrong context verified")
    correct_ok = verifier.verify(envelope, context_id, statement_id)
    if not correct_ok:
        raise E2EError("expected proof verification")

    key = b"acct:" + identity_commitment[:8]
    value = b"bind:" + identity_commitment[:8]
    payload = encode_payload_set(key, value)

    action_payload = {
        "op": "set",
        "key": key.hex(),
        "value": value.hex(),
        "commitment": identity_commitment.hex(),
    }
    action_descriptor = ActionDescriptor(
        kind=ActionKind.STATE_MUTATION,
        module="l1.devnet",
        action="set_state",
        payload=action_payload,
        metadata={"purpose": "week7-e2e"},
    )

    chain_id = ChainId("devnet-0.1")
    chain_adapter = DeterministicInMemoryChainAdapter(chain_id)

    keystore = InMemoryKeyStore()
    keystore.put_key("chain-key", SecretBytes(b"wk7-chain-key"))

    kernel = WalletKernel(
        chain_id=chain_id,
        keystore=keystore,
        signer=HMACSigner(),
        nonce_source=InMemoryNonceSource(salt=b"wk7-nonce"),
        proof_adapter=adapter,
    )

    sender = kernel.create_account("sender-e2e")
    kernel.add_signing_key("chain-key", keystore.get_key("chain-key"))

    fee_engine = FeeEngineV0()
    payer = sender.value
    quote = fee_engine.quote(action_descriptor, payer)
    if quote.fee_vector.total() <= 0:
        raise E2EError("fee total must be positive")
    payment = FeePayment(payer=payer, quote_hash=quote.quote_hash, paid_vector=quote.fee_vector)
    receipt = fee_engine.enforce(quote, payment)

    request = kernel.build_action(sender=sender, payload=payload, proofs=[envelope])
    signed = kernel.sign_action(request, "chain-key")
    pre_root = chain_adapter.read_state(b"")[1].value
    tx_hash = kernel.submit(signed, chain_adapter)
    block_ref = chain_adapter.mine_block()
    post_root = chain_adapter.read_state(b"")[1].value
    finality = chain_adapter.get_finality(tx_hash)
    if finality is None:
        raise E2EError("finality missing")
    state_proof = chain_adapter.build_state_proof(key)

    if compare_digest(pre_root, post_root):
        raise E2EError("state root unchanged")

    if quote.fee_vector.get(FeeComponentId.BASE) <= 0:
        raise E2EError("base fee must be positive")

    proof_trace = ProofEnvelopeTrace.from_envelope(envelope)
    meta = TraceMeta(
        trace_version="e2e-trace/v1",
        repo_head=_repo_head() if repo_head is None else repo_head,
        components={
            "l0-identity": "sealed",
            "l0-zk-id": "mock-prover",
            "l2-economics": "fee-engine-v0",
            "l1-chain": "devnet-0.1",
            "wallet-kernel": "sdk",
            "e2e-demo": "week7",
        },
        note="not production crypto",
    )
    trace = E2ETrace(
        meta=meta,
        identity=IdentityTrace(commitment_hex=identity_commitment.hex()),
        proof=proof_trace,
        sanity=SanityTrace(
            wrong_context_verified=wrong_ok,
            correct_context_verified=correct_ok,
        ),
        action=ActionTrace(
            kind=action_descriptor.kind.value,
            module=action_descriptor.module,
            action=action_descriptor.action,
            payload=action_payload,
            metadata=action_descriptor.metadata,
            action_hash_hex=action_descriptor.action_hash().hex(),
        ),
        fee=FeeTrace(
            payer=payer,
            components=quote.fee_vector.canonical_obj(),
            total=quote.fee_vector.total(),
            quote_hash_hex=quote.quote_hash.hex(),
            receipt_hash_hex=receipt.receipt_hash.hex(),
        ),
        chain=ChainTrace(
            chain_id=chain_id.value,
            sender=sender.value,
            nonce_hex=signed.tx_envelope.nonce.hex(),
            payload_hex=payload.hex(),
            signature_hex=signed.tx_envelope.signature.value.hex(),
            tx_hash_hex=tx_hash.value.hex(),
            block_height=block_ref.height,
            block_hash_hex=block_ref.block_hash.hex(),
            state_root_before_hex=pre_root.hex(),
            state_root_after_hex=post_root.hex(),
            finality_proof_hex=finality.proof_bytes.hex(),
            state_proof=StateProofTrace(
                key_hex=key.hex(),
                value_hex=None if state_proof.value is None else state_proof.value.hex(),
                state_root_hex=state_proof.state_root.value.hex(),
                proof_bytes_hex=state_proof.proof_bytes.hex(),
            ),
        ),
    )

    summary = Summary(
        identity_commitment_prefix=identity_commitment.hex()[:12],
        fee_total=quote.fee_vector.total(),
        tx_hash_prefix=tx_hash.value.hex()[:12],
        block_hash_prefix=block_ref.block_hash.hex()[:12],
        state_root_prefix=post_root.hex()[:12],
        receipt_hash_prefix=receipt.receipt_hash.hex()[:12],
    )
    return trace, summary
