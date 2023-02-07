from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from core import views

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='ProductsPage')
router.register('order_products', views.OrderProductViewSet, basename='OrderProductsPage')
router.register('orders', views.OrderViewSet, basename='OrdersPage')

urlpatterns = [
    path('', include(router.urls)),

    path('product/stock/', views.stock_product, name='ProductStockInOut')
]
