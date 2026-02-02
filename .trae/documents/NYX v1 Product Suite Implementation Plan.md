# NYX v1 Product Suite Implementation Plan

This plan outlines the roadmap to ship the production-grade NYX v1 product suite, adhering to the normative specifications and maintaining a security-first approach.

## Phase 0: Recon & Baseline (Current)
1. **Initialize Workspace**: 
   - Set up a `pnpm` workspace at the root to manage the new JS/TS packages.
   - Create `package.json` at the root with global scripts (`dev`, `test`, `build`).
2. **Documentation**:
   - Create [PLAN_V1.md](file:///Users/huangjiahao/Desktop/NYX/nyx/docs/PLAN_V1.md) detailing milestones and risk assessments.
   - Create [RUNBOOK.md](file:///Users/huangjiahao/Desktop/NYX/nyx/docs/RUNBOOK.md) for a deterministic developer experience.
3. **Audit Readiness**:
   - Verify all normative docs in `frozen/q1/` are respected.
   - Set up CI/CD pipelines (GitHub Actions) for the new packages.

## Phase 1: Wallet Kernel & Extension v1
1. **Wallet Kernel (`packages/wallet-kernel`)**:
   - Shared logic for cryptography (Ed25519/Secp256k1), BIP-32/39/44 derivation.
   - Account management and encrypted storage (using AES-GCM).
   - Alignment with `l0-identity` (Identity != Wallet).
2. **Wallet Extension (`packages/extension`)**:
   - Chrome MV3 implementation.
   - EIP-1193 provider and EIP-6963 discovery.
   - UI for permissions, connection flow, and transaction signing.

## Phase 2: Portal v1 & SDK
1. **NYX Portal (`packages/portal`)**:
   - Web-based control center (Onboarding, Status, Identity).
   - Integration with the extension via standard provider.
2. **NYX SDK (`packages/sdk`)**:
   - Developer tools for interacting with the NYX ecosystem.
   - Examples and documentation.

## Phase 3: Desktop Dapp Browser (Electron)
1. **Browser App (`packages/browser-app`)**:
   - Electron-based desktop application.
   - Integrated `wallet-kernel` for shared account state.
   - Tabbed browsing with built-in dapp registry support.

## Phase 4: Ecosystem Store & Chat
1. **Ecosystem Store (`packages/ecosystem-store`)**:
   - Signed manifest registry for verified dapps.
   - Integration into Portal and Desktop Browser.
2. **Chat / Social Layer (`packages/chat`)**:
   - E2EE messaging using standard libraries (e.g., libp2p or XMTP adapter).
   - Identity-respecting contact management.

## Phase 5: Gateway Service & Hardening
1. **Gateway Service (`services/gateway`)**:
   - Minimal-but-real Gateway API for Web2 mediation.
   - Audit logging and rate limiting.
2. **Hardening**:
   - Final E2E tests (Playwright) covering all user flows.
   - Security audit and "Safe by Default" configuration.

## Technical Requirements
- **Language**: TypeScript for JS packages, Python for core logic/backend.
- **Testing**: Vitest for JS unit tests, Playwright for E2E.
- **CI**: Enforce green builds and coverage gates at each PR.

Do you approve this plan to proceed with Phase 0 and Phase 1?
