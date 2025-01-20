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
    path('mobile/order/<int:pk>/', views.OrderEditView.as_view(), name='order-edit'),
    path('mobile/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('mobile/review/<int:pk>/', views.ReviewEditView.as_view(), name='review-edit'),

    
    path('mobile/products/', views.product_list_view, name='product-list'),
    path('mobile/products/<int:product_id>/', views.product_detail_view, name='product-detail'),
    path('mobile/orders/', views.order_list_view, name='order-list'),
    path('mobile/reviews/', views.review_list_view, name='review-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
