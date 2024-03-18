document.addEventListener("DOMContentLoaded", function () {
  const closeButton = document.getElementById("closeButton");
  const instructionBox = document.getElementById("instructionBox");

  closeButton.addEventListener("click", function () {
    instructionBox.style.display = "none";
  });

  //this is what gets the selected highlighted text and displays it on the extension
  chrome.storage.local.get(['selectedText'], function (result) {
    if (result.selectedText) {
      document.getElementById("highlightedText").textContent = result.selectedText;
    } else {
      document.getElementById("highlightedText").textContent = "No text selected.";
    }
  });
});

// Listener for Summarize Button
document.addEventListener('DOMContentLoaded', function () {
  var button = document.getElementById('sentenceSubmit');
  button.addEventListener('click', function () {
    sendTextToBackend();
  });
});

function sendTextToBackend() {
  let text = document.getElementById("highlightedText").textContent;
  const url = `http://localhost:8000/handleImages/sentenceAnalyze/?content=${encodeURIComponent(text)}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Assuming 'data.content' contains the ChatGPT response
      document.getElementById("chatGPTResponse").textContent = data.content;
    })
    .catch(error => console.error('Error sending text to backend:', error));
}
