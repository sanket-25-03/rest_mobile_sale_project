from django.urls import path
from .views import ProductListView, ProductCreateView, OrderCreateView
from . import views


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'), 
    path('place-order/', OrderCreateView.as_view(), name='place-order'),
    path('', views.index, name='index'),
    path('orders/', views.OrderCreateView.as_view(), name='order_list'),



]