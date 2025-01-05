# your_app/tests/test_forms.py
from django.test import TestCase
from inventory.forms import InventoryItemForm
from inventory.models import InventoryItem


class InventoryItemFormTests(TestCase):

    def test_form_valid_data(self):
        # Test if the form works with valid data
        form_data = {
            'name': 'Test Item',
            'quantity': 10,
            'description': 'A test item for inventory',
        }
        form = InventoryItemForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Save the form and check if the object is created in the database
        form.save()
        self.assertTrue(InventoryItem.objects.filter(name='Test Item').exists())

    def test_form_invalid_data(self):
        # Test if the form does not work with invalid data
        form_data = {
            'name': '',  # Name is empty, so this should be invalid
            'quantity': 10,
            'description': 'A test item without name',
        }
        form = InventoryItemForm(data=form_data)

        # Check if the form is invalid
        self.assertFalse(form.is_valid())

        # Check if the form contains the appropriate error for the 'name' field
        self.assertIn('This field is required.', form.errors['name'])

    def test_form_missing_quantity(self):
        # Test if the form does not work if a required field like quantity is missing
        form_data = {
            'name': 'Test Item Without Quantity',
            'quantity': '',  # Missing quantity
            'description': 'A test item without quantity',
        }
        form = InventoryItemForm(data=form_data)

        # Check if the form is invalid
        self.assertFalse(form.is_valid())

        # Check if the form contains the appropriate error for the 'quantity' field
        self.assertIn('This field is required.', form.errors['quantity'])

    def test_form_optional_description(self):
        # Test if the form works with a missing optional field (description)
        form_data = {
            'name': 'Test Item Without Description',
            'quantity': 10,  # Valid quantity
            'description': '',  # Optional field
        }
        form = InventoryItemForm(data=form_data)

        # Check if the form is valid despite the missing description
        self.assertTrue(form.is_valid())

        # Ensure that the object is created with an empty description
        form.save()
        item = InventoryItem.objects.get(name='Test Item Without Description')
        self.assertEqual(item.description, '')
