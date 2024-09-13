from django.contrib import admin
from .models import Vendor 
from product.models import Product

# Inline display of products under each vendor
class ProductInline(admin.TabularInline):
    model = Product
    extra = 0  # Don't show extra empty forms
    fields = ('name', 'price', 'stock', 'category')
    readonly_fields = ('name', 'price', 'stock', 'category')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'email', 'phone_number', 'address')
    search_fields = ('store_name', 'email')
    inlines = [ProductInline]
    
admin.site.register(Vendor, VendorAdmin)
