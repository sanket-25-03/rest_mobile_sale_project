# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label='Max Price')
    
    brand = django_filters.CharFilter(field_name="brand", lookup_expr='icontains', label='Brand')
    
    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'brand']
