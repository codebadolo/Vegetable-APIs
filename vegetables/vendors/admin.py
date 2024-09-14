from django.contrib import admin
from .models import Vendor 
from product.models import Product
from unfold.admin import ModelAdmin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group

class VendorAdminSite(AdminSite):
    site_header = 'Vendor Dashboard'
    site_title = 'Vendor Portal'

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name='Vendor').exists()

vendor_admin_site = VendorAdminSite(name='vendor_admin')

# Inline display of products under each vendor
class ProductInline(admin.TabularInline):
    model = Product
    extra = 0  # Don't show extra empty forms
    fields = ('name', 'price', 'stock', 'category')
    readonly_fields = ('name', 'price', 'stock', 'category')

class VendorAdmin(ModelAdmin):
    list_display = ('store_name', 'email', 'phone_number', 'address')
    search_fields = ('store_name', 'email')
    inlines = [ProductInline]
    
    



admin.site.register(Vendor, VendorAdmin)

# ve




