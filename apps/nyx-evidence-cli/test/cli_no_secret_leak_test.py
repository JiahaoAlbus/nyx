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

from e2e_private_transfer.hashing import sha256  # noqa: E402
from nyx_evidence_cli.app import run_and_write_evidence  # noqa: E402


class EvidenceNoSecretLeakTests(unittest.TestCase):
    def test_no_secret_in_outputs(self):
        seed = 123
        root_secret = sha256(b"NYX:Q3:W5:ROOT:" + str(seed).encode("ascii")).hex()
        with tempfile.TemporaryDirectory() as tmp:
            bundle = run_and_write_evidence(seed=seed, out_dir=tmp)
            out_dir = Path(tmp)
            blobs = [bundle.stdout_text]
            for path in out_dir.iterdir():
                if path.is_file():
                    blobs.append(path.read_text(encoding="utf-8"))
            combined = "\n".join(blobs)
            self.assertNotIn(root_secret, combined)


if __name__ == "__main__":
    unittest.main()
