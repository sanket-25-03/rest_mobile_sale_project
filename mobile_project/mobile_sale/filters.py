from django_filters import rest_framework as filters
from .models import Product, Reviews

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name': ['icontains'],
            'brand': ['icontains'],
            'category': ['exact'],
            'price': ['gte', 'lte'],
        }

class ReviewFilter(filters.FilterSet):
    class Meta:
        model = Reviews
        fields = {
            'product': ['exact'],
            'user': ['exact'],
            'overall_rating': ['gte', 'lte'],
        }

