from rest_framework import serializers
from .models import ProductType, Category, Product, Variant, VariantValue, ProductImage, ProductSpecification
from django.conf import settings
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = '__all__'

class VariantValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantValue
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    variant_values = VariantValueSerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = '__all__'



from rest_framework import serializers
from django.conf import settings

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return f"{settings.MEDIA_URL}{obj.image.url}"
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'history', 
            'category', 'product_type', 'specifications', 'images', 'gestionnaire'
        ]
        
class ProductPageSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'history', 'slug',
            'category', 'product_type', 'specifications', 'images', 'gestionnaire'
        ]        