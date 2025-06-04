from django.contrib import admin
from .models import Discount, AppliedDiscount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'code', 
        'discount_type', 
        'value', 
        'is_active', 
        'active_from', 
        'active_until', 
        'uses_count', 
        'max_uses',
        'minimum_cart_value',
        'applies_to'
    )
    list_filter = ('discount_type', 'is_active', 'applies_to', 'active_from', 'active_until')
    search_fields = ('name', 'code', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Discount Details', {
            'fields': ('discount_type', 'value', 'code')
        }),
        ('Conditions & Validity', {
            'fields': ('active_from', 'active_until', 'minimum_cart_value', 'max_uses')
        }),
        ('Applicability', {
            'fields': ('applies_to', 'products', 'categories')
        }),
        ('Usage Tracking', {
            'fields': ('uses_count',),
            'classes': ('collapse',), # Initially collapsed as it's usually not directly edited
        })
    )
    filter_horizontal = ('products', 'categories') # Provides a better UI for ManyToManyFields
    readonly_fields = ('uses_count',)

    def get_queryset(self, request):
        # Prefetch related data for efficiency in the admin list display if needed
        return super().get_queryset(request) #.prefetch_related('products', 'categories')

@admin.register(AppliedDiscount)
class AppliedDiscountAdmin(admin.ModelAdmin):
    list_display = ('order_link', 'discount_link', 'amount_saved', 'applied_at')
    list_filter = ('discount', 'applied_at')
    search_fields = ('order__id', 'discount__name') # Assuming order has an 'id' and discount has 'name'
    readonly_fields = ('order', 'discount', 'amount_saved', 'applied_at') # These are typically system-generated

    def order_link(self, obj):
        # Assuming you have an admin view for your Order model
        # and 'orders' is the app_label and 'order' is the model_name
        # You might need to adjust this if your Order model admin is set up differently
        from django.urls import reverse
        from django.utils.html import format_html
        if obj.order:
            link = reverse(f"admin:{obj.order._meta.app_label}_{obj.order._meta.model_name}_change", args=[obj.order.pk])
            return format_html('<a href="{}">Order #{}</a>', link, obj.order.pk)
        return "N/A"
    order_link.short_description = 'Order'

    def discount_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        if obj.discount:
            link = reverse(f"admin:{obj.discount._meta.app_label}_{obj.discount._meta.model_name}_change", args=[obj.discount.pk])
            return format_html('<a href="{}">{}</a>', link, obj.discount.name)
        return "N/A"
    discount_link.short_description = 'Discount'


    def has_add_permission(self, request):
        # AppliedDiscounts are created by the system when an order is processed, not manually
        return False

    def has_change_permission(self, request, obj=None):
        # Typically, these records are not changed manually
        return False

    # Optional: If you want to allow deletion, remove or comment out has_delete_permission
    # def has_delete_permission(self, request, obj=None):
    #     return False
