import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "e2e-private-transfer" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

TOKENS = ["debug", "shortcut", "temporary"]


class NoShortcutTokenTests(unittest.TestCase):
    def test_no_debug_tokens_in_src(self):
        for path in SRC_DIR.rglob("*.py"):
            content = path.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(content.splitlines(), start=1):
                lower = line.lower()
                for token in TOKENS:
                    if token in lower:
                        self.fail(f"token '{token}' found at {path}:{line_no}")


if __name__ == "__main__":
    unittest.main()
