from django.test import TestCase
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.test import Client

# client = Client()

# response = client.get('/')

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        client = Client()
        response = client.get('/')
        response.status_code
        self.assertEqual(response.status_code, 200)
