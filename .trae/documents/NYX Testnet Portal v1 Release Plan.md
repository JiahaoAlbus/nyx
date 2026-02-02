# NYX Testnet Portal v1 - Production Suite Release Plan

This plan outlines the roadmap to ship a production-grade NYX Testnet Portal v1 suite, including iOS, Web, Browser Extension, and Backend enhancements. All work will be performed on a single branch `release/testnet-portal-v1` and delivered via a single PR.

## **Phase 1: Backend & Storage Hardening**
- **Standardize Pagination**: Update `storage.py` to support `limit` and `offset`/`after` for all listing endpoints (Orders, Trades, Messages, Listings).
- **Activity Feed**: Enhance `/portal/v1/activity` to aggregate and filter receipts across all modules.
- **Error Handling**: Standardize JSON error responses across the gateway to eliminate stack traces and provide user-friendly messages.
- **Fee Invariants**: Verify and enforce that `protocol_fee > 0` and platform fees are additive in all state-transition endpoints.

## **Phase 2: Browser Extension (MV3)**
- **MetaMask-like Experience**: Create `packages/extension` with a manifest v3 architecture.
- **EIP-1193 Provider**: Implement an injected provider for seamless dapp interaction.
- **Account Store**: Use WebCrypto for local encrypted key management (no mnemonics for v1, testnet-only).
- **UI**: Popup for account status, connection permissions per origin, and transaction signing approvals.

## **Phase 3: Web Portal UI Rework**
- **8-Tab Layout**: Restructure `nyx-world` to match the new product UX:
  - `Home` / `Wallet` / `Exchange` / `Chat` / `Store` / `Activity` / `Evidence` / `Settings`.
- **Dapp Browser**: Implement an internal "Dapp Browser" page with injected provider support.
- **Design System**: Apply a coherent, high-polish visual design across all screens.

## **Phase 4: iOS App Native SwiftUI Rework**
- **Native Experience**: Replace the current web-wrapper with native SwiftUI screens for all 8 tabs.
- **Backend Integration**: Use the existing `GatewayClient.swift` to fetch real-time data from the backend.
- **Build Quality**: Ensure clean builds for iPhone 16 Pro simulator and prepare `.xcarchive` artifacts.

## **Phase 5: Release Engineering & Artifacts**
- **Automated Packaging**: Create `scripts/build_release_artifacts.sh` to:
  - Run full verification (`nyx_verify_all.sh`).
  - Build and package iOS `.app`, Extension `.zip`, Web `.zip`, and Backend runnable.
  - Generate `SHA256SUMS.txt` for all artifacts.
- **Documentation**: Deliver `RELEASE_NOTES_TESTNET_PORTAL_V1.md`, `PRODUCT_RUNBOOK.md`, and `RULES_ADDENDUM_V2.md`.

## **Phase 6: Final Verification**
- **Zero-Fake Policy**: Run CI gates to ensure no placeholder data or TODOs exist in runtime code.
- **One Single PR**: Submit the final `release/testnet-portal-v1` branch to `main` with all verification outputs.

Do you approve this plan to proceed with the implementation?
