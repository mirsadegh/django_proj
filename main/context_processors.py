
from interests.models import Interest
from cart.cart import Cart

def total_interests(request):
    if request.user.is_authenticated:
        return {'total_interests': Interest.objects.filter(user=request.user).count()}
    return {'total_interests': 0}

def cart(request):
    return {'cart': Cart(request)}