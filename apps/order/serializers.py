# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, OrderHistory

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['characteristic', 'quantity', 'display_item_price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_profile', 'created_at', 'status', 'is_paid', 'shipping_address', 'display_total_price', 'order_items']

class OrderHistorySerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = OrderHistory
        fields = ['user_profile', 'orders']
