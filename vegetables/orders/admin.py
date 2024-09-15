from django.contrib import admin
from .models import Customer, Order, OrderItem, Card, Coupon, Transaction, Wishlist, Promotion
from unfold.admin import ModelAdmin, TabularInline
from vendors.models import Vendor
from django.utils.html import format_html
from django.core.exceptions import PermissionDenied


# Customer Admin
class CustomerAdmin(ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Vendor").exists():
            # Fix: Use the correct reverse relation for the orders
            return qs.filter(order__vendor=request.user.vendor).distinct()  # Assuming customer is tied to orders, and orders have a 'vendor' field
        return qs  # Admin sees all customers


admin.site.register(Customer, CustomerAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'product_image')

    def product_image(self, obj):
        if obj.product.images.exists():
            return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border: 1px solid #ddd; border-radius: 5px;" />', obj.product.images.first().image.url)
        return 'No Image'
    product_image.short_description = 'Product Image'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'status', 'total_price', 'created_at')
    readonly_fields = ('total_price', 'created_at', 'customer_details', 'vendor_details', 'order_items')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__user__username', 'vendor__store_name')

    inlines = [OrderItemInline]

    # Style the order details section and show images in a more visual way
    fieldsets = (
        ('Order Info', {
            'fields': ('customer_details', 'vendor_details', 'status', 'total_price', 'created_at')
        }),
        ('Order Items', {
            'fields': ('order_items',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Vendor").exists():
            return qs.filter(vendor=request.user.vendor)
        return qs

    # More styled customer details
    def customer_details(self, obj):
        return format_html(
            '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">'
            '<p><strong>Name:</strong> {}</p>'
            '<p><strong>Email:</strong> {}</p>'
            '<p><strong>Phone:</strong> {}</p>'
            '</div>',
            obj.customer.user.get_full_name(),
            obj.customer.user.email,
            obj.customer.phone_number
        )
    customer_details.short_description = 'Customer Details'

    # More styled vendor details
    def vendor_details(self, obj):
        return format_html(
            '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">'
            '<p><strong>Vendor:</strong> {}</p>'
            '<p><strong>Store:</strong> {}</p>'
            '</div>',
            obj.vendor.user.get_full_name(),
            obj.vendor.store_name
        )
    vendor_details.short_description = 'Vendor Details'

    # Enhanced display of order items with larger images
    def order_items(self, obj):
        items = obj.items.all()
        items_display = '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">'
        for item in items:
            if item.product.images.exists():
                image = format_html('<img src="{}" style="width: 500px; height: 150px; object-fit: cover; border: 1px solid #ddd; border-radius: 5px;" />', item.product.images.first().image.url)
            else:
                image = 'No Image'
            items_display += f'<div style="display: flex; align-items: center; padding: 5px 0;">{image}<div style="padding-left: 15px;"><strong>{item.product.name}</strong><br>Qty: {item.quantity}<br>Price: {item.price}$</div></div>'
        items_display += '</div>'
        return format_html(items_display)
    order_items.short_description = 'Order Items'

    def get_product_image(self, obj):
        first_item = obj.orderitem_set.first()
        if first_item and first_item.product.images.exists():
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', first_item.product.images.first().image.url)
        return 'No Image'
    get_product_image.short_description = 'Product Image'

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            vendor = Vendor.objects.get(user=request.user)
            if obj.vendor != vendor:
                raise PermissionDenied("You don't have permission to modify this order.")
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)


# Card Admin
class CardAdmin(ModelAdmin):
    list_display = ('customer', 'card_number', 'expiry_date')
    search_fields = ('customer__user__username', 'card_number')

admin.site.register(Card, CardAdmin)


# Coupon Admin
@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ('code', 'discount', 'active', 'start_date', 'end_date')
    search_fields = ('code',)
    list_filter = ('active', 'start_date', 'end_date')


# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'status', 'created_at')
    search_fields = ('transaction_id', 'order__id')
    list_filter = ('status', 'created_at')


# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_products')

    def display_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Vendor").exists():
            return qs.filter(products__vendor=request.user.vendor).distinct()  # Assuming wishlist is linked to products, and products are tied to a vendor
        return qs


# Promotion Admin
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'start_date', 'end_date')
    search_fields = ('name',)

admin.site.register(Promotion, PromotionAdmin)
