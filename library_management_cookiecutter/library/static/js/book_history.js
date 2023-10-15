var data = document.currentScript.dataset;
const bookHistoryURL = data.bookHistoryURL;
$.ajax({
  url: bookHistoryURL,
  method: "POST",
  type: "json",
  headers: { "X-CSRFToken": csrf_token },
  success: function (data) {
    var output = `<h3 align="center">Book History</h3>
                <table class="table mx-auto">
                  <tr class="table-dark" >
                  <th>Book Name</th>
                  <th>Assign Book </th>
                  <th>Return Book </th>
              </tr>`;
    for (i = 0; i < data.book_list.length; i++) {
      var book = data.book_list[i];
      output += `
                 <tr id="book_details">
                <td>${book.name}</td>
                <td id="assig_count" title="${book.assign_user}">${book.assign_count}</td>
                <td title = "${book.assign_user}">${book.return_count}</td>
            </tr>`;
    }
    output += `</table>`;
    document.getElementById("book_items").innerHTML += output;
  },
  error: function (data) {},
});
