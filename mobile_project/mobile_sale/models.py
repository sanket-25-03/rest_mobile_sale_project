from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import User

class Product(models.Model):
    prod_image = models.ImageField(upload_to='products/', null=True, blank=True)
    product_name = models.CharField(max_length=100,unique=True)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.TextField()
    category = models.CharField(max_length=50, default="Mobile")
    overall_rating = models.FloatField(editable=False, null=True, blank=True)
    reviews_count = models.IntegerField(editable=False, default=0)

    def update_ratings(self):
        reviews_data = self.reviews.aggregate(
            avg_rating=Avg('overall_rating'),
            count_reviews=Count('id')
        )
        self.overall_rating = reviews_data['avg_rating'] or 0
        self.reviews_count = reviews_data['count_reviews']
        self.save()


class Reviews(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quality_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    performance_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    user_exp_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    overall_rating = models.FloatField(editable=False)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.overall_rating = (self.quality_rating + self.performance_rating + self.user_exp_rating) / 3
        super().save(*args, **kwargs)


class Inventory(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='inventory')
    imei_number = models.CharField(max_length=15, unique=True)
    detailed_info = models.TextField()
    stock_quantity = models.PositiveIntegerField(default=0)
    os = models.CharField(max_length=50, verbose_name="Operating System")
    ram = models.CharField(max_length=10, verbose_name="RAM")
    storage = models.CharField(max_length=10, verbose_name="Storage")
    battery_capacity = models.CharField(max_length=20, verbose_name="Battery Capacity")
    screen_size = models.CharField(max_length=10, verbose_name="Screen Size")
    camera_details = models.TextField(null=True, blank=True, verbose_name="Camera Details")
    processor = models.CharField(max_length=50, null=True, blank=True, verbose_name="Processor")

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_items_list = models.JSONField()

    def calculate_total_price(self):
        total = 0
        for item in self.ordered_items_list:
            total += item['price'] * item['quantity']
        self.total_price = total
        self.save()
        
        self.calculate_total_price()
        self.save()