from decimal import Decimal
from django.utils import timezone
from .models import Discount
from main.models import Product, Category # Needed for product/category specific discounts

def get_applicable_automatic_discounts(cart, user=None):
    """
    Placeholder: Finds active automatic discounts that apply to the cart/user.
    This would query Discount objects where code is null and other conditions are met.
    For now, returns an empty list.
    """
    # TODO: Implement logic to find and validate automatic discounts
    # Example query:
    # Discount.objects.filter(
    #     is_active=True,
    #     code__isnull=True,
    #     active_from__lte=timezone.now()
    # ).exclude(
    #     active_until__isnull=False,
    #     active_until__lt=timezone.now()
    # )
    return []

def calculate_discount_for_cart(cart, discount_code=None, user=None):
    """
    Calculates the discount amount and the new total for a given cart and discount code.
    Returns: (discount_amount, applied_discount_instance_or_none, message_string)
    """
    cart_subtotal = cart.get_subtotal()
    applied_discount_obj = None
    calculated_discount_amount = Decimal('0.00')
    message = "No discount applied."

    # 1. Attempt to apply coupon code if provided
    if discount_code:
        try:
            discount = Discount.objects.get(code__iexact=discount_code, is_active=True)
            
            is_generally_valid, validation_message = discount.is_valid(cart_total=cart_subtotal)
            if not is_generally_valid:
                return Decimal('0.00'), None, validation_message

            # Check applicability (ENTIRE_ORDER, SPECIFIC_PRODUCTS, SPECIFIC_CATEGORIES)
            base_for_discount = Decimal('0.00')

            if discount.applies_to == 'ENTIRE_ORDER':
                base_for_discount = cart_subtotal
            elif discount.applies_to == 'SPECIFIC_PRODUCTS':
                relevant_items_total = sum(
                    item['total_price'] for item in cart
                    if item['product'] in discount.products.all()
                )
                if relevant_items_total == Decimal('0.00'):
                    return Decimal('0.00'), None, "Coupon not applicable to items in cart."
                base_for_discount = relevant_items_total
            elif discount.applies_to == 'SPECIFIC_CATEGORIES':
                cart_categories = {item['product'].category for item in cart if item['product'].category}
                relevant_items_total = sum(
                   item['total_price'] for item in cart
                   if item['product'].category in discount.categories.all()
                )
                if relevant_items_total == Decimal('0.00'):
                   return Decimal('0.00'), None, "Coupon not applicable to categories in cart."
                base_for_discount = relevant_items_total

            if base_for_discount > Decimal('0.00') or discount.applies_to == 'ENTIRE_ORDER': # Ensure some base for calculation
                if discount.discount_type == 'PERCENTAGE':
                    calculated_discount_amount = (discount.value / Decimal('100')) * base_for_discount
                elif discount.discount_type == 'FIXED_AMOUNT':
                    # Ensure fixed amount does not exceed the base it applies to, or the cart subtotal
                    calculated_discount_amount = min(discount.value, base_for_discount, cart_subtotal)
                
                # Ensure discount doesn't make total negative (especially for fixed amounts)
                calculated_discount_amount = min(calculated_discount_amount, cart_subtotal)

                if calculated_discount_amount > Decimal('0.00'):
                    applied_discount_obj = discount
                    message = f"Discount '{discount.name}' applied."
                elif discount.applies_to != 'ENTIRE_ORDER': # If it was specific but no items matched
                     message = f"Coupon '{discount_code}' is valid but not applicable to items in your cart."


        except Discount.DoesNotExist:
            message = f"Coupon code '{discount_code}' is not valid or has expired."
        except Exception as e:
            # Log this error in a real application
            print(f"Error applying discount: {e}")
            message = "An unexpected error occurred while applying the discount."

    # 2. If no coupon or coupon invalid, check for automatic discounts (placeholder)
    if not applied_discount_obj:
        auto_discounts = get_applicable_automatic_discounts(cart, user)
        if auto_discounts:
            # TODO: Implement logic to choose the best automatic discount if multiple apply
            # For now, this part is a placeholder.
            # applied_discount_obj = auto_discounts[0] # Example: take the first one
            # ... recalculate calculated_discount_amount based on this auto_discount ...
            # message = f"Automatic discount '{applied_discount_obj.name}' applied."
            pass

    return calculated_discount_amount.quantize(Decimal('0.01')), applied_discount_obj, message