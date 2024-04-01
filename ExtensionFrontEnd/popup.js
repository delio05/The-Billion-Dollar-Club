document.addEventListener("DOMContentLoaded", function () {

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

//Listener for Helper text box (minimize and maximize)
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('icon').addEventListener('click', toggleInstructionBox);
  document.getElementById('closeButton').addEventListener('click', toggleInstructionBox);
  document.getElementById('reopenButton').addEventListener('click', reopenInstructionBox);

  document.getElementById('reopenButton').style.display = 'none';
});

function toggleInstructionBox() {
  var instructionBox = document.getElementById("instructionBox");
  instructionBox.classList.toggle("minimized");
  toggleReopenButtonVisibility();
}

function toggleReopenButtonVisibility() {
  var reopenButton = document.getElementById("reopenButton");
  if (reopenButton) {
    reopenButton.style.display = document.getElementById("instructionBox").classList.contains("minimized") ? "block" : "none";
  }
}

function reopenInstructionBox() {
  var instructionBox = document.getElementById("instructionBox");
  instructionBox.classList.remove("minimized");
  toggleReopenButtonVisibility();
}