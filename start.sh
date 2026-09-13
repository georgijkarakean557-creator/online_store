#!/usr/bin/env bash
set -o errexit

echo "==> Applying migrations..."
python manage.py migrate --no-input

echo "==> Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin2026!')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Суперпользователь {username} создан')
else:
    print(f'Пользователь {username} уже существует')
"

echo "==> Starting server..."
gunicorn core.wsgi:application --bind 0.0.0.0:8080