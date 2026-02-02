const DEFAULT_GATEWAY = "http://127.0.0.1:8091";

document.addEventListener("DOMContentLoaded", async () => {
  const noAccount = document.getElementById("no-account");
  const accountInfo = document.getElementById("account-info");
  const addressEl = document.getElementById("address");
  const balanceEl = document.getElementById("balance");
  const statusEl = document.getElementById("status");

  const refreshUI = async () => {
    const { accounts = [] } = await chrome.storage.local.get("accounts");
    if (accounts.length === 0) {
      noAccount.classList.remove("hidden");
      accountInfo.classList.add("hidden");
      statusEl.textContent = "Ready";
      return;
    }

    noAccount.classList.add("hidden");
    accountInfo.classList.remove("hidden");
    const account = accounts[0];
    addressEl.textContent = account.address;
    
    try {
      statusEl.textContent = "Fetching balance...";
      const response = await fetch(`${DEFAULT_GATEWAY}/wallet/balance?address=${account.address}`);
      const data = await response.json();
      balanceEl.textContent = `${data.balance} NYXT`;
      statusEl.textContent = "Synced";
    } catch (err) {
      statusEl.textContent = "Offline";
      console.error(err);
    }
  };

  document.getElementById("create-account").addEventListener("click", async () => {
    const address = "0x" + Array.from(crypto.getRandomValues(new Uint8Array(20)))
      .map(b => b.toString(16).padStart(2, "0")).join("");
    
    await chrome.storage.local.set({ accounts: [{ address }] });
    await refreshUI();
  });

  document.getElementById("refresh").addEventListener("click", refreshUI);

  document.getElementById("faucet").addEventListener("click", async () => {
    const { accounts } = await chrome.storage.local.get("accounts");
    const account = accounts[0];
    statusEl.textContent = "Requesting faucet...";
    
    try {
      const response = await fetch(`${DEFAULT_GATEWAY}/wallet/faucet`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          seed: 123,
          run_id: `faucet-${Date.now()}`,
          payload: { address: account.address, amount: 100 }
        })
      });
      const result = await response.json();
      if (result.error) throw new Error(result.error);
      await refreshUI();
    } catch (err) {
      statusEl.textContent = "Faucet failed";
      alert(err.message);
    }
  });

  await refreshUI();
});
