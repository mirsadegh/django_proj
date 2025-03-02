# store/cart.py
from decimal import Decimal
from main.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()


# self.cart = {
#     "1": {"quantity": 2, "price": "25.00"},
#     "5": {"quantity": 1, "price": "50.00"},
#     "12": {"quantity": 3, "price": "10.00"},
#     "20": {"quantity": 1, "price": "15.00"},
#     "35": {"quantity": 2, "price": "30.00"},
#     "42": {"quantity": 1, "price": "20.00"},
#     "58": {"quantity": 4, "price": "5.00"},
#     "61": {"quantity": 1, "price": "75.00"},
#     "73": {"quantity": 2, "price": "12.00"},
#     "89": {"quantity": 1, "price": "40.00"},
# }

# خروجی محصول از تابع __iter__ برای یک محصول به شکل زیر است:
# # تکرار اول (برای محصول با شناسه "1")
# {'quantity': 2, 'price': Decimal('25.00'), 'product': <Product object with ID=1>, 'total_price': Decimal('50.00')}

# # تکرار دوم (برای محصول با شناسه "5")
# {'quantity': 1, 'price': Decimal('50.00'), 'product': <Product object with ID=5>, 'total_price': Decimal('50.00')}

# # تکرار سوم (برای محصول با شناسه "12")
# {'quantity': 3, 'price': Decimal('10.00'), 'product': <Product object with ID=12>, 'total_price': Decimal('30.00')}

# # ... و به همین ترتیب برای 7 محصول بعدی ...

# # تکرار دهم (برای محصول با شناسه "89")
# {'quantity': 1, 'price': Decimal('40.00'), 'product': <Product object with ID=89>, 'total_price': Decimal('40.00')}










