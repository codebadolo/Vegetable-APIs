import random
from django.core.management.base import BaseCommand
from orders.models import Order, OrderItem
from orders.models import Customer
from product.models import Product
from vendors.models import Vendor
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create random orders for customers, and create a customer named "premierclient" if no customers exist.'

    def handle(self, *args, **kwargs):
        # Check if any customers exist
        if not Customer.objects.exists():
            # Create a new user for the customer
            user = User.objects.create_user(
                username='premierclient',
                email='premierclient@example.com',
                password='randompassword',  # Change the password as necessary
                first_name='Premier',
                last_name='Client',
                is_staff=False
            )
            # Create the customer profile
            customer = Customer.objects.create(
                user=user,
                phone='+1234567890',  # Add a dummy phone number or adjust based on your model
                address='Random Street, Random City'
            )
            self.stdout.write(self.style.SUCCESS('Customer "premierclient" created successfully.'))
        else:
            customer = Customer.objects.first()  # If customers exist, select the first one

        # Check if vendor "rodrigue" exists
        try:
            vendor = Vendor.objects.get(user__username='rodrigue')
        except Vendor.DoesNotExist:
            self.stdout.write(self.style.ERROR('Vendor "rodrigue" not found in the database.'))
            return

        # Get all products
        products = Product.objects.filter(vendor=vendor)

        if not products.exists():
            self.stdout.write(self.style.ERROR(f'No products found for vendor "{vendor.user.username}".'))
            return

        # Define possible statuses
        statuses = ['pending', 'shipped', 'delivered', 'canceled']

        # Create at least 5 orders
        for i in range(5):
            product_choices = random.sample(list(products), random.randint(1, 3))  # Pick 1-3 random products
            total_price = 0

            # Create the order with a random status
            status = random.choice(statuses)
            order = Order.objects.create(
                customer=customer,
                vendor=vendor,  # Assign the vendor
                status=status,  # Assign random status
                created_at=timezone.now(),
                total_price=0  # Initially set the total price to 0
            )

            # Create order items and calculate total price
            for product in product_choices:
                quantity = random.randint(1, 5)  # Random quantity between 1 and 5
                price = product.price * quantity  # Calculate price for this item
                total_price += price  # Add to the total price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price  # Total price for the quantity
                )

            # Update the total price of the order
            order.total_price = total_price
            order.save()

            self.stdout.write(self.style.SUCCESS(f'Order {order.id} created for customer {customer.user.username} with status "{status}" and total price {total_price}.'))

        self.stdout.write(self.style.SUCCESS('5 orders created successfully.'))
