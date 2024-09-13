from rest_framework import viewsets
from .models import Order, Customer, Card
from .serializers import OrderSerializer, CustomerSerializer, CardSerializer
from rest_framework.permissions import IsAuthenticated

# API ViewSet for Orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

# API ViewSet for Customers
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

# API ViewSet for Cards
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
