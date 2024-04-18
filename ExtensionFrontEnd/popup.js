//const { jsPDF } = window.jspdf;
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

// MODAL for Feedback Functionality
document.addEventListener('DOMContentLoaded', function() {
  
  var modal = document.getElementById("feedbackModal");
  var feedbackButton = document.getElementById("feedbackButton");
  var closeBtn = document.getElementsByClassName("close")[0];
  var thumbsUpButton = document.getElementById("thumbsUpButton");
  var thumbsDownButton = document.getElementById("thumbsDownButton");
  var feedbackTextarea = document.getElementById("feedbackText");

  //When the user clicks the THUMBS UP button
  thumbsUpButton.onclick = function() {
    var feedbackComment = feedbackTextarea.value;
    modal.style.display = "none"; // Close modal

    //TODO: Implement with Backend functionality
    // alert(feedbackComment);
    sendFeedbackToBackend(isPositive = true);

    // Clear feedbackText after submission
    feedbackTextarea.value = "";
  }

  //When the user clicks the THUMBS DOWN button
  thumbsDownButton.onclick = function() {
    var feedbackComment = feedbackTextarea.value;
    modal.style.display = "none"; // Close modal
    
    //TODO: Replace with Backend functionality
    // alert(feedbackComment);
    sendFeedbackToBackend(isPositive = false);
    
    // Clear feedbackText after submission
    feedbackTextarea.value = "";
  }

  // When the user clicks the button, open the modal 
  feedbackButton.onclick = function() {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  closeBtn.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
});

// Listener for Summarize Button
document.addEventListener('DOMContentLoaded', function () {
  var button = document.getElementById('sentenceSubmit');
  button.addEventListener('click', function () {
    sendTextToBackend();
  });
  var button1 = document.getElementById('extractButton');
  button1.addEventListener('click', function () {
    sendPDFToBackend();
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

function sendFeedbackToBackend(isPosotive){
  let text = document.getElementById("highlightedText").textContent;
  let language = document.getElementById("languageChooser").value;
  let attitude = null;
  if(isPositive == true){
    attitude = "positive";
  }
  else{
    attitude = "negative";
  }
  let feedback = document.getElementById("feedbackText").value;
  let previous = document.getElementById("chatGPTResponse").textContent;
  const url = `http://localhost:8000/handleImages/feedback/?content=${encodeURIComponent(text)}&language=${encodeURIComponent(language)}&attitude=${encodeURIComponent(attitude)}&feedback=${encodeURIComponent(feedback)}&previous=${encodeURIComponent(previous)}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Assuming 'data.content' contains the ChatGPT response
      if(isPositive == false)
      {
        document.getElementById("chatGPTResponse").textContent = data.content;
      }
      console.log(data.content);
    })
    .catch(error => console.error('Error sending text to backend:', error));
}

// Listener for Extracting buttom
// document.addEventListener('DOMContentLoaded', function () {
//   document.getElementById('extractButton').addEventListener('click', function () {
//     console.log(jsPDF);
//     var doc = new jsPDF();
//     var text = document.getElementById('highlightedText').value;  // Use value for textarea
//     doc.text(text, 10, 10);
//     doc.save('output.pdf');
//   });
// });
function sendPDFToBackend() {
  var doc = new jsPDF();
  var text = document.getElementById('chatGPTResponse').textContent;  // Use value for textarea
  doc.text(text, 10, 10);
  doc.save('output.pdf');
}

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