from django.http import JsonResponse
from orders.models import Order
from product.models import Product
from .models import Gestionnaire
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

# Total Sales Over Time (Gestionnaire-specific)
def total_sales_over_time(request):
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    gestionnaire = Gestionnaire.objects.get(user=request.user)
    
    sales_data = (
        Order.objects.filter(gestionnaire=gestionnaire, created_at__gte=last_30_days, status='shipped')
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

# Sales by Product (Gestionnaire-specific)
def sales_by_product(request):
    gestionnaire = Gestionnaire.objects.get(user=request.user)
    
    product_sales = (
        Product.objects.filter(gestionnaire=gestionnaire)
        .annotate(total_sales=Sum('orderitem__price') * Sum('orderitem__quantity'))
        .order_by('-total_sales')[:10]
    )
    
    # Corrected annotation logic to use OrderItem for accurate sales
    products = [product.name for product in product_sales]
    total_sales = [product.total_sales for product in product_sales]

    data = {
        'labels': products,
        'data': total_sales,
    }
    return JsonResponse(data)

# Order Status Distribution (Gestionnaire-specific)
def order_status_distribution(request):
    gestionnaire = Gestionnaire.objects.get(user=request.user)
    
    order_status = (
        Order.objects.filter(gestionnaire=gestionnaire)
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
