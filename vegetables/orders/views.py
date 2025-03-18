from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order, Wishlist, Coupon , OrderItem
from .serializers import OrderSerializer, WishlistSerializer, CouponSerializer
from product.models import Product
from rest_framework.permissions import AllowAny
# Orders API
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:  # Admin can see all orders
            orders = Order.objects.all()
        else:  # Customers see only their orders
            orders = Order.objects.filter(customer__user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new order (e.g., from cart data)
        data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save(customer=request.user.customer)  # Associate with logged-in customer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if request.user.is_staff or order.customer.user == request.user:
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# Wishlist API
class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        product_id = request.data.get('product_id')
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product_id)
        wishlist.save()
        return Response({'message': 'Product added to wishlist'})

    def delete(self, request):
        product_id = request.data.get('product_id')
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist.products.remove(product_id)
            wishlist.save()
            return Response({'message': 'Product removed from wishlist'})
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist not found'}, status=status.HTTP_404_NOT_FOUND)

# Coupon API
class CouponListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        coupons = Coupon.objects.filter(active=True)
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can create coupons'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gestionnaire=request.user.gestionnaire)  # Associate with admin's gestionnaire account
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddToCartView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, status='pending')
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if not created:
                order_item.quantity += int(quantity)
                order_item.save()
            else:
                order_item.quantity = quantity
                order_item.save()
            return Response({'message': 'Added to cart'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class AddToWishlistView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            wishlist.products.add(product)
            return Response({'message': 'Added to wishlist'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        