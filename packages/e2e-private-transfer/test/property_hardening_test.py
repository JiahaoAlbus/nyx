import copy
import os
import random
import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "e2e-private-transfer" / "src"
PL_SRC = REPO_ROOT / "packages" / "l2-private-ledger" / "src"
ZK_SRC = REPO_ROOT / "packages" / "l0-zk-id" / "src"
ECON_SRC = REPO_ROOT / "packages" / "l2-economics" / "src"
CHAIN_SRC = REPO_ROOT / "packages" / "l1-chain" / "src"
KERNEL_SRC = REPO_ROOT / "packages" / "wallet-kernel" / "src"
for path in (SRC_DIR, PL_SRC, ZK_SRC, ECON_SRC, CHAIN_SRC, KERNEL_SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from e2e_private_transfer.pipeline import run_private_transfer  # noqa: E402
from e2e_private_transfer.replay import replay_and_verify  # noqa: E402
from e2e_private_transfer.trace import TransferTrace  # noqa: E402

PROPERTY_N = int(os.environ.get("PROPERTY_N", "2000"))


def _flip_hex_byte(hex_value: str) -> str:
    data = bytearray(bytes.fromhex(hex_value))
    data[0] ^= 0x01
    return bytes(data).hex()


def _truncate_hex(hex_value: str) -> str:
    if len(hex_value) <= 2:
        return hex_value
    return hex_value[:-2]


def _swap_hex_halves(hex_value: str) -> str:
    mid = len(hex_value) // 2
    return hex_value[mid:] + hex_value[:mid]


def _apply_hex_tamper(payload: dict, path: tuple[str, ...], tamper) -> None:
    node = payload
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = tamper(node[path[-1]])


def _tamper_fee(payload: dict, mode: str) -> None:
    components = payload["fee"]["components"]
    if mode == "flip":
        components[0]["amount"] = int(components[0]["amount"]) + 1
    elif mode == "truncate":
        payload["fee"]["components"] = components[:-1]
    else:
        if len(components) >= 2:
            components[0]["component"], components[1]["component"] = (
                components[1]["component"],
                components[0]["component"],
            )
        else:
            components[0]["component"] = "compute"


def _tamper_payload(payload: dict, rng: random.Random) -> None:
    target = rng.choice(
        [
            "proof_bytes",
            "binding_tag",
            "receipt_hash",
            "payload_hex",
            "fee",
        ]
    )
    mode = rng.choice(["flip", "truncate", "swap"])
    if target == "proof_bytes":
        _apply_hex_tamper(payload, ("proof", "proof_bytes_hex"), _flip_hex_byte if mode == "flip" else (_truncate_hex if mode == "truncate" else _swap_hex_halves))
    elif target == "binding_tag":
        _apply_hex_tamper(payload, ("proof", "binding_tag_hex"), _flip_hex_byte if mode == "flip" else (_truncate_hex if mode == "truncate" else _swap_hex_halves))
    elif target == "receipt_hash":
        _apply_hex_tamper(payload, ("fee", "receipt_hash_hex"), _flip_hex_byte if mode == "flip" else (_truncate_hex if mode == "truncate" else _swap_hex_halves))
    elif target == "payload_hex":
        _apply_hex_tamper(payload, ("chain", "payload_hex"), _flip_hex_byte if mode == "flip" else (_truncate_hex if mode == "truncate" else _swap_hex_halves))
    else:
        _tamper_fee(payload, mode)


class PropertyHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print(f"PROPERTY_N={PROPERTY_N}")

    def test_random_tamper_replay_fails(self):
        trace, _ = run_private_transfer(seed=123)
        base = trace.to_dict()
        rng = random.Random(2024)
        for _ in range(PROPERTY_N):
            payload = copy.deepcopy(base)
            _tamper_payload(payload, rng)
            try:
                tampered = TransferTrace.from_dict(payload)
                result = replay_and_verify(tampered)
            except Exception:
                result = False
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
