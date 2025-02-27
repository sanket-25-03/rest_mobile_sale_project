# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from mobile_sale.models import Inventory

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def create_inventory(db):
#     return Inventory.objects.create(
#         item_name="Test Item",
#         quantity=10,
#         price=100.50,
#         description="Test Description"
#     )

# @pytest.mark.django_db
# def test_create_inventory(api_client):
#     url = reverse("inventory-create")
#     valid_payload = {
#         "item_name": "New Item",
#         "quantity": 5,
#         "price": 50.75,
#         "description": "New Description"
#     }
#     invalid_payload = {
#         "item_name": "",
#         "quantity": "",
#         "price": -10,
#         "description": ""
#     }
    
#     response = api_client.post(url, valid_payload, format="json")
#     assert response.status_code == status.HTTP_201_CREATED
#     assert Inventory.objects.count() == 1
    
#     response = api_client.post(url, invalid_payload, format="json")
#     assert response.status_code == status.HTTP_400_BAD_REQUEST

# @pytest.mark.django_db
# def test_get_inventory_list(api_client, create_inventory):
#     url = reverse("inventory-list")  # Ensure this matches your URL pattern name
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert "results" in response.data
#     assert len(response.data["results"]) > 0

# @pytest.mark.django_db
# def test_get_single_inventory(api_client, create_inventory):
#     url = reverse("inventory-detail", kwargs={"pk": create_inventory.id})
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["item_name"] == "Test Item"

# @pytest.mark.django_db
# def test_update_inventory(api_client, create_inventory):
#     url = reverse("inventory-detail", kwargs={"pk": create_inventory.id})
#     valid_payload = {"item_name": "Updated Item", "quantity": 20}
#     response = api_client.put(url, valid_payload, format="json")
#     assert response.status_code == status.HTTP_200_OK
#     create_inventory.refresh_from_db()
#     assert create_inventory.item_name == "Updated Item"
#     assert create_inventory.quantity == 20

# @pytest.mark.django_db
# def test_delete_inventory(api_client, create_inventory):
#     url = reverse("inventory-detail", kwargs={"pk": create_inventory.id})
#     response = api_client.delete(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert Inventory.objects.count() == 0