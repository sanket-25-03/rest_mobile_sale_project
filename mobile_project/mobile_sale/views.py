from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import Product, Reviews, Inventory, Order
from .serializers import (
    ProductSerializer, ReviewSerializer, InventorySerializer, OrderSerializer, 
    RegisterSerializer, LoginSerializer, UserSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from .pagination import CustomPagination


class ProductAPIView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = self.serializer_class(product)
        else:
            products = Product.objects.all()
            serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for delete"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"success": f"Product with ID {pk} has been deleted."}, status=status.HTTP_200_OK)

class ProductCreateAPIView(GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        products = Product.objects.all()
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = self.serializer_class(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

class ReviewAPIView(GenericAPIView):
    serializer_class = ReviewSerializer

    def get(self, request, pk=None):
        if pk:
            review = get_object_or_404(Reviews, pk=pk)
            serializer = self.serializer_class(review)
        else:
            reviews = Reviews.objects.all()
            serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        review = get_object_or_404(Reviews, pk=pk)
        serializer = self.serializer_class(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for delete"}, status=status.HTTP_400_BAD_REQUEST)
        review = get_object_or_404(Reviews, pk=pk)
        review.delete()
        return Response({"success": "Review deleted."}, status=status.HTTP_200_OK)

class ReviewCreateAPIView(GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        reviews = Reviews.objects.all()
        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)
        serializer = self.serializer_class(paginated_reviews, many=True)
        return paginator.get_paginated_response(serializer.data)

class InventoryAPIView(GenericAPIView):
    serializer_class = InventorySerializer

    def get(self, request, pk=None):
        if pk:
            inventory = get_object_or_404(Inventory, pk=pk)
            serializer = self.serializer_class(inventory)
        else:
            inventories = Inventory.objects.all()
            serializer = self.serializer_class(inventories, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        inventory = get_object_or_404(Inventory, pk=pk)
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for delete"}, status=status.HTTP_400_BAD_REQUEST)
        inventory = get_object_or_404(Inventory, pk=pk)
        inventory.delete()
        return Response({"success": f"Inventory with ID {pk} has been deleted."}, status=status.HTTP_200_OK)

class InventoryCreateAPIView(GenericAPIView):
    serializer_class = InventorySerializer
    pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        inventories = Inventory.objects.all()
        paginator = self.pagination_class()
        paginated_inventories = paginator.paginate_queryset(inventories, request)
        serializer = self.serializer_class(paginated_inventories, many=True)
        return paginator.get_paginated_response(serializer.data)

class OrderAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk, user=request.user)
            serializer = self.serializer_class(order)
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for delete"}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk, user=request.user)
        order.delete()
        return Response({"success": "Order deleted."}, status=status.HTTP_200_OK)

class OrderCreateAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        paginator = self.pagination_class()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = self.serializer_class(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if not user:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'access_token_expiry': api_settings.ACCESS_TOKEN_LIFETIME.total_seconds(),
            'refresh_token_expiry': api_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
        }, status=status.HTTP_200_OK)
