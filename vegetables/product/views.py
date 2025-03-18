from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from unfold.views import UnfoldModelAdminViewMixin
from django.urls import path
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from unfold.views import UnfoldModelAdminViewMixin
from .filters import ProductFilter
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from unfold.views import UnfoldModelAdminViewMixin
from .models import Product
'''class CustomAdminView(UnfoldModelAdminViewMixin, TemplateView):
    template_name = 'admin/custom_admin_page.html'  # Path to your custom template
    title = "Product List"
    permission_required = ('product.view_product',)  # Replace with your actual permission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()  # Fetch all products
        context['products'] = products  # Add the products to the context
        context['add_url'] = reverse('admin:product_product_add')
        return context

    def availability_status(self, obj):
        return obj.get_availability_display()
    availability_status.short_description = 'Status'''
    
    
class OutOfStockProductsView(UnfoldModelAdminViewMixin, TemplateView):
    template_name = "admin/out_of_stock_products.html"
    title = "Out-of-Stock Products"
    permission_required = ('product.view_product',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(stock=0)  # Filter out-of-stock products
        return context
    
    
    
class FeaturedProductsView(UnfoldModelAdminViewMixin, TemplateView):
    template_name = "admin/featured_products.html"
    title = "Featured Products"
    permission_required = ('product.view_product',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_featured=True)  # Filter featured products
        return context    
    
    
    
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProductType, Category, Product
from .serializers import ProductTypeSerializer, CategorySerializer, ProductSerializer

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination
from rest_framework.permissions import AllowAny
from .models import ProductType, Category, Product
from rest_framework.views import APIView
from .serializers import ProductTypeSerializer, CategorySerializer, ProductSerializer
class CustomPagination(pagination.PageNumberPagination):
    page_size = 12  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    # Remove or comment out any permission_classes here
    # permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = Category.objects.all().prefetch_related('children')
    serializer_class = CategorySerializer

class SubCategoriesView(viewsets.ViewSet):
    permission_classes = [AllowAny] 
    def list(self, request, category_id=None):
        try:
            category = Category.objects.get(id=category_id)
            subcategories = category.get_children()
            return Response([{"id": sub.id, "name": sub.name} for sub in subcategories])
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)
#http://localhost:8000/api/category-products/2/        
class CategoryProductsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny] 
    def list(self, request, category_id=None):
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    #filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'category__slug': ['exact'],
        'price': ['gte', 'lte'],
    }
     # Allow anyone to access this endpoint
    # Remove or comment out any permission_classes here
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def featured(self, request):
        """
        Endpoint to get featured products.
        """
        featured_products = Product.objects.filter(...)  # Add your logic to determine featured products
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def related(self, request):
        """
        Endpoint to get related products for a specific product.
        """
        product = self.get_object()
        related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]  # Example
        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def product_detail(self, request, slug=None):  #Removed `pk=None`, using slug
        """
        Custom action to retrieve product details by slug.
        """
        permission_classes = [AllowAny]
        product = self.get_object()  # This now uses the lookup_field ('slug')
        serializer = ProductPageSerializer(product)
        return Response(serializer.data)
    
    
    
from .serializers import ProductPageSerializer
from rest_framework import generics
class ProductPageView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductPageSerializer
    lookup_field = 'slug'  # Use slug instead of pk    