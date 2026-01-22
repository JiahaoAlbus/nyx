import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
PKG_PATHS = [
    SRC,
    ROOT.parents[1] / "packages" / "e2e-private-transfer" / "src",
    ROOT.parents[1] / "packages" / "l2-private-ledger" / "src",
    ROOT.parents[1] / "packages" / "l0-zk-id" / "src",
    ROOT.parents[1] / "packages" / "l2-economics" / "src",
    ROOT.parents[1] / "packages" / "l2-platform-fee" / "src",
    ROOT.parents[1] / "packages" / "l1-chain" / "src",
    ROOT.parents[1] / "packages" / "wallet-kernel" / "src",
]
for path in PKG_PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from nyx_backend.evidence import (  # noqa: E402
    EvidenceError,
    EvidencePayload,
    _safe_artifact_path,
    run_evidence,
    verify_evidence_payload,
)


class EvidenceTamperGuardTests(unittest.TestCase):
    def test_tamper_state_hash_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            payload = run_evidence(
                seed=123,
                run_id="tamper-1",
                module="exchange",
                action="route_swap",
                payload={"route": "basic"},
                base_dir=base_dir,
            )
            outputs = dict(payload.outputs)
            outputs["state_hash"] = "00" * 16
            tampered = EvidencePayload(
                protocol_anchor=payload.protocol_anchor,
                inputs=payload.inputs,
                outputs=outputs,
                receipt_hashes=payload.receipt_hashes,
                state_hash=payload.state_hash,
                replay_ok=payload.replay_ok,
                stdout=payload.stdout,
            )
            with self.assertRaises(EvidenceError):
                verify_evidence_payload(tampered)

    def test_tamper_receipt_hashes_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            payload = run_evidence(
                seed=123,
                run_id="tamper-2",
                module="exchange",
                action="route_swap",
                payload={"route": "basic"},
                base_dir=base_dir,
            )
            outputs = dict(payload.outputs)
            outputs["receipt_hashes"] = ["deadbeef"]
            tampered = EvidencePayload(
                protocol_anchor=payload.protocol_anchor,
                inputs=payload.inputs,
                outputs=outputs,
                receipt_hashes=payload.receipt_hashes,
                state_hash=payload.state_hash,
                replay_ok=payload.replay_ok,
                stdout=payload.stdout,
            )
            with self.assertRaises(EvidenceError):
                verify_evidence_payload(tampered)

    def test_artifact_name_rejects_path_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            _ = run_evidence(
                seed=123,
                run_id="safe-1",
                module="exchange",
                action="route_swap",
                payload={"route": "basic"},
                base_dir=base_dir,
            )
            with self.assertRaises(EvidenceError):
                _ = _safe_artifact_path(base_dir, "safe-1", "../x")


if __name__ == "__main__":
    unittest.main()
