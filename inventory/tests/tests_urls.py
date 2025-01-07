from django.test import SimpleTestCase
from django.urls import reverse, resolve
from inventory.views import inventory_list, add_item, create_order, order_log, update_stock

class URLTests(SimpleTestCase):

    def test_inventory_list_url(self):
        """Test that the inventory list URL resolves to the correct view"""
        url = reverse('inventory_list')
        self.assertEqual(resolve(url).func, inventory_list)

    def test_add_item_url(self):
        """Test that the add item URL resolves to the correct view"""
        url = reverse('add_item')
        self.assertEqual(resolve(url).func, add_item)

    def test_create_order_url(self):
        """Test that the create order URL resolves to the correct view"""
        url = reverse('create_order')
        self.assertEqual(resolve(url).func, create_order)

    def test_order_log_url(self):
        """Test that the order log URL resolves to the correct view"""
        url = reverse('order_log')
        self.assertEqual(resolve(url).func, order_log)

    def test_update_stock_url(self):
        """Test that the update stock URL resolves to the correct view"""
        url = reverse('update_stock', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, update_stock)
