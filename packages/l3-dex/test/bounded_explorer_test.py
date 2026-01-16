import itertools
import pathlib
import sys
import unittest


class BoundedExplorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_bounded_explorer(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.invariants import check_invariants
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState

        create = CreatePool(pool_id="p", asset_a="A", asset_b="B")
        amounts = [(1, 1), (1, 2), (2, 1)]
        adds = [AddLiquidity(pool_id="p", amount_a=a, amount_b=b) for a, b in amounts]

        for depth in range(1, 5):
            for tail in itertools.product(adds, repeat=max(depth - 1, 0)):
                state = DexState(pools=())
                state = apply_action(state, create)
                check_invariants(state)
                for action in tail:
                    state = apply_action(state, action)
                    check_invariants(state)


if __name__ == "__main__":
    unittest.main()
