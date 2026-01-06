# 2026 Q2 Week 1 Plan - Engineering Foundation

Order (PRs)
1. PR-1: mono-repo skeleton (packages L0-L4 + boundary docs)
2. PR-2: frozen/q1 establishment + Q1 frozen docs migration
3. PR-3: CI protection for frozen/q1
4. PR-4: conformance/体系 + CI entrypoint switch
5. PR-5: CI pipeline v0 (build/test/lint/SAST/dep-scan/conformance)

PR-1: Mono-repo skeleton
Purpose
- Establish packages/ with L0-L4 layers and clear boundaries.
- Record Week 1 execution plan in-repo.

Deliverables
- packages/L0 through packages/L4 with boundary README.md per layer.
- docs/week1-plan.md (this document).

Acceptance (red-team)
- Verify L0-L4 directories exist and each README states responsibilities and allowed/prohibited dependencies.
- Introduce a known forbidden pattern under packages/ and confirm the conformance gate fails.

PR-2: Q1 frozen zone
Purpose
- Create a read-only mirror for Q1 frozen documents and declare authority.

Deliverables
- frozen/q1/ with migrated Q1 frozen docs and an authority README.

Acceptance (red-team)
- Ensure only frozen/q1 is treated as the authoritative location for Q1 frozen docs.
- Introduce a known forbidden pattern under tooling/ and confirm the conformance gate fails.

PR-3: CI frozen protection
Purpose
- Enforce a hard CI rule that rejects PRs editing frozen/q1.

Deliverables
- CI job that fails any PR touching frozen/q1.

Acceptance (red-team)
- Modify a file under frozen/q1 in a test PR and confirm the workflow fails.

PR-4: Conformance体系 and CI entrypoint
Purpose
- Introduce a conformance/ system of record and make CI run from it.

Deliverables
- conformance/README.md, conformance/rules/ with rule placeholders and IDs, and mapping to frozen items.
- CI conformance job uses the conformance/ entrypoint.

Acceptance (red-team)
- Add a forbidden pattern in an implementation area and confirm conformance fails via the new entrypoint.

PR-5: CI pipeline v0
Purpose
- Establish structured jobs for build, test, lint, SAST, dependency scan, and conformance.

Deliverables
- CI jobs for build/test/lint/SAST/dep-scan/conformance visible in PRs.

Acceptance (red-team)
- Force build or lint to fail (e.g., by breaking a required check) and confirm workflow fails.
- Ensure conformance still blocks forbidden patterns.