from celery import shared_task

from apps.images.models import Image, ImageLabel, ImageAnalytics
from apps.object_detector import ImageObjectDetectorTask

from django.utils import timezone


@shared_task()
def process_image(image_id):
    image = Image.objects.get(pk=image_id)

    image.status = Image.Status.PENDING
    image.save(update_fields=['status'])

    start = timezone.now()

    labels = ImageObjectDetectorTask().process(image.image.read())

    processing_duration = timezone.now().timestamp() - start.timestamp()

    image_labels = [ImageLabel(name=label.name, confidence=label.confidence, x_cord=label.x, y_cord=label.y,
                               image=image, ) for label in labels]

    image.status = Image.Status.DONE
    image.save(update_fields=['status'])

    ImageAnalytics.objects.create(processing_time=float(processing_duration), size=image.image.size,
                                  image=image, labels_count=len(image_labels, ))

    return ImageLabel.objects.bulk_create(image_labels)
