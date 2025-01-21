from rest_framework.exceptions import APIException
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Reviews, Inventory
from .serializers import ProductSerializer, ReviewSerializer, InventorySerializer

from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.db import IntegrityError
class ProductView(APIView):
    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "A product with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        product_id = request.data.get("id")
        if not product_id:
            return Response({"error": "Product ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except IntegrityError:
                return Response({"error": "A product with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        product_id = request.data.get("id")
        if not product_id:
            return Response({"error": "Product ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return Response({"success": f"Product with ID {product_id} has been deleted."}, status=status.HTTP_200_OK)

from rest_framework.permissions import IsAuthenticated

class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            review = get_object_or_404(Reviews, pk=pk, user=request.user)
            serializer = ReviewSerializer(review)
        else:
            reviews = Reviews.objects.filter(user=request.user)
            serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        review = get_object_or_404(Reviews, pk=request.data.get("id"), user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        review = get_object_or_404(Reviews, pk=request.data.get("id"), user=request.user)
        review.delete()
        return Response({"success": "Review deleted."}, status=status.HTTP_200_OK)


class InventoryView(APIView):
    def get(self, request, pk=None):
        if pk:
            inventory = get_object_or_404(Inventory, pk=pk)
            serializer = InventorySerializer(inventory)
        else:
            inventories = Inventory.objects.all()
            serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        inventory_id = request.data.get("id")
        if not inventory_id:
            return Response({"error": "Inventory ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        inventory = get_object_or_404(Inventory, pk=inventory_id)
        serializer = InventorySerializer(inventory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        inventory_id = request.data.get("id")
        if not inventory_id:
            return Response({"error": "Inventory ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        inventory = get_object_or_404(Inventory, pk=inventory_id)
        inventory.delete()
        return Response({"success": f"Inventory with ID {inventory_id} has been deleted."}, status=status.HTTP_200_OK)

from rest_framework.permissions import IsAuthenticated

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"success": "User deleted."}, status=status.HTTP_200_OK)

from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk, user=request.user)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        order = get_object_or_404(Order, pk=request.data.get("id"), user=request.user)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        order = get_object_or_404(Order, pk=request.data.get("id"), user=request.user)
        order.delete()
        return Response({"success": "Order deleted."}, status=status.HTTP_200_OK)
