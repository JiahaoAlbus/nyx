import re
import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
PATHS = [
    REPO_ROOT / "packages" / "e2e-demo" / "src",
    REPO_ROOT / "packages" / "l0-zk-id" / "src",
    REPO_ROOT / "packages" / "l2-economics" / "src",
    REPO_ROOT / "packages" / "l1-chain" / "src",
    REPO_ROOT / "packages" / "wallet-kernel" / "src",
]
for path in PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from e2e_demo.hashing import sha256  # noqa: E402
from e2e_demo.pipeline import run_e2e  # noqa: E402
import wallet_kernel  # noqa: E402


class HardeningGuardTests(unittest.TestCase):
    def test_trace_meta_present(self):
        trace, _ = run_e2e(seed=123)
        self.assertEqual(trace.meta.trace_version, "e2e-trace/v1")
        self.assertTrue(trace.meta.repo_head)
        self.assertIn("not production crypto", trace.meta.note)
        self.assertIn("l0-zk-id", trace.meta.components)

    def test_sender_not_identity(self):
        seed = 123
        trace, _ = run_e2e(seed=seed)
        root_secret = sha256(b"NYX:W7:ROOT:" + str(seed).encode("ascii"))
        expected_commitment = sha256(b"NYX:IDENTITY:COMMITMENT:v1" + root_secret)
        self.assertEqual(trace.identity.commitment_hex, expected_commitment.hex())
        self.assertNotEqual(trace.chain.sender, trace.identity.commitment_hex)
        identity_input = trace.proof.public_inputs.get("identity_commitment", "")
        self.assertNotIn(trace.chain.sender, identity_input)

    def test_wallet_kernel_verify_only(self):
        for name in dir(wallet_kernel):
            self.assertNotIn("prove", name.lower())
        src_dir = REPO_ROOT / "packages" / "e2e-demo" / "src" / "e2e_demo"
        pattern = re.compile(r"wallet_kernel\.\w*prove", re.IGNORECASE)
        for path in src_dir.rglob("*.py"):
            content = path.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(pattern.search(content), msg=f"prove via wallet_kernel in {path}")


if __name__ == "__main__":
    unittest.main()
