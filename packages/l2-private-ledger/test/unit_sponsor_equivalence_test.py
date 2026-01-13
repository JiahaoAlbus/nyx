import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
PL_SRC = REPO_ROOT / "packages" / "l2-private-ledger" / "src"
ECON_SRC = REPO_ROOT / "packages" / "l2-economics" / "src"
for path in (PL_SRC, ECON_SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from engine import FeeEngineV0  # noqa: E402
from hashing import compare_digest  # noqa: E402
from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateSpend  # noqa: E402
from l2_private_ledger.fee_binding import compute_action_hash, quote_fee_for_private_action  # noqa: E402
from l2_private_ledger.state import empty_state, state_root  # noqa: E402
from l2_private_ledger.types import sha256  # noqa: E402


class SponsorEquivalenceTests(unittest.TestCase):
    def test_sponsor_equivalence(self):
        engine = FeeEngineV0()
        state = empty_state()
        root = state_root(state)
        action = LedgerAction(
            ActionKind.PRIVATE_SPEND,
            PrivateSpend(sha256(b"fee-spend")),
        )
        action_hash = compute_action_hash(action)

        quote_a = quote_fee_for_private_action(
            engine,
            action,
            root,
            action_hash,
            payer="payer-a",
        )
        quote_b = quote_fee_for_private_action(
            engine,
            action,
            root,
            action_hash,
            payer="payer-b",
        )
        self.assertEqual(quote_a.fee_vector, quote_b.fee_vector)
        self.assertTrue(compare_digest(quote_a.action_hash, quote_b.action_hash))

        sponsored = engine.sponsor(quote_a, "payer-c")
        self.assertEqual(sponsored.fee_vector, quote_a.fee_vector)
        self.assertTrue(compare_digest(sponsored.action_hash, quote_a.action_hash))
        self.assertNotEqual(sponsored.payer, quote_a.payer)


if __name__ == "__main__":
    unittest.main()
