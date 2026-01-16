from __future__ import annotations

import hashlib
import hmac
import json
import random
from pathlib import Path
from typing import Iterable

from l3_dex.actions import Swap as DexSwap
from l3_router.actions import RouteSwap

from nyx_reference_client.models import ClientConfig, ClientReport, ClientSummary, RouteStepView

_MAX_STEPS = 8
_MAX_DEPTH = 20
_MAX_BYTES = 65536


class ClientError(ValueError):
    pass


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _framed(parts: Iterable[bytes]) -> bytes:
    out = bytearray()
    for part in parts:
        out.extend(len(part).to_bytes(4, "big"))
        out.extend(part)
    return bytes(out)


def _assert_json_types(value, depth: int = 0) -> None:
    if depth > _MAX_DEPTH:
        raise ClientError("max depth exceeded")
    if value is None or isinstance(value, str) or isinstance(value, bool):
        return
    if isinstance(value, int) and not isinstance(value, bool):
        return
    if isinstance(value, list) or isinstance(value, tuple):
        for item in value:
            _assert_json_types(item, depth + 1)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ClientError("dict keys must be str")
            _assert_json_types(item, depth + 1)
        return
    raise ClientError("unsupported type")


def _canonical_bytes(value) -> bytes:
    _assert_json_types(value)
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    data = raw.encode("utf-8")
    if len(data) > _MAX_BYTES:
        raise ClientError("max bytes exceeded")
    return data


def _build_route(seed: int, steps: int) -> tuple[RouteStepView, ...]:
    rng = random.Random(seed)
    route_steps: list[RouteStepView] = []
    for idx in range(steps):
        pool_id = f"pool-{idx}"
        asset_in = "ASSET_A" if idx % 2 == 0 else "ASSET_B"
        amount_in = rng.randint(1, 1000)
        min_out = 0
        route_steps.append(
            RouteStepView(
                pool_id=pool_id,
                asset_in=asset_in,
                amount_in=amount_in,
                min_out=min_out,
            )
        )
    return tuple(route_steps)


def _route_to_actions(steps: tuple[RouteStepView, ...]) -> RouteSwap:
    swaps = tuple(
        DexSwap(
            pool_id=step.pool_id,
            amount_in=step.amount_in,
            min_out=step.min_out,
            asset_in=step.asset_in,
        )
        for step in steps
    )
    return RouteSwap(steps=swaps)


def _state_hash(steps: tuple[RouteStepView, ...]) -> bytes:
    payload = {
        "v": 1,
        "steps": [step.to_dict() for step in steps],
    }
    return _sha256(_canonical_bytes(payload))


def _receipt_chain_hash(steps: tuple[RouteStepView, ...]) -> bytes:
    receipt_hashes: list[bytes] = []
    for step in steps:
        payload = {
            "pool_id": step.pool_id,
            "asset_in": step.asset_in,
            "amount_in": step.amount_in,
            "min_out": step.min_out,
        }
        receipt_hashes.append(_sha256(_canonical_bytes(payload)))
    return _sha256(_framed(receipt_hashes))


def replay_and_verify(report: ClientReport) -> bool:
    state_hash = _state_hash(report.steps)
    receipt_hash = _receipt_chain_hash(report.steps)
    return hmac.compare_digest(state_hash, bytes.fromhex(report.state_hash_hex)) and hmac.compare_digest(
        receipt_hash, bytes.fromhex(report.receipt_chain_hex)
    )


def run_client(seed: int, out_path: str, steps: int = 2) -> ClientSummary:
    if steps < 1 or steps > _MAX_STEPS:
        raise ClientError("steps out of bounds")
    config = ClientConfig(seed=seed, steps=steps, out_path=out_path)
    route_steps = _build_route(config.seed, config.steps)
    _route_to_actions(route_steps)

    state_hash = _state_hash(route_steps)
    receipt_hash = _receipt_chain_hash(route_steps)

    report = ClientReport(
        steps=route_steps,
        state_hash_hex=state_hash.hex(),
        receipt_chain_hex=receipt_hash.hex(),
    )

    replay_ok = replay_and_verify(report)
    out_file = Path(config.out_path)
    out_file.write_text(
        json.dumps(report.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=True),
        encoding="utf-8",
    )

    return ClientSummary(
        state_hash_hex=report.state_hash_hex,
        receipt_chain_hex=report.receipt_chain_hex,
        replay_ok=replay_ok,
    )
