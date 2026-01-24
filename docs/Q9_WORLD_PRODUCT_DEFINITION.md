# Q9 World Product Definition

## Purpose
Define what the NYX world product is and is not for Q9 Testnet, as a normative baseline for execution.

## Scope
This document governs Q9 Testnet product behavior, UI copy constraints, and feature boundaries.

## Non-Scope
Protocol semantics, evidence format v1, and replay rules are sealed and MUST NOT change.

## Definitions
- NYX World: A single product surface containing exchange, marketplace, chat, and entertainment flows under NYX rules.
- Testnet Alpha: A deterministic, non-mainnet environment intended for verifiable execution only.

## Normative Rules (MUST / MUST NOT)
- The product MUST behave as a real, stateful testnet environment with actual state changes.
- The product MUST NOT claim mainnet operation, live network status, or real market data.
- The product MUST NOT include login, signup, or external wallet connect flows.
- The product MUST require explicit seed input for deterministic runs.
- The product MUST display evidence fields verbatim and MUST NOT compute or alter evidence fields.
- The product MUST label all flows as Testnet Alpha.
- The product MUST NOT embed secrets or sensitive materials in UI, logs, or artifacts.

## Evidence and Verification
- Canonical verification commands:
  - python -m compileall packages/l0-identity/src
  - python scripts/nyx_run_all_unittests.py
  - PYTHONPATH="packages/conformance-v1/src" python -m conformance_v1.runner --out nyx_conformance_report.json

## Freeze / Change Control
- Q1–Q8 semantics are sealed; Q9 changes are additive only.
- Any change that affects determinism or evidence format is prohibited.
