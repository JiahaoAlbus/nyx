import pathlib
import sys
import unittest


class EnforcePaidVectorExactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        l3_src = repo_root / "packages" / "l3-dex" / "src"
        l2_src = repo_root / "packages" / "l2-economics" / "src"
        sys.path.insert(0, str(l3_src))
        sys.path.insert(0, str(l2_src))

    def test_paid_vector_must_match(self) -> None:
        from action import ActionKind
        from engine import FeeEngineError, FeeEngineV0
        from fee import FeeComponentId, FeeVector
        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.fee_binding import enforce_fee_for_action, quote_fee_for_action
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        engine = FeeEngineV0()
        state = DexState(pools=())
        state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
        quote = quote_fee_for_action(
            engine,
            state,
            AddLiquidity(pool_id="p", amount_a=1, amount_b=2),
            payer="payer",
        )
        bad_vector = FeeVector.for_action(
            ActionKind.STATE_MUTATION,
            (
                (FeeComponentId.BASE, 1),
                (FeeComponentId.BYTES, 0),
                (FeeComponentId.COMPUTE, 0),
            ),
        )
        with self.assertRaises(FeeEngineError):
            enforce_fee_for_action(engine, quote, bad_vector, payer=quote.payer)


if __name__ == "__main__":
    unittest.main()
