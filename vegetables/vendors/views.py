from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Vendor
from .serializers import VendorSerializer
from django.shortcuts import render
from orders.models import Order
from product.models import Product
from orders.models import Customer , OrderItem
#
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

class VendorCreateView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

    def perform_create(self, serializer):
        # Create vendor with additional admin-defined data
        serializer.save()


class VendorUpdateView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

    def get_queryset(self):
        # Ensure only the admin can update the vendors
        return Vendor.objects.all()

class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

class VendorDeleteView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this



def vendor_dashboard_view(request):
    """
    Renders the vendor dashboard template.
    No backend queries for now, just front-end placeholders.
    """
    return render(request, 'vendors/vendor_dashboard.html')


from django.views.generic import TemplateView
from django.db.models import Sum, Count
from orders.models import Order, OrderItem
from product.models import Product
from orders.models import Customer
from datetime import datetime

class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gather data for the dashboard
        total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
        total_orders = Order.objects.count()
        active_orders = Order.objects.filter(status='active').count()
        completed_orders = Order.objects.filter(status='completed').count()
        return_orders = Order.objects.filter(status='returned').count()
        new_customers = Customer.objects.filter(created_at__month=datetime.now().month).count()

        # Top-selling products
        top_selling_products = OrderItem.objects.values('product__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:5]

        # Recent orders
        recent_orders = Order.objects.select_related('customer').all().order_by('-created_at')[:5]

        context.update({
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'active_orders': active_orders,
            'completed_orders': completed_orders,
            'return_orders': return_orders,
            'new_customers': new_customers,
            'top_selling_products': top_selling_products,
            'recent_orders': recent_orders,
        })
        return context
