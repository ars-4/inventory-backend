from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='ProductsPage')

urlpatterns = [
    path('', include(router.urls))
]
