from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply_coupon/', views.apply_coupon_view, name='apply_coupon'),
    path('remove_coupon/', views.remove_coupon_view, name='remove_coupon'),
    path('clear/', views.clear_cart_view, name='clear_cart'),
    path('dropdown/', views.cart_dropdown, name='cart_dropdown'),
]
