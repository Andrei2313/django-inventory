# your_app/tests/test_models.py
from django.test import TestCase
from inventory.models import InventoryItem, Notification
from django.utils import timezone


class InventoryItemTests(TestCase):

    def test_inventory_item_creation(self):
        # Create an InventoryItem instance
        item = InventoryItem.objects.create(name="Sample Item", quantity=10, description="A test item")

        # Test if the InventoryItem is correctly saved
        self.assertEqual(item.name, "Sample Item")
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.description, "A test item")
        self.assertTrue(isinstance(item.last_updated, timezone.datetime))

    def test_inventory_item_str(self):
        # Ensure string representation of InventoryItem is correct
        item = InventoryItem.objects.create(name="Sample Item", quantity=10)
        self.assertEqual(str(item), "Sample Item")


class NotificationTests(TestCase):

    def test_notification_creation(self):
        # Create an InventoryItem
        item = InventoryItem.objects.create(name="Sample Item", quantity=10, description="A test item")

        # Create a Notification related to the InventoryItem
        notification = Notification.objects.create(item=item, message="Item quantity is low")

        # Test if the Notification is correctly saved
        self.assertEqual(notification.item, item)
        self.assertEqual(notification.message, "Item quantity is low")
        self.assertTrue(isinstance(notification.created_at, timezone.datetime))

    def test_notification_related_inventory_item(self):
        # Create an InventoryItem
        item = InventoryItem.objects.create(name="Sample Item", quantity=10)

        # Create a Notification
        notification = Notification.objects.create(item=item, message="New Notification")

        # Test if Notification is correctly related to InventoryItem
        self.assertEqual(notification.item.name, "Sample Item")
        self.assertEqual(notification.item.quantity, 10)
