# Testnet 0.2 Invariants

## Core Separation
- Identity layer is context-bound and never derived from account or sender.
- Wallet kernel is a signing utility only; it is not a root of trust.
- Account or address has no identity semantics.

## Proof and Context
- Proofs are bound to context, statement, nonce, and public inputs.
- Any proof with wrong context or statement must fail verification.
- Nullifier reuse is forbidden and must fail deterministically.

## Fees
- State mutation requires a non-zero fee.
- Sponsorship can change payer only; amounts remain unchanged.

## Chain
- Sender and signature are chain execution inputs only.
- State roots and receipts are deterministic and replayable.

## Boundaries
- Mock proof systems are for testnet only and are not production cryptography.
