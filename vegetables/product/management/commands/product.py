from django.core.management.base import BaseCommand
from django.core.files import File
from io import BytesIO
from product.models import ProductType, Category, Product, Variant, VariantValue, ProductImage
from vendors.models import Gestionnaire
from django.utils.text import slugify
from django.db import transaction
from lorem_text import lorem
import random
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = 'Creates a specified number of African art products'

    def add_arguments(self, parser):
        parser.add_argument('num_products', type=int, nargs='?', default=20,
                            help='Number of products to create')

    @transaction.atomic
    def handle(self, *args, **options):
        num_products = options['num_products']

        # Create or Retrieve Product Type
        art_type, created = ProductType.objects.get_or_create(
            name="African Art",
            defaults={'description': "Authentic art pieces originating from Africa"}
        )

        # Create or Retrieve Categories
        categories = [
            {"name": "Sculptures"},
            {"name": "Paintings"},
            {"name": "Textiles"},
            {"name": "Ceramics"},
        ]
        category_objects = []
        for cat_data in categories:
            category, created = Category.objects.get_or_create(name=cat_data['name'])
            category_objects.append(category)

        # Create or Retrieve Variants
        variants = [
            {"name": "Size", "product_type": art_type},
            {"name": "Material", "product_type": art_type},
            {"name": "Style", "product_type": art_type},
        ]
        variant_objects = []
        for var_data in variants:
            variant, created = Variant.objects.get_or_create(
                name=var_data['name'],
                product_type=art_type
            )
            variant_objects.append(variant)

        # Create or Retrieve Variant Values
        variant_values = {
            "Size": ["Small", "Medium", "Large"],
            "Material": ["Wood", "Clay", "Fabric", "Bronze"],
            "Style": ["Traditional", "Modern", "Abstract"],
        }
        variant_value_objects = {}
        for variant_name, values in variant_values.items():
            variant = Variant.objects.get(name=variant_name, product_type=art_type)
            variant_value_objects[variant_name] = []
            for value in values:
                variant_value, created = VariantValue.objects.get_or_create(
                    variant=variant,
                    value=value
                )
                variant_value_objects[variant_name].append(variant_value)

        # Get or Create Gestionnaire (Assuming a default one exists)
        try:
            # Assuming there's a user with ID 2 that you want to associate with
            user = User.objects.get(pk=2)  # Get the user with ID 2
            gestionnaire = Gestionnaire.objects.get(user=user)
        except (Gestionnaire.DoesNotExist, User.DoesNotExist):
            user = User.objects.create(username="testuser", password="testpassword")
            gestionnaire = Gestionnaire.objects.create(user=user, name="testuser")

        for i in range(num_products):
            product_name = f"{fake.city()} Art Piece {i+1}"
            product = Product.objects.create(
                name=product_name,
                description=lorem.paragraph(),
                price=random.uniform(50, 500),
                history=lorem.paragraph(),
                category=random.choice(category_objects),
                gestionnaire=gestionnaire,
                product_type=art_type,
            )
            # Create Product Image (Dummy Image)
            image_content = fake.image(image_format='PNG')
            product_image = ProductImage.objects.create(
                product=product,
                variant=random.choice(variant_objects),
                variant_value=random.choice(variant_value_objects[random.choice(list(variant_values.keys()))]),
                image=File(BytesIO(image_content), name=f'{slugify(product_name)}.png'),
                is_primary=True,
                alt_text=f"Image of {product_name}"
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_products} art products."))
