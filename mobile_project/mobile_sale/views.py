from rest_framework import generics, filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from .models import Product, Order, Reviews
from .serializers import ProductSerializer, OrderSerializer
from django.contrib.auth.models import User



from django_filters import rest_framework as filters

class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    brand = filters.CharFilter(field_name="brand", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'brand']

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    products = Product.objects.all()
    return render(request, 'mobile_sale/index.html', {'products': products})


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'mobile_sale/orders.html', {'orders': orders})


def add_product_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        prod_image = request.FILES.get('prod_image')

        Product.objects.create(
            name=name,
            brand=brand,
            price=price,
            description=description,
            quantity=quantity,
            prod_image=prod_image
        )
        return redirect('index') 
    return render(request, 'mobile_sale/AddProducts.html')

def create_order_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        Order.objects.create(product=product, quantity=quantity, username=request.user)
        return redirect('order-list')
    return render(request, 'mobile_sale/Order.html')

from django.shortcuts import render

def create_order(request):
    brand_name = request.GET.get('brand_name', 'Default Brand')
    return render(request, 'create_order.html', {'brand_name': brand_name})

# view for the Review list
def review_list(request):
    # Fetch all reviews from the database
    reviews = Reviews.objects.all()
    overall_average_rating = 4.5  # Replace with actual calculation if needed

    context = {
        'reviews': reviews,
        'overall_average_rating': overall_average_rating,
        'range': range(1, 6),  # Used for dropdowns
    }
    return render(request, 'reviews.html', context)

def submit_review(request):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')

        # Create and save the review
        review = Reviews(
            reviews=review_text
        )
        review.save()
        return redirect('review_list')  # Redirect to the review list after submission

    return render(request, 'reviews.html')