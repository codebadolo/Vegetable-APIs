from django.contrib import admin
from .models import Gestionnaire
from product.models import Product
from unfold.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import Group

class GestionnaireAdminSite(admin.AdminSite):
    site_header = 'Gestionnaire Dashboard'
    site_title = 'Employee Portal'

    def has_permission(self, request):
        return request.user.is_active and hasattr(request.user, 'gestionnaire')

gestionnaire_admin_site = GestionnaireAdminSite(name='gestionnaire_admin')

class ProductInline(TabularInline):
    model = Product
    extra = 0
    fields = ('name', 'price', 'category')
    readonly_fields = ('name', 'price', 'category')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'gestionnaire'):
            return qs.filter(gestionnaire=request.user.gestionnaire)
        return qs

class GestionnaireAdmin(ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'product_count')
    search_fields = ('name', 'email')
    inlines = [ProductInline]
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Managed Products'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

# Register with both main admin and gestionnaire admin
admin.site.register(Gestionnaire, GestionnaireAdmin)
gestionnaire_admin_site.register(Gestionnaire, GestionnaireAdmin)
gestionnaire_admin_site.register(Group)  # If needed for permissions
