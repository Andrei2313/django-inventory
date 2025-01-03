from django import forms
from .models import Item, Order

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'quantity']
class UpdateStockForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['quantity']