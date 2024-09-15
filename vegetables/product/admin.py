from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, Category
from .forms import ProductForm
# Register Category model (for tree-based categorization)
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category
from unfold.admin import ModelAdmin ,TabularInline
from vendors.models  import Vendor
from product.forms import ProductForm
from django.utils.html import format_html
class CategoryAdmin(ModelAdmin , MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    mptt_level_indent = 20  # Set indentation for subcategories

# Inline admin for managing product images within the product admin
class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1  # Show one empty form for adding images
    fields = ['image']  # Display the image field only


# Inline admin for managing product variants within the product admin
class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1  # Show one empty form for adding variants
    fields = ['name', 'price', 'stock']  # Display these fields for variants
class ProductAdmin(ModelAdmin):
    model = Product
    list_display = ('name', 'vendor', 'price', 'stock', 'category', 'display_image')
    search_fields = ('name', 'vendor__store_name')
    list_filter = ('vendor', 'category')

    # Inlines for images and variants in ProductAdmin
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

    def display_image(self, obj):
        """
        Display the first image of the product in the admin list view.
        """
        if obj.images.exists():  # Assuming related_name='images' in ProductImage model
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', obj.images.first().image.url)
        return "No Image"
    
    display_image.short_description = 'Image'

    def get_queryset(self, request):
        """
        Ensure that vendors can only see their own products in the product list.
        """
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Vendor').exists():
            return qs.filter(vendor__user=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        """
        Automatically assign the vendor based on the logged-in user.
        """
        if not request.user.is_superuser:
            try:
                vendor = Vendor.objects.get(user=request.user)
                obj.vendor = vendor
            except Vendor.DoesNotExist:
                raise ValidationError("You are not associated with any vendor account.")
        super().save_model(request, obj, form, change)


# Register the models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

