import pathlib
import sys
import unittest


class SponsorEquivalenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        l3_src = repo_root / "packages" / "l3-dex" / "src"
        l2_src = repo_root / "packages" / "l2-economics" / "src"
        sys.path.insert(0, str(l3_src))
        sys.path.insert(0, str(l2_src))

    def test_sponsor_keeps_amount(self) -> None:
        from engine import FeeEngineV0
        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.fee_binding import quote_fee_for_action, sponsor_quote
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        engine = FeeEngineV0()
        state = DexState(pools=())
        state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
        quote = quote_fee_for_action(
            engine,
            state,
            AddLiquidity(pool_id="p", amount_a=2, amount_b=3),
            payer="payer-a",
        )
        sponsored = sponsor_quote(engine, quote, new_payer="payer-b")
        self.assertEqual(sponsored.fee_vector, quote.fee_vector)


if __name__ == "__main__":
    unittest.main()
