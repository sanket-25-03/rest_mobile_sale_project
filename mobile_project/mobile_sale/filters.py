from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    brand = filters.CharFilter(field_name="brand", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'brand']
