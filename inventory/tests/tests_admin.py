from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from inventory.models import Item, Order

class AdminTests(TestCase):
    def setUp(self):
        """Set up an admin user for testing."""
        self.user = get_user_model().objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.client.login(username='admin', password='password')  # Ensure we're logged in as admin
        self.item = Item.objects.create(name="Test Item", quantity=20, description="Test Item Description")
        self.order = Order.objects.create(item=self.item, quantity=5)

    def test_item_admin(self):
        """Test that the Item model appears in the admin interface."""
        response = self.client.get(reverse('admin:inventory_item_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')

    def test_order_admin(self):
        """Test that the Order model appears in the admin interface."""
        response = self.client.get(reverse('admin:inventory_order_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order of 5 Test Item(s)')
