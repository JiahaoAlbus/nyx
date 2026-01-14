# Audit Pack — Testnet 0.2 (Draft)

This pack provides a reproducible path to validate Q3 hardening work.

## Threat Model Delta (Q3)
- Private ledger actions bind proof, fee, and chain state in a single replayable trace.
- Reputation events are context-bound and deterministic under ordered replay.
- Red-team drills now cover proof omission, fee mismatch, nullifier reuse, and cross-context link attempts.

## Repro Commands
```bash
python -m compileall packages/l0-identity/src
python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v
```

```bash
PYTHONPATH="packages/e2e-private-transfer/src:packages/l2-private-ledger/src:packages/l0-zk-id/src:packages/l2-economics/src:packages/l1-chain/src:packages/wallet-kernel/src" \
  python -m e2e_private_transfer.run_demo --out /tmp/nyx_q3_w5_trace.json --seed 123
```

```bash
PYTHONPATH="packages/conformance-v1/src" \
  python -m conformance_v1.runner --out /tmp/nyx_conformance_v2_report.json
```

## Boundaries
- Mock proof system and Python reference code are not production cryptography.
- The audit focus is on invariants and replayable evidence, not performance claims.
