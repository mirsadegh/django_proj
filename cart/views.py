from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from discounts.forms import CouponApplyForm
from django.http import JsonResponse

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart_detail.html', 
                  {'cart': cart, 'coupon_apply_form': coupon_apply_form})

@require_POST
def apply_coupon_view(request):
    cart = Cart(request)
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        coupon = form.cleaned_data['code']
        cart.apply_coupon(coupon)
    return redirect('cart:cart_detail')

@require_POST
def remove_coupon_view(request):
    cart = Cart(request)
    cart.remove_coupon()
    return redirect('cart:cart_detail')

def clear_cart_view(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

def cart_dropdown(request):
    cart = Cart(request)
    return JsonResponse({
        'total_items': cart.__len__(),
        'total_price': cart.get_total_price(),
    })
