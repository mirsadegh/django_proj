from decimal import Decimal
from django.conf import settings
from main.models import Product
from discounts.models import Discount # Now needed
from discounts.services import calculate_discount_for_cart

# TODO: Move 'CART_SESSION_DATA_KEY' to Django settings (e.g., settings.CART_SESSION_ID)
CART_SESSION_DATA_KEY = 'cart_session_data' # Keep as is for now

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart_data = self.session.get(CART_SESSION_DATA_KEY)

        if not cart_data:
            cart_data = self.session[CART_SESSION_DATA_KEY] = {
                'items': {},
                'coupon_code': None,
                'applied_discount_id': None,
                'discount_amount': '0.00',
            }
        
        self.cart = cart_data['items']  # self.cart refers to the items dict
        self.coupon_code = cart_data.get('coupon_code')
        self.applied_discount_id = cart_data.get('applied_discount_id')
        # Ensure discount_amount is loaded as Decimal
        self.discount_amount = Decimal(cart_data.get('discount_amount', '0.00'))

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.current_price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product) # Use existing remove logic if quantity becomes zero or less
        else:
            self.recalculate_totals() # Recalculate totals and save

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.recalculate_totals() # Recalculate totals and save

    def save(self):
        session_cart_data = self.session.get(CART_SESSION_DATA_KEY, {})
        session_cart_data['items'] = self.cart
        session_cart_data['coupon_code'] = self.coupon_code
        session_cart_data['applied_discount_id'] = self.applied_discount_id
        session_cart_data['discount_amount'] = str(self.discount_amount.quantize(Decimal('0.01')))
        
        self.session[CART_SESSION_DATA_KEY] = session_cart_data
        self.session.modified = True

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # This should be the final price after cart-level discounts
        subtotal = self.get_subtotal()
        return (subtotal - self.discount_amount).quantize(Decimal('0.01'))

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy() # Use a copy for iteration

        for product in products:
            item_data = cart[str(product.id)]
            item_data['product'] = product
            item_data['price'] = Decimal(item_data['price']) # Price of one unit
            item_data['total_price'] = item_data['price'] * item_data['quantity'] # Total for this line item
            yield item_data
            
    def __len__(self):
        """Count total number of items (sum of quantities) in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        if CART_SESSION_DATA_KEY in self.session:
            del self.session[CART_SESSION_DATA_KEY]
            self.session.modified = True
        # Reset cart object attributes as well
        self.cart = {}
        self.coupon_code = None
        self.applied_discount_id = None
        self.discount_amount = Decimal('0.00')

    def apply_coupon(self, coupon_code):
        self.coupon_code = coupon_code.strip() if coupon_code else None
        return self.recalculate_totals() # recalculate_totals will handle logic and saving

    def clear_discount(self):
        self.coupon_code = None
        # The actual clearing of discount_amount and applied_discount_id
        # will happen in recalculate_totals when no valid coupon is found.
        return self.recalculate_totals()

    def recalculate_totals(self):
        """
        Recalculates cart totals.
        In the future, this will call a discount service.
        For now, it contains STUBBED logic for a test coupon.
        """
        # Call the actual discount service
        # Note: The 'user' argument to calculate_discount_for_cart is not available directly in the Cart model.
        # If user-specific discounts are needed, the view calling this might need to pass the user,
        # or the request object could be passed to the cart and then to the service.
        # For now, we'll pass `user=None`.
        calculated_amount, applied_discount_object, service_message = calculate_discount_for_cart(
            cart=self,  # Pass the cart instance itself
            discount_code=self.coupon_code,
            user=None # Or self.request.user if request is stored in cart
        )

        self.discount_amount = calculated_amount
        if applied_discount_object:
            self.applied_discount_id = applied_discount_object.id
        else:
            self.applied_discount_id = None
            # If the service cleared the discount (e.g., code was invalid), update coupon_code in cart
            if self.coupon_code and not applied_discount_object: # Check if a code was attempted but failed
                 # Check if the message indicates the code was invalid rather than just not applicable
                if "not valid" in service_message or "expired" in service_message or "usage limit" in service_message:
                    self.coupon_code = None


        self.save() # Persist all changes to session
        return service_message
