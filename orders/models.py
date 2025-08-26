from django.db import models
from django.conf import settings
from django.utils import timezone

# If you have a custom user model, ensure it's correctly imported
# from accounts.models import CustomUser (Example)
# Otherwise, settings.AUTH_USER_MODEL will be used by default for ForeignKey to User

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Or models.CASCADE if orders should be deleted with user
        null=True,  # Allow orders for guest users or if user is deleted
        blank=True,
        verbose_name="User"
    )
    # Basic address fields - you might want a separate Address model later
    first_name = models.CharField(max_length=100, verbose_name="اسم")
    last_name = models.CharField(max_length=100, verbose_name="فامیلی")
    email = models.EmailField(verbose_name="ایمیل")
    address = models.CharField(max_length=250, verbose_name="ادرس")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    city = models.CharField(max_length=100, verbose_name="شهر")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=" ایجاد شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    paid = models.BooleanField(default=False, verbose_name="Paid")
    
    # Store the total amount of the order after discounts
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    
    # You might want to add fields for shipping, payment details, etc. later

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"سفارش  {self.id} بوسیله {self.user.get_username() if self.user else 'مهمان'}"

# You would also typically have an OrderItem model:
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey('main.Product', related_name='order_items', on_delete=models.CASCADE) # Adjust 'main.Product' if needed
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return str(self.id)
#
#     def get_cost(self):
#         return self.price * self.quantity