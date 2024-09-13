from django.urls import path , include
from .views import VendorCreateView, VendorUpdateView, VendorListView, VendorDeleteView 
from django.contrib.auth import views as auth_views

#from vegetables.settings import ung

urlpatterns = [
    path('vendors/add/', VendorCreateView.as_view(), name='vendor-add'),
    path('vendors/<int:pk>/edit/', VendorUpdateView.as_view(), name='vendor-edit'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/delete/', VendorDeleteView.as_view(), name='vendor-delete'),

    path('vendors/login/', auth_views.LoginView.as_view(template_name='vendors/login.html'), name='vendor_login'),



]
