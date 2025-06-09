import json
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Product, 
    Rating, 
    Comment, 
    ProductImage,
    Specification,
    ProductSpecification
)

# ثبت مدل دسته‌بندی
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')
    list_filter = ('product_type',)
    

# ثبت مدل محصول (مشترک برای همه محصولات)
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    verbose_name = "مشخصه"
    verbose_name_plural = "مشخصات"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductSpecificationInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Pass product_type to the form for use in JavaScript
        if obj and obj.category:
            form.base_fields['category'].widget.attrs['data-product-type'] = obj.category.product_type
        return form

    def render_change_form(self, request, context, *args, **kwargs):
        # Inject a mapping of category id to product_type for JS
        from .models import Category, Specification
        categories = Category.objects.all()
        
        category_product_types = {
            str(cat.pk): cat.product_type for cat in categories
        }
        context['adminform'].form.fields['category'].widget.attrs['data-product-types'] = category_product_types
        
        # Inject specifications per category for JS
        category_specifications = {}
        for cat in categories:
            category_specifications[str(cat.pk)] = list(
                Specification.objects.filter(category=cat).values('id', 'name')
            )
        context['category_specifications_js'] = mark_safe(
            '<script>window.categorySpecifications = %s;</script>' %
            json.dumps(category_specifications, ensure_ascii=False)
        )
        
        # Also inject category product types as JS variable
        context['category_product_types_js'] = mark_safe(
            '<script>window.categoryProductTypes = %s;</script>' %
            json.dumps(category_product_types, ensure_ascii=False)
        )
        
        return super().render_change_form(request, context, *args, **kwargs)

    class Media:
        js = (
            'admin/js/product_admin_dynamic.js',
        )

admin.site.register(Specification)

# ثبت همه مدل‌ها در پنل ادمین
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(ProductImage)
