from django.contrib import admin
from .models import InventoryItem, Notification

admin.site.register(InventoryItem)
admin.site.register(Notification)
