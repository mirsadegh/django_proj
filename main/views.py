from django.shortcuts import render
from django.views import View
from .models import Product
from django.views.generic import DetailView


class Index(View):
    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        context = {'products': products}
        return render(request, self.template_name, context=context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/detail.html'
    context_object_name = 'product'  # Default is 'object'
    slug_field = 'slug'  # Use 'pk' if using ID
    slug_url_kwarg = 'slug'  # URL parameter name



