from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    RegisterView,
    EmailLoginView,
    ActivateAccountView,
    ResendActivationEmailView,
    CustomPasswordResetDoneView,
    PasswordResetView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/',
         ActivateAccountView.as_view(), name='activate'),
    path('resend-activation-email/', ResendActivationEmailView.as_view(),
         name='resend_activation_email'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/',PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
