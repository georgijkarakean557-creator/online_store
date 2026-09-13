from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение категории', upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_detail', args=[self.slug])


class Product(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('U', 'Унисекс'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', max_length=200, unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    available = models.BooleanField('Доступен', default=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)

    brand = models.CharField('Бренд', max_length=100, blank=True, help_text='Например: Nike, Adidas, Loro Piana')
    composition = models.CharField('Состав', max_length=255, blank=True, help_text='Например: хлопок 50%, полиэстер 50%')
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, default='U')
    color = models.CharField('Цвет', max_length=50, blank=True, help_text='Например: черный, белый, красный')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField('Оценка', choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField('Отзыв', blank=True)   # <-- текст необязателен
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username} — {self.product.name} ({self.rating}★)'