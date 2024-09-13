from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, Category
from .forms import ProductForm
# Register Category model (for tree-based categorization)
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category

class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    mptt_level_indent = 20  # Set indentation for subcategories


# Inline admin for managing product images within the product admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Show one empty form for adding images

# Inline admin for managing product variants within the product admin
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Show one empty form for adding variants

# Product admin with inlines for managing images and variants
class ProductAdmin(admin.ModelAdmin):

    form = ProductForm
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name',)
    list_display = ('name', 'vendor', 'price', 'stock', 'category')
    list_filter = ('vendor', 'category')
    search_fields = ('name', 'vendor__store_name')# Organize the form into fieldsets
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
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
    inlines = [ProductImageInline, ProductVariantInline]  # Add inlines for images and variants
        # Override the queryset to filter products based on the logged-in vendor
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all products
        else:
            # Filter the products to show only those of the current vendor
            return qs.filter(vendor__email=request.user.email)


# Ensure that the custom CSS is applied to all admin models globally


# Register the models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

