from rest_framework import generics, filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.shortcuts import render, redirect
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer



class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr='icontains', label='Brand')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')

    class Meta:
        model = Product
        fields = ['brand', 'price']


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['price', 'name']
    ordering = ['price']


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    products = Product.objects.all()
    return render(request, 'mobile_sale/index.html', {'products': products})


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
