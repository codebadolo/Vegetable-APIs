from django.urls import path, include
from .views import GestionnaireCreateView, GestionnaireUpdateView, GestionnaireListView, GestionnaireDeleteView
from django.contrib.auth import views as auth_views
from .charts import total_sales_over_time, sales_by_product, order_status_distribution
from .views import gestionnaire_dashboard_view
from .custom_views import custom_admin_view
from .views import AdminDashboardView

urlpatterns = [
    path('gestionnaires/add/', GestionnaireCreateView.as_view(), name='gestionnaire-add'),
    path('gestionnaires/<int:pk>/edit/', GestionnaireUpdateView.as_view(), name='gestionnaire-edit'),
    path('gestionnaires/', GestionnaireListView.as_view(), name='gestionnaire-list'),
    path('gestionnaires/<int:pk>/delete/', GestionnaireDeleteView.as_view(), name='gestionnaire-delete'),

    path('gestionnaires/login/', auth_views.LoginView.as_view(template_name='gestionnaires/login.html'), name='gestionnaire_login'),
    path('gestionnaire-dashboard/', gestionnaire_dashboard_view, name='gestionnaire_dashboard'),

    # Chart data endpoints
    path('charts/total-sales/', total_sales_over_time, name='total_sales_over_time'),
    path('charts/sales-by-product/', sales_by_product, name='sales_by_product'),
    path('charts/order-status/', order_status_distribution, name='order_status_distribution'),
    path('custom-page/', custom_admin_view, name='custom_page'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
