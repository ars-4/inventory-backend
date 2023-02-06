from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.models import Product, OrderProduct, Order, Balance
from core.serializers import ProductSerializer, OrderProductSerializer, OrderSerializer, BalanceSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = '__all__'

    def get_queryset(self):
        try:
            return Product.objects.all()
        except:
            return None

    def create(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "error": "false",
                "data": serializer.data
            })
        else:
            return Response({
                "error": "true"
            })


@api_view(['POST'])
def stock_product(request):
    data = request.data
    try:
        product_id = int(data.get("product_id"))
        method = data.get("method")
        stock = int(data.get("stock"))
        msg = ""
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product, many=False)
    except Exception as error:
        return Response({
            "error": "true",
            "message": str(error)
        })
    if method == 'stock_in':
        product.stock = str(int(product.stock) + stock)
        product.save()
        msg = "Stocked In"

    elif method == 'stock_out':
        product.stock = str(int(product.stock) - stock)
        product.save()
        msg = "Stocked Out"
    
    else:
        return Response({
            "error": "true",
            "message": "Method type not found, try \'stock_in\' or \'stock_out\'"
        })

    return Response({
        "error": "false",
        "message": msg,
        "data": serializer.data
    })



class OrderProductViewSet(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = '__all__'

    def get_queryset(self):
        try:
            return OrderProduct.objects.all()
        except:
            return None

    def create(self, request):
        data = request.data
        serializer = OrderProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "error": "false",
                "data": serializer.data
            })
        else:
            return Response({
                "error": "true"
            })


