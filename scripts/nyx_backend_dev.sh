#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
VENV_DIR="$ROOT/.venv"

if [ "${NYX_DEV_NO_VENV:-}" != "1" ]; then
  if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_BIN" -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
fi

export PYTHONPATH="$ROOT/apps/nyx-backend-gateway/src:$ROOT/apps/nyx-backend/src"

ENV_FILE="$ROOT/.env.example"
if [ -f "$ROOT/cswdz.env" ]; then
  ENV_FILE="$ROOT/cswdz.env"
fi

HOST="${NYX_DEV_HOST:-127.0.0.1}"
PORT="${NYX_DEV_PORT:-8091}"

"$PYTHON_BIN" -m nyx_backend_gateway.server --host "$HOST" --port "$PORT" --env-file "$ENV_FILE" &
SERVER_PID=$!

python - <<'PY'
import socket
import sys
import time

import os

host = os.environ.get("NYX_DEV_HOST", "127.0.0.1")
port = int(os.environ.get("NYX_DEV_PORT", "8091"))

deadline = time.time() + 10
while time.time() < deadline:
    sock = socket.socket()
    try:
        sock.settimeout(0.2)
        sock.connect((host, port))
        sock.close()
        sys.exit(0)
    except OSError:
        time.sleep(0.2)

sys.exit(1)
PY

if [ $? -ne 0 ]; then
  echo "Backend failed to bind to ${HOST}:${PORT}" >&2
  kill "$SERVER_PID" >/dev/null 2>&1 || true
  exit 1
fi

echo "READY http://${HOST}:${PORT}"
wait "$SERVER_PID"
