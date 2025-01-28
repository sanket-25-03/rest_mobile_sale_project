from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import Product, Reviews, Inventory, Order
from .serializers import ProductSerializer, ReviewSerializer, InventorySerializer, OrderSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .pagination import CustomPagination

class ProductAPIView(GenericAPIView):
    serializer_class = ProductSerializer
    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
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
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewAPIView(GenericAPIView):
    serializer_class  = ReviewSerializer
    def get(self, request, pk=None):
        if pk:
            review = get_object_or_404(Reviews, pk=pk)
            serializer = ReviewSerializer(review)
        else:
            reviews = Reviews.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        review = get_object_or_404(Reviews, pk=pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
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
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryAPIView(GenericAPIView):
    serializer_class = InventorySerializer
    def get(self, request, pk=None):
        if pk:
            inventory = get_object_or_404(Inventory, pk=pk)
            serializer = InventorySerializer(inventory)
        else:
            inventories = Inventory.objects.all()
            serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        inventory = get_object_or_404(Inventory, pk=pk)
        serializer = InventorySerializer(inventory, data=request.data, partial=True)
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
    serializer_class   = InventorySerializer
    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderAPIView(GenericAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk, user=request.user)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not pk:
            return Response({"message": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order, data=request.data, partial=True)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

#token
class LoginAPI(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if not user:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token_expiry = refresh.access_token['exp'] * 1000  
        refresh_token_expiry = refresh['exp'] * 1000

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'access_token_expiry': access_token_expiry,
            'refresh_token_expiry': refresh_token_expiry
        }, status=status.HTTP_200_OK)


#pagination
class UnifiedPaginatedAPI(GenericAPIView):
    serializer_class = None
    pagination_class = CustomPagination

    def get(self, request):
        model = request.query_params.get("model", "").lower()

        if model == "product":
            queryset = Product.objects.all()
            serializer_class = ProductSerializer
        elif model == "review":
            queryset = Reviews.objects.all()
            serializer_class = ReviewSerializer
        elif model == "inventory":
            queryset = Inventory.objects.all()
            serializer_class = InventorySerializer
        elif model == "order":
            queryset = Order.objects.filter(user=request.user)
            serializer_class = OrderSerializer
        else:
            return Response(
                {"error": "Invalid model specified. Choose from ['product', 'review', 'inventory', 'order']."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
