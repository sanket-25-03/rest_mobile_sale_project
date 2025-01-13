from rest_framework import serializers
from .models import Order, Product, User, Reviews

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Order
        fields = ['id', 'username', 'product', 'quantity', 'order_date']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['username', 'email', 'reviews']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'description', 'reviews', 'quantity', 'prod_image']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
