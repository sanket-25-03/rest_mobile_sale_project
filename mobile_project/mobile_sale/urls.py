from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import ProductListView, ProductCreateView, OrderCreateView, index, add_product_view, order_list, create_order_view

urlpatterns = [
    path('', index, name='index'), 
    
    path('products/', ProductListView.as_view(), name='product-list'),  # Product list view
    path('products/create/', ProductCreateView.as_view(), name='product-create'),  # Product creation view
    path('add-product/', add_product_view, name='add-product'),  # Add product view
    
    path('create-order/', create_order_view, name='order-product'),  # Create order view
    path('orders/', order_list, name='order-list'),  # Order list view
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),  # Order creation view
    path('create-order/', views.create_order, name='create_order'),
    path('', views.review_list, name='review_list'),  
    path('submit_review/', views.submit_review, name='submit_review'),

    path('submit_review', views.submit_review, name='submit_review'),  # Submit review view
    path('review_list', views.review_list, name='review_list'),  # Review list view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
