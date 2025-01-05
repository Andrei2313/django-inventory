# your_app/tests/test_integration.py
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from inventory.models import InventoryItem


class InventoryItemIntegrationTests(TestCase):

    @patch('inventory.forms.InventoryItemForm.save')
    def test_add_inventory_item_with_mocking(self, mock_save):
        """
        Test that a valid form submission creates a new inventory item and redirects to the inventory list.
        Mock the save method to isolate the test.
        """
        # Define valid form data
        form_data = {
            'name': 'Integrated Test Item with Mocking',
            'quantity': 25,
            'description': 'This item is tested through integration and mocking.',
        }

        # Mock the save method to simulate saving the InventoryItem without hitting the database
        mock_save.return_value = InventoryItem(
            name='Integrated Test Item with Mocking',
            quantity=25,
            description='This item is tested through integration and mocking.'
        )

        # Send a POST request to add the inventory item
        response = self.client.post(reverse('add_inventory_item'), data=form_data)

        # Check that the response is a redirect (302), indicating that the form was saved and the user is redirected
        self.assertEqual(response.status_code, 302)

        # Check that the mocked save method was called exactly once
        mock_save.assert_called_once()

        # Verify that the redirect is to the inventory list page
        self.assertRedirects(response, reverse('inventory_list'))

    @patch('inventory.views.InventoryItem.objects.all')
    def test_inventory_item_display_on_list_with_mocking(self, mock_all):
        """
        Test that an item added via POST is displayed on the inventory list page.
        Mock the database query to isolate the view logic.
        """
        # Mock the `all()` method to return a mocked list of inventory items
        mock_all.return_value = [
            InventoryItem(name='Mocked Test Item', quantity=10, description='Mocked description')
        ]

        # Send a GET request to the inventory list page
        response = self.client.get(reverse('inventory_list'))

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the mocked inventory item is visible in the page content
        self.assertContains(response, 'Mocked Test Item')
        self.assertContains(response, '10')  # Quantity should be displayed
        self.assertContains(response, 'Mocked description')  # Description should be displayed
