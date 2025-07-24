from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.views import View

from .models import Order # OrderItem will be needed later
from .forms import OrderForm
from cart.cart import Cart
from discounts.models import Discount, AppliedDiscount

# We should define OrderItem model in orders/models.py and uncomment related lines later
# For now, OrderItem creation will be commented out.

class OrderCreateView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            messages.warning(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart:cart_detail')
            
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['email'] = request.user.email
        form = OrderForm(initial=initial_data)
        
        return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})
        
        
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            messages.warning(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart:cart_detail')
            
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    
                    order.total_amount = cart.get_total_price()
                    order.save()

                    if cart.applied_discount_id and cart.discount_amount > 0:
                        try:
                            discount_instance = Discount.objects.get(id=cart.applied_discount_id)
                            AppliedDiscount.objects.create(
                                order=order,
                                discount=discount_instance,
                                amount_saved=cart.discount_amount
                            )
                            discount_instance.increment_uses()
                        except Discount.DoesNotExist:
                            messages.error(request, "Applied discount was not found. Please try again.")
                            return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

                    cart.clear()
                    request.session['order_id'] = order.id
                    messages.success(request, "Your order has been placed successfully!")
                    return redirect(reverse('orders:order_created_summary'))
                    
            except Exception as e:
                messages.error(request, f"An error occurred while processing your order: {e}")
        else:
            messages.error(request, "There was an error with your information. Please check the details below.")
            
        return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        order = None
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                # Clear order_id from session after displaying summary
                del request.session['order_id']
            except Order.DoesNotExist:
                pass
                
        if not order:
            messages.warning(request, "Could not retrieve your order summary. Please check your order history or contact support.")
            return redirect('index')
            
        return render(request, 'orders/order_created_summary.html', {'order': order})
