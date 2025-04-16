from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(null=True, blank=True,
                            max_length=150,  verbose_name=_('نام کاربر'))
    email = models.EmailField(unique=True, verbose_name=_("ایمیل"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    is_staff = models.BooleanField(default=False, verbose_name=_("کارمند"))
    is_verified = models.BooleanField(
        default=False, verbose_name=_("تایید ایمیل"))
    phone_number = models.CharField(
        max_length=10, null=True, blank=True, verbose_name=_("شماره تلفن"))
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name=_("تاریخ تولد"))

    class Meta:
        verbose_name = _('کاربر ')
        verbose_name_plural = _('کاربران ')

    def __str__(self):
        return self.email

    def get_username(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', verbose_name=_("کاربر"))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("تصویر پروفایل"))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("بیوگرافی"))
    location = models.CharField(max_length=100, blank=True, verbose_name=_("موقعیت مکانی"))
    website = models.URLField(max_length=200, blank=True, verbose_name=_("وبسایت"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("پروفایل")
        verbose_name_plural = _("پروفایل‌ها")

    def __str__(self):
        return f"{self.user.email}'s profile"







