import os
from celery import Celery

# Устанавливаем модуль настроек django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subtrack.settings')

# Создаем Celery приложение
app = Celery('Subtrack')

app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()
