import pathlib
import sys
import unittest


class SkeletonImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        repo_root = pathlib.Path(__file__).resolve().parents[3]
        src_path = repo_root / "packages" / "l3-dex" / "src"
        sys.path.insert(0, str(src_path))

    def test_imports(self) -> None:
        import l3_dex
        from l3_dex import actions, invariants, receipts, replay, state

        self.assertTrue(hasattr(actions, "ActionKind"))
        self.assertTrue(hasattr(state, "DexState"))
        self.assertTrue(hasattr(receipts, "DexReceipt"))
        self.assertTrue(hasattr(replay, "replay_receipt"))
        self.assertTrue(hasattr(invariants, "check_invariants"))
        self.assertTrue(hasattr(l3_dex, "ActionKind"))


if __name__ == "__main__":
    unittest.main()
