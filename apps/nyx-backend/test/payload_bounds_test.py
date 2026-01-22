import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
PKG_PATHS = [
    SRC,
    ROOT.parents[1] / "packages" / "e2e-private-transfer" / "src",
    ROOT.parents[1] / "packages" / "l2-private-ledger" / "src",
    ROOT.parents[1] / "packages" / "l0-zk-id" / "src",
    ROOT.parents[1] / "packages" / "l2-economics" / "src",
    ROOT.parents[1] / "packages" / "l2-platform-fee" / "src",
    ROOT.parents[1] / "packages" / "l1-chain" / "src",
    ROOT.parents[1] / "packages" / "wallet-kernel" / "src",
]
for path in PKG_PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from nyx_backend.evidence import EvidenceError, run_evidence  # noqa: E402


class PayloadBoundsTests(unittest.TestCase):
    def test_payload_text_too_long_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            with self.assertRaises(EvidenceError):
                run_evidence(
                    seed=123,
                    run_id="bounds-1",
                    module="chat",
                    action="message_event",
                    payload={"message": "x" * 300},
                    base_dir=base_dir,
                )

    def test_payload_list_too_large_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            with self.assertRaises(EvidenceError):
                run_evidence(
                    seed=123,
                    run_id="bounds-2",
                    module="exchange",
                    action="route_swap",
                    payload={"items": list(range(100))},
                    base_dir=base_dir,
                )

    def test_payload_depth_too_deep_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            deep = {"a": {"b": {"c": {"d": {"e": {"f": {"g": 1}}}}}}}
            with self.assertRaises(EvidenceError):
                run_evidence(
                    seed=123,
                    run_id="bounds-3",
                    module="exchange",
                    action="route_swap",
                    payload=deep,
                    base_dir=base_dir,
                )


if __name__ == "__main__":
    unittest.main()
