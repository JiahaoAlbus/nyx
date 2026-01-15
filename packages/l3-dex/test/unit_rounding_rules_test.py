import pathlib
import sys
import unittest


class RoundingRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_swap_rounding_floor(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool, Swap
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        state = DexState(pools=())
        state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
        state = apply_action(state, AddLiquidity(pool_id="p", amount_a=1000, amount_b=1000))
        state = apply_action(state, Swap(pool_id="p", amount_in=100, min_out=0, asset_in="A"))
        pool = _get_pool(state, "p")
        self.assertEqual(pool.reserve_a, 1099)
        self.assertEqual(pool.reserve_b, 909)

    def test_remove_rounding_floor(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool, RemoveLiquidity
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        state = DexState(pools=())
        state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
        state = apply_action(state, AddLiquidity(pool_id="p", amount_a=1000, amount_b=1000))
        state = apply_action(state, RemoveLiquidity(pool_id="p", lp_amount=500))
        pool = _get_pool(state, "p")
        self.assertEqual(pool.reserve_a, 750)
        self.assertEqual(pool.reserve_b, 750)
        self.assertEqual(pool.total_lp, 1500)


def _get_pool(state, pool_id: str):
    for pool in state.pools:
        if pool.pool_id == pool_id:
            return pool
    raise AssertionError("pool not found")


if __name__ == "__main__":
    unittest.main()
