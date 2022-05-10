import datetime
from .models import Order


def instock(product):
    stock = []
    product_list = Order.objects.filter(product=product)
    for product in product_list:
        if product.status=="Cancelled":
            stock.append(True)
        return all(stock)