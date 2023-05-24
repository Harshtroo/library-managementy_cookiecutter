let imagesArray = []
const data = document.currentScript.dataset;
const bookURL = data.bookURL;
var bookimage = document.getElementById("id_book_image")
bookimage.addEventListener("change", () => {
    const file = bookimage.files
    imagesArray.push(file[0])
    displayImages()
})

function displayImages() {
    let images = ""
    imagesArray.forEach((image, index) => {
        images += `<div class="image">
                <img src="${URL.createObjectURL(image)}" alt="image">
                
              </div>`
    })
    document.getElementById("output").innerHTML = images
}

function bookdata() {
    var bookname = document.getElementById("id_book_name").value
    var authorname = document.getElementById("id_author_name").value
    var price = document.getElementById("id_price").value
    var quantity = document.getElementById("id_quantity").value
    var bookimage = document.getElementById("id_book_image").files

    var data = {
        "book_name": bookname,
        "author_name": authorname,
        "price": price,
        "quantity": quantity,
        "book_image": bookimage,
    }

    var data = new FormData($('#addbook').get(0))   
    // const data = document.currentScript.dataset;
    // const book_url = data.book_url;
    $.ajax({
        url:bookURL,
        method: "POST",
        processData: false,
        contentType: false,
        headers: { "X-CSRFToken": "{{csrf_token}}" },
        data: data,
        success: function (data) {
            if (data.message == "success") {
                window.location.href = "/"
            }
        },
        error: function (data, error) {
            console.log("data",data.error)
            // document.getElementById("image_error").innerHTML = data.responseJSON.message.book_image[0]
            // document.getElementById("bookname_error").innerHTML = data.responseJSON.message.book_name[0]
            // document.getElementById("authorname_error").innerHTML = data.responseJSON.message.author_name[0]
            // document.getElementById("price_error").innerHTML = data.responseJSON.message.price[0]

        },
    })

}
