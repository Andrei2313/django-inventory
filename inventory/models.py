from django.db import models
from django.db.models import F

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def is_low_stock(self):
        # Resolve the value of quantity before comparing
        item = Item.objects.get(pk=self.pk)
        return item.quantity < 15



class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check if there is enough stock
        if self.item.quantity < self.quantity:
            raise ValueError("Not enough stock to fulfill the order.")

        # Deduct the stock
        self.item.quantity = F('quantity') - self.quantity
        self.item.save()

        # Check for low stock
        if self.item.is_low_stock():
            print(f"Alert: Stock for '{self.item.name}' is below 15!")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order of {self.quantity} {self.item.name}(s)"
