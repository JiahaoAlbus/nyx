#!/usr/bin/env bash
set -euo pipefail

echo "[conformance] NYX frozen-rules gate running..."

# Simple grep-based gate (starter). Evolve into executable conformance tests in Q2.
FORBIDDEN_PATTERNS='
wallet[[:space:]]*=[[:space:]]*identity
wallet.*identity
identity.*wallet
admin.*bypass
privileged.*bypass
fee.*exempt
support override
'

# IMPORTANT: Do NOT scan documentation dirs to avoid false positives.
# Only scan implementation-adjacent dirs.
TARGET_DIRS=".github tooling packages"

for d in $TARGET_DIRS; do
  if [ -d "$d" ]; then
    echo "[conformance] scanning $d"
    echo "$FORBIDDEN_PATTERNS" | while IFS= read -r re; do
      [ -z "$re" ] && continue
     if grep -RIn --exclude-dir=.git --exclude-dir=node_modules --exclude="tooling/scripts/conformance.sh" -E "$re" "$d" >/dev/null 2>&1; then
        echo "[conformance] FAIL: forbidden pattern detected: $re in $d"
        grep -RIn --exclude-dir=.git --exclude-dir=node_modules --exclude="tooling/scripts/conformance.sh" -E "$re" "$d" || true
        exit 1
      fi
    done
  fi
done

echo "[conformance] OK"
