from django.contrib import admin

from .models import Category, Product, Laptop, Mobile, Rating, Comment

# ثبت مدل دسته‌بندی
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    

# ثبت مدل محصول (مشترک برای همه محصولات)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('title',)}

# ثبت مدل لپ‌تاپ (مشخصات اختصاصی لپ‌تاپ)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('product', 'cpu', 'ram', 'storage', 'screen_size')
    search_fields = ('product__name', 'cpu')

# ثبت مدل موبایل (مشخصات اختصاصی موبایل)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('product', 'os', 'camera', 'battery', 'screen_resolution')
    search_fields = ('product__name', 'os')

# ثبت همه مدل‌ها در پنل ادمین
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Mobile, MobileAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
