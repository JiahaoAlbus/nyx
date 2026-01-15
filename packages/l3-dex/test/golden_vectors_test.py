import pathlib
import sys
import unittest


class GoldenVectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_golden_receipt_hashes(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.kernel import apply_action_with_receipt
        from l3_dex.state import DexState

        expected_receipt_hashes = [
            "e84239d7ad79bc36fa698d4c8061ffe99cd5f5ab74443a9646b5214e9c73d3f9",
            "997d14e3b370c067a991cf32b404b65a944168b3c1c493ad991cb365b2d6dd2f",
        ]
        expected_state_hashes = [
            "23117f50eb4badafcb01741b40d1a414906a15143ec190dd4a9fc4ada0240397",
            "1a88133c4331af8296805318245516f3bbeb9e79dff9f3a36cd715c370300f9a",
        ]

        state = DexState(pools=())
        state, receipt1 = apply_action_with_receipt(
            state,
            CreatePool(pool_id="p", asset_a="A", asset_b="B"),
        )
        state, receipt2 = apply_action_with_receipt(
            state,
            AddLiquidity(pool_id="p", amount_a=1, amount_b=2),
        )

        got_receipts = [receipt1.receipt_hash.hex(), receipt2.receipt_hash.hex()]
        got_states = [receipt1.after_hash.hex(), receipt2.after_hash.hex()]

        self.assertEqual(got_receipts, expected_receipt_hashes)
        self.assertEqual(got_states, expected_state_hashes)


if __name__ == "__main__":
    unittest.main()
