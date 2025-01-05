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
        return self.quantity < 15  # Direct comparison to self.quantity

    def is_low_stock(self):
        """Checks if the stock is below 15 using the check_low_stock method."""
        return self.check_low_stock()

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
