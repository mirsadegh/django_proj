from django import template
from django.utils.safestring import mark_safe
import math

register = template.Library()

@register.simple_tag
def get_discount_percentage(product):
    if product.is_on_sale and product.discount_price:
        discount_percent = (product.price - product.discount_price) / product.price * 100
        return f"{math.floor(discount_percent)}%"
    return ""


@register.filter(name='separate_numbers')
def separate_numbers(number):
    """
    Converts a number into a comma-separated string for Persian/Farsi display
    Example: 1234567 -> 1,234,567
    """

    if number is None:
        return "0"
    
    try:
        number = float(number)
        return "{:,.0f}".format(number)
    except (ValueError, TypeError):
        return "0"



@register.filter(name='persian_numbers')
def persian_numbers(number):
    """
    Converts a number to Persian format with thousands separator
    Example: 1234567 -> ۱,۲۳۴,۵۶۷
    """
    if number is None:
        return "۰"
        
    try:
        number = float(number)
        english_number = "{:,.0f}".format(number)
        
        persian_numbers = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
            ',': '،'  # Optional: Change comma to Persian comma
        }
        
        return ''.join(persian_numbers.get(c, c) for c in english_number)
    except (ValueError, TypeError):
        return "۰"



@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a key.
    Usage: {{ my_dict|get_item:my_key }}
    """
    if dictionary is None:
        return None
    
    try:
        return dictionary.get(key)
    except (KeyError, AttributeError):
        return None


@register.filter
def star_rating(rating):
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0

    full_stars = int(rating)  # تعداد ستاره‌های پر
    half_star = (rating - full_stars) >= 0.5  # وجود نیمه‌ستاره
    empty_stars = 5 - full_stars - (1 if half_star else 0)  # تعداد ستاره‌های خالی

    stars_html = ''
    stars_html += '<i class="fa fa-star"></i>' * full_stars
    if half_star:
        stars_html += '<i class="fa fa-star half-star "></i>'
    stars_html += '<i class="fa fa-star-o"></i>' * empty_stars

    return mark_safe(stars_html)

