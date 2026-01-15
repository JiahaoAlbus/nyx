import os
import random
import sys
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
    DEFAULT_DISCLOSE_CONTEXT_ID,
    STATEMENT_ID_AT_LEAST,
    STATEMENT_ID_TIER,
    prove_rep_at_least_mock,
    prove_rep_tier_mock,
    verify_rep_at_least,
    verify_rep_tier,
)
from l0_reputation.hashing import sha256  # noqa: E402
from l0_reputation.kernel import new_pseudonym  # noqa: E402

PROPERTY_N = int(os.environ.get("PROPERTY_N", "2000"))


def rand_bytes32(rng: random.Random) -> bytes:
    return bytes(rng.getrandbits(8) for _ in range(32))


def random_context(rng: random.Random, tag: bytes) -> bytes:
    return sha256(tag + rand_bytes32(rng))


class PropertyDisclosureSeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print(f"PROPERTY_N={PROPERTY_N}")

    def test_context_statement_rep_root_separation(self):
        rng = random.Random(3319)
        for _ in range(PROPERTY_N):
            rep_root = sha256(rand_bytes32(rng))
            pseudo = new_pseudonym(rand_bytes32(rng))
            nonce = rand_bytes32(rng)
            k = rng.randint(0, 50)
            tier = f"tier-{rng.randint(1, 5)}"
            witness = {"note": "ok"}

            env_at = prove_rep_at_least_mock(
                rep_root=rep_root,
                pseudonym_id=pseudo,
                k=k,
                nonce=nonce,
                witness=witness,
            )
            self.assertTrue(verify_rep_at_least(env_at, rep_root, pseudo, k))

            for idx in range(10):
                wrong_context = sha256(b"ctx" + bytes([idx]) + rep_root)
                self.assertFalse(
                    verify_rep_at_least(
                        env_at,
                        rep_root,
                        pseudo,
                        k,
                        context_id=wrong_context,
                    )
                )

            for statement_id in ("NYX:STATEMENT:OTHER:v1", "NYX:STATEMENT:ALT:v1", "NYX:STATEMENT:X:v1"):
                self.assertFalse(
                    verify_rep_at_least(
                        env_at,
                        rep_root,
                        pseudo,
                        k,
                        statement_id=statement_id,
                    )
                )

            for idx in range(3):
                wrong_root = sha256(b"root" + bytes([idx]) + rep_root)
                self.assertFalse(
                    verify_rep_at_least(env_at, wrong_root, pseudo, k)
                )

            env_tier = prove_rep_tier_mock(
                rep_root=rep_root,
                pseudonym_id=pseudo,
                tier=tier,
                nonce=nonce,
                witness=witness,
            )
            self.assertTrue(verify_rep_tier(env_tier, rep_root, pseudo, tier))

            for idx in range(10):
                wrong_context = sha256(b"ctx" + bytes([idx]) + rep_root)
                self.assertFalse(
                    verify_rep_tier(
                        env_tier,
                        rep_root,
                        pseudo,
                        tier,
                        context_id=wrong_context,
                    )
                )

            for statement_id in ("NYX:STATEMENT:OTHER:v1", "NYX:STATEMENT:ALT:v1", "NYX:STATEMENT:X:v1"):
                self.assertFalse(
                    verify_rep_tier(
                        env_tier,
                        rep_root,
                        pseudo,
                        tier,
                        statement_id=statement_id,
                    )
                )

            for idx in range(3):
                wrong_root = sha256(b"root" + bytes([idx]) + rep_root)
                self.assertFalse(
                    verify_rep_tier(env_tier, wrong_root, pseudo, tier)
                )


if __name__ == "__main__":
    unittest.main()
