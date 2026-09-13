from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField('Название (например, Дом, Работа)', max_length=50, blank=True)
    country = models.CharField('Страна', max_length=100, default='Россия')
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=200)
    house = models.CharField('Дом', max_length=20)
    apartment = models.CharField('Квартира/офис', max_length=20, blank=True)
    postal_code = models.CharField('Индекс', max_length=20, blank=True)
    is_default = models.BooleanField('Адрес по умолчанию', default=False)

    # НОВЫЕ ПОЛЯ — координаты для карты
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.name or "Адрес"} - {self.city}, {self.street} {self.house}'

    @property
    def full_address(self):
        parts = [self.country, self.city, f'{self.street} {self.house}']
        if self.apartment:
            parts[-1] += f', кв. {self.apartment}'
        return ', '.join(p for p in parts if p)


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField('Сообщение')
    is_bot = models.BooleanField('От бота', default=False)
    created_at = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'

    def __str__(self):
        return f'{self.user.username} - {self.message[:20]}'


# Сигналы для автоматического создания профиля
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()