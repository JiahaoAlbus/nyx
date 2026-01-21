import tempfile
from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
PATHS = [
    REPO_ROOT / "apps" / "reference-ui-backend" / "src",
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

from nyx_reference_ui_backend.evidence import build_export_zip, run_evidence  # noqa: E402


class ExportZipDeterminismTests(unittest.TestCase):
    def test_export_zip_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            run_evidence(seed=123, run_id="seed-123", base_dir=base_dir)
            zip_a = build_export_zip("seed-123", base_dir)
            zip_b = build_export_zip("seed-123", base_dir)
            self.assertEqual(zip_a, zip_b)


if __name__ == "__main__":
    unittest.main()
