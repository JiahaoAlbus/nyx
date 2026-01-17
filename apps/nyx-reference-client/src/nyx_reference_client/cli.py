from __future__ import annotations

import argparse

from nyx_reference_client.app import run_client


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NYX reference client")
    parser.add_argument("--seed", type=int, default=123, help="Deterministic seed")
    parser.add_argument("--steps", type=int, default=2, help="Route step count")
    parser.add_argument("--out", required=True, help="Report output path")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    summary = run_client(seed=args.seed, out_path=args.out, steps=args.steps)
    print(
        "summary:"
        f" state_hash={summary.state_hash_hex}"
        f" receipt_chain={summary.receipt_chain_hex}"
        f" replay_ok={summary.replay_ok}"
    )


if __name__ == "__main__":
    main()
