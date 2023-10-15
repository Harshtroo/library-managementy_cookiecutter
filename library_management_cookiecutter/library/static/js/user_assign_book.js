function returnBook(elem) {
  let book_id = elem.getAttribute("book_id");
  commanAjax(book_id, "return_book");
}

function count(elem) {
  let book_id = elem.getAttribute("book_id");
  $("#userpopbox").modal("show");

  var modal_show = $(event.relatedTarget).data("date_borrowed");
  $(this).find(".modal-body").text(modal_show);
  commanAjax(book_id, "count");
}
function commanAjax(book_id, button_action) {
  $.ajax({
    url: "/user_assign_book_list/",
    method: "POST",
    headers: { "X-CSRFToken": csrf_token },
    data: { book: book_id, button_action: button_action },
    success: function (data) {
      if (data.message) {
        document.getElementById(
          "message"
        ).innerHTML = `<div class="alert alert-success" role="alert">
                ${data.message} </div>`;
        setInterval(function () {
          window.location.reload();
        }, 2000);
      } else {
        $("#userpopbox").modal("show");
        let tableHtml = document.createElement("table");
        tableHtml.border = "2px";
        tableHtml.className = "table table-bordered ";

        let tableHead = document.createElement("thead");

        var tr = document.createElement("tr");

        var th = document.createElement("th");
        let addDate = document.createTextNode("Assign Book Date");
        th.appendChild(addDate);
        tr.appendChild(th);

        tableHead.appendChild(tr);
        tableHtml.appendChild(tableHead);

        let tableBody = document.createElement("tbody");

        data.forEach((value, key) => {
          let myDate = new Date(value.date_borrowed);
          var tr = document.createElement("tr");

          var td = document.createElement("td");
          var myDate1 = `${myDate.getDate()}-${myDate.getMonth()}-${myDate.getFullYear()} (${myDate.getHours()} :${myDate.getMinutes()} : ${myDate.getSeconds()})`;
          var date = document.createTextNode(myDate1);
          td.appendChild(date);
          tr.appendChild(td);

          tableBody.appendChild(tr);
        });
        tableHtml.appendChild(tableBody);
        $("#userpopbox").find(".modal-body").html(tableHtml);
      }
    },
    error: function (error) {
      console.log("Error: ", error);
    },
  });
}
