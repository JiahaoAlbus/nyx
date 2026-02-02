(function() {
  class NyxProvider {
    constructor() {
      this.isNyx = true;
      this.isMetaMask = false; // NYX is NOT MetaMask, but some dapps check this
      this._listeners = {};
    }

    async request({ method, params }) {
      console.log("[NYX Provider] Request:", method, params);
      return new Promise((resolve, reject) => {
        const id = Math.random().toString(36).substring(2);
        const listener = (event) => {
          if (event.data && event.data.type === "NYX_RESPONSE" && event.data.id === id) {
            window.removeEventListener("message", listener);
            if (event.data.error) {
              reject(new Error(event.data.error));
            } else {
              resolve(event.data.result);
            }
          }
        };
        window.addEventListener("message", listener);
        window.postMessage({ type: "NYX_REQUEST", id, method, params, origin: window.location.origin }, "*");
      });
    }

    on(event, callback) {
      if (!this._listeners[event]) this._listeners[event] = [];
      this._listeners[event].push(callback);
    }

    removeListener(event, callback) {
      if (this._listeners[event]) {
        this._listeners[event] = this._listeners[event].filter(cb => cb !== callback);
      }
    }
  }

  window.ethereum = new NyxProvider();
  window.dispatchEvent(new Event("ethereum#initialized"));
  console.log("[NYX Provider] Injected");
})();
