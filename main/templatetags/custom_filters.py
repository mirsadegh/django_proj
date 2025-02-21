from django import template


register = template.Library()

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


