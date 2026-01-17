# Security Disclosure Process

## Purpose
Define the disclosure process for Q5 security reports.

## Scope
- Router v1, reference client v1, and DEX v0 invariants.

## Non-Scope
- Third-party infrastructure and external systems.

## MUST
- Reports MUST include deterministic reproduction steps.
- Reports MUST include evidence and affected invariants.
- Fixes MUST include regression tests or drills.
- Reports MUST include the evidence bundle fields defined in `docs/BUG_BOUNTY_PROGRAM.md`.

## MUST NOT
- Do not publish unpatched vulnerabilities.
- Do not include secret material in reports.

## Timeline
- Acknowledge within 2 business days.
- Triage within 5 business days.
- Remediation plan within 10 business days for Critical and High issues.
- Coordinated disclosure window by mutual agreement after fix validation.

## Evidence / Verification
- Use `docs/AUDIT_REPRO_COMMANDS.md` for reproduction.
- Provide minimal input data and outputs.

## Freeze & Change Control
- Changes follow `docs/CHANGE_CONTROL.md`.
