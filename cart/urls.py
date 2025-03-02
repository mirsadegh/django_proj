# store/urls.py
from django.urls import path
from .views import  (
                      AddToCartAjaxView,
                      RemoveFromCartView, 
                      CartView, 
                      UpdateCartView,
                      CartDropdownView, 
                    )

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='shopping_cart'),
    path('add/<int:product_id>/', AddToCartAjaxView.as_view(), name='add_to_cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),  
    path("update/<int:product_id>/", UpdateCartView.as_view(), name="update_cart"),
    path("dropdown/", CartDropdownView.as_view(), name="cart_dropdown"),
]
