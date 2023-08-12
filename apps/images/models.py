import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.core.models import TimestampAbstractModel
from apps.users.models import User


class Image(TimestampAbstractModel):
    class Status(models.TextChoices):
        PLANNED = "PL", _("PLANNED")
        PENDING = "PE", _("PENDING")
        DONE = "DN", _("DONE")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.FileField(upload_to='images/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PLANNED
    )


class ImageLabel(TimestampAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    confidence = models.DecimalField(max_digits=4, decimal_places=2)
    x_cord = models.IntegerField()
    y_cord = models.IntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class ImageAnalytics(TimestampAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    processing_time = models.DecimalField(max_digits=20, decimal_places=10)
    size = models.IntegerField()
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    labels_count = models.IntegerField()

