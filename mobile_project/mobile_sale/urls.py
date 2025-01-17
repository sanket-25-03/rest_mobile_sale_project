from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('mobile/', views.index, name='index'), 
    path('mobile/products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('mobile/products/update/<int:product_id>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('mobile/products/filter/', views.ProductListView.as_view(), name='product-list'),  
    path('mobile/products/delete/<int:product_id>/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('mobile/order/', views.OrderCreateView.as_view(), name='order-create'),
    path('mobile/review/', views.ReviewCreateView.as_view(), name='review-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
