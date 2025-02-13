from django.shortcuts import render
from django.views import View
from .models import Product



class Index(View):
    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        context = {'products': products}
        return render(request, self.template_name, context=context)


