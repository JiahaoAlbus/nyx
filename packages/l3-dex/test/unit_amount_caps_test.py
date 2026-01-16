import pathlib
import sys
import unittest


class AmountCapsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_reserve_caps_enforced(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.errors import ValidationError
        from l3_dex.kernel import apply_action
        from l3_dex.state import DexState, MAX_RESERVE

        state = DexState(pools=())
        state = apply_action(state, CreatePool(pool_id="p", asset_a="A", asset_b="B"))
        state = apply_action(
            state,
            AddLiquidity(pool_id="p", amount_a=MAX_RESERVE, amount_b=MAX_RESERVE),
        )
        with self.assertRaises(ValidationError):
            apply_action(state, AddLiquidity(pool_id="p", amount_a=1, amount_b=1))


if __name__ == "__main__":
    unittest.main()
