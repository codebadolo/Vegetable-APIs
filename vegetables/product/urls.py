from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'product-types', views.ProductTypeViewSet, basename='product-type')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'subcategories/<int:category_id>', views.SubCategoriesView, basename='subcategories')
urlpatterns = [
    path('', include(router.urls)),
     
]
