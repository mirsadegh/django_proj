from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views
from .forms import EmailAuthenticationForm



class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    pending_template_name = 'accounts/registration_pending.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return render(request, self.pending_template_name)
        return render(request, self.template_name, {'form': form})



class LoginCustomView(views.LoginView):
    template_name = 'accounts/login.html'
    form_class=EmailAuthenticationForm
    



class ActivateAccountView(View):
    invalid_template_name = 'accounts/activation_invalid.html'
    success_redirect = 'home'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        print(user)
        print(account_activation_token.check_token(user, token))
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            user.backend = 'accounts.backends.EmailAuthBackend' 
            login(request, user)
            return redirect(self.success_redirect)
        else:
            return render(request, self.invalid_template_name)


class PasswordResetRequestView(View):
    template_name = 'accounts/password_reset_form.html'
    done_template_name = 'accounts/password_reset_done.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
        except CustomUser.DoesNotExist:
            pass

        return render(request, self.done_template_name)


class PasswordResetConfirmView(View):
    invalid_template_name = 'users/password_reset_invalid.html'
    confirm_template_name = 'users/password_reset_confirm.html'
    success_redirect = 'login'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            return render(request, self.confirm_template_name)
        else:
            return render(request, self.invalid_template_name)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            return redirect(self.success_redirect)
        else:
            return render(request, self.invalid_template_name)

