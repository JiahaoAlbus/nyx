import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "e2e-private-transfer" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from e2e_private_transfer.canonical import CanonicalizationError, canonicalize  # noqa: E402


class CanonicalLimitsTests(unittest.TestCase):
    def test_depth_limit(self):
        nested = []
        for _ in range(25):
            nested = [nested]
        with self.assertRaises(CanonicalizationError):
            canonicalize(nested)

    def test_size_limit(self):
        payload = {"k": "a" * 70000}
        with self.assertRaises(CanonicalizationError):
            canonicalize(payload)

    def test_illegal_types(self):
        with self.assertRaises(CanonicalizationError):
            canonicalize({"k": 1.25})
        with self.assertRaises(CanonicalizationError):
            canonicalize({"k": b"bad"})


if __name__ == "__main__":
    unittest.main()
