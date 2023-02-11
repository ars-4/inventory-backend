from django.contrib import admin
from core.models import Product, OrderProduct, Order, Balance, Person

registered_models = [
    Product,
    OrderProduct,
    Order,
    Balance,
    Person
]

admin.site.register(registered_models)
