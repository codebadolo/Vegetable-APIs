from django.urls import path , include
from .views import VendorCreateView, VendorUpdateView, VendorListView, VendorDeleteView 
from django.contrib.auth import views as auth_views
from .charts  import  total_sales_over_time, sales_by_product, order_status_distribution
#from vegetables.settings import ung
from .views import vendor_dashboard_view
urlpatterns = [
    path('vendors/add/', VendorCreateView.as_view(), name='vendor-add'),
    path('vendors/<int:pk>/edit/', VendorUpdateView.as_view(), name='vendor-edit'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/delete/', VendorDeleteView.as_view(), name='vendor-delete'),

    path('vendors/login/', auth_views.LoginView.as_view(template_name='vendors/login.html'), name='vendor_login'),
     path('vendor-dashboard/', vendor_dashboard_view, name='vendor_dashboard'),
    
    # Chart data endpoints
    path('charts/total-sales/', total_sales_over_time, name='total_sales_over_time'),
    path('charts/sales-by-product/', sales_by_product, name='sales_by_product'),
    path('charts/order-status/', order_status_distribution, name='order_status_distribution'),

]
