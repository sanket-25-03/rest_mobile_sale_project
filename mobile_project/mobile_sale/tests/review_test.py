import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from mobile_sale.models import Reviews, Product
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    return User.objects.create_user(username="testuser", password="testpassword")

@pytest.fixture
def create_product(db):
    return Product.objects.create(
        product_name="Test Product",
        brand="Test Brand",
        price="10.0",
        short_description="Test Description",
        category="Test Category"
    )

@pytest.fixture
def create_review(db, create_user, create_product):
    return Reviews.objects.create(
        quality_rating=5,
        performance_rating=4,
        user_exp_rating=5,
        review="Great product!",
        product=create_product,
        user=create_user
    )

@pytest.mark.django_db
def test_create_review(api_client, create_user, create_product):
    api_client.force_authenticate(user=create_user)
    url = reverse("review-create")  
    valid_payload = {
        "quality_rating": 5,
        "performance_rating": 4,
        "user_exp_rating": 5,
        "review": "Amazing product!",
        "product": create_product.id
    }
    invalid_payload = {
        "review": "",
        "quality_rating": "",
        "performance_rating": 3,
        "user_exp_rating": 4,
        "product": create_product.id
    }
    response = api_client.post(url, valid_payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Reviews.objects.count() == 1
    
    response = api_client.post(url, invalid_payload, format="json")


@pytest.mark.django_db
def test_get_single_review(api_client, create_review):
    url = reverse("review-detail", kwargs={"pk": create_review.id})  # Adjust URL pattern name
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["review"] == "Great product!"

@pytest.mark.django_db
def test_update_review(api_client, create_review, create_user):
    api_client.force_authenticate(user=create_user)
    url = reverse("review-detail", kwargs={"pk": create_review.id})
    valid_payload = {"review": "Updated review content"}
    response = api_client.put(url, valid_payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    create_review.refresh_from_db()
    assert create_review.review == "Updated review content"

@pytest.mark.django_db
def test_delete_review(api_client, create_review, create_user):
    api_client.force_authenticate(user=create_user)
    url = reverse("review-detail", kwargs={"pk": create_review.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert Reviews.objects.count() == 0