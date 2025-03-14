from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Gestionnaire
from .serializers import GestionnaireSerializer
from django.shortcuts import render
from orders.models import Order
from product.models import Product
from orders.models import Customer, OrderItem
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from datetime import datetime

class GestionnaireCreateView(generics.CreateAPIView):
    queryset = Gestionnaire.objects.all()
    serializer_class = GestionnaireSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

class GestionnaireUpdateView(generics.UpdateAPIView):
    queryset = Gestionnaire.objects.all()
    serializer_class = GestionnaireSerializer
    permission_classes = [IsAdminUser]

class GestionnaireListView(generics.ListAPIView):
    queryset = Gestionnaire.objects.all()
    serializer_class = GestionnaireSerializer
    permission_classes = [IsAdminUser]

class GestionnaireDeleteView(generics.DestroyAPIView):
    queryset = Gestionnaire.objects.all()
    serializer_class = GestionnaireSerializer
    permission_classes = [IsAdminUser]

def gestionnaire_dashboard_view(request):
    """Gestionnaire operational dashboard"""
    context = {
        'managed_products': Product.objects.filter(gestionnaire=request.user.gestionnaire).count(),
        'pending_orders': Order.objects.filter(gestionnaire=request.user.gestionnaire, status='pending').count(),
        'completed_orders': Order.objects.filter(gestionnaire=request.user.gestionnaire, status='shipped').count()
    }
    return render(request, 'gestionnaires/dashboard.html', context)

class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Global platform statistics
        time_threshold = timezone.now() - timedelta(days=30)
        
        context.update({
            'total_gestionnaires': Gestionnaire.objects.count(),
            'active_products': Product.objects.filter(availability='available').count(),
            'recent_orders': Order.objects.select_related('customer')
                                  .filter(created_at__gte=time_threshold)
                                  .order_by('-created_at')[:10],
            'top_products': OrderItem.objects.values('product__name')
                                  .annotate(total_sales=Sum('quantity'))
                                  .order_by('-total_sales')[:5],
            'customer_growth': Customer.objects.filter(created_at__gte=time_threshold).count(),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, 'admin/access_denied.html')
        return super().dispatch(request, *args, **kwargs)
