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
    prove_rep_at_least_mock,
    prove_rep_tier_mock,
    verify_rep_at_least,
    verify_rep_tier,
)
from l0_reputation.hashing import sha256  # noqa: E402
from l0_reputation.kernel import new_pseudonym  # noqa: E402


class DisclosureHappyPathTests(unittest.TestCase):
    def test_rep_at_least_happy_path(self):
        rep_root = sha256(b"rep-root-1")
        pseudo = new_pseudonym(sha256(b"rep-secret-1"))
        nonce = sha256(b"rep-nonce-1")
        envelope = prove_rep_at_least_mock(
            rep_root=rep_root,
            pseudonym_id=pseudo,
            k=5,
            nonce=nonce,
            witness={"note": "ok"},
        )
        self.assertTrue(verify_rep_at_least(envelope, rep_root, pseudo, 5))
        bad_context = sha256(b"rep-bad-context")
        self.assertFalse(
            verify_rep_at_least(
                envelope,
                rep_root,
                pseudo,
                5,
                context_id=bad_context,
            )
        )

    def test_rep_tier_happy_path(self):
        rep_root = sha256(b"rep-root-2")
        pseudo = new_pseudonym(sha256(b"rep-secret-2"))
        nonce = sha256(b"rep-nonce-2")
        envelope = prove_rep_tier_mock(
            rep_root=rep_root,
            pseudonym_id=pseudo,
            tier="gold",
            nonce=nonce,
            witness={"note": "ok"},
        )
        self.assertTrue(verify_rep_tier(envelope, rep_root, pseudo, "gold"))
        bad_context = sha256(b"rep-bad-context-2")
        self.assertFalse(
            verify_rep_tier(
                envelope,
                rep_root,
                pseudo,
                "gold",
                context_id=bad_context,
            )
        )


if __name__ == "__main__":
    unittest.main()
