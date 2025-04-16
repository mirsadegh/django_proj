from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.conf import settings
 



CustomUser = settings.AUTH_USER_MODEL

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for user {instance}") # پیام برای اشکال‌زدایی


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
        print(f"Profile saved for user {instance}") # پیام برای اشکال‌زدایی
    except Profile.DoesNotExist:
         # این حالت نباید با سیگنال اول اتفاق بیفتد، اما برای اطمینان اضافه شده
         Profile.objects.create(user=instance)
         print(f"Profile did not exist for user {instance}, created now.")
         
         
         