from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('created/', views.OrderSummaryView.as_view(), name='order_created_summary'),
    # Add other order-related URLs here, e.g., order history, order detail
]
