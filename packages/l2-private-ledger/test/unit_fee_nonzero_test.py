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
from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint, PrivateSpend  # noqa: E402
from l2_private_ledger.fee_binding import compute_action_hash, quote_fee_for_private_action  # noqa: E402
from l2_private_ledger.state import empty_state, state_root  # noqa: E402
from l2_private_ledger.types import sha256  # noqa: E402


class FeeNonZeroTests(unittest.TestCase):
    def test_fee_nonzero_for_mint_and_spend(self):
        engine = FeeEngineV0()
        state = empty_state()
        root = state_root(state)

        mint_action = LedgerAction(
            ActionKind.PRIVATE_MINT,
            PrivateMint(sha256(b"fee-mint")),
        )
        mint_hash = compute_action_hash(mint_action)
        mint_quote = quote_fee_for_private_action(
            engine,
            mint_action,
            root,
            mint_hash,
            payer="payer-a",
        )
        self.assertGreater(mint_quote.fee_vector.total(), 0)

        spend_action = LedgerAction(
            ActionKind.PRIVATE_SPEND,
            PrivateSpend(sha256(b"fee-spend")),
        )
        spend_hash = compute_action_hash(spend_action)
        spend_quote = quote_fee_for_private_action(
            engine,
            spend_action,
            root,
            spend_hash,
            payer="payer-b",
        )
        self.assertGreater(spend_quote.fee_vector.total(), 0)


if __name__ == "__main__":
    unittest.main()
