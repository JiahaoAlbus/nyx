import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Normalize test environment to avoid external env influence
os.environ.pop("NYX_TESTNET_TREASURY_ADDRESS", None)
os.environ.setdefault("NYX_TESTNET_FEE_ADDRESS", "testnet-fee-address")
