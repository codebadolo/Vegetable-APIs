from django.core.management.base import BaseCommand
from product.models import Category

class Command(BaseCommand):
    help = 'Create product categories and subcategories'

    def handle(self, *args, **kwargs):
        categories = {
            'Légumes': ['Frais', 'Surgelés'],
            'Fruits': ['Tropicaux', 'Pomme', 'Agrumes'],
            'Epicerie': ['Conserves', 'Epices', 'Riz'],
            'Céréales & Graines': ['Blé', 'Avoine', 'Quinoa'],
            'Boucherie': ['Viandes', 'Poulet', 'Porc'],
            'Charcuterie': ['Jambon', 'Saucisson'],
            'Poissonnerie': ['Poissons', 'Fruits de mer'],
            'Boissons': ['Sodas', 'Eaux', 'Jus'],
            'Produits laitiers': ['Lait', 'Fromage', 'Yaourt'],
            'Recettes': [],
        }

        for category_name, subcategories in categories.items():
            parent_category, created = Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f"Category '{category_name}' created."))
            for subcategory_name in subcategories:
                subcategory, created = Category.objects.get_or_create(name=subcategory_name, parent=parent_category)
                self.stdout.write(self.style.SUCCESS(f"Subcategory '{subcategory_name}' created under '{category_name}'."))

        self.stdout.write(self.style.SUCCESS('Categories and subcategories created successfully!'))
