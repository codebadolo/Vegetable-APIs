import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from vendors.models import Vendor
from django.contrib.contenttypes.models import ContentType
from orders.models import Order
from product.models import Product, ProductImage, ProductVariant


class Command(BaseCommand):
    help = 'Creates multiple vendors, assigns them to the Vendor group, sets permissions, and prints their usernames and passwords.'

    def handle(self, *args, **kwargs):
        # Check if the Vendor group exists, create it if not
        group_name = 'Vendor'
        vendor_group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" already exists.'))

        # Create 5 random vendors
        vendor_details = []  # To store vendor usernames and passwords for display later

        for i in range(5):
            # Random username and password generation
            username = f'vendor{i + 1}'
            email = f'{username}@example.com'
            password = f'{username}pass{random.randint(1000, 9999)}'
            first_name = f'Vendor{i + 1}'
            last_name = 'Lastname'

            # Create the user
            user, user_created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={'first_name': first_name, 'last_name': last_name, 'is_staff': True})

            if user_created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User "{username}" created successfully.'))
                vendor_details.append({'username': username, 'password': password})
            else:
                self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))

            # Assign the user to the Vendor group
            user.groups.add(vendor_group)
            self.stdout.write(self.style.SUCCESS(f'User "{username}" added to group "{group_name}".'))

            # Create a vendor profile for the user
            store_name = f'Store {i + 1}'
            phone_number = f'+226 52030{i + 10}'
            address = f'Address {i + 1}'

            vendor, vendor_created = Vendor.objects.get_or_create(
                user=user,
                defaults={
                    'store_name': store_name,
                    'phone_number': phone_number,
                    'address': address
                }
            )

            if vendor_created:
                self.stdout.write(self.style.SUCCESS(f'Vendor profile for "{store_name}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Vendor profile for "{store_name}" already exists.'))

        # Display the vendor details (username and password)
        self.stdout.write(self.style.SUCCESS('\nVendor Usernames and Passwords:'))
        for vendor in vendor_details:
            self.stdout.write(self.style.SUCCESS(f'Username: {vendor["username"]}, Password: {vendor["password"]}'))

        # Add necessary permissions to the Vendor group (view/edit their own products, variants, images, and orders)
        product_content_type = ContentType.objects.get_for_model(Product)
        product_image_content_type = ContentType.objects.get_for_model(ProductImage)
        product_variant_content_type = ContentType.objects.get_for_model(ProductVariant)
        order_content_type = ContentType.objects.get_for_model(Order)

        # Permissions for managing products
        view_product_permission = Permission.objects.get(codename='view_product', content_type=product_content_type)
        add_product_permission = Permission.objects.get(codename='add_product', content_type=product_content_type)
        change_product_permission = Permission.objects.get(codename='change_product', content_type=product_content_type)
        delete_product_permission = Permission.objects.get(codename='delete_product', content_type=product_content_type)

        # Permissions for managing product images
        view_image_permission = Permission.objects.get(codename='view_productimage', content_type=product_image_content_type)
        add_image_permission = Permission.objects.get(codename='add_productimage', content_type=product_image_content_type)
        change_image_permission = Permission.objects.get(codename='change_productimage', content_type=product_image_content_type)
        delete_image_permission = Permission.objects.get(codename='delete_productimage', content_type=product_image_content_type)

        # Permissions for managing product variants
        view_variant_permission = Permission.objects.get(codename='view_productvariant', content_type=product_variant_content_type)
        add_variant_permission = Permission.objects.get(codename='add_productvariant', content_type=product_variant_content_type)
        change_variant_permission = Permission.objects.get(codename='change_productvariant', content_type=product_variant_content_type)
        delete_variant_permission = Permission.objects.get(codename='delete_productvariant', content_type=product_variant_content_type)

        # Permissions for managing orders
        view_order_permission = Permission.objects.get(codename='view_order', content_type=order_content_type)
        add_order_permission = Permission.objects.get(codename='add_order', content_type=order_content_type)
        change_order_permission = Permission.objects.get(codename='change_order', content_type=order_content_type)
        delete_order_permission = Permission.objects.get(codename='delete_order', content_type=order_content_type)

        # Assign the permissions to the Vendor group
        vendor_group.permissions.add(view_product_permission, add_product_permission, change_product_permission, delete_product_permission)
        vendor_group.permissions.add(view_image_permission, add_image_permission, change_image_permission, delete_image_permission)
        vendor_group.permissions.add(view_variant_permission, add_variant_permission, change_variant_permission, delete_variant_permission)
        vendor_group.permissions.add(view_order_permission, add_order_permission, change_order_permission, delete_order_permission)

        self.stdout.write(self.style.SUCCESS(f'Permissions assigned to group "{group_name}".'))

        self.stdout.write(self.style.SUCCESS(f'Vendors created and set up successfully.'))
