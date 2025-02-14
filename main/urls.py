from django.urls import path, re_path
from .views import Index, ProductDetailView 


urlpatterns = [
    path('', Index.as_view() , name="index"),
    re_path(r'^detail/(?P<slug>[\w-]+)/?$', ProductDetailView.as_view(), name='product_detail')
]
