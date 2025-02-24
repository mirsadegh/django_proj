from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Count

from .models import Product, Interest

class InterestListView(LoginRequiredMixin, ListView):
    model = Interest
    template_name = 'interests/interest_list.html'
    context_object_name = 'interests'
    
    def get_queryset(self):
        return Interest.objects.filter(user=self.request.user).select_related('product').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_interests'] = self.get_queryset().count()
        return context

class ProductInterestListView(DetailView):
    model = Product
    template_name = 'interests/product_interest_list.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interested_users'] = self.object.interests.select_related('user')\
            .order_by('-created_at')
        return context

class ToggleInterestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, id=self.kwargs['product_id'])
            
            
            interest = Interest.objects.filter(
                    user=request.user,
                    product=product
                ).first()
            
            if interest:
                    # If interest exists, delete it
                    interest.delete()
                    is_interested = False
            else:
                    # If no interest exists, create it
                    Interest.objects.create(
                        user=request.user,
                        product=product
                    )
                    is_interested = True
                
            data = {
                'is_interested': is_interested,
                'interest_count': product.interests.count(),
                'product_id': product.id
            }
            
            return JsonResponse(data)
        except Exception as e:
            print(f"Error in ToggleInterestView: {str(e)}")  # For debugging
            return JsonResponse({'error': str(e)}, status=400)

class InterestDeleteView(LoginRequiredMixin, DeleteView):
    model = Interest
    success_url = reverse_lazy('interest_list')
    
    def get_queryset(self):
        # Ensure users can only delete their own interests
        return super().get_queryset().filter(user=self.request.user)
    
    