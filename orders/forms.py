from django import forms
from .models import Order
import json

class DishForm(forms.Form):
    name = forms.CharField(label="Название блюда", widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label="Цена", widget=forms.NumberInput(attrs={'class': 'form-control'}))

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status']
        widgets = {
            'table_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dish_form = DishForm(prefix='dish')  # Форма для одного блюда

    def save(self, commit=True):
        order = super().save(commit=False)
        dish_form = self.dish_form
        if dish_form.is_valid():
            dish = {
                "name": dish_form.cleaned_data['name'],
                "price": float(dish_form.cleaned_data['price']),
            }
            order.items = json.dumps([dish])  # Сохраняем одно блюдо
            order.total_price = dish['price']  # Общая стоимость равна цене блюда
            if commit:
                order.save()
        return order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }