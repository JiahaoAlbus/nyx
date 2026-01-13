import os
import random
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


class FeeBindingPropertyTests(unittest.TestCase):
    def test_fee_binding_properties(self):
        n = int(os.getenv("PROPERTY_N", "2000"))
        print(f"PROPERTY_N={n}")
        rng = random.Random(2711)
        engine = FeeEngineV0()
        root = state_root(empty_state())

        for idx in range(n):
            if rng.random() < 0.5:
                commitment = sha256(b"c" + rng.getrandbits(256).to_bytes(32, "big"))
                action = LedgerAction(ActionKind.PRIVATE_MINT, PrivateMint(commitment))
            else:
                nullifier = sha256(b"n" + rng.getrandbits(256).to_bytes(32, "big"))
                action = LedgerAction(ActionKind.PRIVATE_SPEND, PrivateSpend(nullifier))
            action_hash = compute_action_hash(action)
            payer_a = f"payer-{idx}-a"
            payer_b = f"payer-{idx}-b"

            quote_a = quote_fee_for_private_action(
                engine,
                action,
                root,
                action_hash,
                payer=payer_a,
            )
            quote_b = quote_fee_for_private_action(
                engine,
                action,
                root,
                action_hash,
                payer=payer_b,
            )

            self.assertGreater(quote_a.fee_vector.total(), 0)
            self.assertEqual(quote_a.fee_vector, quote_b.fee_vector)


if __name__ == "__main__":
    unittest.main()
