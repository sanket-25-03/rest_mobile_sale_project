from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('mobile/', views.ProductView.as_view(), name='ProductView'), 
    path('review/', views.ReviewView.as_view(), name='ReviewView'), 
    path('Inventory/', views.InventoryView.as_view(), name='InventoryView'), 
    path('user/', views.UserView.as_view(), name='UserView'), 
    path('order/', views.OrderView.as_view(), name='OrderView'), 
    path('register/', views.RegisterAPI.as_view(), name='RegisterAPI'),
    path('login/', views.LoginAPI.as_view(), name='LoginAPI'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
