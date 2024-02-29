var serverhost = "http://127.0.0.1:8000";

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  var url =
    serverhost +
    "/handleImages/sentenceAnalyze/?content=" +
    encodeURIComponent(request.sentence);

  console.log(url);

  fetch(url, {
    mode: "no-cors",
  })
    .then((response) => response.json())
    .then((response) => sendResponse({ farewell: response }))
    .catch((error) => console.log);

  return true;
});
