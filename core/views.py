from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from core.models import Product, OrderProduct, Order, Balance
from core.serializers import ProductSerializer, OrderProductSerializer, OrderSerializer, BalanceSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.queryset

    def create(self, request):
        data = request.data
        serializer = ProductSerializer(self.get_object, many=False, data=data)
        if serializer.is_valid():
            return Response({
                "error": "false",
                "data": serializer.data
            })
        else:
            return Response({
                "error": "true"
            })
        
