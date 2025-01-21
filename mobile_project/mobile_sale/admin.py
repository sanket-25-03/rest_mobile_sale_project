from django.contrib import admin
from .models import Order, Product, Reviews, Inventory

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'status']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'brand', 'price', 'short_description', 'overall_rating', 'reviews_count']
    list_filter = ['brand', 'price']
    search_fields = ['product_name', 'brand']
    readonly_fields = ['overall_rating', 'reviews_count']

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['product', 'quality_rating', 'performance_rating', 'user_exp_rating', 'overall_rating', 'created_at']
    list_filter = ['created_at', 'overall_rating']
    search_fields = ['product__product_name', 'review']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'imei_number', 'stock_quantity', 'os', 'ram', 'storage', 'battery_capacity']
    list_filter = ['os', 'stock_quantity']
    search_fields = ['product__product_name', 'imei_number', 'os']

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Inventory, InventoryAdmin)
