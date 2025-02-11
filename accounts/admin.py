from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ['email']
    list_display = ['name', 'email', 'is_active', 'is_staff', 'is_verified']
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('date_of_birth', 'phone_number')}),
        ('مجوزها', {'fields': ('is_active',
         'is_staff', 'is_superuser', 'is_verified')}),
        ('تاریخ آخرین ورود', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'date_of_birth'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
