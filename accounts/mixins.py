from django.shortcuts import redirect
from django.conf import settings

class AnonymousUserRequiredMixin:
    """
    Mixin that redirects authenticated users away from views intended
    for anonymous users (e.g., login and registration).
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect to a specified URL, e.g., settings.LOGIN_REDIRECT_URL
            return redirect(getattr(settings, 'LOGIN_REDIRECT_URL', 'index'))
        return super().dispatch(request, *args, **kwargs)
    

