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
        # Define valid form data
        form_data = {
            'name': 'New Test Item',
            'quantity': 10,
            'description': 'A new test item',
        }

        # Send a POST request with valid data to the 'add_inventory_item' view
        response = self.client.post(reverse('add_inventory_item'), data=form_data)

        # Check if the response is a redirect (should redirect to the inventory list)
        self.assertEqual(response.status_code, 302)

        # Check if the new item exists in the database
        self.assertTrue(InventoryItem.objects.filter(name='New Test Item').exists())

        # Check if the redirect URL is correct
        self.assertRedirects(response, reverse('inventory_list'))

    def test_add_inventory_item_view_post_invalid(self):
        # Test if the 'add inventory item' view handles invalid data
        self.client.login(username='testuser', password='password')

        # Define invalid form data (missing required field)
        form_data = {
            'name': '',
            'quantity': 10,
            'description': 'A test item without name',
        }

        response = self.client.post(reverse('add_inventory_item'), data=form_data)

        # Check if the response status is 200 (OK) because the form is invalid
        self.assertEqual(response.status_code, 200)

        # Check if the form has errors
        self.assertFormError(response, 'form', 'name', 'This field is required.')
