from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='ProductsPage')
router.register('order_products', views.OrderProductViewSet, basename='OrderProductsPage')

urlpatterns = [
    path('', include(router.urls)),

    path('product/stock/', views.stock_product, name='ProductStockInOut')
]
