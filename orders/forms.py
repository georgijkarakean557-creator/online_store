from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code'
        ]
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Индекс'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес',
            'city': 'Город',
            'postal_code': 'Индекс',
        }