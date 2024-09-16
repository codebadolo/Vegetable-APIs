import random
from django.core.management.base import BaseCommand
from orders.models import Promotion
from vendors.models import Vendor
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create random promotions for vendors'

    def handle(self, *args, **kwargs):
        vendors = Vendor.objects.all()
        
        if not vendors.exists():
            self.stdout.write(self.style.ERROR('No vendors found.'))
            return
        
        for vendor in vendors:
            promotion = Promotion.objects.create(
                name=f'{vendor.store_name} Promo {random.randint(1000, 9999)}',
                discount=random.uniform(5, 30),  # Random discount between 5% and 30%
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=random.randint(10, 30)),  # Random end date between 10 and 30 days
                active=random.choice([True, False])
            )
            self.stdout.write(self.style.SUCCESS(f'Created promotion "{promotion.name}" for vendor "{vendor.store_name}".'))

        self.stdout.write(self.style.SUCCESS('Promotions created successfully.'))
