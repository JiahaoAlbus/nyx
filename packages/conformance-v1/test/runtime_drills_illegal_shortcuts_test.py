import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "conformance-v1" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from conformance_v1.drills import run_drills  # noqa: E402


class RuntimeDrillTests(unittest.TestCase):
    def test_drills_pass(self):
        results = run_drills()
        failures = [result for result in results if not result.passed]
        self.assertEqual(failures, [])
        expected_ids = {
            "Q4-DEX-01",
            "Q4-DEX-02",
            "Q4-DEX-03",
            "Q4-DEX-04",
            "Q4-DEX-05",
            "Q4-DEX-06",
            "Q4-BRIDGE-01",
            "Q4-ONOFF-01",
        }
        result_ids = {result.rule_id for result in results}
        self.assertTrue(expected_ids.issubset(result_ids))


if __name__ == "__main__":
    unittest.main()
