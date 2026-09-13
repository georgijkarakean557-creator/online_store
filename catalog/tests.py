from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class CatalogTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория', slug='test-cat')
        self.product = Product.objects.create(
            category=self.category,
            name='Тестовый товар',
            slug='test-product',
            description='Описание',
            price=1000,
            available=True
        )

    def test_product_list(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый товар')

    def test_product_detail(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый товар')

    def test_category_filter(self):
        response = self.client.get(reverse('catalog:category_detail', args=['test-cat']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый товар')