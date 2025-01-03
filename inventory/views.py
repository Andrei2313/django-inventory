from django.shortcuts import render, redirect
from .models import InventoryItem
from .forms import InventoryItemForm

# Inventory List View
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'inventory/inventory_list.html', {'items': items})

# Add Inventory Item View
def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')  # Redirect to the inventory list after saving
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/add_inventory_item.html', {'form': form})
