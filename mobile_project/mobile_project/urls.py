from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mobile_sale.urls')),
    path('auth/', include('mobile_sale.urls')),  # Add this line to include authentication URLs

]
