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


class EvidenceSmokeTests(unittest.TestCase):
    def test_evidence_bundle_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = run_and_write_evidence(seed=123, out_dir=tmp)
            self.assertTrue(bundle.outputs.replay_ok)
            out_dir = Path(tmp)
            required = [
                "protocol_anchor.json",
                "inputs.json",
                "outputs.json",
                "receipt_hashes.json",
                "state_hash.txt",
                "replay_ok.txt",
                "stdout.txt",
            ]
            for name in required:
                self.assertTrue((out_dir / name).exists())
            outputs = json.loads((out_dir / "outputs.json").read_text(encoding="utf-8"))
            self.assertTrue(outputs["replay_ok"])


if __name__ == "__main__":
    unittest.main()
