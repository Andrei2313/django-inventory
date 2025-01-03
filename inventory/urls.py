from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),  # Inventory List
    path('add/', views.add_inventory_item, name='add_inventory_item'),  # Add Inventory Item
]
