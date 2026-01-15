# Testnet 0.2 Runbook

## Prereqs
- Python 3.x
- Repository checked out at the intended tag or branch

## CI-Equivalent Gate
```bash
python -m compileall packages/l0-identity/src
python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v
```

## Private Transfer Demo
```bash
PYTHONPATH="packages/e2e-private-transfer/src:packages/l2-private-ledger/src:packages/l0-zk-id/src:packages/l2-economics/src:packages/l1-chain/src:packages/wallet-kernel/src" \
  python -m e2e_private_transfer.run_demo --out /tmp/nyx_q3_w5_trace.json --seed 123
```
Expected output includes:
- fee_total
- tx_hash (prefix)
- block_hash (prefix)
- state_root (prefix)
- receipt_hash (prefix)
- replay_ok=True

## Determinism Check
Run the demo twice with the same seed and compare the hash prefixes.

## Conformance Runner
```bash
PYTHONPATH="packages/conformance-v1/src" \
  python -m conformance_v1.runner --out /tmp/nyx_conformance_v2_report.json
```

## Boundaries
- Mock proof systems are for testnet only.
- This runbook validates invariants and replayability, not production crypto.
