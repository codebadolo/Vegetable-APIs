from django.contrib.auth.models import User
from django.db import models


# User Model for Gestionnaire
class Gestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendors_gestionnaire')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name