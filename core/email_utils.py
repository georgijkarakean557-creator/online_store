from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user_email, username):
    subject = 'Добро пожаловать в наш магазин!'
    message = (
        f'Привет, {username}!\n\n'
        'Спасибо за регистрацию на нашем сайте. '
        'Теперь вы можете оформлять заказы и добавлять товары в избранное.\n\n'
        'С уважением, команда магазина.'
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)

def send_order_confirmation_email(user_email, order_id, total_price, first_name):
    subject = f'Подтверждение заказа №{order_id}'
    message = (
        f'Здравствуйте, {first_name}!\n\n'
        f'Ваш заказ №{order_id} успешно оформлен.\n'
        f'Сумма заказа: {total_price} руб.\n\n'
        'Спасибо за покупку! Мы свяжемся с вами в ближайшее время.'
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)