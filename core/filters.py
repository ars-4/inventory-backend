from django_filters.rest_framework import DjangoFilterBackend
from core.models import Product

class ProductFilter(DjangoFilterBackend):
    class Meta:
        model = Product
        fields = '__all__'