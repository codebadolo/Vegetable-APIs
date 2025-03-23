from django.urls import path

from . import views
urlpatterns = [
    path('cart/add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('wishlist/add/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
     path('cart/', views.CartView.as_view(), name='cart'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
     path('wishlist/remove/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
       path('cart/remove/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
           path('cart/update/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
           path('complete/', views.CompleteOrderView.as_view(), name='complete_order'),
]
