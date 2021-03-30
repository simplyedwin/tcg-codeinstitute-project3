$(document).ready(function () {
  $("#add-form").on("submit", function (event) {
    event.preventDefault();
    toastr.options.preventDuplicates = true;

    var formData = new FormData(document.getElementById("add-form"));

    let name = formData.get("name");

    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        return xhr;
      },
      type: "POST",
      url: "/",
      data: formData,
      processData: false,
      contentType: false,
      complete: function (xhr) {
        statuscode = xhr.status;
        var i = 0;
        // to show the progress bar if receive code 200
        uploadingprogress(statuscode);
        function uploadingprogress(scode) {
          if (scode === 200) {
            $("#addprogressBar").css("width", "100%").text("100%");
          } else if (scode != 400) {
            if (i < 100) {
              i = i + 1;
              $("#addprogressBar")
                .css("width", i + "%")
                .text(i + " %");
            }
            // Wait for sometime before running this script again
            setTimeout(uploadingprogress, 100, scode);
          }
        }
      },
      success: function (data) {
        toastr.success(name + " successfully added!");
      },
      error: function (xhr) {
        let msg;
        // if resceive response to be code 400, flash error message
        if (xhr.status === 400) {
          resobj = JSON.parse(xhr.responseText);
          msg = resobj["message"];
          for (var error in msg) {
            toastr.warning(msg[error]);
          }
        }
      },
    });
  });
});
