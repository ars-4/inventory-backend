from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .consumer import OrderConsumer
from core import views

router = DefaultRouter()

router.register('persons', views.PersonViewSet, basename='PersonsPage')
router.register('products', views.ProductViewSet, basename='ProductsPage')
router.register('order_products', views.OrderProductViewSet, basename='OrderProductsPage')
router.register('orders', views.OrderViewSet, basename='OrdersPage')
router.register('balances', views.BalanceViewSet, basename='BalancesPage')

urlpatterns = [
    path('auth/', views.get_token, name='GetTokenView'),

    path('', include(router.urls)),

    path('product/stock/', views.stock_product, name='ProductStockInOut'),
    path('order/', views.delete_order, name='DeleteOrder'),
    path('balance/', views.get_balances_by_date, name='GetBalancesByDate')
]

websocket_urlpatterns = [
    re_path(r"ws/chats/(?P<room_name>\w+)/$", OrderConsumer.as_asgi()),
]
