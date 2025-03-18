from rest_framework import serializers
from .models import Order, OrderItem, Customer, Card, Wishlist, Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'gestionnaire', 'total_price', 'status', 'created_at', 'items']

class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'gestionnaire', 'code', 'discount_type', 'discount_value', 'active', 'start_date', 'end_date', 'usage_limit']