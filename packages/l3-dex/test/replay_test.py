import pathlib
import sys
import unittest


class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_replay_receipts(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.kernel import apply_action_with_receipt
        from l3_dex.replay import replay_receipt
        from l3_dex.state import DexState, state_hash

        state = DexState(pools=())
        create = CreatePool(pool_id="p", asset_a="A", asset_b="B")
        state, receipt1 = apply_action_with_receipt(state, create)
        state, receipt2 = apply_action_with_receipt(
            state,
            AddLiquidity(pool_id="p", amount_a=1, amount_b=2),
        )

        replay_state = DexState(pools=())
        replay_state = replay_receipt(replay_state, receipt1)
        replay_state = replay_receipt(replay_state, receipt2)

        self.assertEqual(state_hash(replay_state), state_hash(state))


if __name__ == "__main__":
    unittest.main()
