from django.test import TestCase
from inventory.forms import ItemForm, OrderForm, UpdateStockForm
from inventory.models import Item

class ItemFormTests(TestCase):
    def test_item_form_valid(self):
        """Test that the ItemForm is valid."""
        form_data = {'name': 'Test Item', 'quantity': 10}
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        """Test that the ItemForm is invalid without required fields."""
        form = ItemForm(data={})
        self.assertFalse(form.is_valid())

class OrderFormTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(name="Test Item", quantity=20, description="Test Item Description")

    def test_order_form_valid(self):
        """Test that the OrderForm is valid."""
        form_data = {'item': self.item.id, 'quantity': 5}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid_quantity(self):
        """Test that the OrderForm is invalid when quantity exceeds stock."""
        form_data = {'item': self.item.id, 'quantity': 25}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())

class UpdateStockFormTests(TestCase):
    def test_update_stock_form_valid(self):
        """Test that the UpdateStockForm is valid."""
        item = Item.objects.create(name="Test Item", quantity=10, description="Test Item Description")
        form = UpdateStockForm(data={'quantity': 15}, instance=item)
        self.assertTrue(form.is_valid())

    def test_update_stock_form_invalid(self):
        """Test that the UpdateStockForm is invalid with a negative quantity."""
        item = Item.objects.create(name="Test Item", quantity=10, description="Test Item Description")
        form = UpdateStockForm(data={'quantity': -5}, instance=item)
        self.assertFalse(form.is_valid())
