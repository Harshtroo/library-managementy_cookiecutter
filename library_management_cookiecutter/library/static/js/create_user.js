var data = document.currentScript.dataset;
const createUserURL = data.createUserURL

// const successURL = data.successURL

function addData() {

    var username = document.getElementById("username").value
    var firstname = document.getElementById("firstname").value
    var lastname = document.getElementById("lastname").value
    var email = document.getElementById("email").value
    var role = document.getElementById("role").value;

    var data = {
        "username": username,
        "first_name": firstname,
        "last_name": lastname,
        "email": email,
        "role": role,
    }

    $.ajax({
        url: createUserURL,
        type: "POST",
        headers: { "X-CSRFToken": csrf_token },
        data: data,
        success: function (data) {
            console.log(data);
            if (data.message == "success") {
                window.location.href = "/success_register/"
            }
        },
        error: function (data, error) {
            console.log(data.responseJSON.message.username[0]);
            document.getElementById("firstname_error").innerHTML += data.responseJSON.message.first_name[0]
            document.getElementById("lastname_error").innerHTML += data.responseJSON.message.last_name[0]
            document.getElementById("email_error").innerHTML += data.responseJSON.message.email[0]
            document.getElementById("username_error").innerHTML += data.responseJSON.message.username[0]

        },

    });

}