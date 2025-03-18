from django.urls import path
from .views import OrderListView, OrderDetailView, WishlistView, CouponListView
from . import views
urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
   path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('wishlist/', views.AddToWishlistView.as_view(), name='add-to-wishlist'),
]
