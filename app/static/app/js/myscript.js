$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();  // Get the product ID
    var eml = this.parentNode.children[2];  // Get the element where quantity will be updated
    
    console.log(id);  // Log the product ID to the console for debugging
    
    $.ajax({
        type: "GET",
        url: "/pluscart",  // URL for the AJAX request
        data: {
            prod_id: id  // Send the product ID in the request
        },
        success: function (data) {
            eml.innerText = data.quantity;  // Update the quantity displayed in the UI
            // Optionally, you can log the response data for debugging:
            // console.log(data);
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        },
        error: function (xhr, status, error) {
            console.error("Error in AJAX request:", error);
        }
    });
});

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity;
            $('#amount').text(data.amount);
            $('#totalamount').text(data.totalamount);
            if (data.quantity === 0) {
                // Optionally, remove the item from the UI if quantity is 0
                $(this).closest('.cart-item').remove();
            }
        },
        error: function (xhr, status, error) {
            console.error("Error in AJAX request:", error);
        }
    });
});
$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var elm = $(this); // Use jQuery to keep it robust

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function (data) {
            // Update amounts dynamically
            $('#amount').text(data.amount);
            $('#totalamount').text(data.totalamount);

            // Remove the cart item dynamically
            elm.closest('.cart-item').remove();
        },
        error: function (xhr, status, error) {
            console.error("Error in AJAX request:", error);
        }
    });
});
