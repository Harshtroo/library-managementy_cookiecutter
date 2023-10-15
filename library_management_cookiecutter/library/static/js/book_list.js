var data = document.currentScript.dataset;
const bookListURL = data.bookListURL;

function trunString(string, words = 17) {
  return string.slice(0, words) + (string.length > words ? "..." : "");
}

var ids = {};

function bookId(val) {
  $("#userpopbox").modal("show");
  ids["btn_action"] = val.name;
  ids["book"] = val.dataset.id;
}

function selectUser() {
  var selectUserId = $("#option").val();
  ids["user"] = selectUserId;

  $.ajax({
    method: "POST",
    url: bookListURL,
    headers: { "X-CSRFToken": csrf_token },
    data: ids,
    success: (data) => {
      document.getElementById(
        "errormessage"
      ).innerHTML = `<div class="alert alert-success" role="alert">
            ${data.message} </div>`;
      if (data.rem) {
        document.getElementById(`available${data.book_id}`).innerHTML =
          data.rem;
      }
      setInterval(function () {
        window.location.reload();
      }, 2000);
    },
    error: (response) => {
      let json_response = response.responseJSON;
      document.getElementById(
        "errormessage"
      ).innerHTML = `<div class="alert alert-danger" role="alert">Already assign book this user</div>`;
      setInterval(function () {
        window.location.reload();
      }, 2000);
    },
  });
}

$.ajax({
  url: bookListURL,
  method: "GET",
  headers: { "X-CSRFToken": csrf_token },
  success: function bookList(book) {
    output = "";
    for (i = 0; i < book.length; i++) {
      output += `
                       <div class="col-3">
                        <div class="card w-80 h-60 mx-auto">
                        <img src="${
                          book[i].book_image
                        }" style="height:100px;width:min-content;align-self:center">
                        <div class="card-body">
                            <p class="card-title box.item.cupcake" id="book name" title=${
                              book[i].book_name
                            }"><b>${trunString(book[i].book_name)}</b></p>
                            <button name="assign_book"  class="btn btn-primary" data-id ="${
                              book[i].id
                            }" id="bookbtn_${
        book[i].id
      }"  onclick="bookId(this)">Assign Book</button><br>

                            <p style="margin-left:225px margin-bottom:-39px">Author Name:<br>${trunString(
                              book[i].author_name,
                              5
                            )}</p>
                            <p style="margin-right:209px" id="total" >Total Quantity:${
                              book[i].quantity
                            }</p>
                            <p style="margin-right:189px" id="available${
                              book[i].id
                            }">Available Quantity:${book[i].available}</p>
                        </div>
                        </div>
                        </div>`;
    }
    document.getElementById("bookcard").innerHTML = output;
  },
});
