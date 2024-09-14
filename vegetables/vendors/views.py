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


'''
@staff_member_required  # Ensures only staff (vendors) can access the dashboard

# Vendor Dashboard View
def vendor_dashboard_view(request):
    vendor = Vendor.objects.get(user=request.user)
    today = timezone.now()
    last_30_days = today - timedelta(days=30)

    sales_data = (
        OrderItem.objects.filter(product__vendor=vendor, order__created_at__gte=last_30_days, order__status='completed')
        .extra(select={'day': 'date(order__created_at)'})
        .values('day')
        .annotate(total_sales=Sum('price'))
        .order_by('day')
    )
    # Get total revenue for this vendor (completed orders)
    total_revenue = (
    OrderItem.objects.filter(product__vendor=vendor, order__status='completed')
    .aggregate(total_revenue=Sum('price'))
    .get('total_revenue', 0)
    )


    # Total number of products by the vendor
    total_products = Product.objects.filter(vendor=vendor).count()

    # Total orders for this vendor
    total_orders = Order.objects.filter(vendor=vendor).count()

    # Total customers who ordered from this vendor
    total_customers = Order.objects.filter(vendor=vendor).values('customer').distinct().count()

    # Get the top 5 selling products for this vendor
    top_selling_products = (
        OrderItem.objects.filter(product__vendor=vendor, order__status='completed')
        .values('product__name')  # Group by product name
        .annotate(total_sales=Sum('price'))  # Sum the sales for each product
        .order_by('-total_sales')[:5]  # Get the top 5 selling products
    )

  
    days = [item['day'] for item in sales_data]
    total_sales_over_time = [item['total_sales'] for item in sales_data]

    # Recent orders (last 5 orders)
    recent_orders = (
        Order.objects.filter(vendor=vendor)
        .order_by('-created_at')[:5]
    )

    # Order status distribution (for charting purposes)
    order_status_distribution = (
        Order.objects.filter(vendor=vendor)
        .values('status')
        .annotate(status_count=Count('id'))
    )
    statuses = [item['status'] for item in order_status_distribution]
    status_counts = [item['status_count'] for item in order_status_distribution]

    # Prepare context data for the dashboard
    context = {
       # 'total_revenue': total_revenue or 0,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'top_selling_products': top_selling_products,
        'sales_data': {'days': days, 'total_sales_over_time': total_sales_over_time},
        'recent_orders': recent_orders,
        'order_status_distribution': {'statuses': statuses, 'counts': status_counts},
    }

    #return JsonResponse(context)
    return render(request, 'vendors/vendor_dashboard.html', context)
'''


def vendor_dashboard_view(request):
    """
    Renders the vendor dashboard template.
    No backend queries for now, just front-end placeholders.
    """
    return render(request, 'vendors/vendor_dashboard.html')