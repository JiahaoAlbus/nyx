# Q6 Provenance Pack

Purpose
- Record provenance evidence for Q6 release artifacts and commands.

Scope
- Artifact hashes, command outputs, and lineage references.

Non-Scope
- Any protocol change or semantic change.

MUST and MUST NOT
- Provenance MUST include deterministic hashes and command outputs.
- Provenance MUST NOT include secrets or sensitive material.

Provenance Entries
- Artifact:
- Hash:
- Source command:
- Output summary:

Evidence / Verification
- Canonical commands are listed in `docs/AUDIT_REPRO_COMMANDS.md`.

Freeze / Change Control
- Execution-only evidence; no protocol changes.
