# urls.py
from django.urls import path
from .views import CategoryView, FeaturedProductView, PromotionView, MostWishedProductView, RecommendationsView
from . import views
urlpatterns = [
    path('api/categories/', CategoryView.as_view()),
    path('api/featured-products/', FeaturedProductView.as_view()),
    path('api/promotions/', PromotionView.as_view()),
    path('api/most-wished-product/', MostWishedProductView.as_view()),
    path('api/recommendations/', RecommendationsView.as_view()),
      path('api/promotions/hero/', views.HeroPromotionView.as_view(), name='hero-promotion'),
       path('api/featured-categories/', views.FeaturedCategoriesView.as_view(), name='featured-categories'),
    path('api/featured-products/', views.FeaturedProductsView.as_view(), name='featured-products'),
]
