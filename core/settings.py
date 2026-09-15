"""
Django settings for core project.

Работает и локально (SQLite), и на RelaxDev (PostgreSQL через DATABASE_URL).
"""

import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ===== БЕЗОПАСНОСТЬ =====
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-sa71n!=tb-5*yx2v0#n+&47o1tv0#7-ohh=f)^0$=)-1(@_b53'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.relaxdev.ru',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]


# ===== ПРИЛОЖЕНИЯ =====
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'cart',
    'orders',
    'users',
    'wishlist',
]


# ===== MIDDLEWARE =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalog.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# ===== БАЗА ДАННЫХ =====
_db_url = os.environ.get('DATABASE_URL', '')

if _db_url:
    parsed = urlparse(_db_url)
    query_params = parse_qs(parsed.query)

    for param in [
        'connection_limit', 'pool_timeout', 'sslmode', 'ssl',
        'channel_binding', 'pgbouncer', 'statement_cache_size',
        'application_name',
    ]:
        query_params.pop(param, None)

    new_query = urlencode(query_params, doseq=True)
    cleaned_url = urlunparse(parsed._replace(query=new_query))

    DATABASES = {
        'default': dj_database_url.parse(
            cleaned_url,
            conn_max_age=600,
            ssl_require=False,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ===== ПАРОЛИ =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===== ЯЗЫК И ВРЕМЯ =====
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# ===== СТАТИКА =====
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ===== МЕДИА =====
# Картинки товаров и аватары. Раздаём через отдельный URL /media/.
# Раздача настраивается в core/urls.py.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===== ПРОЧЕЕ =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CART_SESSION_ID = 'cart'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/users/profile/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMIN_SITE_HEADER = "Управление магазином"
ADMIN_SITE_TITLE = "Мой магазин — Админка"