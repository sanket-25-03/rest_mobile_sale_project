from django.contrib import admin
from .models import User, Product, Reviews, Inventory, Order, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'status', 'total_price', 'created_at')
    search_fields = ('order_id', 'user__username')
    list_filter = ('status', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')
    search_fields = ('order__order_id', 'product__product_name')