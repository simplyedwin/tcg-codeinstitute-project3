$(document).ready(function () {
  $("#update-form").on("submit", function (event) {
    var formData = new FormData(document.getElementById("update-form"));

    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();

        xhr.upload.addEventListener("progress", function (e) {
          if (e.lengthComputable) {
            console.log("Bytes Loaded: " + e.loaded);
            console.log("Total Size: " + e.total);
            console.log("Percentage Uploaded: " + e.loaded / e.total);

            var percent = Math.round((e.loaded / e.total) * 100);

            $("#updateprogressBar")
              .attr("aria-valuenow", percent)
              .css("width", percent + "%")
              .text(percent + "%");
          }
        });

        return xhr;
      },
      type: "POST",
      url: "/update",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        console.log(data);
      },
    });
  });
});
