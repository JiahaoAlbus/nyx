# NYX Product Runbook (v1)

This runbook provides step-by-step instructions for a new user to set up and verify the NYX Testnet Portal v1 suite.

## **Step 1: Backend Setup**
1. Ensure Python 3.10+ is installed.
2. `pip install -r requirements.txt` (if applicable) or install packages in editable mode.
3. Start the gateway: `python -m nyx_backend_gateway.server`
4. Verify at `http://127.0.0.1:8091/healthz`.

## **Step 2: Web Portal**
1. `cd nyx-world && npm install && npm run dev`
2. Open `http://localhost:5173`.
3. Create a handle and request testnet funds from the Wallet tab.

## **Step 3: Browser Extension**
1. Open Chrome and navigate to `chrome://extensions`.
2. Enable "Developer mode".
3. Click "Load unpacked" and select the `packages/extension` directory.
4. Click the NYX icon in the toolbar to create an account.

## **Step 4: iOS Simulator**
1. Open `apps/nyx-ios/NYXPortal.xcodeproj` in Xcode.
2. Select "iPhone 16 Pro" as the target destination.
3. Press CMD+R to build and run.
4. Navigate through the native tabs to verify connectivity.

## **Step 5: E2E Verification**
1. Run `bash scripts/nyx_verify_all.sh --seed 123 --run-id smoke-test`.
2. Inspect the generated evidence in `docs/proof/`.
3. Run `bash scripts/nyx_pack_proof_artifacts.sh` to package the proof.
