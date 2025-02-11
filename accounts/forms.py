from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    
    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both "
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """Initialize the form with request context."""
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        """Validate credentials and user status through authentication workflow."""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user_cache = self._authenticate(email, password)
            self.confirm_login_allowed(self.user_cache)

        return cleaned_data

    def _authenticate(self, email: str, password: str):
        """Handle core authentication logic with error reporting."""
        user = authenticate(self.request, email=email, password=password)
        if user is None:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )
        return user

    def confirm_login_allowed(self, user):
        """Verify user account is active and permitted to log in."""
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        """Expose authenticated user instance post-validation."""
        return self.user_cache

    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'        







