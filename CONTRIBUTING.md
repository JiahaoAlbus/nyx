# Contributing to NYX

Thank you for improving the NYX engineering foundation. This repository prioritizes auditability, safety, and long-term maintainability.

## Language and PR naming
- PR titles must be in English and follow the format: type(scope): concise summary.
- PR descriptions must start with an English summary that includes Purpose, Deliverables, and Verification.
- Optional: provide Chinese details after the English summary if helpful.

## Scope boundaries
- Do not introduce business implementation code unless explicitly approved for the current milestone.
- Respect the L0-L4 layering in packages/ and avoid cross-layer dependencies.

## Conformance and frozen rules
- frozen/q1 is the single authoritative location for Q1 frozen artifacts.
- Changes to frozen artifacts require break-glass approval and must be documented.
- Conformance runs from conformance/run.sh and must remain backwards compatible.

## CI expectations
- Placeholder jobs must be replaced before real product code lands.
- Use ci/force-fail-* files to validate CI gates intentionally.

## Submitting changes
1. Create a branch with a descriptive name.
2. Update or add documentation when changing policies or guardrails.
3. Ensure CI passes and the PR includes red-team verification steps.