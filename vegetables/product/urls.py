from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'product-types', views.ProductTypeViewSet, basename='product-type')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'category-products/(?P<category_id>\d+)', views.CategoryProductsViewSet, basename='category-products')
#router.register(r'subcategories/<int:category_id>', views.SubCategoriesView, basename='subcategories')
router.register(r'subcategories/(?P<category_id>\d+)', views.SubCategoriesView, basename='subcategories')
#router.register(r'product-page/<slug:slug>/' ,views.ProductPageView , basename='product_detail')
urlpatterns = [
    path('', include(router.urls)),
        path('product-page/<slug:slug>/', views.ProductPageView.as_view(), name='product_detail'),
   # path('category-products/<int:category_id>/', views.CategoryProductsView.as_view()),
]
