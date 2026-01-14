import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
ZK_SRC = REPO_ROOT / "packages" / "l0-zk-id" / "src"
REP_SRC = REPO_ROOT / "packages" / "l0-reputation" / "src"
if str(ZK_SRC) not in sys.path:
    sys.path.insert(0, str(ZK_SRC))
if str(REP_SRC) not in sys.path:
    sys.path.insert(0, str(REP_SRC))

from l0_reputation.disclosure_wiring import (  # noqa: E402
    STATEMENT_ID_AT_LEAST,
    build_public_inputs_at_least,
    validate_public_inputs_shape,
)
from l0_reputation.errors import ValidationError  # noqa: E402
from l0_reputation.hashing import sha256  # noqa: E402
from l0_reputation.kernel import new_pseudonym  # noqa: E402


class DisclosureLimitTests(unittest.TestCase):
    def test_depth_limit_rejected(self):
        rep_root = sha256(b"rep-limit-root")
        pseudo = new_pseudonym(sha256(b"rep-limit-secret"))
        public_inputs = build_public_inputs_at_least(rep_root, pseudo, 1)
        nested = []
        for _ in range(25):
            nested = [nested]
        public_inputs["extra"] = nested
        with self.assertRaises(ValidationError):
            validate_public_inputs_shape(public_inputs, STATEMENT_ID_AT_LEAST)

    def test_size_limit_rejected(self):
        rep_root = sha256(b"rep-limit-root-2")
        pseudo = new_pseudonym(sha256(b"rep-limit-secret-2"))
        public_inputs = build_public_inputs_at_least(rep_root, pseudo, 2)
        public_inputs["extra"] = "a" * 70000
        with self.assertRaises(ValidationError):
            validate_public_inputs_shape(public_inputs, STATEMENT_ID_AT_LEAST)

    def test_illegal_type_rejected(self):
        rep_root = sha256(b"rep-limit-root-3")
        pseudo = new_pseudonym(sha256(b"rep-limit-secret-3"))
        public_inputs = build_public_inputs_at_least(rep_root, pseudo, 3)
        public_inputs["k"] = 1.5
        with self.assertRaises(ValidationError):
            validate_public_inputs_shape(public_inputs, STATEMENT_ID_AT_LEAST)


if __name__ == "__main__":
    unittest.main()
