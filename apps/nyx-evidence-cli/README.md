# NYX Evidence CLI (Q7 Reference)

## Purpose
Generate a deterministic evidence bundle that conforms to Q7 Evidence Format v1.

## Scope
This CLI is a text-only reference tool. It does not implement any UI.

## Usage
```
PYTHONPATH="apps/nyx-evidence-cli/src:packages/e2e-private-transfer/src:packages/l2-private-ledger/src:packages/l0-zk-id/src:packages/l2-economics/src:packages/l1-chain/src:packages/wallet-kernel/src" \
  python -m nyx_evidence_cli.cli --seed 123 --out-dir /tmp/nyx_q7_evidence
```

## Outputs
The output directory contains the required evidence files defined in Q7 Evidence Format v1.
