import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from mobile_sale.models import Product, Inventory

@pytest.mark.django_db
@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
@pytest.fixture
def create_product():
    return Product.objects.create(
        product_name="Test Phone",
        brand="Test Brand",
        price=50000.00,
        short_description="A test smartphone",
        category="Mobile"
    )

@pytest.mark.django_db
@pytest.fixture
def create_inventory(create_product):
    return Inventory.objects.create(
        product=create_product,
        imei_number="123456789012345",
        detailed_info="Test inventory item",
        stock_quantity=10,
        os="Android",
        ram="8GB",
        storage="128GB",
        battery_capacity="5000mAh",
        screen_size="6.5 inches",
        camera_details="64MP + 12MP",
        processor="Snapdragon 888"
    )

@pytest.mark.django_db
def test_create_inventory(client):
    url = reverse("inventory-create")

    product = Product.objects.create(
        product_name="New Phone",
        brand="New Brand",
        price=45000.00,
        short_description="A new smartphone",
        category="Mobile"
    )

    data = {
        "product": product.id,
        "imei_number": "987654321098765",
        "detailed_info": "New inventory item",
        "stock_quantity": 5,
        "os": "iOS",
        "ram": "6GB",
        "storage": "256GB",
        "battery_capacity": "4000mAh",
        "screen_size": "6.1 inches",
        "camera_details": "48MP + 12MP",
        "processor": "A15 Bionic"
    }

    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["imei_number"] == "987654321098765"

@pytest.mark.django_db
def test_get_inventory_list(client, create_inventory):
    url = reverse("inventory-create") 

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_get_single_inventory(client, create_inventory):
    url = reverse("inventory-detail", kwargs={"pk": create_inventory.id})

    response = client.get(url)
    assert response.status_code == 200
    assert response.data["imei_number"] == create_inventory.imei_number

@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_data, expected_status",
    [
        ({"stock_quantity": 20}, 200),  
        ({"imei_number": ""}, 400),  
        ({"imei_number": "invalid-imei"}, 400),  
    ]
)
def test_update_inventory(client, create_inventory, update_data, expected_status):
    url = reverse("inventory-detail", kwargs={"pk": create_inventory.id})

    response = client.put(url, update_data, format="json")
    print("Response Data:", response.data)  

    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}. Response: {response.data}"

@pytest.mark.django_db
def test_delete_inventory(client, create_inventory):
    url = reverse("inventory-detail", kwargs={"pk": create_inventory.id})

    response = client.delete(url)
    assert response.status_code == 200
    assert not Inventory.objects.filter(id=create_inventory.id).exists()
