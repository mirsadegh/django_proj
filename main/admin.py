from django.contrib import admin

from .models import (
    Category,
    Product, 
    Rating, 
    Comment, 
    ProductImage
                     )

# ثبت مدل دسته‌بندی
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')
    list_filter = ('product_type',)
    

# ثبت مدل محصول (مشترک برای همه محصولات)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('title',)}

# ثبت همه مدل‌ها در پنل ادمین
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(ProductImage)
