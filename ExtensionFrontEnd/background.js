let highlightedText = "";

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === "highlightedText") {
    highlightedText = request.text;
  }
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "getHighlightedText") {
    sendResponse({ text: highlightedText });
  }
});