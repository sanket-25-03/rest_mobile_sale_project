from django.test import TestCase
from .models import *
from faker import Faker
fake = Faker()
from django.test import TestCase, Client
from django.contrib.auth.models import User
import json

class FirstTestCase(TestCase):
    
    def setUp(self):
        print('setup called')

    def test_equal(self):
        self.assertEqual(1,1)


class RegisterViewTest(TestCase):
    def setUp(self):
        # Initialize the client
        self.client = Client()
        self.register_url = '/register/'  # Update with the actual endpoint if necessary

    def test_register_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'User created successfully.')
        print("test_register_success passed.")

    def test_missing_fields(self):
        data = {
            'username': '',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'All fields are required.')
        print("test_missing_fields passed.")

    def test_duplicate_username(self):
        User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        data = {
            'username': 'testuser',
            'password': 'newpassword',
            'email': 'newemail@example.com'
        }
        response = self.client.post(self.register_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Username already exists.')
        print("test_duplicate_username passed.")

    def test_duplicate_email(self):
        User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.register_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Email already exists.')
        print("test_duplicate_email passed.")

    def test_invalid_http_method(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json().get('error'), 'Invalid HTTP method.')
        print("test_invalid_http_method passed.")
