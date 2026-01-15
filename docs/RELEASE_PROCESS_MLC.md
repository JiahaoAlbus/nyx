# RELEASE_PROCESS_MLC

## Purpose
Define the release process for MLC (DEX v0) with objective gates.

## Scope
- Release candidate tagging.
- Mainnet tagging if and only if checklist is Go.
- Evidence collection for audit and release notes.

## Non-Scope
- Production deployment automation.
- External bridge or on/off integrations.

## Invariants/Rules
- All release actions MUST be based on a clean main branch.
- Any failed gate MUST stop the release.
- Patch-only fixes require a regression test or drill.

## Evidence/Verification
Canonical commands:

```
python -m compileall packages/l0-identity/src
python -m unittest discover -s packages/l0-identity/test -p "*_test.py" -v
```

Conformance report:

```
PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out /tmp/nyx_conformance_report.json
```

## Tagging (Maintainer Action)
Release candidate:

```
git tag -a mlc-1.0-rc1 -m "NYX MLC 1.0 RC1"
git push origin mlc-1.0-rc1
gh release create mlc-1.0-rc1 -t "NYX MLC 1.0 RC1" -n "Release candidate"
```

Mainnet (Go only):

```
git tag -a mainnet-1.0 -m "NYX Mainnet 1.0"
git push origin mainnet-1.0
gh release create mainnet-1.0 -t "NYX Mainnet 1.0" -n "Mainnet release"
```

## Freeze/Change Control
- Follow `docs/CHANGE_CONTROL.md`.
- After freeze: patch-only or additive extensions only.
