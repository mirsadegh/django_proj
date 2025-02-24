from django.db import models
from django.contrib.auth import get_user_model
from main.models import Product
from django.utils import timezone

User = get_user_model()


class Interest(models.Model):
    product = models.ForeignKey(Product, related_name='interests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='interests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True)
    
    class Meta:
        unique_together = ['product', 'user']  # Prevent duplicate interests
        verbose_name = "علاقمند"
        verbose_name_plural = "علاقمندی ها"
        
    
    def __str__(self):
        return f"{self.user.name}'s interest in {self.product.title}"
    

