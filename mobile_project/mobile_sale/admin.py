from django.contrib import admin
from .models import User,Order,Product,Reviews

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','password']
    list_filter = ['email']
    search_fields = ['email', 'username']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','order_date']
    search_fields = ['order_date']
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','brand','price','description','quantity']
    list_filter = ['name','brand','price']
    search_fields = ['name', 'brand','price']
    
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['reviews']

admin.site.register(User,UserAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Reviews,ReviewsAdmin)