from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UnifiedPaginatedAPI

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import (
    ProductAPIView, ProductCreateAPIView,
    ReviewAPIView, ReviewCreateAPIView,
    InventoryAPIView, InventoryCreateAPIView,
    OrderAPIView, OrderCreateAPIView,
    RegisterAPI, LoginAPI
)

urlpatterns = [
    path('mobile/', ProductCreateAPIView.as_view(), name='product-create'),
    path('mobile/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
    
    path('review/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewAPIView.as_view(), name='review-detail'),

    path('Inventory/', InventoryCreateAPIView.as_view(), name='inventory-create'),
    path('Inventory/<int:pk>/', InventoryAPIView.as_view(), name='inventory-detail'),

    path('order/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/<int:pk>/', OrderAPIView.as_view(), name='order-detail'),

    path('register/', RegisterAPI.as_view(), name='RegisterAPI'),
    path('login/', LoginAPI.as_view(), name='LoginAPI'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # using this fetch /api/unified/?model=    (product, review, inventory, order)
    path('api/unified/', UnifiedPaginatedAPI.as_view(), name='unified-paginated-api'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

