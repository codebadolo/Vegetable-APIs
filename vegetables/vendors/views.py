from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Vendor
from .serializers import VendorSerializer

class VendorCreateView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

    def perform_create(self, serializer):
        # Create vendor with additional admin-defined data
        serializer.save()


class VendorUpdateView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

    def get_queryset(self):
        # Ensure only the admin can update the vendors
        return Vendor.objects.all()

class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

class VendorDeleteView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]  # Only admins can access this

