from django.test import TestCase
from inventory.models import Item, Order
from inventory.forms import ItemForm, OrderForm, UpdateStockForm


class ItemFormTests(TestCase):

    def test_item_form_valid(self):
        """Test that the ItemForm is valid when given valid data"""
        data = {
            'name': 'Test Item',
            'quantity': 10
        }
        form = ItemForm(data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        """Test that the ItemForm is invalid when missing required fields"""
        data = {
            'name': '',  # Empty name is invalid
            'quantity': 10
        }
        form = ItemForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class OrderFormTests(TestCase):

    def setUp(self):
        """Create an item for the order form tests"""
        self.item = Item.objects.create(name='Test Item', quantity=10)

    def test_order_form_valid(self):
        """Test that the OrderForm is valid when given valid data"""
        data = {
            'item': self.item.pk,
            'quantity': 5
        }
        form = OrderForm(data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid_quantity(self):
        """Test that the OrderForm is invalid when quantity exceeds stock"""
        data = {
            'item': self.item.pk,
            'quantity': 15  # Exceeds available stock
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_order_form_invalid_item(self):
        """Test that the OrderForm is invalid when item is not provided"""
        data = {
            'item': None,  # No item provided
            'quantity': 5
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('item', form.errors)


class UpdateStockFormTests(TestCase):

    def setUp(self):
        """Create an item to use for the UpdateStockForm tests"""
        self.item = Item.objects.create(name='Test Item', quantity=10)

    def test_update_stock_form_valid(self):
        """Test that the UpdateStockForm is valid when given a valid quantity"""
        data = {
            'quantity': 15  # Valid quantity update
        }
        form = UpdateStockForm(data, instance=self.item)
        self.assertTrue(form.is_valid())

        # Test that the quantity is updated correctly
        form.save()
        self.item.refresh_from_db()  # Refresh from the database
        self.assertEqual(self.item.quantity, 15)

    def test_update_stock_form_invalid(self):
        """Test that the UpdateStockForm is invalid with a negative quantity"""
        data = {
            'quantity': -5  # Invalid negative quantity
        }
        form = UpdateStockForm(data, instance=self.item)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)
