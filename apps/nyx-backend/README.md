# NYX Ecosystem Backend (Week 03)

Purpose
- Provide a deterministic gateway for Q8 ecosystem modules.

Scope
- Evidence generation and export for module actions.
- Deterministic run storage and artifact delivery.

Non-Scope
- Protocol semantics changes.
- Accounts, identity, or wallet features.
- Live operational metrics.

Run (Dev)
```
PYTHONPATH="apps/nyx-backend/src:packages/e2e-private-transfer/src:packages/l2-private-ledger/src:packages/l0-zk-id/src:packages/l2-economics/src:packages/l1-chain/src:packages/wallet-kernel/src" \
  python -m nyx_backend.server
```

Endpoints
- POST /run
- GET /status?run_id=...
- GET /evidence?run_id=...
- GET /artifact?run_id=...&name=...
- GET /export.zip?run_id=...
- GET /list

Notes
- Evidence fields are returned verbatim and exported deterministically.
