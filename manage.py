#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # === АВТОМАТИЧЕСКИЕ ДЕЙСТВИЯ ПРИ ЗАПУСКЕ runserver ===
    # Нужно для серверов, у которых нет возможности выполнить консольные команды.
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        from django.core.management import call_command
        from django.db import connection

        # 1. Применяем миграции
        try:
            call_command('migrate', interactive=False, verbosity=1)
        except Exception as e:
            print(f'[auto-migrate] Ошибка: {e}')

        # 2. Создаём суперпользователя, если его нет
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin2026!')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print(f'[auto-superuser] Создан {username}')
            else:
                print(f'[auto-superuser] {username} уже существует')
        except Exception as e:
            print(f'[auto-superuser] Ошибка: {e}')

        # 3. Собираем статику
        try:
            call_command('collectstatic', interactive=False, verbosity=0)
            print('[auto-static] Статика собрана')
        except Exception as e:
            print(f'[auto-static] Ошибка: {e}')

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()