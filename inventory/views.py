from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from .forms import ItemForm, OrderForm, UpdateStockForm
from .models import Order
from django.shortcuts import get_object_or_404

def update_stock(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = UpdateStockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = UpdateStockForm(instance=item)
    return render(request, 'inventory/update_stock.html', {'form': form, 'item': item})

def inventory_list(request):
    items = Item.objects.all()
    low_stock_items = items.filter(quantity__lt=15)
    return render(request, 'inventory/inventory_list.html', {'items': items, 'low_stock_items': low_stock_items})

def order_log(request):
    orders = Order.objects.select_related('item').order_by('-created_at')  # Latest first
    return render(request, 'inventory/order_log.html', {'orders': orders})
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Order created successfully!")
                return redirect('inventory_list')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = OrderForm()

    return render(request, 'inventory/create_order.html', {'form': form})
