console.log("This is a popup!");

//simulates a scenario such that the loading screen will show for test purposes, remove later
setTimeout(function () {
  document.getElementById("loader-container").style.display = "none";
  document.getElementById("chart-heading").style.display = "block";
  document.getElementById("chartContainer").style.display = "block";
}, 500);

$(function () {
  $("#sentenceSubmit").click(function () {
    var sent_sentence = $("#sentence").val();

    if (sent_sentence) {
      chrome.runtime.sendMessage(
        { sentence: sent_sentence },
        function (response) {
          console.log(response);
          //   result = response.farewell;
          //   alert(result.summary);

          //   var notif = {
          //     type: "basic",
          //     iconUrl: "myChartIcon.png",
          //     title: "Notification",
          //     message: result.summary,
          //   };
          //   chrome.notifications.create("notification", notif);
        }
      );
    }

    $("#sentence").val("");
  });
});
