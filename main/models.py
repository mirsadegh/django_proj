from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="دسته‌بندی")
    

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



class Laptop(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='laptop_details',
        verbose_name="محصول مرتبط"
    )
    cpu = models.CharField(max_length=100, verbose_name="پردازنده")
    ram = models.CharField(max_length=50, verbose_name="حافظه رم")
    storage = models.CharField(max_length=50, verbose_name="حافظه داخلی")
    screen_size = models.CharField(max_length=50, verbose_name="اندازه صفحه نمایش")

    def __str__(self):
        return f"Laptop: {self.product.title}"
    
    class Meta: 
        verbose_name = 'لپ تاپ'
        verbose_name_plural = 'لپتاپ ها'

# مدل موبایل - فیلدهای اختصاصی موبایل
class Mobile(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='mobile_details',
        verbose_name="محصول مرتبط"
    )
    os = models.CharField(max_length=50, verbose_name="سیستم عامل")
    camera = models.CharField(max_length=50, verbose_name="دوربین")
    battery = models.CharField(max_length=50, verbose_name="باتری")
    screen_resolution = models.CharField(max_length=50, verbose_name="رزولوشن صفحه نمایش")

    def __str__(self):
        return f"Mobile: {self.product.title}"
    
    class Meta: 
        verbose_name = 'گوشی'
        verbose_name_plural = 'گوشیها'






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
