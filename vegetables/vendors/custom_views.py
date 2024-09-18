from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from django.db.models import Sum
from product.models import Product
from orders.models import OrderItem
from django.db.models import Sum
from orders.models import Customer
from django.utils import timezone
from datetime import timedelta

def get_total_revenue():
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    return total_revenue
def get_total_orders():
    total_orders = Order.objects.count()
    return total_orders
def get_total_orders():
    total_orders = Order.objects.count()
    return total_orders



def get_new_customers():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    new_customers = Customer.objects.filter(user__date_joined__gte=last_week).count()
    return new_customers



def get_top_selling_products():
    top_products = OrderItem.objects.values('product__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:5]
    return top_products

def get_average_order_value():
    total_revenue = get_total_revenue()
    total_orders = get_total_orders()
    if total_orders > 0:
        return total_revenue / total_orders
    return 0
def get_cart_abandonment_rate():
    total_orders = Order.objects.filter(status__in=['pending', 'canceled']).count()
    abandoned_carts = Order.objects.filter(status='abandoned').count()
    if total_orders > 0:
        return (abandoned_carts / total_orders) * 100
    return 0
from product.models import Category

def get_sales_by_category():
    sales_by_category = OrderItem.objects.values('product__category__name').annotate(total_sales=Sum('price')).order_by('-total_sales')
    return sales_by_category



def get_inventory_levels():
    low_stock_products = Product.objects.filter(stock__lte=10).order_by('stock')[:5]  # Products with stock less than or equal to 10
    return low_stock_products




def custom_admin_view(request):
    total_revenue = Order.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue']
    total_orders = Order.objects.count()
    top_selling_products = Order.objects.values('items__product__name').annotate(total_sales=Sum('items__quantity')).order_by('-total_sales')[:5]
    new_customers = Customer.objects.filter(created_at__gte=timezone.now()-timedelta(days=7)).count()
    average_order_value = total_revenue / total_orders if total_orders else 0
    sales_by_category = Product.objects.values('category__name').annotate(total_sales=Sum('orderitem__quantity')).order_by('-total_sales')

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'top_selling_products': top_selling_products,
        'new_customers': new_customers,
        'average_order_value': average_order_value,
        'sales_by_category': sales_by_category,
    }
    print(context)
    return render(request, 'admin/custom_page.html', context)
