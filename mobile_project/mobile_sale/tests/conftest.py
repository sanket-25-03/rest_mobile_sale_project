import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from mobile_sale.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_product(db):
    """Fixture to create a sample product"""
    return Product.objects.create(name="Laptop", price=1000, stock=10)
