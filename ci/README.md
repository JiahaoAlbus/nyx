CI Placeholders and Policies

This repository runs a minimal CI surface while the implementation stack is still small.
The build, test, and lint jobs now validate the L0 identity skeleton and remain minimal.

Build/Test/Lint
- Build runs Python compile checks for packages/l0-identity/src.
- Test runs the L0 identity unittest suite in packages/l0-identity/test.
- Lint runs Python compile checks for packages/l0-identity/test until a linter is selected.

Placeholder controls
- ci/force-fail-build: forces Build to fail
- ci/force-fail-test: forces Test to fail
- ci/force-fail-lint: forces Lint to fail
- ci/force-fail-sast: forces SAST to fail
- ci/force-fail-deps: forces Dependency Scan to fail

Supply-chain posture
- All GitHub Actions are pinned to commit SHA.
- SAST uses GitHub CodeQL for Python.
- Dependency review runs on PRs; placeholder SARIF remains until package manifests exist.

TODO before production
- Replace compile-based checks with real build and lint tooling.
- Add package manifests and real dependency scanning (e.g., lockfiles).
- Expand CodeQL coverage as the codebase grows.
- Update cache strategy and keys to match the chosen build system.
