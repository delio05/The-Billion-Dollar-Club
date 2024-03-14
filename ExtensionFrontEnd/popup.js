document.addEventListener("DOMContentLoaded", function() {
  const closeButton = document.getElementById("closeButton");
  const instructionBox = document.getElementById("instructionBox");

  closeButton.addEventListener("click", function() {
    instructionBox.style.display = "none";
  });

  //this is what gets the selected highlighted text and displays it on the extension
  chrome.storage.local.get(['selectedText'], function(result) {
    if (result.selectedText) {
      document.getElementById("highlightedText").textContent = result.selectedText;
    } else {
      document.getElementById("highlightedText").textContent = "No text selected.";
    }
  });
});
