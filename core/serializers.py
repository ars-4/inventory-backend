from core.models import Product, OrderProduct, Order, Balance
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField('%Y-%m-%d,%H:%M:%S')
    date_updated = serializers.DateTimeField('%Y-%m-%d,%H:%M:%S')
    class Meta:
        model = Balance
        fields = '__all__'

