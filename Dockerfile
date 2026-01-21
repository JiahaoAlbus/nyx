FROM python:3.11-slim

WORKDIR /app
COPY . /app

ENV PYTHONPATH="/app/apps/reference-ui-backend/src:/app/packages/e2e-private-transfer/src:/app/packages/l2-private-ledger/src:/app/packages/l0-zk-id/src:/app/packages/l2-economics/src:/app/packages/l1-chain/src:/app/packages/wallet-kernel/src"

EXPOSE 8080

CMD ["python", "-m", "nyx_reference_ui_backend.server"]
