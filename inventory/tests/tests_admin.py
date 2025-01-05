# your_app/tests/test_admin.py
from django.test import TestCase
from django.contrib.admin.sites import site
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import InventoryItem, Notification


class AdminTests(TestCase):

    def setUp(self):
        # Create a user for admin access
        self.admin_user = User.objects.create_superuser(username='admin', password='password',
                                                        email='admin@example.com')

        # Create InventoryItem and Notification instances for testing
        self.item = InventoryItem.objects.create(name="Test Item", quantity=10, description="Test description")
        self.notification = Notification.objects.create(item=self.item, message="Test notification")

    def test_inventory_item_model_registration(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Test if InventoryItem is registered in the admin site
        response = self.client.get(reverse('admin:inventory_inventoryitem_changelist'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the InventoryItem appears in the list page
        self.assertContains(response, "Test Item")

    def test_notification_model_registration(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Test if Notification is registered in the admin site
        response = self.client.get(reverse('admin:inventory_notification_changelist'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the Notification appears in the list page
        self.assertContains(response, "Test notification")

    def test_inventory_item_addition_in_admin(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Test if the admin can add an InventoryItem
        response = self.client.get(reverse('admin:inventory_inventoryitem_add'))
        self.assertEqual(response.status_code, 200)

        # Post data to add a new InventoryItem
        form_data = {
            'name': 'New Item',
            'quantity': 15,
            'description': 'New item added via admin',
        }
        response = self.client.post(reverse('admin:inventory_inventoryitem_add'), data=form_data)

        # Check if the new item was successfully added
        self.assertRedirects(response, reverse('admin:inventory_inventoryitem_changelist'))
        self.assertTrue(InventoryItem.objects.filter(name='New Item').exists())

    def test_notification_addition_in_admin(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Test if the admin can add a Notification
        response = self.client.get(reverse('admin:inventory_notification_add'))
        self.assertEqual(response.status_code, 200)

        # Post data to add a new Notification
        form_data = {
            'item': self.item.id,
            'message': 'New notification from admin',
        }
        response = self.client.post(reverse('admin:inventory_notification_add'), data=form_data)

        # Check if the new notification was successfully added
        self.assertRedirects(response, reverse('admin:inventory_notification_changelist'))
        self.assertTrue(Notification.objects.filter(message='New notification from admin').exists())
