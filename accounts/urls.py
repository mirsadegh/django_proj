from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
                    RegisterView, 
                    EmailLoginView,
                    ActivateAccountView, 
                    PasswordResetRequestView, 
                    PasswordResetConfirmView,
                    )


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
