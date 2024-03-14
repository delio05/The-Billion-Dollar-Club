//not currently using with extension, but can expand on in the future

const mediumHighlighter = document.createElement("medium-highlighter");
document.body.appendChild(mediumHighlighter);

const setMarkerPosition = (markerPosition) =>
  mediumHighlighter.setAttribute(
    "markerPosition",
    JSON.stringify(markerPosition)
  );

const getSelectedText = () => window.getSelection().toString();

document.addEventListener("click", () => {
  if (getSelectedText().length > 0) {
    setMarkerPosition(getMarkerPosition());
  }
});

document.addEventListener("selectionchange", () => {
  if (getSelectedText().length === 0) {
    setMarkerPosition({ display: "none" });
  }
});

document.addEventListener("selectionchange", () => {
  const selectedText = getSelectedText();
  if (selectedText.length > 0) {
    chrome.storage.local.set({ 'selectedText': selectedText }, function() {
      console.log('Selected text is saved');
    });
  }
});

function getMarkerPosition() {
  const rangeBounds = window
    .getSelection()
    .getRangeAt(0)
    .getBoundingClientRect();
  return {
    left: rangeBounds.left + rangeBounds.width / 2 - 20,
    top: rangeBounds.top - 30,
    display: "flex",
  };
}
