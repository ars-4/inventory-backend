from django.contrib import admin
from core.models import Product, OrderProduct, Order, Balance

registered_models = [
    Product,
    OrderProduct,
    Order,
    Balance
]

admin.site.register(registered_models)
