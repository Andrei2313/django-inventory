import logging
from django.db import models
from django.db.models import F

logger = logging.getLogger('inventory.models')  # Ensure logger is defined here

class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    description = models.TextField()

    def check_low_stock(self):
        """Checks if the stock is below 15."""
        if self.quantity < 15:
            return True
        return False

    # Optionally, you can define an is_low_stock method as well
    def is_low_stock(self):
        """Checks if the stock is below 15 using the check_low_stock method."""
        return self.check_low_stock()

    def __str__(self):
        """Return a human-readable string representation of the item."""
        return self.name  # This will display the item's name instead of the default "Item Object (1)"

class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check if there is enough stock to fulfill the order
        if self.item.quantity < self.quantity:
            raise ValueError("Not enough stock to fulfill the order.")

        # Deduct the stock atomically
        self.item.quantity -= self.quantity  # Subtract the ordered quantity
        self.item.save(update_fields=['quantity'])  # Ensure atomicity

        # Check for low stock
        if self.item.check_low_stock():
            logger.info(f"Alert: Stock for '{self.item.name}' is below 15!")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order of {self.quantity} {self.item.name}(s)"
