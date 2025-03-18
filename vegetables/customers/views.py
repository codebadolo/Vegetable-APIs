from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from orders.models import Customer
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerProfileSerializer, CustomerSignupSerializer , CustomerLoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CustomerSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Check if a Customer already exists for this user
        if not Customer.objects.filter(user=user).exists():
            Customer.objects.create(user=user)
from rest_framework import status
class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Customer.objects.get(user=self.request.user)
