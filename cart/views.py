from django.views.generic import ListView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from main.models import Product
from .cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse




class CartView(View):
    template_name = "main/shopping_cart.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)  # دریافت اطلاعات سبد خرید
        return render(request, self.template_name, {"cart": cart})
        

# Class-based view to handle adding a product to the cart.

class AddToCartAjaxView(View):
    def post(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get("product_id")  # دریافت از URL
            if not product_id:
                return JsonResponse({"error": "❌ شناسه محصول ارسال نشده است"}, status=400)
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            cart.add(product=product, quantity=1)

            return JsonResponse({
                "message": f"✅ {product.title} به سبد خرید اضافه شد!",
                "cart_total": cart.get_total_price(),
            })

        except Product.DoesNotExist:
            return JsonResponse({"error": "❌ محصول یافت نشد!"}, status=404)

# Class-based view to handle removing a product from the cart.
class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)

        return redirect(request.META.get('HTTP_REFERER', 'cart:add_to_cart'))



class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        action = request.POST.get("action")  # 'increase' یا 'decrease'
        cart = Cart(request)
        product = Product.objects.get(id=product_id)

        if action == "increase":
            cart.add(product=product, quantity=1)  # افزایش تعداد
        elif action == "decrease":
            if cart.cart[str(product_id)]["quantity"] > 1:
                cart.cart[str(product_id)]["quantity"] -= 1  # کاهش تعداد
                cart.save()
            else:
                cart.remove(product)  # حذف از سبد اگر فقط ۱ عدد باقی‌مانده بود

        # بررسی اینکه محصول حذف شده یا نه
        is_removed = str(product_id) not in cart.cart

        return JsonResponse({
            "quantity": cart.cart[str(product_id)]["quantity"] if not is_removed else 0,
            "price": str(product.price),
            "total_price": str(cart.get_total_price()),  # مبلغ کل سبد خرید
            "is_removed": is_removed  # آیا محصول حذف شد؟
        })



class CartDropdownView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = []

        for item in cart:
            cart_items.append({
                "id": item["product"].id,
                "name": item["product"].title,
                "price": str(item["price"]),
                "quantity": item["quantity"],
                "total_price": str(item["total_price"]),
                "image": item["product"].image.url
            })

        return JsonResponse({
            "items": cart_items,
            "total_price": str(cart.get_total_price()),
        })




