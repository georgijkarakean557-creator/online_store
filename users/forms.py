from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return cd.get('password2')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone']
        labels = {
            'avatar': 'Аватар',
            'phone': 'Телефон',
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'name', 'country', 'city', 'street', 'house',
            'apartment', 'postal_code', 'is_default',
            'latitude', 'longitude',
        ]
        labels = {
            'name': 'Название (например, Дом, Работа)',
            'country': 'Страна',
            'city': 'Город',
            'street': 'Улица',
            'house': 'Дом',
            'apartment': 'Квартира / офис',
            'postal_code': 'Индекс',
            'is_default': 'Сделать адресом по умолчанию',
            'latitude': 'Широта (для карты)',
            'longitude': 'Долгота (для карты)',
        }
        widgets = {
            'latitude': forms.NumberInput(attrs={
                'step': '0.000001',
                'placeholder': 'Например: 43.585472',
                'class': 'form-control',
            }),
            'longitude': forms.NumberInput(attrs={
                'step': '0.000001',
                'placeholder': 'Например: 39.723098',
                'class': 'form-control',
            }),
        }