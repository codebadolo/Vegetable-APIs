from .models import Order

from django.contrib import admin
from .models import Customer, Order, OrderItem, Card
from unfold.admin import ModelAdmin

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
    list_display = ('customer', 'vendor', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('customer__user__username', 'vendor__name')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Vendor').exists():
            return qs.filter(vendor__user=request.user)
        return qs

admin.site.register(Order, OrderAdmin)
