from rest_framework.permissions import AllowAny
from .serializers import CustomerSignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from orders.models  import Customer
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer

class CustomerSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSignupSerializer

class CustomerLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomerLoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })
    

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"success": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
