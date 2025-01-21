from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Reviews, Inventory, Order, OrderItem
from .serializers import ProductSerializer, ReviewSerializer, InventorySerializer, OrderSerializer, OrderItemSerializer
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

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


class ReviewView(APIView):
    def get(self, request, pk=None):
        if pk:
            review = get_object_or_404(Reviews, pk=pk)
            serializer = ReviewSerializer(review)
        else:
            reviews = Reviews.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        review_id = request.data.get("id")
        if not review_id:
            return Response({"error": "Review ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(Reviews, pk=review_id)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        review_id = request.data.get("id")
        if not review_id:
            return Response({"error": "Review ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(Reviews, pk=review_id)
        review.delete()
        return Response({"success": f"Review with ID {review_id} has been deleted."}, status=status.HTTP_200_OK)


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


class OrderView(APIView):
    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        order_id = request.data.get("id")
        if not order_id:
            return Response({"error": "Order ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        order_id = request.data.get("id")
        if not order_id:
            return Response({"error": "Order ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response({"success": f"Order with ID {order_id} has been deleted."}, status=status.HTTP_200_OK)


class OrderItemView(APIView):
    def get(self, request, pk=None):
        if pk:
            order_item = get_object_or_404(OrderItem, pk=pk)
            serializer = OrderItemSerializer(order_item)
        else:
            order_items = OrderItem.objects.all()
            serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        order_item_id = request.data.get("id")
        if not order_item_id:
            return Response({"error": "OrderItem ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        order_item = get_object_or_404(OrderItem, pk=order_item_id)
        serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        order_item_id = request.data.get("id")
        if not order_item_id:
            return Response({"error": "OrderItem ID is required in the JSON body"}, status=status.HTTP_400_BAD_REQUEST)

        order_item = get_object_or_404(OrderItem, pk=order_item_id)
        order_item.delete()
        return Response({"success": f"OrderItem with ID {order_item_id} has been deleted."}, status=status.HTTP_200_OK)


User = get_user_model()

class UserView(APIView):
    def post(self, request):
        # Use the UserSerializer to validate the request data
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the user instance
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)