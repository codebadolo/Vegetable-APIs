from django.contrib import admin
from .models import Vendor 
from product.models import Product
from unfold.admin import ModelAdmin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group

from unfold.admin import TabularInline
from product.admin import  ProductImageInline , ProductVariantInline
'''class VendorAdminSite(AdminSite):
    site_header = 'Vendor Dashboard'
    site_title = 'Vendor Portal'

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name='Vendor').exists()

vendor_admin_site = VendorAdminSite(name='vendor_admin')
'''
# Inline display of products under each vendor
class ProductInline(TabularInline):
    model = Product
    extra = 0  # Don't show extra empty forms
    fields = ('name', 'price', 'stock', 'category' )
    readonly_fields = ('name', 'price', 'stock', 'category')
    inlines = [ProductImageInline, ProductVariantInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Vendor').exists():
            return qs.filter(vendor__user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            try:
                vendor = Vendor.objects.get(user=request.user)
                obj.vendor = vendor
            except Vendor.DoesNotExist:
                raise ValidationError("You are not associated with any vendor account.")
        super().save_model(request, obj, form, change)
   

class VendorAdmin(ModelAdmin):
    list_display = ('store_name', 'email', 'phone_number', 'address')
    search_fields = ('store_name', 'email')
    inlines = [ProductInline ]
    
    



admin.site.register(Vendor, VendorAdmin)

# ve




