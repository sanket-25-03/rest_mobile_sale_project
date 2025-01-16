from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import ProductListView, ProductCreateView, OrderCreateView, index, add_product_view, order_list, create_order_view

urlpatterns = [
    path('', index, name='index'),  # Home page
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),  # Product creation view
    path('place-order/', OrderCreateView.as_view(), name='place-order'),  # Order creation view
    path('add-product/', add_product_view, name='add-product'),  # Add product view
    path('orders/create/', create_order_view, name='order-create'),  
    path('orders/', order_list, name='order-list'),  # Order list view
    path('create-order/', views.create_order, name='create_order'),
    path('', views.review_list, name='review_list'),  
    path('submit_review/', views.submit_review, name='submit_review'),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    