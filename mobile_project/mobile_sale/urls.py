from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('mobile/', views.ProductView.as_view(), name='ProductView'), 
    path('review/', views.ReviewView.as_view(), name='ReviewView'), 
    path('Inventory/', views.InventoryView.as_view(), name='InventoryView'), 
    path('order/', views.OrderView.as_view(), name='OrderView'), 
    path('register/', views.RegisterAPI.as_view(), name='RegisterAPI'),
    path('login/', views.LoginAPI.as_view(), name='LoginAPI'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

