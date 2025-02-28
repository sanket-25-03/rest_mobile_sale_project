from rest_framework import serializers
from .models import Product, Reviews, Inventory, Order
from django.contrib.auth.models import User
from .validators import validate_imei_number

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    # Field-Level Validation
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
    #Object-Level Validation 
        read_only_fields = ['overall_rating', 'user']  # Prevent users from manually setting these fields

    def validate(self, data):
        quality_rating = data.get('quality_rating')
        performance_rating = data.get('performance_rating')
        user_exp_rating = data.get('user_exp_rating')
        review = data.get('review')

        # Validate individual rating fields
        for field_name, value in {
            "quality_rating": quality_rating,
            "performance_rating": performance_rating,
            "user_exp_rating": user_exp_rating,
        }.items():
            if value and (value < 1 or value > 5):
                raise serializers.ValidationError({field_name: "Rating must be between 1 and 5."})

        # Validate review length
        if review and len(review.strip()) < 10:
            raise serializers.ValidationError({"review": "Review must be at least 10 characters long."})

        return data
    
    
class InventorySerializer(serializers.ModelSerializer):
    imei_number = serializers.CharField(validators=[validate_imei_number])  
    # Custom validator 
    class Meta:
        model = Inventory
        fields = '__all__'
    

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
