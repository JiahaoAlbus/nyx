# Engineering Foundation

This document describes the long-term engineering constraints for NYX.
It complements conformance, frozen rules, and CI as enforceable guardrails.

## Layer boundaries (L0-L4)
- L0: shared primitives and pure utilities.
- L1: core domain primitives and policy interfaces.
- L2: use-case orchestration and stateless services.
- L3: application composition and runtime wiring.
- L4: external integration adapters.

Rules
- Dependencies must flow downward only (L4 -> L3 -> L2 -> L1 -> L0).
- No cycles or back-propagation of privileges.

## Frozen rules engineering
- frozen/q1 is the single authoritative location for Q1 frozen artifacts.
- Any change to frozen artifacts requires explicit break-glass approval.
- CI rejects PRs that touch frozen/q1 by default.

## Conformance extension
- Add new rules under conformance/rules with stable Rule IDs.
- Update the rule mapping index to trace rules back to frozen sources.
- Conformance must run from conformance/run.sh to stay auditable.

## CI checks semantics
- Frozen Q1 Lock: rejects any PR touching frozen/q1.
- Build/Test/Lint: placeholders until build system lands; must be replaced.
- SAST/Dependency Scan: placeholder SARIF until scanners are configured.
- Conformance: rejects forbidden implementation patterns.

## PR policy
- PR titles must be English and use type(scope): summary.
- PR descriptions must start with an English summary containing Purpose, Deliverables, and Verification.
- Red-team steps are mandatory for any guardrail changes.