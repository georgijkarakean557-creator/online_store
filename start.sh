#!/usr/bin/env bash
set -o errexit

echo "==> Applying migrations..."
python manage.py migrate --no-input

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Starting server..."
gunicorn core.wsgi:application --bind 0.0.0.0:8080