from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser named Badolo with admin privileges'

    def handle(self, *args, **kwargs):
        # Define user details
        username = 'Badolo'
        email = 'badolo@gmail.com'
        password = "M1v'1//_$J/:"

        # Check if the superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
        else:
            # Create the superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            user.is_staff = True  # Ensure user has staff privileges
            user.is_superuser = True  # Ensure user is a superuser
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully with password "{password}".'))
