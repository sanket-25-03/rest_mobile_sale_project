from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order, Reviews
from .serializers import ProductSerializer, OrderSerializer
from django.contrib.auth.models import User

# Django Filters
from django_filters import rest_framework as filters

# Product Filter for the list view
class ProductFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    brand = filters.CharFilter(field_name="brand", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'brand']

# Product list view with filtering, searching, and ordering
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return render(request, 'mobile_sale/product_list.html', {'products': response.data})

# Product creation view
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Order creation view
class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Index page with all products
def index(request):
    # Fetch all products to display on the frontend
    products = Product.objects.all()
    return render(request, 'mobile_sale/index.html', {'products': products})

# Order list page
def order_list(request):
    # Fetch all orders to display on the frontend
    orders = Order.objects.all()
    return render(request, 'mobile_sale/orders.html', {'orders': orders})

# Add product view (Function-based)
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
        return redirect('index')  # Redirect to the index page after product creation

    return render(request, 'mobile_sale/AddProducts.html')

# Order creation view (Function-based)
def create_order_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        order_date = request.POST.get('order_date')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return render(request, 'mobile_sale/Order.html', {'error': 'Invalid product selected.'})

        Order.objects.create(
            product=product,
            quantity=quantity,
            order_date=order_date
        )

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'mobile_sale/Order.html', context)

# Create order view (simplified version)
def create_order(request):
    # Example: Retrieve the selected brand name from a GET parameter or session
    brand_name = request.GET.get('brand_name', 'Default Brand')
    return render(request, 'create_order.html', {'brand_name': brand_name})

# Review list view
def review_list(request):
    reviews = Reviews.objects.all()
    overall_average_rating = 4.5  # Replace with actual calculation if needed

    context = {
        'reviews': reviews,
        'overall_average_rating': overall_average_rating,
        'range': range(1, 6),  # Used for dropdowns
    }
    return render(request, 'reviews.html', context)

# Submit review view
def submit_review(request):
    if request.method == 'POST':
        review_text = request.POST.get('review_text')

        # Create and save the review
        review = Reviews(
            reviews=review_text
        )
        review.save()