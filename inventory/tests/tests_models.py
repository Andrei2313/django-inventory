from django.test import TestCase
from django.db import IntegrityError
from inventory.models import Item, Order

class ItemModelTests(TestCase):

    def test_is_low_stock(self):
        """Test that the is_low_stock method works as expected"""
        # Create an item with quantity 10
        item = Item.objects.create(name='Test Item', quantity=10)

        # Assert that it is low stock
        self.assertTrue(item.is_low_stock())

        # Create an item with quantity 20
        item2 = Item.objects.create(name='Another Item', quantity=20)

        # Assert that it is not low stock
        self.assertFalse(item2.is_low_stock())


class OrderModelTests(TestCase):

    def setUp(self):
        """Create an item to use in tests"""
        self.item = Item.objects.create(name='Test Item', quantity=20)

    def test_create_order_success(self):
        """Test that an order is created successfully and stock is deducted"""
        # Create an order
        order = Order.objects.create(item=self.item, quantity=5)

        # Assert the order is saved correctly
        self.assertEqual(order.item.quantity, 15)  # Stock should be deducted by 5
        self.assertEqual(order.quantity, 5)

    def test_create_order_insufficient_stock(self):
        """Test that creating an order with insufficient stock raises an error"""
        # Create an order that exceeds stock
        order = Order(item=self.item, quantity=25)

        # Assert that the error is raised
        with self.assertRaises(ValueError):
            order.save()

    def test_low_stock_alert(self):
        """Test that low stock alert is triggered when stock falls below 15"""
        # Patch the print function to check if the alert is printed
        with self.assertLogs('django', level='INFO') as log:
            # Create an order that makes the stock go below 15
            order = Order.objects.create(item=self.item, quantity=10)

            # Check if the alert was printed
            self.assertIn("Alert: Stock for 'Test Item' is below 15!", log.output)
