
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




document.addEventListener("DOMContentLoaded", function () {
    let cartToggle = document.getElementById("cart-toggle");
	updateCartDropdown(); // هنگام لود صفحه، مقدار سبد خرید را تنظیم کند

    cartToggle.addEventListener("click", function () {
        updateCartDropdown(); // هنگام کلیک روی سبد خرید، مقدار آن به‌روزرسانی شود
    });

    let updateButtons = document.querySelectorAll(".update-cart");

    updateButtons.forEach(button => {
        button.addEventListener("click", function () {
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
                    quantityInput.value = data.quantity; // مقدار باید عددی بماند
                    totalPriceElement.innerText = `${convertToPersianNumbers((data.quantity * parseFloat(data.price)).toFixed())} تومان`;
                }
                totalCartPriceElement.innerText = `${convertToPersianNumbers(data.total_price)} تومان`;

                updateCartDropdown(); // ✅ سبد خرید را به‌روزرسانی کنیم
            })
            .catch(error => console.error("Error:", error));
        });
    });
});



// 📌  نوشتن AJAX برای دریافت سبد خرید و نمایش در dropdown
// ✅ هر بار که کاربر روی دکمه "سبد خرید" کلیک کند، اطلاعات سبد خرید بدون رفرش بارگذاری می‌شود.
document.addEventListener("DOMContentLoaded", function () {
    let cartToggle = document.getElementById("cart-toggle");
	updateCartDropdown();

    cartToggle.addEventListener("click", function () {
        updateCartDropdown()
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



function populateCartDropdownUI(data) {
    let cartList = document.getElementById("cart-list");
    let cartItemCount = document.getElementById("cart-item-count");
    let cartItemsCount = document.getElementById("cart-items-count");
    let cartTotal = document.getElementById("cart-total");

    if (data.items.length === 0) {
        cartList.innerHTML = `<p class="text-center text-muted">سبد خرید شما خالی است</p>`;
    } else {
        cartList.innerHTML = "";
        data.items.forEach(item => {
            cartList.innerHTML += `
                <div class="cart-item">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-img"> <!-- 👈 کلاس جدید -->
                    <div>
                        <p>${item.name}</p>
                        <small>${convertToPersianNumbers(item.quantity)} × ${convertToPersianNumbers(item.price)} تومان</small>
                    </div>
                </div>`;
        });
    }

    cartItemCount.innerText = convertToPersianNumbers(data.items.length);
    cartItemsCount.innerText = `${convertToPersianNumbers(data.items.length)} محصول انتخاب شده`;
    cartTotal.innerText = `${convertToPersianNumbers(data.total_price)} تومان`;
}


function convertToPersianNumbers(number) {
    return Number(number).toLocaleString("fa-IR"); // تبدیل عدد به فارسی و سه‌رقمی کردن
}



    









