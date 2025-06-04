from django.db import models
from django.utils import timezone
from django.conf import settings
# Assuming your Product and Category models are in the 'main' app
# Adjust the import path if they are located elsewhere.
from main.models import Product, Category

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED_AMOUNT', 'Fixed Amount'),
        # Consider adding 'FREE_SHIPPING' if needed later
    ]

    APPLIES_TO_CHOICES = [
        ('ENTIRE_ORDER', 'Entire Order'),
        ('SPECIFIC_PRODUCTS', 'Specific Products'),
        ('SPECIFIC_CATEGORIES', 'Specific Categories'),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name="Discount Name")
    is_automatic = models.BooleanField(
        default=False,
        help_text="Apply automatically without coupon code",
        verbose_name="Automatic Discount"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name="Discount Type")
    value = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text="Percentage (e.g., 10 for 10%) or fixed amount.", verbose_name="Value")
    code = models.CharField(max_length=50, unique=True, blank=True, null=True,
                            help_text="Coupon code. Leave blank for automatic discounts.", verbose_name="Coupon Code")
    
    active_from = models.DateTimeField(default=timezone.now, verbose_name="Active From")
    active_until = models.DateTimeField(blank=True, null=True, verbose_name="Active Until")
    
    minimum_cart_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                           help_text="Minimum cart total for discount to apply.", verbose_name="Minimum Cart Value")
    
    applies_to = models.CharField(max_length=20, choices=APPLIES_TO_CHOICES, default='ENTIRE_ORDER', verbose_name="Applies To")
    products = models.ManyToManyField(
        Product, 
        blank=True,
        help_text="Select products if 'Applies To' is 'Specific Products'.",
        verbose_name="Applicable Products"
    )
    categories = models.ManyToManyField(
        Category, 
        blank=True,
        help_text="Select categories if 'Applies To' is 'Specific Categories'.",
        verbose_name="Applicable Categories"
    )

    max_uses = models.PositiveIntegerField(blank=True, null=True, help_text="Maximum total uses for this discount.", verbose_name="Maximum Uses")
    uses_count = models.PositiveIntegerField(default=0, editable=False, verbose_name="Times Used")

    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.name} ({self.get_discount_type_display()})"

    def is_valid(self, cart_total=None, cart_items=None):
        """
        Checks if the discount is currently valid based on dates, uses, and minimum purchase.
        Does NOT check product/category applicability here, that's handled during application logic.
        """
        if not self.is_active:
            return False, "Discount is not active."
        if self.active_from > timezone.now():
            return False, "Discount is not yet active."
        if self.active_until and self.active_until < timezone.now():
            return False, "Discount has expired."
        if self.max_uses is not None and self.uses_count >= self.max_uses:
            return False, "Discount has reached its maximum usage limit."
        if self.minimum_cart_value and cart_total is not None and cart_total < self.minimum_cart_value:
            return False, f"Cart total must be at least {self.minimum_cart_value} to use this discount."
        return True, "Discount is valid."
    
    def valid_for_product(self, product):
        """
        Check if discount applies to a specific product
        """
        if self.applies_to == 'ENTIRE_ORDER':
            return True
        elif self.applies_to == 'SPECIFIC_PRODUCTS':
            return self.products.filter(pk=product.pk).exists()
        elif self.applies_to == 'SPECIFIC_CATEGORIES':
            return self.categories.filter(pk=product.category.pk).exists()
        return False
    
    def calculate_discounted_price(self, product):
        """
        Calculate discounted price for a product
        """
        if self.discount_type == 'PERCENTAGE':
            return int(product.price * (1 - self.value / 100))
        elif self.discount_type == 'FIXED_AMOUNT':
            return max(0, product.price - int(self.value))
        return product.price

    def increment_uses(self):
        self.uses_count = models.F('uses_count') + 1
        self.save(update_fields=['uses_count'])

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"


class AppliedDiscount(models.Model):
    # Assuming you have an 'Order' model, likely in an 'orders' app.
    # If your Order model is in a different app or named differently, adjust the ForeignKey.
    # For now, using a placeholder string. You'll need to resolve this when 'orders' app is ready.
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='applied_discounts_records', verbose_name="Order")
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, verbose_name="Discount Applied") # PROTECT to prevent deleting a discount that was used
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Saved")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Applied At")

    def __str__(self):
        return f"{self.discount.name} on Order #{self.order_id} (Saved: {self.amount_saved})"

    class Meta:
        verbose_name = "Applied Discount Record"
        verbose_name_plural = "Applied Discount Records"
