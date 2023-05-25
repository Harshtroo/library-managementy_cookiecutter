var data = document.currentScript.dataset;
const loginURL = data.loginURL;

function logindata() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  var data = {
    username: username,
    password: password,
  };
  $.ajax({
    url: loginURL,
    type: "POST",
    headers: { "X-CSRFToken": csrf_token },
    data: data,
    success: function (data) {
      if (data.message == "success") {
        window.location.href = "/";
      }
    },
    error: function (data, a, b) {
      console.log(a);
      console.log(b);
      console.log(data.responseJSON.message);
      document.getElementById("error").innerHTML += data.responseJSON.message;
    },
  });
}
