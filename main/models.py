from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    PRODUCT_TYPES = [
        ('general', 'عمومی'),
        ('laptop', 'لپ تاپ'),
        ('mobile', 'گوشی'),
    ]
    
    name = models.CharField(max_length=200, unique=True, verbose_name="دسته‌بندی")
    product_type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPES,
        default='general',
        verbose_name='نوع محصول'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'



class Product(models.Model):
    
    title = models.CharField(max_length=100, verbose_name='عنوان')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="دسته‌بندی"
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name='آدرس یکتا',allow_unicode=True)
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='product_images', verbose_name='تصویر محصول')
    available = models.BooleanField(default=True, verbose_name="موجود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    @property
    def average_rating(self):
        # Calculate average rating using aggregate
        result = self.ratings.aggregate(Avg('rating'))
        return result['rating__avg'] or 0.0

    @property
    def total_ratings(self):
        return self.ratings.count()
        
    @property
    def current_price(self):
        """
        Get current price considering active automatic discounts
        """
        from discounts.models import Discount
        now = timezone.now()
        
        # Find valid automatic discounts for this product
        discounts = Discount.objects.filter(
            is_automatic=True,
            is_active=True,
            active_from__lte=now,
            active_until__gte=now,
        ).filter(
            models.Q(products=self) | 
            models.Q(categories=self.category)
        )
        
        # Apply the first valid discount found
        if discounts.exists():
            return discounts.first().calculate_discounted_price(self)
        return self.price

    @property
    def discount_percentage(self):
        """
        Calculate discount percentage if product is on sale
        """
        if self.current_price < self.price:
            discount_amount = self.price - self.current_price
            return round((discount_amount / self.price) * 100)
        return 0





class Rating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازات"

    def __str__(self):
        return f"{self.user.name}'s {self.rating}-star rating"



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"Comment by {self.user.name} on {self.product.title}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='product_gallery_images', verbose_name='تصویر گالری محصول')

    class Meta:
        verbose_name = 'تصویر گالری محصول'
        verbose_name_plural = 'تصاویر گالری محصول'

    def __str__(self):
        return f"Image for {self.product.title}"


class Specification(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام مشخصه")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='specifications',
        verbose_name="دسته‌بندی"
    )

    class Meta:
        unique_together = ('name', 'category')
        verbose_name = 'مشخصه'
        verbose_name_plural = 'مشخصات'

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_specifications',
        verbose_name="محصول"
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        verbose_name="مشخصه"
    )
    value = models.CharField(max_length=255, verbose_name="مقدار")

    class Meta:
        unique_together = ('product', 'specification')
        verbose_name = 'مشخصه محصول'
        verbose_name_plural = 'مشخصات محصول'

    def __str__(self):
        return f"{self.product.title} - {self.specification.name}: {self.value}"
