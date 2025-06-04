from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from main.models import Product # Assuming Product model is in 'main'
from .cart import Cart
from discounts.models import Discount 

def cart_detail(request):
    cart = Cart(request)
    applied_discount_instance = None
    if cart.applied_discount_id:
        try:
            # This import should be here or at the top if used more broadly 
            applied_discount_instance = Discount.objects.get(id=cart.applied_discount_id)
        except Discount.DoesNotExist:
            # If discount ID in session is invalid, clear it from cart
            cart.clear_discount() 
            messages.error(request, "تخفیف قبلی دیگر معتبر نیست و حذف شده است.")
            # No need to redirect here, cart_detail will render with updated cart object

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'applied_discount': applied_discount_instance
    })

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1)) # Default to 1 if not specified
    override_quantity = request.POST.get('override_quantity', 'false').lower() == 'true'
    
    cart.add(product=product, quantity=quantity, override_quantity=override_quantity)
    messages.success(request, f"'{product.title}' has been added to your cart.")
    return redirect('cart:cart_detail') # Assuming you have a URL name 'cart_detail'

@require_POST # Or handle GET if you want a confirmation page before removal
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"'{product.title}' has been removed from your cart.")
    return redirect('cart:cart_detail')

@require_POST
def apply_coupon_view(request):
    cart = Cart(request)
    coupon_code = request.POST.get('coupon_code', '').strip()

    if not coupon_code:
        # If user submits empty coupon, treat as clearing existing one or do nothing
        # cart.clear_discount() # Optionally clear if empty code submitted
        messages.warning(request, "Please enter a coupon code.")
        return redirect('cart:cart_detail')

    message = cart.apply_coupon(coupon_code) # This calls recalculate_totals internally

    if cart.applied_discount_id and cart.discount_amount > 0 : # Check if a discount was actually applied
        messages.success(request, message or "Coupon applied successfully.")
    elif cart.coupon_code and not cart.applied_discount_id : # Coupon code was set, but no discount applied (e.g. not applicable)
        messages.warning(request, message or f"Coupon '{coupon_code}' could not be applied.")
    else: # No coupon code or it was invalid and cleared by the service
        messages.error(request, message or "Invalid coupon code.")
            
    return redirect('cart:cart_detail')

def remove_coupon_view(request): # Can be GET or POST, POST is safer for state changes
    cart = Cart(request)
    if cart.coupon_code or cart.applied_discount_id:
        cart.clear_discount() # This calls recalculate_totals internally
        messages.info(request, "Coupon has been removed.")
    else:
        messages.info(request, "No coupon was applied to remove.")
    return redirect('cart:cart_detail')

# View to clear the entire cart
def clear_cart_view(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Your shopping cart has been cleared.")
    return redirect('cart:cart_detail')
