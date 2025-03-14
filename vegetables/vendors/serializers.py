from rest_framework import serializers
from .models import Gestionnaire

class GestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestionnaire
        fields = ['id', 'name', 'email', 'phone_number', 'user']

    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value

    def validate_email(self, value):
        if Gestionnaire.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
