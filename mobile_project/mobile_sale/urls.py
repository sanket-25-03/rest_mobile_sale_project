from django.urls import path
from .views import ProductListView, ProductCreateView, OrderCreateView
from . import views
from .views import add_product_view

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'), 
    path('place-order/', OrderCreateView.as_view(), name='place-order'),
    path('', views.index, name='index'),
    path('orders/', views.OrderCreateView.as_view(), name='order_list'),
    path('', views.index, name='index'),  # Index page
    path('products/', ProductListView.as_view(), name='product-list'),  # Product list view
    path('products/add/', add_product_view, name='add_product'),  # Add product form
    path('products/create/', ProductCreateView.as_view(), name='product-create'),  # Keep this for backward compatibility
    path('place-order/', OrderCreateView.as_view(), name='place-order'),  # Place order view
]