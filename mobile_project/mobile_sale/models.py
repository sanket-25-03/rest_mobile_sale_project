from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .validators import validate_imei_number


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')    
    imei_number = models.CharField(max_length=15, unique=True, validators=[validate_imei_number])
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
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    


@receiver(post_save, sender=Reviews)
@receiver(post_delete, sender=Reviews)
def update_product_ratings(sender, instance, **kwargs):
    product = instance.product
    product.update_ratings()