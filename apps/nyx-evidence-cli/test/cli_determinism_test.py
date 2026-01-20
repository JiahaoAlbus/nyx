import json
import tempfile
from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
PATHS = [
    REPO_ROOT / "apps" / "nyx-evidence-cli" / "src",
    REPO_ROOT / "packages" / "e2e-private-transfer" / "src",
    REPO_ROOT / "packages" / "l2-private-ledger" / "src",
    REPO_ROOT / "packages" / "l0-zk-id" / "src",
    REPO_ROOT / "packages" / "l2-economics" / "src",
    REPO_ROOT / "packages" / "l1-chain" / "src",
    REPO_ROOT / "packages" / "wallet-kernel" / "src",
]
for path in PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from nyx_evidence_cli.app import run_and_write_evidence  # noqa: E402


class EvidenceDeterminismTests(unittest.TestCase):
    def test_evidence_determinism(self):
        with tempfile.TemporaryDirectory() as tmp_a, tempfile.TemporaryDirectory() as tmp_b:
            run_and_write_evidence(seed=123, out_dir=tmp_a)
            run_and_write_evidence(seed=123, out_dir=tmp_b)
            files = [
                "outputs.json",
                "receipt_hashes.json",
                "state_hash.txt",
                "replay_ok.txt",
            ]
            for name in files:
                a_text = (Path(tmp_a) / name).read_text(encoding="utf-8")
                b_text = (Path(tmp_b) / name).read_text(encoding="utf-8")
                self.assertEqual(a_text, b_text)

            out_a = json.loads((Path(tmp_a) / "outputs.json").read_text(encoding="utf-8"))
            out_b = json.loads((Path(tmp_b) / "outputs.json").read_text(encoding="utf-8"))
            self.assertEqual(out_a, out_b)


if __name__ == "__main__":
    unittest.main()
