from .models import Order

from django.contrib import admin
from .models import Customer, Order, OrderItem, Card
from unfold.admin import ModelAdmin , TabularInline
from vendors.models import Vendor
# Registering the Customer model in Admin
# customers/admin.py
from django.contrib import admin
from .models import Customer
from django.utils.html import format_html
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')  # Ensure these fields exist in your model
    search_fields = ('user__username', 'phone')  # Assuming 'user' is a ForeignKey to 'auth.User'
    list_filter = ('user__is_active', 'user__date_joined')



# Registering the Order model in Admin
class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0 # Allows adding extra order items
    # Custom method to show product name and image
    def product_name(self, obj):
        return obj.product.name

      # Show product image
    def product_image(self, obj):
        if obj.product.images.exists():
            return format_html('<img src="{}" width="50" height="50" />', obj.product.images.first().image.url)
        return 'No Image'

    # Displaying product details
    fields = ('product_name', 'product_image', 'quantity', 'price')
    readonly_fields = ('product_name', 'product_image')

    # Naming the fields for display
    product_name.short_description = 'Product Name'
    product_image.short_description = 'Product Image'

# Registering the Card model in Admin
class CardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'expiry_date')
    search_fields = ('customer__user__username', 'card_number')

admin.site.register(Card, CardAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'status', 'total_price', 'created_at', 'get_product_image')
    search_fields = ('customer__user__username', 'vendor__store_name')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]  # Show Order Items in the Order
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
    def get_product_image(self, obj):
        # Get the first product in the order's items
        first_item = obj.items.first()
        if first_item and first_item.product.images.exists():
            return format_html('<img src="{}" width="100" height="100" />', first_item.product.images.first().image.url)
        return 'No Image'
    get_product_image.short_description = 'Product Image'
    def save_model(self, request, obj, form, change):
        """
        Restrict changes to only orders that belong to the vendor's products.
        """
        if not request.user.is_superuser:
            vendor = Vendor.objects.get(user=request.user)
            if obj.vendor != vendor:
                raise PermissionDenied("You don't have permission to modify this order.")
        super().save_model(request, obj, form, change)

        def get_product_image(self, obj):
            # Assuming each order has at least one order item
            first_item = obj.orderitem_set.first()
            if first_item and first_item.product.images.exists():
                return format_html('<img src="{}" width="50" height="50" />', first_item.product.images.first().image.url)
            return 'No Image'
    
        get_product_image.short_description = 'Product Image'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)