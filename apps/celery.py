from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

app = Celery('apps')

app.config_from_object('settings.local', namespace='CELERY')

app.autodiscover_tasks()