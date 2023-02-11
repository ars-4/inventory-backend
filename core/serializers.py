from core.models import Product, OrderProduct, Order, Balance, Person
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'groups']


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'user', 'date_created', 'date_updated']


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
    date_created = serializers.DateTimeField('%Y-%m-%d')
    date_updated = serializers.DateTimeField('%Y-%m-%d,%H:%M:%S')
    class Meta:
        model = Balance
        fields = '__all__'

