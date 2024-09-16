import os
import sys
import django
import streamlit as st
import pandas as pd
from django.db.models import Sum, Count
from streamlit_autorefresh import st_autorefresh  # For auto-refreshing

# Add the Django project directory to the Python path
sys.path.append('/home/ye/symbiose/vegetables')  # Make sure this path points to your Django project

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetables.settings')  # Replace 'vegetables' with your project name if needed

# Initialize Django
django.setup()

# Now import models after setting up Django
from orders.models import Order, Transaction, Customer , OrderItem
from product.models import Product
from vendors.models import Vendor

# Automatically refresh the dashboard every 60 seconds
st_autorefresh(interval=60 * 1000)  # 60 seconds in milliseconds

# Set the title
st.title('Admin Dashboard (Real-Time)')

# Sidebar for KPIs
st.sidebar.header('Key Performance Indicators (KPIs)')

# Fetch data from the database
total_orders = Order.objects.all().count()
total_customers = Customer.objects.all().count()
total_revenue = Transaction.objects.aggregate(total_revenue=Sum('amount'))['total_revenue']
total_products = Product.objects.all().count()
vendors = Vendor.objects.all().count()

# Display KPIs in the sidebar
st.sidebar.write(f"Total Orders: {total_orders}")
st.sidebar.write(f"Total Customers: {total_customers}")
st.sidebar.write(f"Total Revenue: {total_revenue}")
st.sidebar.write(f"Total Products: {total_products}")
st.sidebar.write(f"Total Vendors: {vendors}")

# Fetch top 5 products by sales
st.subheader('Top 5 Products by Sales')
top_products = (
    OrderItem.objects.values('product__name')
    .annotate(total_sales=Sum('quantity'))
    .order_by('-total_sales')[:5]
)

# Convert top products to a DataFrame and display as a chart
top_products_df = pd.DataFrame(list(top_products))
st.bar_chart(top_products_df.set_index('product__name')['total_sales'])


# Fetch and display recent transactions in the sidebar
st.sidebar.subheader('Recent Transactions')
recent_transactions = Transaction.objects.all().order_by('-created_at')[:5]
recent_transactions_df = pd.DataFrame(list(recent_transactions.values()))
st.sidebar.table(recent_transactions_df)

# Display order statuses
st.subheader('Order Status Distribution')
order_status = Order.objects.values('status').annotate(count=Count('status'))
order_status_df = pd.DataFrame(list(order_status))
st.bar_chart(order_status_df.set_index('status')['count'])

# Footer message
st.write("This dashboard updates every 60 seconds.")
