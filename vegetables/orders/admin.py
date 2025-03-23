from django.contrib import admin
from .models import Customer, Order, OrderItem, Card, Coupon, Transaction, Wishlist, Promotion , Cart , CartItem
from unfold.admin import ModelAdmin, TabularInline
from vendors.models import Gestionnaire
from django.utils.html import format_html
from django.core.exceptions import PermissionDenied

# Customer Admin
admin.site.register(Cart)
admin.site.register(CartItem)
class CustomerAdmin(ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(order__gestionnaire=request.user.gestionnaire).distinct()
        return qs
admin.site.register(Customer)

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'product_image')

    def product_image(self, obj):
        if obj.product.images.exists():
            return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border: 1px solid #ddd; border-radius: 5px;" />', obj.product.images.first().image.url)
        return 'No Image'
    product_image.short_description = 'Product Image'

class OrderAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'gestionnaire', 'status', 'total_price', 'created_at')
    readonly_fields = ('total_price', 'created_at', 'customer_details', 'gestionnaire_details', 'order_items')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__user__username', 'gestionnaire__name')

    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('customer_details', 'gestionnaire_details', 'status', 'total_price', 'created_at')
        }),
        ('Order Items', {
            'fields': ('order_items',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(gestionnaire=request.user.gestionnaire)
        return qs

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

    def gestionnaire_details(self, obj):
        return format_html(
            '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">'
            '<p><strong>Gestionnaire:</strong> {}</p>'
            '</div>',
            obj.gestionnaire.name
        )
    gestionnaire_details.short_description = 'Gestionnaire Details'

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

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            gestionnaire = Gestionnaire.objects.get(user=request.user)
            if obj.gestionnaire != gestionnaire:
                raise PermissionDenied("You don't have permission to modify this order.")
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)

# Card Admin
class CardAdmin(ModelAdmin):
    list_display = ('customer', 'card_number', 'expiry_date')
    search_fields = ('customer__user__username', 'card_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(customer__order__gestionnaire=request.user.gestionnaire).distinct()
        return qs

admin.site.register(Card, CardAdmin)

# Coupon Admin
@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ('code', 'discount_value', 'active', 'start_date', 'end_date')
    search_fields = ('code',)
    list_filter = ('active', 'start_date', 'end_date')
    readonly_fields = ('gestionnaire',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(gestionnaire=request.user.gestionnaire)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.gestionnaire = Gestionnaire.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'status', 'created_at')
    search_fields = ('transaction_id', 'order__id')
    list_filter = ('status', 'created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(order__gestionnaire=request.user.gestionnaire)
        return qs

# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(ModelAdmin):
    list_display = ('user', 'display_products')

    def display_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Gestionnaire").exists():
            return qs.filter(products__gestionnaire=request.user.gestionnaire).distinct()
        return qs

# Promotion Admin
class PromotionAdmin(ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_date', 'end_date', 'active')
    list_filter = ('active', 'start_date', 'end_date')
    search_fields = ('name',)
    fieldsets = (
        ('promotion creations', {
            'fields': ('name', 'discount_percentage', 'start_date', 'end_date', 'active' ,'link' , 'is_hero' ,'image')
        }),
       
    ) 

admin.site.register(Promotion, PromotionAdmin)
