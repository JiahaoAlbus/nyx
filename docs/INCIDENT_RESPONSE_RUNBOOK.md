# INCIDENT_RESPONSE_RUNBOOK

## Purpose
Define the incident response process for DEX v0 and conformance failures.

## Scope
- Security incidents affecting replay, receipts, or fee enforcement.
- Conformance drill failures that indicate invariant regressions.

## Non-Scope
- Production operations for external bridges or ramps.
- Operational uptime guarantees.

## Invariants/Rules
- Any suspected invariant breach MUST trigger immediate triage.
- Do not publish sensitive material in logs or incident notes.
- Remediation MUST include a regression test or drill.

## Evidence/Verification
- Preserve failing test output and conformance report JSON.
- Record exact commit hash and reproduction command.

## Response Phases
1) Detect
   - Capture logs and failing command output.
2) Triage
   - Identify invariant impacted and scope of effect.
3) Contain
   - Disable affected demo flow if needed (documentation only).
4) Eradicate
   - Apply patch-only fix and add regression test.
5) Recover
   - Re-run full suite and conformance runner.
6) Post-Incident
   - Update audit pack findings and mitigations.

## Freeze/Change Control
- Follow `docs/CHANGE_CONTROL.md` for any post-freeze updates.
