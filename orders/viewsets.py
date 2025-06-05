from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated




class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    
    """
    A viewset for viewing products.
    """
    
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    
class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing orders.
    """
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm an order.
        """
        order = self.get_object()
        if order.status != 'draft':
            return Response({'detail': 'Order cannot be confirmed.'}, status=400)
        
        order.status = 'confirmed'
        order.save()
        return Response({"status": "Order confirmed"}, status=http_status.HTTP_200_OK)
    
