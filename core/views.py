from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.models import Product, OrderProduct, Order, Balance
from core.serializers import ProductSerializer, OrderProductSerializer, OrderSerializer, BalanceSerializer
from core.utils import generate_balances, generate_profit, generate_expense, generate_sale, get_total_cash, equalize


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
        cash_in_hand = get_total_cash()

    except Exception as error:
        return Response({
            "error": "true",
            "message": str(error)
        })
    if method == 'stock_in':
        product.stock = str(int(product.stock) + stock)
        product.save()
        msg = "Stocked In"
        expense = stock * int(product.purchase_price)
        generate_expense(expense)
        equalize(cash_in_hand, expense)
    

    elif method == 'stock_out':
        product.stock = str(int(product.stock) - stock)
        product.save()
        msg = "Stocked Out"
        sale = stock * int(product.sale_price)
        expense = stock * int(product.purchase_price)
        profit = sale - expense
        generate_profit(profit)
        equalize(cash_in_hand, expense)
        generate_sale(sale)
        
    
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
        product = product=Product.objects.get(id=int(data.get('product')))
        quantity = data.get('quantity')
        sale_bill = int(product.sale_price) * int(quantity)
        purchase_bill = int(product.purchase_price) * int(quantity)
        order_product = OrderProduct.objects.create(
            product=product,
            quantity=quantity,
            sale_bill=str(sale_bill),
            purchase_bill=str(purchase_bill)
        )
        order_product.save()
        generate_sale(sale_bill)
        generate_profit(sale_bill-purchase_bill)
        equalize(sale_bill, purchase_bill)
        serializer = OrderProductSerializer(order_product, many=False)
        return Response({
            "error":"false",
            "data": serializer.data
        })


