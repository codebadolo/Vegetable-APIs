# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product, Category
from orders.models import  Promotion, Wishlist
from product.serializers import ProductSerializer, CategorySerializer 
from orders.models import Order, Transaction, Customer , OrderItem 
from orders.serializers import PromotionSerializer 
class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class FeaturedProductView(APIView):
    def get(self, request):
        products = Product.objects.filter(featured=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class PromotionView(APIView):
    def get(self, request):
        promotions = Promotion.objects.filter(active=True)
        serializer = PromotionSerializer(promotions, many=True)
        return Response(serializer.data)

class MostWishedProductView(APIView):
    def get(self, request):
        # Fetch the most wished product based on Wishlist model
        most_wished = Wishlist.objects.all().order_by('-products__count').first()
        product = most_wished.products.first()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class RecommendationsView(APIView):
    def get(self, request):
        # Fetch recommendations based on user wishlist
        user = request.user
        wishlist = Wishlist.objects.filter(user=user).first()
        if wishlist:
            products = wishlist.products.all()
            recommended_products = Product.objects.filter(category__in=[p.category for p in products])
            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data)
        return Response([])
    
class HeroPromotionView(APIView): # Hero promotion only
    def get(self, request):
        promotion = Promotion.objects.filter(active=True, is_hero=True).first()
        serializer = PromotionSerializer(promotion)
        return Response(serializer.data)
        
class FeaturedCategoriesView(APIView):
    def get(self, request):
        featured_categories = Category.objects.filter(featured=True)
        serializer = CategorySerializer(featured_categories, many=True)
        return Response(serializer.data)

class FeaturedProductsView(APIView):
    def get(self, request):
        featured_products = []
        featured_categories = Category.objects.filter(featured=True)
        for category in featured_categories:
            category_products = Product.objects.filter(category=category, featured=True)[:3] # Fetch first 3 featured products
            featured_products.extend(category_products)
        serializer = ProductSerializer(featured_products, many=True)
        return Response(serializer.data)    