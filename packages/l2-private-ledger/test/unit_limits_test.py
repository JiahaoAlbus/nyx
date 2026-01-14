import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "l2-private-ledger" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from l2_private_ledger.actions import ActionKind, LedgerAction, PrivateMint  # noqa: E402
from l2_private_ledger.errors import ValidationError  # noqa: E402
from l2_private_ledger.proof_wiring import (  # noqa: E402
    build_public_inputs,
    compute_action_hash,
    validate_public_inputs_shape,
)
from l2_private_ledger.state import empty_state, state_root  # noqa: E402
from l2_private_ledger.types import sha256  # noqa: E402


class PublicInputLimitTests(unittest.TestCase):
    def test_depth_limit_rejected(self):
        commitment = sha256(b"limit-commitment")
        action = LedgerAction(ActionKind.PRIVATE_MINT, PrivateMint(commitment))
        root = state_root(empty_state())
        action_hash = compute_action_hash(action)
        public_inputs = build_public_inputs(root, action, action_hash)
        nested = []
        for _ in range(25):
            nested = [nested]
        public_inputs["extra"] = nested
        with self.assertRaises(ValidationError):
            validate_public_inputs_shape(public_inputs)

    def test_size_limit_rejected(self):
        commitment = sha256(b"limit-commitment-2")
        action = LedgerAction(ActionKind.PRIVATE_MINT, PrivateMint(commitment))
        root = state_root(empty_state())
        action_hash = compute_action_hash(action)
        public_inputs = build_public_inputs(root, action, action_hash)
        public_inputs["extra"] = "a" * 70000
        with self.assertRaises(ValidationError):
            validate_public_inputs_shape(public_inputs)

    def test_illegal_type_rejected(self):
        commitment = sha256(b"limit-commitment-3")
        action = LedgerAction(ActionKind.PRIVATE_MINT, PrivateMint(commitment))
        root = state_root(empty_state())
        action_hash = compute_action_hash(action)
        public_inputs = build_public_inputs(root, action, action_hash)
        public_inputs["payload"] = {"commitment": b"bad"}
        with self.assertRaises(ValidationError):
            validate_public_inputs_shape(public_inputs)


if __name__ == "__main__":
    unittest.main()
