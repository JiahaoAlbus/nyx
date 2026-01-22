# Q8 Go / No-Go Checklist

Purpose
- Provide objective gating for Q8 release candidate readiness.

Scope
- Q8 ecosystem web portal, backend gateway, and reference iOS client.

Non-Scope
- Protocol semantic changes, bridge execution, or on/off ramp execution.

Go Criteria (Must all be satisfied)
- Canonical verification commands pass:
  - python -m compileall packages/l0-identity/src
  - python scripts/nyx_run_all_unittests.py
  - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
- One-shot reproducibility script passes:
  - python scripts/q8_repro_one_shot.py
- Evidence bundle fields and ordering match v1 contract.
- UI copy guard passes (no account or live status semantics).

No-Go Criteria (Any one is sufficient)
- Any failed unit test or conformance drill.
- Any evidence field missing or reordered.
- Any path traversal regression or artifact access bypass.
- Any UI copy introduces account, wallet, or live system claims.

Tagging (Maintainer Commands)
- git tag -a q8-rc1 -m "NYX Q8 RC1"
- git push origin q8-rc1

Freeze and Change Control
- If any criteria are not met, tag is deferred and remediation must be documented.
