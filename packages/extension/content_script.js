const script = document.createElement("script");
script.src = chrome.runtime.getURL("scripts/provider.js");
script.onload = function() {
  this.remove();
};
(document.head || document.documentElement).appendChild(script);

window.addEventListener("message", (event) => {
  if (event.source !== window || !event.data || event.data.type !== "NYX_REQUEST") {
    return;
  }

  chrome.runtime.sendMessage(event.data, (response) => {
    window.postMessage({
      type: "NYX_RESPONSE",
      id: event.data.id,
      result: response ? response.result : null,
      error: response ? response.error : "Unknown error"
    }, "*");
  });
});
