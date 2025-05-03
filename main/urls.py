from django.urls import path, re_path
from .views import (
                    Index, 
                    ProductDetailView, 
                    RatingSubmitView, 
                    CommentSubmitView,
                    SearchView,
)


urlpatterns = [
    path('', Index.as_view() , name="index"),
    path('search/', SearchView.as_view(), name='search'),
    re_path(r'^detail/(?P<slug>[\w-]+)/?$', ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^product/(?P<product_slug>[\w\-\u0600-\u06FF]+)/rate/$', RatingSubmitView.as_view(), name='submit_rating'),
    re_path(r'^product/(?P<product_slug>[\w\-\u0600-\u06FF]+)/comment/$', CommentSubmitView.as_view(), name='submit_comment'),
    
]
