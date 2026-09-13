from django.db import models
from django.conf import settings
from catalog.models import Product


class PickupPoint(models.Model):
    CARRIER_CHOICES = (
        ('cdek', 'СДЭК'),
        ('boxberry', 'Boxberry'),
        ('post', 'Почта России'),
        ('yandex', 'Яндекс.Доставка'),
        ('dellin', 'Деловые Линии'),
        ('other', 'Другая'),
    )

    CARRIER_COLORS = {
        'cdek': 'success',
        'boxberry': 'danger',
        'post': 'primary',
        'yandex': 'warning',
        'dellin': 'info',
        'other': 'secondary',
    }

    carrier = models.CharField('Транспортная компания', max_length=20, choices=CARRIER_CHOICES)
    name = models.CharField('Название пункта', max_length=200)
    address = models.CharField('Адрес', max_length=300)
    city = models.CharField('Город', max_length=100)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    work_time = models.CharField('Часы работы', max_length=200, blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'
        ordering = ['carrier', 'city', 'name']

    def __str__(self):
        return f'{self.get_carrier_display()} — {self.name} ({self.city})'

    @property
    def carrier_color(self):
        return self.CARRIER_COLORS.get(self.carrier, 'secondary')


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=250)
    city = models.CharField('Город', max_length=100)
    postal_code = models.CharField('Почтовый индекс', max_length=20)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)
    paid = models.BooleanField('Оплачен', default=False)
    total_price = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)

    # НОВОЕ ПОЛЕ — выбранный пункт выдачи
    pickup_point = models.ForeignKey(
        PickupPoint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пункт выдачи'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ {self.id} от {self.first_name} {self.last_name}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_cost(self):
        return self.price * self.quantity