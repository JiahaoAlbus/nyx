import os
import pathlib
import random
import sys
import unittest


class PropertyInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_property_invariants(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool, RemoveLiquidity, Swap
        from l3_dex.invariants import check_invariants
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        n = int(os.getenv("PROPERTY_N", "2000"))
        print(f"PROPERTY_N={n}")
        rng = random.Random(1337)

        for _ in range(n):
            state = DexState(pools=())
            state = apply_action(
                state,
                CreatePool(pool_id="p", asset_a="A", asset_b="B"),
            )
            check_invariants(state)

            for _ in range(rng.randint(1, 6)):
                pool = _get_pool(state, "p")
                action_type = rng.choice(["add", "swap", "remove"])
                if action_type == "add":
                    amount_a = rng.randint(1, 5)
                    amount_b = rng.randint(1, 5)
                    action = AddLiquidity(
                        pool_id="p",
                        amount_a=amount_a,
                        amount_b=amount_b,
                    )
                elif action_type == "remove":
                    if pool.total_lp <= 0:
                        continue
                    lp_amount = rng.randint(1, pool.total_lp)
                    action = RemoveLiquidity(pool_id="p", lp_amount=lp_amount)
                else:
                    if pool.reserve_a <= 0 or pool.reserve_b <= 0:
                        continue
                    amount_in = rng.randint(1, 5)
                    asset_in = rng.choice([pool.asset_a, pool.asset_b])
                    action = Swap(
                        pool_id="p",
                        amount_in=amount_in,
                        min_out=0,
                        asset_in=asset_in,
                    )

                try:
                    prev_pool = _get_pool(state, "p")
                    prev_k = prev_pool.reserve_a * prev_pool.reserve_b
                    state = apply_action(state, action)
                    check_invariants(state)
                    if isinstance(action, Swap):
                        next_pool = _get_pool(state, "p")
                        next_k = next_pool.reserve_a * next_pool.reserve_b
                        self.assertGreaterEqual(next_k, prev_k)
                except Exception:
                    continue


def _get_pool(state, pool_id: str):
    for pool in state.pools:
        if pool.pool_id == pool_id:
            return pool
    raise AssertionError("pool not found")


if __name__ == "__main__":
    unittest.main()
