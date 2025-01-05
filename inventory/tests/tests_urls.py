# your_app/tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse


from django.test import TestCase

class TestUrls(TestCase):  # Change SimpleTestCase to TestCase
    def test_inventory_list_url(self):
        url = reverse('inventory_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_inventory_item_url(self):
        url = reverse('add_inventory_item')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


