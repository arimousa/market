from django import forms
from market.models import Product, Order, OrderRow


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'inventory']


class OrderRowForm(forms.ModelForm):
    class Meta:
        model = OrderRow
        fields = ['amount']
