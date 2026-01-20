from __future__ import annotations

import argparse
import sys

from nyx_evidence_cli.app import EvidenceError, run_and_write_evidence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NYX Q7 evidence CLI")
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--out-dir", default="q7_evidence")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        bundle = run_and_write_evidence(seed=args.seed, out_dir=args.out_dir)
    except EvidenceError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    sys.stdout.write(bundle.stdout_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
