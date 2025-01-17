from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, Reviews
from .serializers import ProductSerializer, OrderSerializer, ReviewSerializer
from .filters import ProductFilter 

class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
        products = product_filter.qs
        product_data = ProductSerializer(products, many=True).data
        return JsonResponse({'products': product_data})
class ProductCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewCreateView(APIView):
    def post(self, request, *args, **kwargs):
        model_number = request.data.get('model_number')
        product = Product.objects.filter(model_number=model_number).first()
        if not product:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        review_data = request.data.get('reviews')
        review = Reviews.objects.create(model_number=model_number, reviews=review_data)
        product.reviews.add(review)
        return JsonResponse({'message': 'Review added successfully', 'review': ReviewSerializer(review).data}, status=status.HTTP_201_CREATED)

def index(request):
    products = Product.objects.all()
    product_data = ProductSerializer(products, many=True).data
    return JsonResponse({'products': product_data})


class ProductUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = Product.objects.filter(id=product_id).first()

        if not product:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Product updated successfully', 'product': serializer.data}, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = Product.objects.filter(id=product_id).first()

        if not product:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()

        return JsonResponse({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)