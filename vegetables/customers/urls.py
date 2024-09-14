from django.urls import path
from .views import (
    CustomerSignupView, CustomerLoginView, CustomerProfileView, ChangePasswordView
)

urlpatterns = [
    path('signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('login/', CustomerLoginView.as_view(), name='customer-login'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
