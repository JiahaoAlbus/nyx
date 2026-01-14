import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "conformance-v1" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from conformance_v1.drills import run_drills  # noqa: E402


class RuntimeDrillV2Tests(unittest.TestCase):
    def test_v2_drills_present_and_pass(self):
        results = {result.rule_id: result for result in run_drills()}
        required = ("Q3-RT-01", "Q3-RT-02", "Q3-RT-03", "Q3-RT-04")
        for rule_id in required:
            self.assertIn(rule_id, results)
            self.assertTrue(results[rule_id].passed, msg=f"{rule_id} failed")


if __name__ == "__main__":
    unittest.main()
