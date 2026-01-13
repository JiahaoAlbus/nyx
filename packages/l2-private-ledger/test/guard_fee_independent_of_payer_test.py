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
from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint  # noqa: E402
from l2_private_ledger.fee_binding import compute_action_hash, quote_fee_for_private_action  # noqa: E402
from l2_private_ledger.state import empty_state, state_root  # noqa: E402
from l2_private_ledger.types import sha256  # noqa: E402


class FeeIndependentOfPayerGuardTests(unittest.TestCase):
    def test_fee_independent_of_payer(self):
        engine = FeeEngineV0()
        state = empty_state()
        root = state_root(state)
        action = LedgerAction(
            ActionKind.PRIVATE_MINT,
            PrivateMint(sha256(b"guard")),
        )
        action_hash = compute_action_hash(action)

        payers = ["payer-a", "payer-b", "payer-c", "payer-d"]
        quotes = [
            quote_fee_for_private_action(
                engine,
                action,
                root,
                action_hash,
                payer=payer,
            )
            for payer in payers
        ]
        base_vector = quotes[0].fee_vector
        for quote in quotes[1:]:
            self.assertEqual(base_vector, quote.fee_vector)


if __name__ == "__main__":
    unittest.main()
