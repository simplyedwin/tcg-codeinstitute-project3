$(document).ready(function () {
  $("#add-form").on("submit", function (event) {
    event.preventDefault();

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
        // hide the preloader (progress bar)
        console.log(statuscode);
        var i = 0;
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
      error: function (xhr, textStatus, errorThrown) {
        console.log(xhr.responseText);
        console.log(xhr.status);
        let error_status;
        let msg;
        if (xhr.status === 400) {
          resobj = JSON.parse(xhr.responseText);
          console.log(resobj);
          error_status = resobj["error_status"];
          msg = resobj["message"];
          for (var error in msg) {
            if (error === "title_is_blank") {
              console.log(error);
              $("#add-title").text(msg[error]);
            }
            $("#add-title").html('Testing');

            console.log(error);

            toastr.warning(msg[error]);
          }
        }
      },
    });
  });
});
