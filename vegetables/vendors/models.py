from django.contrib.auth.models import User
from django.db import models

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Vendor's description
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Vendor's contact number
    address = models.TextField(blank=True, null=True)  # Vendor's physical address
    image = models.ImageField(upload_to='vendor_images/', blank=True, null=True)  # Profile image for the vendor
    email = models.EmailField(max_length=100, blank=True, null=True)  # Optional separate email

    def __str__(self):
        return self.store_name
