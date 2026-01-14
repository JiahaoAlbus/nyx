import sys
from dataclasses import replace
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
ZK_SRC = REPO_ROOT / "packages" / "l0-zk-id" / "src"
REP_SRC = REPO_ROOT / "packages" / "l0-reputation" / "src"
if str(ZK_SRC) not in sys.path:
    sys.path.insert(0, str(ZK_SRC))
if str(REP_SRC) not in sys.path:
    sys.path.insert(0, str(REP_SRC))

from l0_reputation.disclosure_wiring import (  # noqa: E402
    prove_rep_at_least_mock,
    prove_rep_tier_mock,
    verify_rep_at_least,
    verify_rep_tier,
)
from l0_reputation.hashing import sha256  # noqa: E402
from l0_reputation.kernel import new_pseudonym  # noqa: E402


def flip_bit(data: bytes) -> bytes:
    return bytes([data[0] ^ 0x01]) + data[1:]


class DisclosureTamperTests(unittest.TestCase):
    def test_rep_at_least_tamper(self):
        rep_root = sha256(b"rep-root-3")
        pseudo = new_pseudonym(sha256(b"rep-secret-3"))
        envelope = prove_rep_at_least_mock(
            rep_root=rep_root,
            pseudonym_id=pseudo,
            k=7,
            nonce=sha256(b"rep-nonce-3"),
            witness={"note": "ok"},
        )

        tampered_inputs = dict(envelope.public_inputs)
        tampered_root = flip_bit(bytes.fromhex(tampered_inputs["rep_root"]))
        tampered_inputs["rep_root"] = tampered_root.hex()
        tampered_env = replace(envelope, public_inputs=tampered_inputs)
        self.assertFalse(verify_rep_at_least(tampered_env, rep_root, pseudo, 7))

        tampered_inputs = dict(envelope.public_inputs)
        tampered_inputs["k"] = 8
        tampered_env = replace(envelope, public_inputs=tampered_inputs)
        self.assertFalse(verify_rep_at_least(tampered_env, rep_root, pseudo, 7))

        tampered_env = replace(envelope, nonce=flip_bit(envelope.nonce))
        self.assertFalse(verify_rep_at_least(tampered_env, rep_root, pseudo, 7))

        tampered_env = replace(envelope, binding_tag=flip_bit(envelope.binding_tag))
        self.assertFalse(verify_rep_at_least(tampered_env, rep_root, pseudo, 7))

    def test_rep_tier_tamper(self):
        rep_root = sha256(b"rep-root-4")
        pseudo = new_pseudonym(sha256(b"rep-secret-4"))
        envelope = prove_rep_tier_mock(
            rep_root=rep_root,
            pseudonym_id=pseudo,
            tier="silver",
            nonce=sha256(b"rep-nonce-4"),
            witness={"note": "ok"},
        )

        tampered_inputs = dict(envelope.public_inputs)
        tampered_root = flip_bit(bytes.fromhex(tampered_inputs["rep_root"]))
        tampered_inputs["rep_root"] = tampered_root.hex()
        tampered_env = replace(envelope, public_inputs=tampered_inputs)
        self.assertFalse(verify_rep_tier(tampered_env, rep_root, pseudo, "silver"))

        tampered_inputs = dict(envelope.public_inputs)
        tampered_inputs["tier"] = "bronze"
        tampered_env = replace(envelope, public_inputs=tampered_inputs)
        self.assertFalse(verify_rep_tier(tampered_env, rep_root, pseudo, "silver"))

        tampered_env = replace(envelope, nonce=flip_bit(envelope.nonce))
        self.assertFalse(verify_rep_tier(tampered_env, rep_root, pseudo, "silver"))

        tampered_env = replace(envelope, binding_tag=flip_bit(envelope.binding_tag))
        self.assertFalse(verify_rep_tier(tampered_env, rep_root, pseudo, "silver"))


if __name__ == "__main__":
    unittest.main()
