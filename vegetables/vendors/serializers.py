from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'description', 'phone_number', 'address', 'image', 'email', 'user']

    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value

    def validate_email(self, value):
        if Vendor.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
