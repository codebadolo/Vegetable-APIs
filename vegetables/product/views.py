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
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    # Remove or comment out any permission_classes here
    # permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    ermission_classes = [AllowAny] 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('children')

class SubCategoriesView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            subcategories = category.get_children()  # Fetch subcategories
            return Response([{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories])
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name']  # Enable filtering by category and product_type
    search_fields = ['name', 'description']  # Enable search by name and description
    ordering_fields = ['price', 'name']  # Enable ordering by price and name
    pagination_class = CustomPagination
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