from django.core.management.base import BaseCommand
from orders.models import Order, OrderItem
from vendors.models import Vendor
from product.models import Product
from orders.models import Customer
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates dummy orders for testing purposes'

    def handle(self, *args, **kwargs):
        # Get all vendors, customers, and products
        vendors = Vendor.objects.all()
        customers = Customer.objects.all()
        products = Product.objects.all()

        if not vendors.exists():
            self.stdout.write(self.style.ERROR('No vendors found.'))
            return
        if not customers.exists():
            self.stdout.write(self.style.ERROR('No customers found.'))
            return
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found.'))
            return

        # Create 10 dummy orders
        for _ in range(10):
            customer = random.choice(customers)
            vendor = random.choice(vendors)
            order = Order.objects.create(
                customer=customer,
                vendor=vendor,
                total_price=0,  # Will update after adding items
                status=random.choice(['pending', 'shipped', 'completed', 'canceled']),
                created_at=timezone.now()
            )

            total_price = 0
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                price = product.price * quantity
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total_price += price

            # Update the order total price
            order.total_price = total_price
            order.save()

            self.stdout.write(self.style.SUCCESS(f'Order {order.id} created with {order.items.count()} items for {customer.user.username}.'))

        self.stdout.write(self.style.SUCCESS('Dummy orders created successfully.'))
