# NYX iOS Reference Client (Testnet Beta)

Purpose
- Provide a SwiftUI reference client that mirrors deterministic flows and renders evidence verbatim.

Scope
- Connects to the NYX backend gateway API to run deterministic flows and fetch evidence bundles.
- Displays evidence fields verbatim and exports bundles without modification.

Non-Scope
- No user access flows, no identity model, no credential handoff, no real-money claims.
- No live market data, no trading claims, no protocol semantics.

Run (local)
- Start the backend gateway on localhost:8091.
- Open NYXPortal.xcodeproj in Xcode.
- Select an iPhone Simulator and Run.

Rules
- Seed and run_id are required inputs.
- Evidence is read-only and is not computed or modified in the client.
- All outputs are deterministic for the same inputs.
