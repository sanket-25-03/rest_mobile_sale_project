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
        self.authenticate()
        product_data = {'product_name': 'Test Product', 'short_description': 'Test description', 'brand': 'Test Brand', 'price': 99.99}

        # POST request - Creating a product
        response = self.client.post(self.product_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data['id']

        # POST request again with the same product name (should fail due to duplication)
        response = self.client.post(self.product_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product_name', response.data)

        # GET request - Ensure the product was created correctly
        response = self.client.get(f"{self.product_url}{product_id}/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # PUT request
    #     updated_data = {'product_name': 'Updated Product', 'short_description': 'Updated description', 'brand': 'Updated Brand', 'price': 149.99}
    #     response = self.client.put(f"{self.product_url}{product_id}/", updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # DELETE request
    #     response = self.client.delete(f"{self.product_url}{product_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_inventory_api(self):
    #     self.authenticate()
    #     product = Product.objects.create(product_name='Test Product', short_description='Test description', brand='Test Brand', price=99.99)
    #     inventory_data = {'imei_number': '123456789012345', 'detailed_info': 'Test details', 'stock_quantity': 10, 'product': product.id}

    #     # POST request - Creating an inventory
    #     response = self.client.post(self.inventory_url, inventory_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     inventory_id = response.data['id']

    #     # POST request without product (should fail)
    #     inventory_data_missing_product = {'imei_number': '987654321098765', 'detailed_info': 'Updated details', 'stock_quantity': 20}
    #     response = self.client.post(self.inventory_url, inventory_data_missing_product, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('product', response.data)

    #     # GET request
    #     response = self.client.get(f"{self.inventory_url}{inventory_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # PUT request
    #     updated_data = {'imei_number': '987654321098765', 'detailed_info': 'Updated details', 'stock_quantity': 20, 'product': product.id}
    #     response = self.client.put(f"{self.inventory_url}{inventory_id}/", updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # DELETE request
    #     response = self.client.delete(f"{self.inventory_url}{inventory_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_review_api(self):
    #     self.authenticate()
    #     product = Product.objects.create(product_name='Test Product', short_description='Test description', brand='Test Brand', price=99.99)
    #     review_data = {'quality_rating': 5, 'performance_rating': 4, 'user_exp_rating': 5, 'review': 'Great product!', 'product': product.id}

    #     # POST request - Creating a review
    #     response = self.client.post(self.review_url, review_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     review_id = response.data['id']

    #     # POST request without product (should fail)
    #     review_data_missing_product = {'quality_rating': 5, 'performance_rating': 4, 'user_exp_rating': 5, 'review': 'Great product!'}
    #     response = self.client.post(self.review_url, review_data_missing_product, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('product', response.data)

    #     # GET request
    #     response = self.client.get(f"{self.review_url}{review_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # PUT request
    #     updated_data = {'quality_rating': 4, 'performance_rating': 3, 'user_exp_rating': 4, 'review': 'Good product.', 'product': product.id}
    #     response = self.client.put(f"{self.review_url}{review_id}/", updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # DELETE request
    #     response = self.client.delete(f"{self.review_url}{review_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_order_api(self):
    #     self.authenticate()
    #     product = Product.objects.create(product_name='Test Product', short_description='Test description', brand='Test Brand', price=99.99)
    #     user = User.objects.get(username='testuser')
    #     order_data = {'user': user.id, 'order_date': '2025-01-21T10:47:26.176632Z', 'shipping_address': '123 Main St', 'total_price': 150.50, 'status': 'pending', 'payment_method': 'Credit Card', 'payment_status': 'Pending', 'product': product.id}

    #     # POST request - Creating an order
    #     response = self.client.post(self.order_url, order_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     order_id = response.data['id']

    #     # POST request without required fields (should fail)
    #     order_data_missing_product = {'user': user.id, 'order_date': '2025-01-21T10:47:26.176632Z', 'shipping_address': '123 Main St', 'total_price': 150.50, 'status': 'pending', 'payment_method': 'Credit Card', 'payment_status': 'Pending'}
    #     response = self.client.post(self.order_url, order_data_missing_product, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('product', response.data)

    #     # GET request
    #     response = self.client.get(f"{self.order_url}{order_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # PUT request
    #     updated_data = {'user': user.id, 'order_date': '2025-01-22T10:47:26.176632Z', 'shipping_address': '456 Another St', 'total_price': 200.00, 'status': 'shipped', 'payment_method': 'PayPal', 'payment_status': 'Paid', 'product': product.id}
    #     response = self.client.put(f"{self.order_url}{order_id}/", updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # DELETE request
    #     response = self.client.delete(f"{self.order_url}{order_id}/", format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
