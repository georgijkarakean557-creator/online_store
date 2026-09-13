from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Category, Product

class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Тест', slug='test')
        self.product = Product.objects.create(
            name='Товар для корзины',
            slug='cart-product',
            price=500,
            category=self.category,
            available=True
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # редирект в корзину
        # Проверяем, что товар в сессии
        cart = self.client.session.get('cart', {})
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 2)

    def test_cart_detail(self):
        # Сначала добавим товар
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Товар для корзины')

    def test_cart_remove(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        response = self.client.get(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)