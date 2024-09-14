from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, Category
from .forms import ProductForm
# Register Category model (for tree-based categorization)
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline 
from vendors.models  import Vendor
class CategoryAdmin(ModelAdmin , MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    mptt_level_indent = 20  # Set indentation for subcategories


# Inline admin for managing product images within the product admin
class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1  # Show one empty form for adding images

# Inline admin for managing product variants within the product admin
class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1  # Show one empty form for adding variants

class ProductAdmin(ModelAdmin):
    model = Product
    list_display = ('name', 'vendor', 'price', 'stock', 'category')
    search_fields = ('name', 'vendor__store_name')
    list_filter = ('vendor', 'category')

    # Add inlines for images and variants
    inlines = [ProductImageInline, ProductVariantInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Pricing Information', {
            'fields': ('price', 'stock')
        }),
        ('Category Information', {
            'fields': ('category',)
        }),
    )

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



# Ensure that the custom CSS is applied to all admin models globally


# Register the models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

