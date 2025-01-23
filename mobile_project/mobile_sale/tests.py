from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from mobile_sale.models import Product


class APITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('RegisterAPI')
        self.login_url = reverse('LoginAPI')
        self.product_url = reverse('ProductView')
        self.inventory_url = reverse('InventoryView')
        self.review_url = reverse('ReviewView')
        self.order_url = reverse('OrderView')

    def authenticate(self):
        self.test_create_user()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_user(self):
        data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.token = response.data['token']

    def test_product_api(self):
        product_data = {'product_name': 'Test Product', 'short_description': 'Test description', 'brand': 'Test Brand', 'price': 99.99}

        response = self.client.post(self.product_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data['id']

        response = self.client.post(self.product_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product_name', response.data)

        response = self.client.get(f"{self.product_url}?id={product_id}", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_data = {'id':product_id, 'product_name': 'Updated Product', 'short_description': 'Updated description', 'brand': 'Updated Brand', 'price': 149.99}
        response = self.client.put(f"{self.product_url}?id={product_id}", updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'id':product_id}
        response = self.client.delete(f"{self.product_url}?id={product_id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class InventoryAPITest(APITestCase):
    def setUp(self):
        self.api_test = APITest()
        self.api_test.setUp()
        self.api_test.authenticate()
        self.client = self.api_test.client
        self.product_url = self.api_test.product_url
        self.inventory_url = self.api_test.inventory_url

    def test_create_inventory(self):
        product = Product.objects.create(product_name='Test Product', short_description='Test description', brand='Test Brand', price=99.99)
        response = self.client.get(f"{self.product_url}", format='json')
        product_id = response.data[0]['id']
        inventory_data = {
            "imei_number": "0123456781234",
            "detailed_info": "Entry-level phone with basic features.",
            "stock_quantity": 25,
            "os": "Android 10",
            "ram": "2GB",
            "storage": "16GB",
            "battery_capacity": "3000mAh",
            "screen_size": "5.5 inches",
            "camera_details": "8MP single camera",
            "processor": "MediaTek MT6739",
            "product": product_id
        }
        response = self.client.post(self.inventory_url, inventory_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        inventory_id = response.data['id']

    def test_create_inventory_without_product(self):
        inventory_data = {
            "imei_number": "987654321098765",
            "detailed_info": "Updated details",
            "stock_quantity": 20
        }
        response = self.client.post(self.inventory_url, inventory_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product', response.data)