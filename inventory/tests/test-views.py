from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item, Order
from .forms import ItemForm, OrderForm, UpdateStockForm

class ViewTests(TestCase):

    def setUp(self):
        """Create users, items, and orders for testing"""
        # Create a normal user and an admin user
        self.user = User.objects.create_user(username='user', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='password')

        # Create an item and an order
        self.item = Item.objects.create(name='Test Item', quantity=100)
        self.order = Order.objects.create(item=self.item, quantity=5)

    def test_inventory_list_url(self):
        """Test that the inventory list page is accessible"""
        url = reverse('inventory_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_item_url_for_admin(self):
        """Test that only admins can access the add item page"""
        url = reverse('add_item')
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_item_url_for_non_admin(self):
        """Test that non-admins cannot access the add item page"""
        url = reverse('add_item')
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_create_order_url(self):
        """Test that users can access the create order page"""
        url = reverse('create_order')
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_stock_url_for_admin(self):
        """Test that only admins can update stock"""
        url = reverse('update_stock', kwargs={'pk': self.item.pk})
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_stock_url_for_non_admin(self):
        """Test that non-admins cannot access the update stock page"""
        url = reverse('update_stock', kwargs={'pk': self.item.pk})
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_order_log_url_for_admin(self):
        """Test that only admins can access the order log"""
        url = reverse('order_log')
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_log_url_for_non_admin(self):
        """Test that non-admins cannot access the order log page"""
        url = reverse('order_log')
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

class FormTests(TestCase):

    def setUp(self):
        """Create a user and an item for form testing"""
        self.user = User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        self.item = Item.objects.create(name='Test Item', quantity=10)

    def test_item_form_valid(self):
        """Test the ItemForm with valid data"""
        data = {'name': 'New Item', 'quantity': 20}
        form = ItemForm(data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        """Test the ItemForm with invalid data"""
        data = {'name': '', 'quantity': 20}  # Missing name
        form = ItemForm(data)
        self.assertFalse(form.is_valid())

    def test_order_form_valid(self):
        """Test the OrderForm with valid data"""
        data = {'item': self.item.pk, 'quantity': 5}
        form = OrderForm(data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        """Test the OrderForm with invalid data (exceeds stock)"""
        data = {'item': self.item.pk, 'quantity': 15}  # Exceeds stock
        form = OrderForm(data)
        self.assertFalse(form.is_valid())

    def test_update_stock_form_valid(self):
        """Test the UpdateStockForm with valid data"""
        data = {'quantity': 15}
        form = UpdateStockForm(data, instance=self.item)
        self.assertTrue(form.is_valid())

        # Save and check that the quantity is updated
        form.save()
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 15)

    def test_update_stock_form_invalid(self):
        """Test the UpdateStockForm with invalid data"""
        data = {'quantity': -5}  # Invalid negative quantity
        form = UpdateStockForm(data, instance=self.item)
        self.assertFalse(form.is_valid())
