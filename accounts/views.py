from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser, Profile
from .tokens import account_activation_token
from .forms import EmailAuthenticationForm
from django.urls import reverse
from .mixins import AnonymousUserRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView

from .forms import ProfileUpdateForm, UserUpdateForm






class EmailLoginView(AnonymousUserRequiredMixin, View):
    form_class = EmailAuthenticationForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Pass the request object!
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(reverse('index'))

        return render(request, self.template_name, {'form': form})


def send_email(request, user):
    try:
        current_site = get_current_site(request)
        mail_subject = _('Activate your account')
        message = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
    except Exception as e:
        # می‌توانید خطا را ثبت کنید یا اقدام مناسب انجام دهید
        print("Error sending email:", e)
        # یا از logging استفاده کنید


class RegisterView(AnonymousUserRequiredMixin, View):
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

            send_email(request, user)

            return render(request, self.pending_template_name, {'email': user.email})
        return render(request, self.template_name, {'form': form})


class ActivateAccountView(View):
    invalid_template_name = 'accounts/activation_invalid.html'
    success_redirect = 'index'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            user.backend = 'accounts.backends.EmailAuthBackend'
            login(request, user)
            return redirect(self.success_redirect)
        else:
            return render(request, self.invalid_template_name)


class ResendActivationEmailView(View):
    template_name = 'accounts/registration_pending.html'

    def get(self, request):
        # اگر می‌خواهید ایمیل را از query string یا به روش دیگری دریافت کنید:
        email = request.GET.get('email')
        return render(request, self.template_name, {'email': email})

    def post(self, request):
        # دریافت ایمیل از فرم
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email, is_active=False)
            send_email(request, user)
            messages.success(
                request, 'ایمیل فعال‌سازی مجدداً ارسال شد. لطفاً صندوق ایمیل خود را بررسی کنید.')
        except CustomUser.DoesNotExist:
            messages.error(
                request, 'کاربری با این ایمیل یافت نشد یا حساب کاربری قبلاً فعال شده است.')

        # مجدداً همان قالب را رندر می‌کنیم تا کاربر در همان صفحه بماند
        return render(request, self.template_name, {'email': email})



class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    extra_email_context = None  # Explicitly set default value

    def get_success_url(self):
        """Append email parameter to success URL"""
        base_url = super().get_success_url()
        email = self.request.POST.get('email', '')
        return f"{base_url}?email={email}"



class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        email = self.request.GET.get('email', '')
        context['email'] = email
        context['email_exists'] = User.objects.filter(email=email).exists()
        return context



class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm  
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):  # Simplified method
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
            context['profile_form'] = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        profile_form = context['profile_form']
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, 'پروفایل شما با موفقیت بروزرسانی شد')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))






