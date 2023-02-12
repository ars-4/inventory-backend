from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
# from core.filters import BalanceFilter
from core.models import Product, OrderProduct, Order, Balance, Person
from core.serializers import ProductSerializer, OrderProductSerializer, OrderSerializer, BalanceSerializer, PersonSerializer
from core.utils import generate_from_order_product, generate_profit, generate_expense, generate_sale, get_total_cash, equalize
from core.auth import get_or_create_token


@api_view(['POST'])
def get_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            person = Person.objects.get(user=user)
            serializer = PersonSerializer(person, many=False)
            token = get_or_create_token(user)
            type = user.groups.all()[0]
            return Response({
                "error":"false",
                "data": serializer.data,
                "token": str(token),
                "type": str(type)
            })
        else:
            return Response({
                "error":"true",
                "data": "User passsword is wrong"
            })
    except Exception as err:
        return Response({
            "error":"true",
            "data":str(err)
        })
    


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['user__groups', 'first_name', 'last_name', 'date_created']

    def get_queryset(self):
        # queryset = Person.objects.filter(user__groups=Group.objects.get(id=2))
        return self.queryset


    def create(self, request):
        data = request.data
        user_exist = False
        for user in User.objects.all():
            if user.username == data.get('username'):
                user_exist = True
        
        if user_exist == False:

            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password')
            )
            try:
                user.save()
                user.groups.add(Group.objects.get(id=int(data.get('role'))))
                person = Person.objects.create(
                    user=user,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    email=user.email,
                    address=data.get('address')
                )
                person.save()
                serializer = PersonSerializer(person, many=False)
                return Response({
                    "error":"false",
                    "data":serializer.data
                })
            except Exception as err:
                return Response({
                    "error":"false",
                    "data":str(err)
                })
        else:
            return Response({
                    "error":"false",
                    "data":"User already exists"
                })



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = '__all__'

    def get_queryset(self):
        # print(self.request.user.groups.all()[0])
        try:
            return Product.objects.all()
        except:
            return None

    def create(self, request):
        data = request.data
        if request.user.groups.all()[0] == Group.objects.get(id=1):
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
        else:
            return Response({
                "error":"true",
                "data":"User must be admin"
            })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

        if cash_in_hand < int(product.purchase_price) * stock:
            return Response({
                "error":"true",
                "data":"Cuurent cash must be equal or greater then product purchase price"
            })
        
        else:
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


    except Exception as error:
        return Response({
            "error": "true",
            "message": str(error)
        })



class OrderProductViewSet(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
        user = Person.objects.get(user__username=data.get('customer_name'))
        description = ""
        product_existence = True
        sale = 0
        purchase = 0
        order = Order.objects.create(
            customer_name=user
        )
        for product_order in order_products:
            try:
                prod = Product.objects.get(id=int(product_order[0]))
                qty = product_order[1]
                cash_in_hand = get_total_cash()
                if cash_in_hand < int(prod.purchase_price) * int(qty):
                    return Response({
                        "error":"true",
                        "data":"Current cash balance must be greater or equal to purchase bill"
                    })
                else:
                    order_product = generate_from_order_product(prod.id, qty)
                    sale = sale + int(order_product.sale_bill)
                    purchase = purchase + int(order_product.purchase_bill)
                    description = description + " " + qty + " " + prod.title + ",\n"
                    order.products.add(order_product)
            except Exception as err:
                product_existence = False
                return Response({
                    "error":"true",
                    "data":str(err)
                })
        
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

    def destroy(self):
        instance = self.get_object()
        print(instance)
        return Response({
            "data":"yes"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_order(request):
    params = request.query_params
    if params.get('pk') is not None:
        order_id = params.get('pk')
        order = Order.objects.get(id=int(order_id))
        profits = Balance.objects.filter(balance='profit')
        current_profit = 0
        for product in order.products.all():
            prod = Product.objects.get(id=int(product.product.id))
            prod.stock = int(prod.stock) + int(product.quantity)
            prod.save()
            product.delete()
        
        for profit in profits:
            current_profit = current_profit + int(profit.bill)
        
        current_profit = current_profit - int(order.sale)
        equal_amount = current_profit / profits.count()
        for profit in profits:
            profit.bill = str(equal_amount)
            profit.save()
        order.delete()
        return Response({
            "error":"false",
            "data":"Order returned successfully"
        })
    else:
        return Response({
            "error":"true",
            "data":"No primary key found"
        })


class BalanceViewSet(ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = '__all__'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balances_by_date(request):
    params = request.query_params
    balances = Balance.objects.all()

    if params.get('start') is not None and params.get('end') is not None:
        balances = Balance.objects.filter(date_created__date__lte=params.get('end'), date_created__date__gte=params.get('start'))

    serializer = BalanceSerializer(balances, many=True)
    print(balances)
    return Response({
        "error":"false",
        "data": serializer.data
    })
