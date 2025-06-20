from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created_summary, name='order_created_summary'),
    # Add other order-related URLs here, e.g., order history, order detail
]