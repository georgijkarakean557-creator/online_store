import os
import sys

# Путь к проекту на PythonAnywhere (заменишь YOUR_USERNAME на свой логин)
path = '/home/YOUR_USERNAME/online_store'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()