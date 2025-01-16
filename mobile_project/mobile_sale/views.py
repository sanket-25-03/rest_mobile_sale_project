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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def add_product_view(request, product_id=None):
    product = None
    if product_id:
        product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        prod_image = request.FILES.get('prod_image')

        if product:
            # Update existing product
            product.name = name
            product.brand = brand
            product.price = price
            product.description = description
            product.quantity = quantity
            if prod_image:
                product.prod_image = prod_image
            product.save()
        else:
            # Create a new product
            Product.objects.create(
                name=name,
                brand=brand,
                price=price,
                description=description,
                quantity=quantity,
                prod_image=prod_image
            )
        return redirect('index')

    return render(request, 'mobile_sale/AddProducts.html', {'product': product})

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
