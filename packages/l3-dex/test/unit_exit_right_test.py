import pathlib
import sys
import unittest


class ExitRightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_remove_all_lp_redeems(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool, RemoveLiquidity
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        state = DexState(pools=())
        state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
        state = apply_action(state, AddLiquidity(pool_id="p", amount_a=10, amount_b=20))
        pool = _get_pool(state, "p")
        state = apply_action(state, RemoveLiquidity(pool_id="p", lp_amount=pool.total_lp))
        pool = _get_pool(state, "p")
        self.assertEqual(pool.reserve_a, 0)
        self.assertEqual(pool.reserve_b, 0)
        self.assertEqual(pool.total_lp, 0)


def _get_pool(state, pool_id: str):
    for pool in state.pools:
        if pool.pool_id == pool_id:
            return pool
    raise AssertionError("pool not found")


if __name__ == "__main__":
    unittest.main()
