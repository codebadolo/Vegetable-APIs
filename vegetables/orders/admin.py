from .models import Order

from django.contrib import admin
from .models import Customer, Order, OrderItem, Card
from unfold.admin import ModelAdmin
from vendors.models import Vendor
# Registering the Customer model in Admin
class CustomerAdmin(ModelAdmin):
    list_display = ('user', 'address', 'phone')
    search_fields = ('user__username', 'address', 'phone')

admin.site.register(Customer, CustomerAdmin)

# Registering the Order model in Admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Allows adding extra order items


# Registering the Card model in Admin
class CardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'expiry_date')
    search_fields = ('customer__user__username', 'card_number')

admin.site.register(Card, CardAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')

    def get_queryset(self, request):
        """
        Ensure that vendors can only see orders related to their own products.
        """
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Vendor').exists():
            vendor = Vendor.objects.get(user=request.user)
            # Filter orders that include products owned by the vendor
            return qs.filter(vendor=vendor)
        return qs  # Admins can see all orders

    def save_model(self, request, obj, form, change):
        """
        Restrict changes to only orders that belong to the vendor's products.
        """
        if not request.user.is_superuser:
            vendor = Vendor.objects.get(user=request.user)
            if obj.vendor != vendor:
                raise PermissionDenied("You don't have permission to modify this order.")
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)