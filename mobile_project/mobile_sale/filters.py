from django_filters import rest_framework as filters
from .models import Product, Reviews, Order

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

class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'user': ['exact'],
            'status': ['exact'],
            'created_at': ['date__gte', 'date__lte'],
        }
