from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter 

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter

    search_fields = ['name', 'brand']
    ordering_fields = ['price', 'name']

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return render(request, 'mobile_sale/product_list.html', {'products': response.data})


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


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product
import json

def add_product_view(request, product_id=None):
    if request.method == 'POST':
        # Handle adding a new product
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

    elif request.method == 'PATCH' and product_id:
        # Handle updating an existing product
        product = get_object_or_404(Product, id=product_id)
        body = request.body.decode('utf-8')
        data = json.loads(body)  # Parse JSON data from the PATCH request

        # Update fields if present in the request
        if 'name' in data:
            product.name = data['name']
        if 'brand' in data:
            product.brand = data['brand']
        if 'price' in data:
            product.price = data['price']
        if 'description' in data:
            product.description = data['description']
        if 'quantity' in data:
            product.quantity = data['quantity']
        if 'prod_image' in request.FILES:
            product.prod_image = request.FILES['prod_image']

        product.save()
        return JsonResponse({'message': 'Product updated successfully'}, status=200)

    return render(request, 'mobile_sale/AddProducts.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, Order

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



from django.shortcuts import render

def create_order(request):
    brand_name = request.GET.get('brand_name', 'Default Brand')
    return render(request, 'create_order.html', {'brand_name': brand_name})
