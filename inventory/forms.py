from django import forms
from .models import Item, Order

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']

class OrderForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.IntegerField()

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        item = self.cleaned_data['item']

        if quantity > item.quantity:
            raise forms.ValidationError("Quantity exceeds stock.")
        return quantity
from django import forms
from .models import Item

class UpdateStockForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity < 0:  # Reject negative quantity
            raise forms.ValidationError("Quantity cannot be negative.")

        return quantity
