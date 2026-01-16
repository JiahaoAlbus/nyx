import pathlib
import sys
import unittest


class DeterminismGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_same_sequence_same_hashes(self) -> None:
        from l3_dex.actions import AddLiquidity, CreatePool, RemoveLiquidity, Swap
        from l3_dex.kernel import apply_action_with_receipt
        from l3_dex.state import DexState, state_hash

        actions = [
            CreatePool(pool_id="p", asset_a="A", asset_b="B"),
            AddLiquidity(pool_id="p", amount_a=10, amount_b=12),
            Swap(pool_id="p", amount_in=3, min_out=0, asset_in="A"),
            RemoveLiquidity(pool_id="p", lp_amount=5),
        ]

        hashes_a = _run(actions)
        hashes_b = _run(actions)
        self.assertEqual(hashes_a, hashes_b)


def _run(actions):
    from l3_dex.kernel import apply_action_with_receipt
    from l3_dex.state import DexState, state_hash

    state = DexState(pools=())
    receipt_hashes = []
    for action in actions:
        state, receipt = apply_action_with_receipt(state, action)
        receipt_hashes.append(receipt.receipt_hash.hex())
    receipt_hashes.append(state_hash(state).hex())
    return receipt_hashes


if __name__ == "__main__":
    unittest.main()
