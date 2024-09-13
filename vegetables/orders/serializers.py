from rest_framework import serializers
from .models import Order, OrderItem, Customer, Card

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'vendor', 'total_price', 'status', 'items']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'address', 'phone']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['customer', 'card_number', 'expiry_date']
