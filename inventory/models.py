from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
