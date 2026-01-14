import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
PL_SRC = REPO_ROOT / "packages" / "l2-private-ledger" / "src"
ECON_SRC = REPO_ROOT / "packages" / "l2-economics" / "src"
for path in (PL_SRC, ECON_SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from fee import FeeComponentId, FeeVector  # noqa: E402
from engine import FeeEngineV0  # noqa: E402
from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint  # noqa: E402
from l2_private_ledger.errors import ValidationError  # noqa: E402
from l2_private_ledger.fee_binding import (  # noqa: E402
    compute_action_hash,
    enforce_fee_for_private_action,
    quote_fee_for_private_action,
)
from l2_private_ledger.state import empty_state, state_root  # noqa: E402
from l2_private_ledger.types import sha256  # noqa: E402


class EnforcePaidVectorExactTests(unittest.TestCase):
    def test_paid_vector_must_match(self):
        engine = FeeEngineV0()
        state = empty_state()
        root = state_root(state)
        action = LedgerAction(
            ActionKind.PRIVATE_MINT,
            PrivateMint(sha256(b"fee")),
        )
        action_hash = compute_action_hash(action)
        quote = quote_fee_for_private_action(
            engine,
            action,
            root,
            action_hash,
            payer="payer-a",
        )

        components = []
        for component, amount in quote.fee_vector.components:
            if component == FeeComponentId.BASE:
                components.append((component, amount + 1))
            else:
                components.append((component, amount))
        wrong_vector = FeeVector(tuple(components))
        with self.assertRaises(ValidationError):
            enforce_fee_for_private_action(
                engine,
                quote,
                wrong_vector,
                payer="payer-a",
            )

        receipt = enforce_fee_for_private_action(
            engine,
            quote,
            quote.fee_vector,
            payer="payer-a",
        )
        self.assertEqual(receipt.paid_vector, quote.fee_vector)


if __name__ == "__main__":
    unittest.main()
