import random
import string
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from orders.models import Coupon
from vendors.models import Vendor

class Command(BaseCommand):
    help = 'Create random coupons for each vendor'

    def handle(self, *args, **kwargs):
        # Get all vendors
        vendors = Vendor.objects.all()

        if not vendors.exists():
            self.stdout.write(self.style.ERROR('No vendors found.'))
            return

        # Define coupon settings
        number_of_coupons = 5  # Number of coupons per vendor
        discount_range = (5, 50)  # Discount range in percentage

        # Function to generate random coupon codes
        def generate_coupon_code(length=8):
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        # Create random coupons for each vendor
        for vendor in vendors:
            for _ in range(number_of_coupons):
                # Generate random coupon code
                coupon_code = generate_coupon_code()

                # Generate random discount value
                discount = random.uniform(discount_range[0], discount_range[1])

                # Set random start and end dates
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=random.randint(10, 90))  # Coupon valid for 10-90 days

                # Create the coupon
                coupon = Coupon.objects.create(
                    vendor=vendor,
                    code=coupon_code,
                    discount=discount,
                    start_date=start_date,
                    end_date=end_date,
                    active=True
                )

                self.stdout.write(self.style.SUCCESS(f'Created coupon "{coupon.code}" with {coupon.discount}% discount for vendor "{vendor.store_name}".'))

        self.stdout.write(self.style.SUCCESS('Coupons created successfully for all vendors.'))
