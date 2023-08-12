import uuid

from apps.core.models import TimestampAbstractModel
from django.db import models


class AnalyticReport(TimestampAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    average_image_processing_time = models.DecimalField(max_digits=20, decimal_places=10)
    average_image_size = models.IntegerField()
    average_image_labels_count = models.IntegerField()
    last_logged_users_count = models.IntegerField()
    last_joined_users_count = models.IntegerField()
