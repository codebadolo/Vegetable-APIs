from django.contrib import admin
from .models import (
    ProductType,
    Variant,
    VariantValue,
    Product,
    ProductImage,
    Gestionnaire,
    Category,
    ProductSpecification
)
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from django.urls import path
from unfold.admin import ModelAdmin, TabularInline
from .forms import ProductForm
from django import forms
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .views import  FeaturedProductsView ,OutOfStockProductsView
from django.core.exceptions import ValidationError

class CategoryAdmin(ModelAdmin, MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    mptt_level_indent = 20
    list_filter = ('parent',)  # Add filtering by parent category

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(TabularInline):
    model = ProductSpecification
    extra = 1
class ProductAdmin(ModelAdmin):
    #form = ProductForm

    list_display = ('name', 'history', 'price', 'category', 'display_image')
    search_fields = ('name', 'category__name')
    list_filter = ('gestionnaire', 'category')
    inlines = [ProductSpecificationInline ,ProductImageInline]  # Include inline

    fieldsets = (
        ('Name  & History', {
            'fields': ('name', 'description', 'gestionnaire' , 'history' ,'featured')
        }),
           

  
        ('Pricing & Categorization', {
            'fields': ('price', 'category', 'product_type')
        }),
    
   
     
    )

    def display_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover;" />', 
                             primary_image.image.url)
        else:
            return "No Image"
    display_image.short_description = 'Main Image'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # For Gestionnaires: show only their products
            try:
                gestionnaire = Gestionnaire.objects.get(user=request.user)
                return qs.filter(gestionnaire=gestionnaire)
            except Gestionnaire.DoesNotExist:
                pass
        return qs

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            #path('custom-admin-page/', self.admin_site.admin_view(CustomAdminView.as_view(model_admin=self)), name='product_product_tools'),
            path('featured-products/', self.admin_site.admin_view(FeaturedProductsView.as_view(model_admin=self)), name='product_product_featured_products'),
            path('out-of-stock-products/', self.admin_site.admin_view(OutOfStockProductsView.as_view(model_admin=self)), name='product_product_out_of_stock_products'),
        ]
        return custom_urls + urls
    def custom_admin_view(self, request):
        return CustomAdminView.as_view(model_admin=self)(request)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Add custom context data here if needed
        extra_context['custom_variable'] = "This is a custom product list!"
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            try:
                # Auto-assign gestionnaire if not superuser
                obj.gestionnaire = Gestionnaire.objects.get(user=request.user)
            except Gestionnaire.DoesNotExist:
                raise ValidationError("You must be a registered Gestionnaire to manage products")
        super().save_model(request, obj, form, change)

    def availability_status(self, obj):
        return obj.get_availability_display()
    availability_status.short_description = 'Status'

class VariantValueInline(TabularInline):
    model = VariantValue
    extra = 1

class VariantInline(TabularInline):
    model = Variant
    extra = 1
    inlines = [VariantValueInline]  # Nested inline

class ProductTypeAdmin(ModelAdmin):
    list_display = ('name', 'description')
    inlines = [VariantInline]  # Show related variants

    
class VariantAdmin(ModelAdmin):
    pass

class VariantValueAdmin(ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(VariantValue, VariantValueAdmin)
