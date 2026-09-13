from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product
from cart.cart import Cart

class OrderTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Тест', slug='test')
        self.product = Product.objects.create(
            name='Товар для заказа',
            slug='order-product',
            price=1000,
            category=self.category,
            available=True
        )
        # Добавляем товар в корзину
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})

    def test_order_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivan@example.com',
            'phone': '+79991234567',
            'address': 'ул. Ленина, д. 1',
            'city': 'Москва',
            'postal_code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'заказ')  # страница created.html

    def test_order_requires_auth_or_form(self):
        # Неавторизованный пользователь может оформить заказ (у вас так реализовано?)
        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'Пётр',
            'last_name': 'Петров',
            'email': 'petr@example.com',
            'phone': '+79998765432',
            'address': 'ул. Пушкина, д. 5',
            'city': 'СПб',
            'postal_code': '654321'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'заказ')