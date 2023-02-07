from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.models import Product, OrderProduct, Order, Balance
from core.serializers import ProductSerializer, OrderProductSerializer, OrderSerializer, BalanceSerializer
from core.utils import generate_from_order_product, generate_profit, generate_expense, generate_sale, get_total_cash, equalize


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
        product=Product.objects.get(id=int(data.get('product')))
        quantity = data.get('quantity')
        order_product = generate_from_order_product(product.id, quantity)
        # sale_bill = int(product.sale_price) * int(quantity)
        # purchase_bill = int(product.purchase_price) * int(quantity)
        # order_product = OrderProduct.objects.create(
        #     product=product,
        #     quantity=quantity,
        #     sale_bill=str(sale_bill),
        #     purchase_bill=str(purchase_bill)
        # )
        # order_product.save()
        # generate_sale(sale_bill)
        # generate_profit(sale_bill-purchase_bill)
        # equalize(sale_bill, purchase_bill)
        serializer = OrderProductSerializer(order_product, many=False)
        return Response({
            "error":"false",
            "data": serializer.data
        })



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = '__all__'

    def get_queryset(self):
        try:
            return self.queryset
        except:
            return None

    def create(self, request):
        data = request.data
        order_products = data.get("order_products")
        description = ""
        product_existence = True
        sale = 0
        purchase = 0
        order = Order.objects.create(
            customer_name=data.get('customer_name')
        )
        for product_order in order_products:
            try:
                prod = Product.objects.get(id=int(product_order[0]))
                qty = product_order[1]
                order_product = generate_from_order_product(prod.id, qty)
                sale = sale + int(order_product.sale_bill)
                purchase = purchase + int(order_product.purchase_bill)
                description = description + " " + qty + " " + prod.title + ",\n"
                order.products.add(order_product)
            except Exception:
                product_existence = False
                break;
        
        order.description = description
        order.sale = str(sale)
        order.purchase = str(purchase)

        try:
            if product_existence:
                order.save()
                serializer = OrderSerializer(order, many=False)
                return Response({
                    "error": "false",
                    "data": serializer.data
                })
            else:
                return Response({
                    "error": "true",
                    "data": "No such product"
                })
        except Exception as error:
            return Response({
                "error": "true",
                "data": str(error)
            })


