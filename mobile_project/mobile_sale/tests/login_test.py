import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
@pytest.fixture
def create_test_user():
    return User.objects.create_user(username="sanket", password="userpassword")

@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, expected_status",
    [
        ("sanket", "userpassword", 200),
        ("", "password123", 400), 
        ("validuser", "", 400),
        ("invaliduser", "password123", 401),
        ("sanket", "wrongpassword", 401),
    ]
)
def test_login(create_test_user, username, password, expected_status):
    client = APIClient()
    url = reverse("LoginAPI")
    
    response = client.post(url, {"username": username, "password": password}, format="json")
    
    assert response.status_code == expected_status
