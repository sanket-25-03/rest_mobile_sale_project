import pytest
from mobile_sale.models import Product
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_productcreate():
    client = APIClient()
    url = reverse("product-create")
    valid_payload = {
        "prod_image": None,
        "product_name": "string",
        "brand": "string",
        "price": "-.4",
        "short_description": "string",
        "category": "string"
    }
    invalid_payload = {
        'name': '',
        'description': 'Test Description',
        'price': 100.0
    }

    response = client.post(url, valid_payload, format="json")
    assert response.status_code == 201

    response = client.post(url, invalid_payload, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_productdetail():
    client = APIClient()
    product = Product.objects.create(
        product_name="string",
        brand="string",
        price="-.4",
        short_description="string",
        category="string"
    )
    url = reverse("product-detail", kwargs={"pk": product.pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_productupdate():
    client = APIClient()
    product = Product.objects.create(
        product_name="string",
        brand="string",
        price="-.4",
        short_description="string",
        category="string"
    )
    url = reverse("product-detail", kwargs={"pk": product.pk})
    valid_payload = {
        "product_name": "string",
        "brand": "string",
        "price": "-.4",
        "short_description": "string",
        "category": "string"
    }
    response = client.put(url, valid_payload, format="json")
    assert response.status_code == 200
  