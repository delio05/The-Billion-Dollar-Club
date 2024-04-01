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
  let language = document.getElementById("languageChooser").value;
  const url = `http://localhost:8000/handleImages/sentenceAnalyze/?content=${encodeURIComponent(text)}&language=${encodeURIComponent(language)}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Assuming 'data.content' contains the ChatGPT response
      document.getElementById("chatGPTResponse").textContent = data.content;
    })
    .catch(error => console.error('Error sending text to backend:', error));
}

// Listener for Extracting buttom
document.getElementById('extractButton').addEventListener('click', function () {

  var textToExtract = document.getElementById('highlightedText').innerText;

  var blob = new Blob([textToExtract], { type: 'text/plain' });
  console.log(blob);
  var url = URL.createObjectURL(blob);
  console.log(blob);
  var link = document.createElement('a');
  link.href = url;
  link.download = 'extracted_text.pdf'; // Set the download attribute
  link.click(); // Simulate a click on the link
});
