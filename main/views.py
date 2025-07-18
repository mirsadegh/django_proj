from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Rating,Comment, Category
from django.views.generic import DetailView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
import logging
from django.core.paginator import Paginator
from interests.models import Interest
from django.db.models import Prefetch



class Index(View):
    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True).order_by('-created_at')
        context = {}
        if self.request.user.is_authenticated:
            products = products.prefetch_related(
                Prefetch(
                    'interests',
                    queryset=Interest.objects.filter(user=request.user),
                    to_attr='user_interests'
                )
            )
            
            # Create a dictionary of product interests for efficient lookup
            context['product_interests'] = {
                product.id: bool(product.user_interests) 
                for product in products
            }
        context['products'] = products

        return render(request, self.template_name, context=context)
    
        


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/detail.html'
    context_object_name = 'product'  # Default is 'object'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        comments = Comment.objects.filter(status=True).order_by('-created_at')
        context['approved_comments_count'] = comments.count()
        paginator = Paginator(comments, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['average_rating'] = product.average_rating
        context['total_ratings'] = product.total_ratings
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                user=self.request.user,
                product=self.object
            ).first()
            
            context['user_rating'] = user_rating
        return context  # URL parameter name



class RatingSubmitView(LoginRequiredMixin, View):
    """
    Class-based view for handling rating submissions.
    LoginRequiredMixin ensures only authenticated users can submit ratings.
    """
    
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        
        
        try:
            # Get and validate rating value
            
            rating_value = request.POST.get('rating')
            if not rating_value:
                messages.error(request, "لطفا امتیاز را انتخاب کنید.")
                return redirect('product_detail', slug=product_slug)
            
            rating_value = float(rating_value)
      
            
            if not (1.0 <= rating_value <= 5.0):
                messages.error(request, 'امتیاز باید بین ۱ تا ۵ باشد')
                return redirect('product_detail', slug=product_slug)
            
            
    
            with transaction.atomic():
                existing_rating = Rating.objects.filter(user=request.user, product=product).first()

                if existing_rating:
                    existing_rating.rating = rating_value
                    existing_rating.save()
                    messages.success(request, "امتیاز شما با موفقیت بروزرسانی شد.")
                else:
                    Rating.objects.create(
                        user=request.user,
                        product=product,
                        rating=rating_value
                    )

                    messages.success(request, "امتیاز شما با موفقیت ثبت شد.")

                page = request.GET.get('page')
                if page:
                    return redirect(f"{reverse('product_detail', args=[product_slug])}?page={page}")    
                    
                    
     
        except ValueError as ve:
            messages.error(request, f"مقدار امتیاز نامعتبر است.  Error: {ve}")
            logging.error(f"Invalid rating value: {ve}")
            
        except Exception as e:
            messages.error(request, f"خطایی در ثبت امتیاز رخ داد. Error: {e}")
            logging.exception(f"Error saving rating: {e}")
            
        finally:
            return redirect('product_detail', slug=product_slug)

    def get(self, request, product_slug):
        """Handle GET requests by redirecting to product detail"""
       
        return redirect('product_detail', slug=product_slug)
    

class CommentSubmitView(LoginRequiredMixin, View):
    """Handles comment submissions for a product."""

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        comment_text = request.POST.get('comment', '').strip()

        if not comment_text:
            messages.error(request, "لطفا نظر خود را وارد کنید.")
            return redirect('product_detail', slug=product_slug)

        try:
            Comment.objects.create(
                product=product,
                user=request.user,
                text=comment_text
            )
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
            page = request.GET.get('page')
            if page:
                return redirect(f"{reverse('product_detail', args=[product_slug])}?page={page}")
        except Exception as e:
            logging.exception(f"Error saving comment: {e}")
            messages.error(request, f"خطایی در ثبت نظر رخ داد: {e}")
        finally:
            return redirect('product_detail', slug=product_slug)

    def get(self, request, product_slug):
        return redirect('product_detail', slug=product_slug)


class SearchView(View):
    template_name = "main/search.html"
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        category_id = request.GET.get('category', '')
        
        products = Product.objects.filter(available=True)
        
        if query:
            products = products.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category_id:
            products = products.filter(category_id=category_id)
        
        # Paginate results
        paginator = Paginator(products, 12)  # Show 12 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get all categories for the filter dropdown
        categories = Category.objects.all()
        
        # Handle user interests for authenticated users
        if request.user.is_authenticated:
            products = products.prefetch_related(
                Prefetch(
                    'interests',
                    queryset=Interest.objects.filter(user=request.user),
                    to_attr='user_interests'
                )
            )
            
            # Create a dictionary of product interests for efficient lookup
            product_interests = {
                product.id: bool(product.user_interests) 
                for product in products
            }
        else:
            product_interests = {}
            
        context = {
            'products': page_obj,
            'query': query,
            'selected_category': category_id,
            'categories': categories,
            'product_interests': product_interests,
            'total_results': paginator.count
        }
        
        return render(request, self.template_name, context=context)
