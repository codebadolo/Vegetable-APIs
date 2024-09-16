import random
import os
from django.core.management.base import BaseCommand
from product.models import Product, Category, ProductImage
from vendors.models import Vendor
from django.conf import settings

class Command(BaseCommand):
    help = 'Create vegetable products for each vendor with varying numbers of products'

    def handle(self, *args, **kwargs):
        # List of vendors' usernames
        vendor_usernames = ['vendor1', 'vendor2', 'vendor3', 'vendor4', 'vendor5']

        # Define vegetable data (name and image file paths)
        vegetable_data = [
            {'name': 'Aubergines', 'image': 'aubergines.jpeg'},
            {'name': 'Banane', 'image': 'banane.jpeg'},
            {'name': 'Carottes', 'image': 'carottes.jpeg'},
            {'name': 'Choux', 'image': 'chouz.jpeg'},
            {'name': 'Concombre', 'image': 'concombre.jpeg'},
            {'name': 'Gombo Frais', 'image': 'gombo frais.jpeg'},
            {'name': 'Orange', 'image': 'orange.jpeg'},
            {'name': 'Poire', 'image': 'poire.jpeg'},
            {'name': 'Pommes', 'image': 'pommes.jpeg'},
            {'name': 'Tomate Rouge', 'image': 'tomate rouge.jpeg'},
        ]

        # List of random categories (assumed to exist in the database)
        categories = Category.objects.all()

        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found in the database.'))
            return

        # Assign different numbers of products to each vendor
        for i, username in enumerate(vendor_usernames):
            try:
                vendor = Vendor.objects.get(user__username=username)
            except Vendor.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Vendor "{username}" not found'))
                continue

            # Determine how many products this vendor should register
            num_products = i + 1  # vendor1 gets 1 product, vendor2 gets 2, etc.

            for j in range(num_products):
                vegetable = random.choice(vegetable_data)  # Random vegetable
                category = random.choice(categories)  # Pick a random category

                # Create the product
                product = Product.objects.create(
                    name=vegetable['name'],
                    description=f'{vegetable["name"]} from {vendor.store_name}.',
                    price=random.uniform(1.0, 5.0),  # Random price between 1 and 5
                    stock=random.randint(10, 100),  # Random stock between 10 and 100
                    vendor=vendor,
                    category=category
                )

                # Add product image
                image_path = os.path.join(settings.BASE_DIR, 'static', 'product_images', vegetable['image'])
                if os.path.exists(image_path):
                    ProductImage.objects.create(
                        product=product,
                        image=f'product_images/{vegetable["image"]}'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created product "{product.name}" for "{vendor.store_name}" with image.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Image for "{product.name}" not found: {image_path}'))

        self.stdout.write(self.style.SUCCESS('Products created successfully for all vendors.'))
