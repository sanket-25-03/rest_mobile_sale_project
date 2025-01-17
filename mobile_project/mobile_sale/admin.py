from django.contrib import admin
from .models import Order,Product,Reviews
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','order_date']
    search_fields = ['order_date']
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','brand','price','description','quantity']
    list_filter = ['name','brand','price']
    search_fields = ['name', 'brand','price']

admin.site.register(Order,OrderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Reviews)