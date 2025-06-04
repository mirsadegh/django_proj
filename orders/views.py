from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required # Or LoginRequiredMixin for CBV
from django.contrib import messages
from django.db import transaction

from .models import Order # OrderItem will be needed later
from .forms import OrderForm
from cart.cart import Cart
from discounts.models import Discount, AppliedDiscount

# We should define OrderItem model in orders/models.py and uncomment related lines later
# For now, OrderItem creation will be commented out.

# @login_required # Recommended for checkout
def order_create(request):
    cart = Cart(request)
    if not cart: # If cart is empty, redirect to cart page or homepage
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('cart:cart_detail') # Or your shop's homepage

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic(): # Ensure all DB operations succeed or fail together
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    
                    order.total_amount = cart.get_total_price() # Get final price after discounts
                    order.save() # Save the order to get an ID

                    # Discount handling
                    if cart.applied_discount_id and cart.discount_amount > 0:
                        try:
                            discount_instance = Discount.objects.get(id=cart.applied_discount_id)
                            AppliedDiscount.objects.create(
                                order=order,
                                discount=discount_instance,
                                amount_saved=cart.discount_amount
                            )
                            discount_instance.increment_uses()
                            # Optionally, store discount name/code on order itself if needed for quick display
                            # order.discount_name = discount_instance.name 
                            # order.save(update_fields=['discount_name'])
                        except Discount.DoesNotExist:
                            # This should ideally not happen if cart state is consistent
                            messages.error(request, "Applied discount was not found. Please try again.")
                            # Potentially log this issue
                            return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


                    # TODO: Create OrderItem instances
                    # for item_data in cart:
                    #     OrderItem.objects.create(
                    #         order=order,
                    #         product=item_data['product'],
                    #         price=item_data['price'], # Price per unit at the time of purchase
                    #         quantity=item_data['quantity']
                    #     )
                    
                    cart.clear()
                    
                    # Store order_id in session for thank you page or payment processing
                    request.session['order_id'] = order.id 
                    # return redirect(reverse('payment:process')) # Example redirect to payment
                    messages.success(request, "Your order has been placed successfully!")
                    # For now, redirect to a simple "order created" page or homepage
                    # We'll need an order_created_summary.html template
                    return redirect(reverse('orders:order_created_summary')) 

            except Exception as e:
                # Log the exception e
                messages.error(request, f"An error occurred while processing your order: {e}")
        else:
            messages.error(request, "There was an error with your information. Please check the details below.")
    else:
        # Pre-fill form if user is authenticated and has profile info, or allow guest checkout
        initial_data = {}
        if request.user.is_authenticated:
            # Example: prefill email, first_name, last_name if available on user model/profile
            initial_data['email'] = request.user.email 
            # initial_data['first_name'] = request.user.first_name 
            # initial_data['last_name'] = request.user.last_name
        form = OrderForm(initial=initial_data)
        
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


def order_created_summary(request):
    order_id = request.session.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass # Order not found, perhaps session cleared or invalid id
            
    if not order: # If no order_id in session or order not found
        messages.warning(request, "Could not retrieve your order summary. Please check your order history or contact support.")
        return redirect('index') # Redirect to homepage

    # Clear order_id from session after displaying summary to prevent re-showing
    # request.session['order_id'] = None 
    # Or del request.session['order_id'] if you are sure it exists

    return render(request, 'orders/order_created_summary.html', {'order': order})