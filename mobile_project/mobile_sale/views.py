from rest_framework import generics, filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


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
    # Fetch all products to display on the frontend
    products = Product.objects.all()
    return render(request, 'mobile_sale/index.html', {'products': products})


def order_list(request):
    # Fetch all orders to display on the frontend
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
        return redirect('order-list')

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'mobile_sale/Order.html', context)



from django.shortcuts import render

def create_order(request):
    # Example: Retrieve the selected brand name from a GET parameter or session
    brand_name = request.GET.get('brand_name', 'Default Brand')
    return render(request, 'create_order.html', {'brand_name': brand_name})
