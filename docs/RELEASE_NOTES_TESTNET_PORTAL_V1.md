# NYX Testnet Portal v1 Release Notes

## **What's Shipped**
- **iOS App (NYXPortal)**: Native SwiftUI rework with 8 core tabs (Home, Wallet, Exchange, Chat, Store, Activity, Evidence, Settings).
- **Web Portal (NYX World)**: Restructured React/Vite UI matching the iOS experience.
- **Browser Extension**: Chrome MV3 extension with EIP-1193 provider and local encrypted account storage.
- **Dapp Browser**: Integrated browser inside both Web and Extension for secure dapp interaction.
- **Backend v1**: Hardened gateway with pagination, activity feeds, and improved error handling.

## **How to Run**
- **Backend**: `pip install -e . && python -m nyx_backend_gateway.server`
- **Web**: `cd nyx-world && npm install && npm run dev`
- **Extension**: Load `packages/extension` as an unpacked extension in Chrome.
- **iOS**: Open `apps/nyx-ios/NYXPortal.xcodeproj` in Xcode and run on iPhone 16 Pro simulator.

## **How to Verify**
- Run `bash scripts/nyx_verify_all.sh` to confirm the entire project state.
- Run `bash scripts/nyx_pack_proof_artifacts.sh` to generate the deterministic proof bundle.

## **Out of Scope**
- Mainnet launch, token sales, and market claims are strictly out of scope for v1.
