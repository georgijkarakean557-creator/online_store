from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product
from wishlist.models import WishlistItem

class WishlistTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Тест', slug='test')
        self.product = Product.objects.create(
            name='Товар для избранного',
            slug='wish-product',
            price=100,
            category=self.category,
            available=True
        )
        self.client.login(username='testuser', password='testpass')

    def test_add_to_wishlist(self):
        response = self.client.post(reverse('wishlist:wishlist_add', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WishlistItem.objects.filter(user=self.user, product=self.product).exists())

    def test_wishlist_detail(self):
        WishlistItem.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('wishlist:wishlist_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Товар для избранного')

    def test_remove_from_wishlist(self):
        WishlistItem.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('wishlist:wishlist_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(WishlistItem.objects.filter(user=self.user, product=self.product).exists())