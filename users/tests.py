from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # редирект после регистрации
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_invalid(self):
        # Отправляем пустые данные
        response = self.client.post(reverse('users:register'), {
            'username': '',
            'password1': '123',
            'password2': '456',
        })
        self.assertEqual(response.status_code, 200)  # форма снова показана
        # Проверяем, что есть ошибки валидации (например, поле username имеет класс is-invalid)
        self.assertContains(response, 'is-invalid')
        # Также можно проверить наличие конкретной ошибки
        self.assertContains(response, 'This field is required')

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_success(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_login_fail(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get('_auth_user_id'))