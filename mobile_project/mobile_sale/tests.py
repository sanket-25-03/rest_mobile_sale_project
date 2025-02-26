# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from django.contrib.auth.models import User
# from .models import Product

# class ProductCreateAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('product-create')
#         self.valid_payload = {
#             "prod_image": None,
#             "product_name": "string",
#             "brand": "string",
#             "price": "-.4",
#             "short_description": "string",
#             "category": "string"
#         }
#         self.invalid_payload = {
#             'name': '',
#             'description': 'Test Description',
#             'price': 100.0
#         }

#     def test_create_valid_product(self):
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_product(self):
#         response = self.client.post(self.url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class ReviewCreateAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.product = Product.objects.create(product_name="string", brand="string", price="-24022760.60", short_description="string", category="string")        
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('review-create')
#         self.valid_payload = {
#             "quality_rating": 1,
#             "performance_rating": 1,
#             "user_exp_rating": 1,
#             "review": "string",
#             "product": self.product.id,
#             "user": self.user.id
#         }
#         self.invalid_payload = {
#             'product': self.product.id,
#             'rating': 6,
#             'comment': 'Great product!'
#         }

#     def test_create_valid_review(self):
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_review(self):
#         response = self.client.post(self.url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class InventoryCreateAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.product = Product.objects.create(product_name="string", brand="string", price="-24022760.60", short_description="string", category="string")        
#         self.url = reverse('inventory-create')
#         self.valid_payload = {
#             "imei_number": "string",
#             "detailed_info": "string",
#             "stock_quantity": 2147483647,
#             "os": "string",
#             "ram": "string",
#             "storage": "string",
#             "battery_capacity": "string",
#             "screen_size": "string",
#             "camera_details": "string",
#             "processor": "string",
#             "product": self.product.id
# }
#         self.invalid_payload = {
#             'product': self.product.id,
#             'processor': 'string'
#         }

#     def test_create_valid_inventory(self):
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_inventory(self):
#         response = self.client.post(self.url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class OrderCreateAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.product = Product.objects.create(product_name="string", brand="string", price="-24022760.60", short_description="string", category="string")         
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('order-create')
#         self.valid_payload = {
#             "shipping_address": "string",
#             "total_price": "-29832899",
#             "status": "pending",
#             "payment_method": "string",
#             "payment_status": "string",
#             "user": self.user.id,
#         }
#         self.invalid_payload = {
#             'product': self.product.id,
#             'quantity': 0
#         }

#     def test_create_valid_order(self):
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_invalid_order(self):
#         response = self.client.post(self.url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class RegisterAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('RegisterAPI')
#         self.valid_payload = {
#             'username': 'newuser',
#             'password': 'newpassword',
#             'email': 'newuser@example.com'
#         }
#         self.invalid_payload = {
#             'username': '',
#             'password': 'newpassword',
#             'email': 'invalid@example.com'
#         }

#     def test_register_valid_user(self):
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_register_invalid_user(self):
#         response = self.client.post(self.url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
# class LoginAPITest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.url = reverse('LoginAPI')
#         self.valid_payload = {
#             'username': 'testuser',
#             'password': 'testpassword'
#         }
#         self.invalid_payload = {
#             'username': 'testuser',
#             'password': 'wrongpassword'
#         }

#     def test_login_valid_user(self):
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_login_invalid_user(self):
#         response = self.client.post(self.url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
