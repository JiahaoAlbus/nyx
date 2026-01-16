import pathlib
import sys
import unittest


class ReplayRejectsTamperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_replay_rejects_tamper(self) -> None:
        from dataclasses import replace

        from l3_dex.actions import AddLiquidity, CreatePool
        from l3_dex.errors import ValidationError
        from l3_dex.kernel import apply_action_with_receipt
        from l3_dex.replay import replay_receipt
        from l3_dex.state import DexState

        state = DexState(pools=())
        state, _ = apply_action_with_receipt(
            state,
            CreatePool(pool_id="p", asset_a="A", asset_b="B"),
        )
        state, receipt = apply_action_with_receipt(
            state,
            AddLiquidity(pool_id="p", amount_a=1, amount_b=2),
        )

        def flip_last(value: bytes) -> bytes:
            raw = bytearray(value)
            raw[-1] ^= 1
            return bytes(raw)

        bad_receipt = replace(receipt, receipt_hash=flip_last(receipt.receipt_hash))
        with self.assertRaises(ValidationError):
            replay_receipt(DexState(pools=()), bad_receipt)


if __name__ == "__main__":
    unittest.main()
