# inventory/tests/test_admin.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from inventory.models import Item, Order


class AdminTests(TestCase):

    def setUp(self):
        """Create a superuser and items for testing the admin interface"""
        self.user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.client.login(username='admin', password='password')

        self.item = Item.objects.create(name='Test Item', quantity=100)
        self.order = Order.objects.create(item=self.item, quantity=5)

    def test_item_admin(self):
        """Test that the Item model appears in the admin interface and lists correctly"""
        url = reverse('admin:inventory_item_changelist')  # Admin URL for Item model
        response = self.client.get(url)

        # Check if the item appears in the list view
        self.assertContains(response, self.item.name)
        self.assertContains(response, self.item.quantity)

    def test_order_admin(self):
        """Test that the Order model appears in the admin interface and lists correctly"""
        url = reverse('admin:inventory_order_changelist')  # Admin URL for Order model
        response = self.client.get(url)

        # Check if the order appears in the list view
        self.assertContains(response, str(self.order))
        self.assertContains(response, self.order.quantity)

    def test_order_inline_in_item_admin(self):
        """Test that orders appear as inline models in the Item admin"""
        url = reverse('admin:inventory_item_change', args=[self.item.pk])  # Admin URL for editing an item
        response = self.client.get(url)

        # Check if the order inline form is displayed
        self.assertContains(response, 'Orders')  # Inline for orders should appear
        self.assertContains(response, str(self.order))  # Check if the order is listed in the inline form
