# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Cart, CartItem, Wishlist
from .serializers import CartItemSerializer, WishlistSerializer
from product.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist, Product , Order ,OrderItem  , Customer , Transaction
from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product)

        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)

class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(user=request.user)

        wishlist.products.add(product)
        return Response({"message": "Product added to wishlist"}, status=status.HTTP_200_OK)
    
    
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart_items = CartItem.objects.filter(cart__user=request.user)
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            serializer = WishlistSerializer(wishlist.products.all(), many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class RemoveFromWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist.products.remove(product_id)
            return Response({"message": "Product removed from wishlist"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
        
class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_item_id = request.data.get('cart_item_id')
            CartItem.objects.get(id=cart_item_id).delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_item_id = request.data.get('cart_item_id')
            quantity = request.data.get('quantity')
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"message": "Cart item updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                 
        
        
        
class CompleteOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.create(customer=customer, total_price=request.data.get('total_price'))
            for cart_item in CartItem.objects.filter(cart__user=request.user):
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
                cart_item.delete()
            Transaction.objects.create(order=order, transaction_id='MockTransactionID', payment_method='card', amount=order.total_price, status='completed')
            return Response({"message": "Order completed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)