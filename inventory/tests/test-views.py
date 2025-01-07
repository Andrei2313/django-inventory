from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import Item, Order
from inventory.forms import ItemForm, OrderForm, UpdateStockForm

class InventoryViewTests(TestCase):
    def setUp(self):
        """Set up an admin and a regular user for testing."""
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='userpassword')
        self.client.login(username='admin', password='adminpassword')  # Log in as admin
        self.item = Item.objects.create(name="Test Item", quantity=20, description="Test Item Description")

    def test_inventory_list_view(self):
        """Test that inventory items are listed correctly and low stock items are displayed."""
        response = self.client.get(reverse('inventory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Item")
        self.assertNotContains(response, "Warning! The following items are low in stock:")

        # Test low stock by reducing quantity
        self.item.quantity = 10
        self.item.save()
        response = self.client.get(reverse('inventory_list'))
        self.assertContains(response, "Warning! The following items are low in stock:")
        self.assertContains(response, "Test Item (10 left)")

    def test_add_item_view_admin(self):
        """Test that an admin can add a new inventory item."""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('add_item'), {'name': 'New Test Item', 'quantity': 15, 'description': 'New Item Description'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inventory_list'))
        new_item = Item.objects.get(name='New Test Item')
        self.assertEqual(new_item.quantity, 15)

    def test_add_item_view_regular_user(self):
        """Test that a regular user cannot add an inventory item."""
        self.client.login(username='regularuser', password='userpassword')
        response = self.client.get(reverse('add_item'))
        self.assertEqual(response.status_code, 403)

    def test_create_order_view(self):
        """Test creating an order and updating stock."""
        self.client.login(username='regularuser', password='userpassword')
        response = self.client.post(reverse('create_order'), {'item': self.item.id, 'quantity': 5})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inventory_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 15)

    def test_create_order_insufficient_stock(self):
        """Test that an error is raised when there is insufficient stock."""
        self.client.login(username='regularuser', password='userpassword')
        response = self.client.post(reverse('create_order'), {'item': self.item.id, 'quantity': 25})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'quantity', 'Quantity exceeds stock.')

    def test_update_stock_view_admin(self):
        """Test that an admin can update the stock of an item."""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('update_stock', args=[self.item.id]), {'quantity': 30})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inventory_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 30)

    def test_update_stock_view_regular_user(self):
        """Test that a regular user cannot update the stock of an item."""
        self.client.login(username='regularuser', password='userpassword')
        response = self.client.get(reverse('update_stock', args=[self.item.id]))
        self.assertEqual(response.status_code, 403)

    def test_order_log_view_admin(self):
        """Test that an admin can view the order log."""
        self.client.login(username='admin', password='adminpassword')
        order = Order.objects.create(item=self.item, quantity=5)
        response = self.client.get(reverse('order_log'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order of 5 Test Item(s)")

    def test_order_log_view_regular_user(self):
        """Test that a regular user cannot view the order log."""
        self.client.login(username='regularuser', password='userpassword')
        response = self.client.get(reverse('order_log'))
        self.assertEqual(response.status_code, 403)
