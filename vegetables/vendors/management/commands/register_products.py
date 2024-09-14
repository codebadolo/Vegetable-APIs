import random
import os
from django.core.management.base import BaseCommand
from product.models import Product, Category, ProductImage
from vendors.models import Vendor
from django.conf import settings

class Command(BaseCommand):
    help = 'Create vegetable products for vendor Rodrigue with random categories'

    def handle(self, *args, **kwargs):
        # Get the vendor (rodrigue)
        try:
            vendor = Vendor.objects.get(user__username='rodrigue')
        except Vendor.DoesNotExist:
            self.stdout.write(self.style.ERROR('Vendor "rodrigue" not found'))
            return

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

        # Create products
        for vegetable in vegetable_data:
            category = random.choice(categories)  # Pick a random category
            product = Product.objects.create(
                name=vegetable['name'],
                description=f'{vegetable["name"]} from Rodrigue\'s farm.',
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
                self.stdout.write(self.style.SUCCESS(f'Created product "{product.name}" with image.'))
            else:
                self.stdout.write(self.style.WARNING(f'Image for "{product.name}" not found: {image_path}'))

        self.stdout.write(self.style.SUCCESS('Vegetable products created successfully.'))
