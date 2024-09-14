from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from vendors.models import Vendor
from product.models import Product
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates a vendor with specific details, assigns the Vendor group, and sets permissions.'

    def handle(self, *args, **kwargs):
        # Check if the Vendor group exists, create it if not
        group_name = 'Vendor'
        vendor_group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" already exists.'))

        # Create the user
        username = 'rodrigue'
        email = 'rodri@gmail.com'
        password = 'passrodri'
        first_name = 'Rodrigue'
        last_name = 'Yameogo'

        user, user_created = User.objects.get_or_create(
        username=username,
        email=email,
        defaults={'first_name': first_name, 'last_name': last_name, 'is_staff': True})


        if user_created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))

        # Assign the user to the Vendor group
        user.groups.add(vendor_group)
        self.stdout.write(self.style.SUCCESS(f'User "{username}" added to group "{group_name}".'))

        # Create a vendor profile for the user
        store_name = 'SYMBIOSE STORE'
        phone_number = '+226 52030409'
        address = 'Paglayiri'

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

        # Add necessary permissions to the Vendor group (view/edit their own products)
        content_type = ContentType.objects.get_for_model(Product)
        view_product_permission = Permission.objects.get(codename='view_product', content_type=content_type)
        add_product_permission = Permission.objects.get(codename='add_product', content_type=content_type)
        change_product_permission = Permission.objects.get(codename='change_product', content_type=content_type)
        delete_product_permission = Permission.objects.get(codename='delete_product', content_type=content_type)

        vendor_group.permissions.add(view_product_permission)
        vendor_group.permissions.add(add_product_permission)
        vendor_group.permissions.add(change_product_permission)
        vendor_group.permissions.add(delete_product_permission)

        self.stdout.write(self.style.SUCCESS(f'Permissions assigned to group "{group_name}".'))

        self.stdout.write(self.style.SUCCESS(f'Vendor "{store_name}" with user "{username}" is set up.'))
