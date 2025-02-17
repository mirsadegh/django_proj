from django.urls import path, re_path
from .views import Index, ProductDetailView, RatingSubmitView , CommentSubmitView


urlpatterns = [
    path('', Index.as_view() , name="index"),
    re_path(r'^detail/(?P<slug>[\w-]+)/?$', ProductDetailView.as_view(), name='product_detail'),
    path('product/<slug:product_slug>/rate/', RatingSubmitView.as_view(), name='submit_rating'),
    path('product/<slug:product_slug>/comment/', CommentSubmitView.as_view(), name='submit_comment'), 
]
