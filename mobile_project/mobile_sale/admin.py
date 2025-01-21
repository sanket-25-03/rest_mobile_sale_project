from django.contrib import admin
from django.contrib import admin
from .models import Product, Reviews, Inventory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'brand', 'price', 'category', 'overall_rating', 'reviews_count')
    search_fields = ('product_name', 'brand', 'category')
    list_filter = ('brand', 'category')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'overall_rating', 'created_at', 'updated_at')
    search_fields = ('product__product_name', 'user__username')
    list_filter = ('created_at', 'updated_at')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'imei_number', 'stock_quantity', 'os', 'ram', 'storage')
    search_fields = ('product__product_name', 'imei_number')
    list_filter = ('os',)
    
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_price', 'status', 'payment_method', 'payment_status']
    list_filter = ['status', 'payment_status', 'order_date']
    search_fields = ['user__username', 'shipping_address']
    ordering = ['-order_date']

admin.site.register(Order, OrderAdmin)

from django.contrib import admin
from rest_framework.authtoken.models import Token

admin.site.register(Token)

