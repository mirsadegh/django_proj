from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)

class AccountActivationEmailSender:
    """
    کلاسی برای ارسال ایمیل فعال‌سازی حساب کاربری.
    """

    def __init__(self, request, user, template_name='accounts/account_activation_email.html'):
        self.request = request
        self.user = user
        self.template_name = template_name
        self.current_site = get_current_site(request)

    def _generate_uid(self):
        """تولید UID کدگذاری شده برای کاربر"""
        return urlsafe_base64_encode(force_bytes(self.user.pk))

    def _generate_token(self):
        """تولید توکن فعال‌سازی (باید در خارج تعریف شده باشد)"""
        from accounts.tokens import account_activation_token  # یا هر جایی که توکن شما تعریف شده
        return account_activation_token.make_token(self.user)

    def _render_email_body(self):
        """رندر کردن بدنه ایمیل با استفاده از تمپلیت"""
        context = {
            'user': self.user,
            'domain': self.current_site.domain,
            'uid': self._generate_uid(),
            'token': self._generate_token(),
        }
        return render_to_string(self.template_name, context)

    def send(self):
        """ارسال ایمیل فعال‌سازی"""
        try:
            subject = _('Activate your account')
            message = self._render_email_body()
            to_email = [self.user.email]

            email = EmailMessage(subject, message, to=to_email)
            email.content_subtype = "html"  # اگر تمپلیت HTML است
            sent = email.send()

            if sent:
                logger.info(f"Activation email sent to {self.user.email}")
                return True
            else:
                logger.warning(f"Failed to send activation email to {self.user.email}")
                return False

        except Exception as e:
            logger.error(f"Error sending activation email to {self.user.email}: {e}")
            return False