import os

from abc import ABC

from storages.backends.s3boto3 import S3Boto3Storage

from settings.base import *

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True


class MinioMediaStorage(S3Boto3Storage, ABC):
    location = 'media'
    file_overwrite = False


class MinioStaticStorage(S3Boto3Storage, ABC):
    location = 'static'


STORAGES = {
    "default": {
        "BACKEND": "settings.local.MinioMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "settings.local.MinioStaticStorage",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 1

AWS_ACCESS_KEY_ID = os.environ.get('MINIO_ROOT_USER', 'access_key')
AWS_SECRET_ACCESS_KEY = os.environ.get('MINIO_ROOT_PASSWORD', 'secret_key')
AWS_STORAGE_BUCKET_NAME = os.environ.get('MINIO_PUBLIC_BUCKET_NAME', 'django-backend-dev-public')
AWS_S3_ENDPOINT_URL = os.environ.get('MINIO_ENDPOINT', 'http://minio:9000')

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_BACKEND_URL = os.environ.get('CELERY_BACKEND_URL')

CELERY_TIMEZONE = 'Europe/Warsaw'
TIME_ZONE = 'Europe/Warsaw'

CELERY_BEAT_SCHEDULE = {
    'send-summary-every-hour': {
        'task': 'create_report',
        'schedule': 120.0,
        'args': (),
    },
}

CLASSES_FILE_NAME = "coco.names"

SIMPLE_JWT = {
    'UPDATE_LAST_LOGIN': True,
}
