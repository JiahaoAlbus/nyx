from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Iterable

from e2e_private_transfer.pipeline import run_private_transfer
from e2e_private_transfer.replay import replay_and_verify


class EvidenceError(ValueError):
    pass


@dataclass(frozen=True)
class EvidenceOutputs:
    state_hash: str
    receipt_hashes: list[str]
    replay_ok: bool


@dataclass(frozen=True)
class EvidenceBundle:
    protocol_anchor: dict[str, str]
    inputs: dict[str, object]
    outputs: EvidenceOutputs
    stdout_text: str
    out_dir: Path


def _json_dumps(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _run_git(args: Iterable[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _protocol_anchor() -> dict[str, str]:
    commit = _run_git(["rev-parse", "HEAD"])
    describe = _run_git(["describe", "--tags", "--always"])
    tags_raw = _run_git(["tag", "--points-at", "HEAD"])
    tags = sorted([t for t in tags_raw.splitlines() if t.strip()])
    tag = tags[0] if tags else ""
    return {
        "tag": tag,
        "commit": commit,
        "describe": describe,
    }


def _format_stdout(outputs: EvidenceOutputs) -> str:
    receipt_join = ",".join(outputs.receipt_hashes)
    replay_text = "true" if outputs.replay_ok else "false"
    lines = [
        "NYX Q7 Evidence CLI",
        f"state_hash={outputs.state_hash}",
        f"receipt_hashes={receipt_join}",
        f"replay_ok={replay_text}",
        "",
    ]
    return "\n".join(lines)


def _validate_seed(seed: int) -> None:
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise EvidenceError("seed must be int")


def run_and_write_evidence(seed: int, out_dir: str) -> EvidenceBundle:
    _validate_seed(seed)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    trace, _ = run_private_transfer(seed=seed)
    replay_ok = replay_and_verify(trace)

    receipt_hashes = [
        trace.fee.receipt_hash_hex,
        trace.chain.tx_hash_hex,
        trace.chain.block_hash_hex,
    ]
    outputs = EvidenceOutputs(
        state_hash=trace.chain.state_root_after_hex,
        receipt_hashes=receipt_hashes,
        replay_ok=replay_ok,
    )
    if not outputs.replay_ok:
        raise EvidenceError("replay verification failed")

    protocol_anchor = _protocol_anchor()
    inputs = {"seed": seed}

    stdout_text = _format_stdout(outputs)

    _write_text(out_path / "protocol_anchor.json", _json_dumps(protocol_anchor))
    _write_text(out_path / "inputs.json", _json_dumps(inputs))
    _write_text(
        out_path / "outputs.json",
        _json_dumps(
            {
                "state_hash": outputs.state_hash,
                "receipt_hashes": outputs.receipt_hashes,
                "replay_ok": outputs.replay_ok,
            }
        ),
    )
    _write_text(out_path / "receipt_hashes.json", _json_dumps(outputs.receipt_hashes))
    _write_text(out_path / "state_hash.txt", outputs.state_hash + "\n")
    _write_text(out_path / "replay_ok.txt", ("true" if outputs.replay_ok else "false") + "\n")
    _write_text(out_path / "stdout.txt", stdout_text)

    return EvidenceBundle(
        protocol_anchor=protocol_anchor,
        inputs=inputs,
        outputs=outputs,
        stdout_text=stdout_text,
        out_dir=out_path,
    )
