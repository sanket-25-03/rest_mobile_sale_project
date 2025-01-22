from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Product, Inventory, Reviews, Order

class APITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('RegisterAPI')
        self.login_url = reverse('LoginAPI')
        self.product_url = reverse('ProductView')
        self.inventory_url = reverse('InventoryView')
        self.review_url = reverse('ReviewView')
        self.order_url = reverse('OrderView')

    def test_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.token = response.data['token']

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_product(self):
        self.test_create_user()
        self.authenticate()
        data = {
            'product_name': 'Test Product',
            'short_description': 'This is a test product.',
            'brand': 'Test Brand',
            'price': 99.99
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.first()
        self.assertIsNotNone(product, "Product creation failed")

    def test_add_inventory(self):
        self.test_create_product()
        product = Product.objects.first()
        self.assertIsNotNone(product, "Product should not be None")
        data = {
            'imei_number': '123456789012345',
            'detailed_info': 'Test inventory details.',
            'stock_quantity': 10,
            'os': 'Android 11',
            'ram': '4GB',
            'storage': '64GB',
            'battery_capacity': '4000mAh',
            'screen_size': '6.0 inches',
            'camera_details': '12MP dual camera',
            'processor': 'Snapdragon 720G',
            'product': product.id
        }
        response = self.client.post(self.inventory_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_review(self):
        self.test_create_product()
        product = Product.objects.first()
        self.assertIsNotNone(product, "Product should not be None")
        data = {
            'quality_rating': 5,
            'performance_rating': 4,
            'user_exp_rating': 5,
            'review': 'Great product!',
            'product': product.id
        }
        response = self.client.post(self.review_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_order(self):
        self.test_create_product()
        self.authenticate()
        product = Product.objects.first()
        self.assertIsNotNone(product, "Product should not be None")
        user = User.objects.first()
        self.assertIsNotNone(user, "User should not be None")
        data = {
            'user': user.id,
            'order_date': '2025-01-21T10:47:26.176632Z',
            'shipping_address': '123 Main Street, Cityville, State, 12345',
            'total_price': '150.50',
            'status': 'pending',
            'payment_method': 'Credit Card',
            'payment_status': 'Pending',
            'product': product.id
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_orders(self):
        self.test_add_order()
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_input_validation(self):
        self.test_create_user()
        self.authenticate()
        data = {
            'product_name': '',
            'short_description': '',
            'brand': '',
            'price': ''
        }
        response = self.client.post(self.product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
