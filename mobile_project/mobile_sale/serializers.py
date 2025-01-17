from rest_framework import serializers
from .models import Reviews, Product, Order

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['model_number', 'reviews']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id','name', 'model_number', 'brand', 'price', 'description', 'reviews', 'quantity', 'prod_image']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','product', 'quantity', 'order_date']
