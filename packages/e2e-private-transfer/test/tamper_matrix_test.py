import copy
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


def _append_case(cases: list[dict], base: dict, mutator) -> None:
    payload = copy.deepcopy(base)
    mutator(payload)
    cases.append(payload)


def _tamper_hex_field(cases: list[dict], base: dict, path: tuple[str, ...]) -> None:
    def get_ref(payload: dict) -> dict:
        node = payload
        for key in path[:-1]:
            node = node[key]
        return node

    def flip(payload: dict) -> None:
        node = get_ref(payload)
        node[path[-1]] = _flip_hex_byte(node[path[-1]])

    def truncate(payload: dict) -> None:
        node = get_ref(payload)
        node[path[-1]] = _truncate_hex(node[path[-1]])

    def swap(payload: dict) -> None:
        node = get_ref(payload)
        node[path[-1]] = _swap_hex_halves(node[path[-1]])

    for mutator in (flip, truncate, swap):
        _append_case(cases, base, mutator)


def _tamper_fee_components(cases: list[dict], base: dict) -> None:
    def flip(payload: dict) -> None:
        components = payload["fee"]["components"]
        components[0]["amount"] = int(components[0]["amount"]) + 1

    def truncate(payload: dict) -> None:
        components = payload["fee"]["components"]
        payload["fee"]["components"] = components[:-1]

    def swap(payload: dict) -> None:
        components = payload["fee"]["components"]
        if len(components) >= 2:
            components[0]["component"], components[1]["component"] = (
                components[1]["component"],
                components[0]["component"],
            )
        else:
            components[0]["component"] = "compute"

    for mutator in (flip, truncate, swap):
        _append_case(cases, base, mutator)


class TamperMatrixTests(unittest.TestCase):
    def test_tamper_matrix(self):
        trace, _ = run_private_transfer(seed=123)
        base = trace.to_dict()

        cases: list[dict] = []

        _tamper_hex_field(cases, base, ("proof", "proof_bytes_hex"))
        _tamper_hex_field(cases, base, ("proof", "binding_tag_hex"))
        _tamper_fee_components(cases, base)
        _tamper_hex_field(cases, base, ("fee", "receipt_hash_hex"))
        _tamper_hex_field(cases, base, ("chain", "payload_hex"))

        for index, payload_case in enumerate(cases):
            with self.subTest(index=index):
                try:
                    tampered = TransferTrace.from_dict(payload_case)
                    result = replay_and_verify(tampered)
                except Exception:
                    result = False
                self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
