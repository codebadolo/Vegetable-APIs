import random
from django.core.management.base import BaseCommand
from orders.models import Wishlist
from product.models import Product
from orders.models import Customer

class Command(BaseCommand):
    help = 'Create random wishlists for customers'

    def handle(self, *args, **kwargs):
        customers = Customer.objects.all()
        products = Product.objects.all()

        if not customers.exists():
            self.stdout.write(self.style.ERROR('No customers found.'))
            return
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found.'))
            return

        for customer in customers:
            wishlist = Wishlist.objects.create(
                user=customer.user
            )
            # Add random products to the wishlist
            for product in random.sample(list(products), random.randint(1, 5)):  # 1-5 random products
                wishlist.products.add(product)
            
            self.stdout.write(self.style.SUCCESS(f'Created wishlist for customer "{customer.user.username}" with {wishlist.products.count()} products.'))

        self.stdout.write(self.style.SUCCESS('Wishlists created successfully.'))
