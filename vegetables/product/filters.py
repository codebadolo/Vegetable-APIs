# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category_slug = django_filters.CharFilter(field_name='category__slug', method='filter_category_slug')

    class Meta:
        model = Product
        fields = ['category', 'product_type', 'price']  # Only direct model fields

    def filter_category_slug(self, queryset, name, value):
        return queryset.filter(category__slug=value)
