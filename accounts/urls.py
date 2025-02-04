from django.urls import path
from .views import (
                    RegisterView, 
                    LoginCustomView,
                    ActivateAccountView, 
                    PasswordResetRequestView, 
                    PasswordResetConfirmView,
                    )


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', LoginCustomView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
