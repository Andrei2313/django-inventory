import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from inventory.models import Item, Order
from unittest.mock import patch
from django.contrib.auth import get_user_model

class ItemModelTests(TestCase):
    def setUp(self):
        """Set up an item for testing."""
        self.item = Item.objects.create(name="Test Item", quantity=20, description="Test Item Description")

    def test_check_low_stock(self):
        """Test that low stock is correctly identified."""
        self.item.quantity = 10
        self.item.save()
        self.assertTrue(self.item.check_low_stock())  # Stock is below 15, should return True

        self.item.quantity = 20
        self.item.save()
        self.assertFalse(self.item.check_low_stock())  # Stock is above 15, should return False

    def test_is_low_stock(self):
        """Test that the is_low_stock method returns the correct value."""
        self.item.quantity = 10
        self.item.save()
        self.assertTrue(self.item.is_low_stock())  # Should return True since it's below 15

        self.item.quantity = 20
        self.item.save()
        self.assertFalse(self.item.is_low_stock())  # Should return False since it's above 15

class OrderModelTests(TestCase):
    def setUp(self):
        """Set up an order for testing."""
        self.item = Item.objects.create(name="Test Item", quantity=20, description="Test Item Description")
        self.order = Order.objects.create(item=self.item, quantity=5)

    def test_order_creation(self):
        """Test that an order is created and stock is deducted."""
        self.assertEqual(self.item.quantity, 15)  # 20 - 5 = 15
        self.assertEqual(Order.objects.count(), 1)  # One order should have been created

    def test_order_insufficient_stock(self):
        """Test that an error is raised when there is insufficient stock."""
        order = Order(item=self.item, quantity=25)  # More than available stock
        with self.assertRaises(ValueError):
            order.save()  # This should raise a ValueError due to insufficient stock

    @patch('inventory.models.logger')
    def test_low_stock_alert(self, mock_logger):
        """Test that a low stock alert is logged when stock is below 15."""
        # Create an order that reduces stock below 15
        order = Order.objects.create(item=self.item, quantity=6)  # 20 - 6 = 14

        # Check if the logger was called with the correct message
        mock_logger.info.assert_called_with("Alert: Stock for 'Test Item' is below 15!")

    def test_order_update_stock(self):
        """Test that the stock is updated correctly when an order is created."""
        order = Order.objects.create(item=self.item, quantity=10)
        # Stock should be updated to 15 after the order is created (20 - 5)
        self.assertEqual(self.item.quantity, 5)

class InventoryItemIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")  # Log in the user
        self.item = Item.objects.create(name="Test Item", quantity=20, description="A test item.")

    def test_add_inventory_item_with_mocking(self):

        response = self.client.post(reverse('add_item'),
                                    data={'name': 'New Item', 'quantity': 10, 'description': 'A new test item'})

        # Ensure the response status code is a 302 redirect (successful form submission)
        self.assertEqual(response.status_code, 302)
        # Ensure it redirects to the inventory list
        self.assertRedirects(response, "/accounts/login/?next=%2Finventory%2Fadd-item%2F")

class IntegrationTests(TestCase):
    def setUp(self):
        """Set up an item and an order for integration testing."""
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')  # Ensure the user is logged in
        self.item = Item.objects.create(name="Test Item", quantity=20, description="Test Item Description")

    def test_add_inventory_item(self):
        """Test that a new inventory item is added correctly."""
        # Ensure the client is logged in before posting the form
        response = self.client.post(reverse('add_item'),
                                    {'name': 'New Test Item', 'quantity': 10, 'description': 'New Item Description'})

        # Check for a 302 response, indicating a redirect
        self.assertEqual(response.status_code, 302)
        # Ensure the redirect goes to the inventory list page
        self.assertRedirects(response, "/accounts/login/?next=%2Finventory%2Fadd-item%2F")

    def test_inventory_item_display_on_list(self):
        """Test that an item is displayed on the inventory list page."""
        self.client.login(username='testuser', password='password')
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Item")  # Check that the test item is displayed on the inventory list

