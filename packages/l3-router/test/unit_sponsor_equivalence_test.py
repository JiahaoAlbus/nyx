import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIRS = [
    REPO_ROOT / "packages" / "l3-router" / "src",
    REPO_ROOT / "packages" / "l3-dex" / "src",
    REPO_ROOT / "packages" / "l2-economics" / "src",
]
for path in SRC_DIRS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from l2_economics.engine import FeeEngineV0  # noqa: E402
from l3_dex.actions import Swap  # noqa: E402
from l3_dex.state import DexState, PoolState  # noqa: E402
from l3_router.actions import RouteSwap, RouterAction, RouterActionKind  # noqa: E402
from l3_router.fee_binding import quote_fee_for_route  # noqa: E402
from l3_router.state import RouterState  # noqa: E402


class SponsorEquivalenceTests(unittest.TestCase):
    def test_sponsor_keeps_amounts(self) -> None:
        state = RouterState(
            dex_state=DexState(
                pools=(
                    PoolState(
                        pool_id="pool-1",
                        asset_a="ASSET_A",
                        asset_b="ASSET_B",
                        reserve_a=1000,
                        reserve_b=1000,
                        total_lp=1000,
                    ),
                ),
            )
        )
        step = Swap(pool_id="pool-1", amount_in=100, min_out=0, asset_in="ASSET_A")
        action = RouterAction(
            kind=RouterActionKind.ROUTE_SWAP,
            payload=RouteSwap(steps=(step,)),
        )
        engine = FeeEngineV0()
        quote_a = quote_fee_for_route(engine, state, action, payer="payer-a")
        quote_b = engine.sponsor(quote_a, "payer-b")
        quote_c = quote_fee_for_route(engine, state, action, payer="payer-c")

        self.assertEqual(quote_a.fee_vector, quote_b.fee_vector)
        self.assertEqual(quote_a.action_hash, quote_b.action_hash)
        self.assertEqual(quote_a.fee_vector, quote_c.fee_vector)


if __name__ == "__main__":
    unittest.main()
