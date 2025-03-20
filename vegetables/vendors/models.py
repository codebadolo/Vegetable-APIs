from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# User Model for Gestionnaire
class Gestionnaire(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendors_gestionnaire')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # Add this line
    def __str__(self):
        return self.name