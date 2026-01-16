import argparse
import pathlib
import random
import sys


def run_demo(seed: int) -> tuple[str, list[str], bool]:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    econ_src = repo_root / "packages" / "l2-economics" / "src"
    sys.path.insert(0, str(econ_src))
    src_path = repo_root / "packages" / "l3-dex" / "src"
    sys.path.insert(0, str(src_path))

    from l3_dex.actions import AddLiquidity, CreatePool, RemoveLiquidity, Swap
    from l3_dex.kernel import apply_action_with_receipt
    from l3_dex.replay import replay_receipt
    from l3_dex.state import DexState, state_hash

    rng = random.Random(seed)
    state = DexState(pools=())
    receipts = []

    state, receipt = apply_action_with_receipt(
        state,
        CreatePool(pool_id="p", asset_a="A", asset_b="B"),
    )
    receipts.append(receipt)

    amount_a = rng.randint(10, 20)
    amount_b = rng.randint(12, 24)
    state, receipt = apply_action_with_receipt(
        state,
        AddLiquidity(pool_id="p", amount_a=amount_a, amount_b=amount_b),
    )
    receipts.append(receipt)

    amount_in = rng.randint(3, 7)
    state, receipt = apply_action_with_receipt(
        state,
        Swap(pool_id="p", amount_in=amount_in, min_out=0, asset_in="A"),
    )
    receipts.append(receipt)

    pool = _get_pool(state, "p")
    lp_amount = max(1, pool.total_lp // 4)
    state, receipt = apply_action_with_receipt(
        state,
        RemoveLiquidity(pool_id="p", lp_amount=lp_amount),
    )
    receipts.append(receipt)

    final_hash = state_hash(state).hex()
    receipt_hashes = [r.receipt_hash.hex() for r in receipts]

    replay_state = DexState(pools=())
    for receipt in receipts:
        replay_state = replay_receipt(replay_state, receipt)
    replay_ok = state_hash(replay_state) == state_hash(state)

    return final_hash, receipt_hashes, replay_ok


def _get_pool(state, pool_id: str):
    for pool in state.pools:
        if pool.pool_id == pool_id:
            return pool
    raise AssertionError("pool not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    final_hash, receipt_hashes, replay_ok = run_demo(args.seed)
    print(f"state_hash={final_hash}")
    print(f"receipt_hashes={','.join(receipt_hashes)}")
    print(f"replay_ok={replay_ok}")


if __name__ == "__main__":
    main()
