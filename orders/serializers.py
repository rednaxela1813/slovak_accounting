from rest_framework import serializers
from .models import Product, Order, OrderItem




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']       
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']
        read_only_fields = ['id', 'order']
        
        


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'updated_at', 'total_price', 'status', 'items']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_price']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create()
        total = 0
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total += order_item.product.price * order_item.quantity
        order.total_price = total
        order.save()
        return order
    