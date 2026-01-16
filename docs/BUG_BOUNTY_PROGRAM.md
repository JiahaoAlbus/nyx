# Bug Bounty Program

## Purpose
Define scope, safe-harbor boundaries, and evidence requirements for Q5.

## Scope
- Router v1 and reference client v1.
- DEX v0 invariants and receipt replay integrity.

## Non-Scope
- Production bridge or on/off implementations.
- External infrastructure outside this repository.

## MUST
- Submissions MUST include deterministic reproduction steps.
- Evidence MUST include command output and hashes.
- Report MUST specify impacted invariant and scope.
- Reports MUST include an evidence bundle with fields: report_id, summary, severity, repro_steps, evidence, environment.

## MUST NOT
- Do not include secrets or sensitive materials in reports.
- Do not test against third-party systems.
- Do not claim safe-harbor protection outside the scope defined here.

## SLA / Response Windows
- Acknowledge within 2 business days.
- Triage within 5 business days.
- Fix plan within 10 business days for Critical and High issues.

## Safe Harbor
- In-scope testing per this document is permitted.
- Out-of-scope targets are not covered.

## Evidence / Verification
- Use commands in `docs/AUDIT_REPRO_COMMANDS.md`.
- Provide failing output excerpts and minimal inputs.

## Freeze & Change Control
- Changes follow `docs/CHANGE_CONTROL.md`.
