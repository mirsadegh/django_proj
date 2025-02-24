from django.urls import path
from .views import InterestListView, ProductInterestListView, ToggleInterestView, InterestDeleteView

app_name = 'interests'

urlpatterns = [
    path('', 
         InterestListView.as_view(), 
         name='interest_list'),
    
    path('product/<int:pk>/interests/', 
         ProductInterestListView.as_view(), 
         name='product_interest_list'),
    
    path('product/<int:product_id>/toggle-interest/',
         ToggleInterestView.as_view(),name='toggle_interest'),
         
    path('interest/<int:pk>/delete/',
          InterestDeleteView.as_view(), name='interest_delete'),
]