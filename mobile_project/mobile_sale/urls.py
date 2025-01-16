from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import ProductListView, ProductCreateView, OrderCreateView, index, add_product_view, order_list, create_order_view

urlpatterns = [
    path('', index, name='index'), 
    
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('add-product/', add_product_view, name='add-product'),
    path('products/add/', add_product_view, name='add_product'),  # For adding a product
    path('products/edit/<int:product_id>/', add_product_view, name='edit_product'), 


    path('create-order/', create_order_view, name='order-product'),
    path('order/create/', OrderCreateView.as_view(), name='order-create'),  

    path('products/', ProductListView.as_view(), name='product-list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    