from django.contrib.auth.models import User
from rest_framework import serializers
from orders.models import Customer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer

# In your serializer (e.g., customers/serializers.py)
from rest_framework import serializers
from django.contrib.auth import get_user_model

'''class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Ensure to use the custom user model
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure the password is write-only
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)  # Use create_user for password hashing
        return user


class OverriddenUserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        ref_name = "DjoserUserSerializer"  # Unique ref name for Swagger

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["phone_number", "address"]

class UserSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "customer"]

    def create(self, validated_data):
        customer_data = validated_data.pop("customer", None)
        user = User.objects.create_user(**validated_data)
        if customer_data:
            Customer.objects.create(user=user, **customer_data)
        return user
'''

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']