# urls.py
from django.urls import path
from .views import PromotionView

urlpatterns = [
    path('api/promotions/', PromotionView.as_view(), name='promotions'),
]
