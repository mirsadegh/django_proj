
from interests.models import Interest  # مدل مربوط به علاقه‌مندی‌ها را ایمپورت کنید

def total_interests(request):
    if request.user.is_authenticated:
        return {'total_interests': Interest.objects.filter(user=request.user).count()}
    return {'total_interests': 0}