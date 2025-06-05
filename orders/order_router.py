from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet, OrderViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')



urlpatterns = router.urls
    
