# Audit Checklist — Testnet 0.2

Phase 0 — Clean Room
[ ] git status must be clean
    - git status
[ ] main must be up to date
    - git checkout main && git pull
[ ] record HEAD for audit log
    - git rev-parse HEAD

Phase 1 — CI-Equivalent Gate
[ ] compile check
    - python -m compileall packages/l0-identity/src
[ ] full tests must pass
    - python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v
    PASS: output ends with "OK" and no failures

Phase 2 — Private Transfer Integrity
[ ] E2E demo reproducible (seed=123)
    - PYTHONPATH="packages/e2e-private-transfer/src:packages/l2-private-ledger/src:packages/l0-zk-id/src:packages/l2-economics/src:packages/l1-chain/src:packages/wallet-kernel/src" \
      python -m e2e_private_transfer.run_demo --out /tmp/nyx_q3_w5_trace.json --seed 123
    PASS: output includes replay_ok=True

Phase 3 — Conformance v2
[ ] conformance runner produces JSON
    - PYTHONPATH="packages/conformance-v1/src" \
      python -m conformance_v1.runner --out /tmp/nyx_conformance_v2_report.json
    PASS: exit code 0 and file present

Phase 4 — Freeze & Tag
[ ] tag on main only
    - git checkout main && git pull
[ ] create annotated tag
    - git tag -a testnet-0.2 -m "NYX Testnet 0.2"
[ ] push tag
    - git push origin testnet-0.2
[ ] optional release
    - gh release create testnet-0.2 -t "NYX Testnet 0.2" -n "<release notes summary>"

Fail Fast: any failure stops the release.
No Override: do not use temporary switches to bypass checks.
Break-Glass only: changes to frozen foundations require explicit approval.
