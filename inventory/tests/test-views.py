# your_app/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import InventoryItem
from inventory.forms import InventoryItemForm


class InventoryItemViewTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create an InventoryItem instance for testing the list view
        self.item = InventoryItem.objects.create(name="Test Item", quantity=5, description="Test description")

    def test_inventory_list_view(self):
        # Test if inventory list view displays the items correctly
        self.client.login(username='testuser', password='password')  # Log in to use views that require authentication

        response = self.client.get(reverse('inventory_list'))

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the inventory item appears in the response content
        self.assertContains(response, "Test Item")
        self.assertContains(response, "5")
        self.assertContains(response, "Test description")

    def test_add_inventory_item_view_get(self):
        # Test if the 'add inventory item' view renders the form correctly
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('add_inventory_item'))

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the form is in the response
        self.assertContains(response, '<form')

    def test_add_inventory_item_view_post_valid(self):
        """
        Test that when valid form data is provided, the form is saved and the user is redirected.
        """
        # Define valid form data
        form_data = {
            'name': 'New Test Item',
            'quantity': 10,
            'description': 'A new test item added via the form',
        }

        # Send a POST request with valid data to the 'add_inventory_item' view
        response = self.client.post(reverse('add_inventory_item'), data=form_data)

        # Check if the response is a redirect (302 - should redirect to the inventory list)
        self.assertEqual(response.status_code, 302)

        # Verify that the new item exists in the database
        self.assertTrue(InventoryItem.objects.filter(name='New Test Item').exists())

        # Check that the redirect is to the 'inventory_list' view
        self.assertRedirects(response, reverse('inventory_list'))

    def test_add_inventory_item_view_post_invalid(self):
        """
        Test that when invalid form data is provided, the form is re-rendered with errors.
        """
        # Define invalid form data (missing a required field, such as name)
        form_data = {
            'name': '',  # Name is empty, so the form should be invalid
            'quantity': 10,
            'description': 'A test item without a name',
        }

        # Send a POST request with invalid data to the 'add_inventory_item' view
        response = self.client.post(reverse('add_inventory_item'), data=form_data)

        # Check if the response status code is 200 (the form should re-render because the form is invalid)
        self.assertEqual(response.status_code, 200)

        # Check if the form contains the appropriate error for the 'name' field
        self.assertFormError(response, 'form', 'name', 'This field is required.')