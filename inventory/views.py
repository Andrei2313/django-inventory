from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Item, Order
from .forms import ItemForm, OrderForm, UpdateStockForm

# Helper function to check if a user is admin
def is_admin(user):
    return user.is_staff

# Inventory list view - accessible to all logged-in users
@login_required
def inventory_list(request):
    items = Item.objects.all()
    low_stock_items = items.filter(quantity__lt=15)
    return render(request, 'inventory/inventory_list.html', {'items': items, 'low_stock_items': low_stock_items})

# View for admins to add new items
@login_required
@user_passes_test(is_admin)  # Restrict to admins only
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully!")
            return redirect('inventory_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

# View for users to create orders
@login_required
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

# View for admins to update stock
@login_required
@user_passes_test(is_admin)  # Restrict to admins only
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

# View for admins to see the order log
@login_required
@user_passes_test(is_admin)  # Restrict to admins only
def order_log(request):
    orders = Order.objects.select_related('item').order_by('-created_at')  # Latest first
    return render(request, 'inventory/order_log.html', {'orders': orders})
