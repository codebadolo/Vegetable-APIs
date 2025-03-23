from django.db import models
from vendors.models import Gestionnaire  # Import Vendor from the vendor app
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.db import models
from django.db import models
from django.utils.text import slugify

from django.utils.text import slugify
# Product Type Model
class ProductType(models.Model):
    name = models.CharField(max_length=100)  # Product type (e.g., Electronics, Clothing)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Category Model
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', blank=True, null=True) 
    featured = models.BooleanField(default=False) # Add this field
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    history = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    gestionnaire = models.ForeignKey(
        Gestionnaire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=1  # Set a default value here
    )
    product_type = models.ForeignKey('ProductType', on_delete=models.SET_NULL, null=True, blank=True)
    featured = models.BooleanField(default=False) # Add this field

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"

@receiver(pre_save, sender=Product)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)
# Product Specification Model
class Variant(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, related_name='variants', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class VariantValue(models.Model):
    variant = models.ForeignKey(Variant, related_name='variant_values', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value
# Product Image Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, blank=True, null=True)
    variant_value = models.ForeignKey(VariantValue, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)  # Add this line
    alt_text = models.CharField(max_length=255, blank=True, null=True) # Add this line

    def __str__(self):
        return f"Image for {self.product.name}"