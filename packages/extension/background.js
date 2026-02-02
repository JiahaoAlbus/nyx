const DEFAULT_GATEWAY = "http://127.0.0.1:8091";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "NYX_REQUEST") {
    handleRequest(request, sender)
      .then(result => sendResponse({ result }))
      .catch(error => sendResponse({ error: error.message }));
    return true; // async
  }
});

async function handleRequest(request, sender) {
  const { method, params, origin } = request;

  switch (method) {
    case "eth_requestAccounts":
    case "eth_accounts":
      return await getAccounts(origin);
    case "eth_chainId":
      return "0x7978"; // 'nyx' in hex?
    case "eth_sendTransaction":
      return await sendTransaction(params[0], origin);
    case "personal_sign":
      return await signMessage(params[0], params[1], origin);
    default:
      throw new Error(`Method ${method} not supported`);
  }
}

async function getAccounts(origin) {
  const { accounts = [] } = await chrome.storage.local.get("accounts");
  if (accounts.length === 0) {
    // Proactively suggest creating an account if none exist
    return [];
  }
  // Check permissions
  const { permissions = {} } = await chrome.storage.local.get("permissions");
  if (permissions[origin]) {
    return [accounts[0].address];
  }
  
  // If not permitted, we would normally open a popup. 
  // For this testnet v1, we'll return the first account if it exists for now,
  // but in a real flow we'd trigger a permission UI.
  return [accounts[0].address];
}

async function sendTransaction(tx, origin) {
  // Mocking transaction submission to the NYX gateway
  console.log("[NYX Background] Sending transaction:", tx, "from", origin);
  const { accounts } = await chrome.storage.local.get("accounts");
  const account = accounts[0];
  
  const response = await fetch(`${DEFAULT_GATEWAY}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      seed: 123,
      run_id: `ext-tx-${Date.now()}`,
      module: "wallet",
      action: "transfer",
      payload: {
        from_address: account.address,
        to_address: tx.to,
        amount: parseInt(tx.value, 16) || 0
      }
    })
  });
  
  const result = await response.json();
  if (result.error) throw new Error(result.error);
  return result.run_id;
}

async function signMessage(message, address, origin) {
  console.log("[NYX Background] Signing message:", message, "for", address, "from", origin);
  // In a real implementation, we'd use the private key stored in chrome.storage.local (encrypted)
  // and sign the message using WebCrypto.
  return "0x_mock_signature_" + Date.now();
}
