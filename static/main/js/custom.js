
$(document).ready(function() {
	// Attach click event handler to the logout link
	$("#logout-link").on("click", function(event) {
	  event.preventDefault(); // Prevent default anchor tag behavior

	  // Optionally, prompt a confirmation before logging out
	  if (confirm("Are you sure you want to log out?")) {
		$("#logout-form").submit(); // Submit the hidden logout form
	  }
	});
  });



  $(document).ready(function() {
    // Display messages with a fade-out effect
    $('.notify').fadeIn(500);
    $('.notify').delay(5000).fadeOut(500);
});


//shopping cart
function getCSRFToken() {
    let csrfToken = document.querySelector("meta[name='csrf-token']");
    return csrfToken ? csrfToken.getAttribute("content") : "";
}

document.addEventListener("DOMContentLoaded", function() {
    let addToCartButtons = document.querySelectorAll(".add-to-cart-btn");
    
    addToCartButtons.forEach(button => {
        button.addEventListener("click", function() {
            let productId = this.getAttribute("data-product-id");

            fetch(`/cart/add/${productId}/`, {  // مسیر API برای افزودن
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: ""
            })
            .then(response => response.json())
            .then(data => {
                showNotification(data.message);
                updateCartTotal(data.cart_total);
            })
            .catch(error => alert(`❌ خطا: ${error.message}`));
        });
    });




  function showNotification(message) {
    let notification = document.createElement("div");
    notification.className = "cart-notification alert alert-success";
    notification.innerText = message;

    document.body.appendChild(notification);

    // بعد از ۳ ثانیه، به آرامی ناپدید شود
    setTimeout(() => {
        notification.style.opacity = "0";
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

    function updateCartTotal(cartTotal) {
        let cartTotalElement = document.getElementById("cart-total");
        if (cartTotalElement) {
            cartTotalElement.innerText = `${cartTotal} تومان`;
        }
    }
});



document.addEventListener("DOMContentLoaded", function() {
	let updateButtons = document.querySelectorAll(".update-cart");

	updateButtons.forEach(button => {
		button.addEventListener("click", function() {
			let productId = this.getAttribute("data-product-id");
			let action = this.getAttribute("data-action");

			fetch(`/cart/update/${productId}/`, {
				method: "POST",
				headers: {
					"X-CSRFToken": getCSRFToken(),
					"Content-Type": "application/x-www-form-urlencoded"
				},
				body: `action=${action}`
			})
			.then(response => response.json())
			.then(data => {
				let quantityInput = this.parentElement.querySelector(".quantity-input");
				let totalPriceElement = this.parentElement.parentElement.querySelector(".total-price");
				let totalCartPriceElement = document.getElementById("total-cart-price");
				let productRow = this.closest(".card"); // کل کارت محصول

				if (data.is_removed) {
					productRow.remove(); // حذف محصول از صفحه
				} else {
					quantityInput.value = data.quantity;
					totalPriceElement.innerText = `${(data.quantity * parseFloat(data.price)).toFixed()} تومان`;
				}

				totalCartPriceElement.innerText = `${data.total_price} تومان`;

			})
			.catch(error => console.error("Error:", error));
		});
	});

	
});




function populateCartDropdownUI(data) {
    let cartList = document.getElementById("cart-list");
    let cartTotal = document.getElementById("cart-total");
    let cartItemCount = document.getElementById("cart-item-count");
    let cartItemsCountText = document.getElementById("cart-items-count");

    cartList.innerHTML = "";

    if (data.items.length === 0) {
        cartList.innerHTML = "<p class='text-center text-muted'>سبد خرید شما خالی است.</p>";
    } else {
        data.items.forEach(item => {
            let itemElement = document.createElement("div");
            itemElement.className = "product-widget d-flex align-items-center";
            itemElement.innerHTML = `
                <div class="product-img">
                    <img src="${item.image}" width="50" height="50" alt="${item.name}">
                </div>
                <div class="product-body text-right ms-3">
                    <h3 class="product-name"><a href="#">${item.name}</a></h3>
                    <h4 class="product-price"><span class="qty">${item.quantity}x</span> ${item.total_price} تومان</h4>
                </div>
                <button class="delete" onclick="removeFromCart(${item.id})"><i class="fa fa-close"></i></button>
            `;
            cartList.appendChild(itemElement);
        });

        cartTotal.innerText = `${data.total_price} تومان`;
        cartItemCount.innerText = data.items.length;
        cartItemsCountText.innerText = `${data.items.length} محصول انتخاب شده`;
    }
}



// 📌  نوشتن AJAX برای دریافت سبد خرید و نمایش در dropdown
// ✅ هر بار که کاربر روی دکمه "سبد خرید" کلیک کند، اطلاعات سبد خرید بدون رفرش بارگذاری می‌شود.
document.addEventListener("DOMContentLoaded", function () {
    let cartToggle = document.getElementById("cart-toggle");
	updateCartDropdown();

    cartToggle.addEventListener("click", function () {
        fetch("/cart/dropdown/")
            .then(response => response.json())
            .then(data => {
                populateCartDropdownUI(data);
            })
            .catch(error => console.error("Error loading cart:", error));
    });
});




// 📌  اضافه کردن AJAX به دکمه "افزودن به سبد خرید" برای به‌روزرسانی dropdown
// ✅ وقتی محصولی به سبد خرید اضافه شد، dropdown به‌روز شود.

function updateCartDropdown() {
    fetch("/cart/dropdown/")
        .then(response => response.json())
        .then(data => {
            populateCartDropdownUI(data);
        })
        .catch(error => console.error("Error updating cart dropdown:", error));
}






    









