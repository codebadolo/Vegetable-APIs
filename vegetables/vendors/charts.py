from django.http import JsonResponse
from orders.models import Order
from product.models import Product
from .models import Vendor
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

# Total Sales Over Time (Vendor-specific)
def total_sales_over_time(request):
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    vendor = Vendor.objects.get(user=request.user)
    
    sales_data = (
        Order.objects.filter(vendor=vendor, created_at__gte=last_30_days, status='completed')
        .extra(select={'day': 'date(created_at)'})
        .values('day')
        .annotate(total_sales=Sum('total_price'))
        .order_by('day')
    )
    
    days = [item['day'] for item in sales_data]
    total_sales = [item['total_sales'] for item in sales_data]

    data = {
        'labels': days,
        'data': total_sales,
    }
    return JsonResponse(data)

# Sales by Product (Vendor-specific)
def sales_by_product(request):
    vendor = Vendor.objects.get(user=request.user)
    
    product_sales = (
        Product.objects.filter(vendor=vendor, order__status='completed')
        .annotate(total_sales=Sum('order__total_price'))
        .order_by('-total_sales')[:10]
    )
    
    products = [product.name for product in product_sales]
    total_sales = [product.total_sales for product in product_sales]

    data = {
        'labels': products,
        'data': total_sales,
    }
    return JsonResponse(data)

# Order Status Distribution (Vendor-specific)
def order_status_distribution(request):
    vendor = Vendor.objects.get(user=request.user)
    
    order_status = (
        Order.objects.filter(vendor=vendor)
        .values('status')
        .annotate(status_count=Count('id'))
    )

    statuses = [item['status'] for item in order_status]
    counts = [item['status_count'] for item in order_status]

    data = {
        'labels': statuses,
        'data': counts,
    }
    return JsonResponse(data)
