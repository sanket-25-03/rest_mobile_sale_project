from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('mobile/', views.index, name='index'), 
    path('mobile/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('mobile/update/<int:product_id>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('mobile/filter/', views.ProductListView.as_view(), name='product-list'),  
    path('mobile/delete/<int:product_id>/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('mobile/order/', views.OrderCreateView.as_view(), name='order-create'),
    path('mobile/review/', views.ReviewCreateView.as_view(), name='review-create'),
    
    
    path('mobile/products/', views.product_list_view, name='product-list'),
    path('mobile/products/<int:product_id>/', views.product_detail_view, name='product-detail'),
    path('mobile/orders/', views.order_list_view, name='order-list'),
    path('mobile/reviews/', views.review_list_view, name='review-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
