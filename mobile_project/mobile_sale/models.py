from django.db import models

class Reviews(models.Model):
    model_number = models.CharField(max_length=100, default="Unknown")
    reviews = models.CharField(max_length=200)

class Product(models.Model):
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    reviews = models.ManyToManyField(Reviews, blank=True)
    quantity = models.IntegerField()
    prod_image = models.ImageField(upload_to='products/', null=True)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField()
