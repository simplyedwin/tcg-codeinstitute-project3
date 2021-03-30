$(document).ready(function () {
  $("#update-form").on("submit", function (event) {
    event.preventDefault();
    toastr.options.preventDuplicates = true;

    var pathname = window.location.pathname;

    $("#update-upload-btn").click(function(){
      location.reload();
  });

  $("#closeupdate-btn").click(function(){
    location.reload();
});

    var formData = new FormData(document.getElementById("update-form"));

    let name = formData.get("name");

    $.ajax({
    //   xhr: function () {
    //     var xhr = new window.XMLHttpRequest();

    //     return xhr;
    //   },
      type: "POST",
      url: pathname + "/update",
      data: formData,
      processData: false,
      contentType: false,
      dataType: "json",
      complete: function (xhr) {
        statuscode = xhr.status;
        var i = 0;
        // to show the progress bar if receive code 200
        uploadingprogress(statuscode);
        function uploadingprogress(scode) {
          if (scode === 200) {
            $("#updateprogressBar").css("width", "100%").text("100%");
          } else if (scode != 400) {
            if (i < 100) {
              i = i + 1;
              $("#updateprogressBar")
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
