from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


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
